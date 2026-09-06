"""Rebuild every Goalie Performance figure from the original MoneyPuck sample.

The original article used 5v5 unblocked attempts from the 2007-08 through
2022-23 seasons.  Download the official ``shots_YYYY.zip`` files and the
MoneyPuck player biography lookup into a temporary directory, then run:

    python scripts/rebuild_goalie_figures.py --data-dir /path/to/zips

Only published figures are written to ``figs/``. The source data stays outside
the repository. This is a Python translation of the archived R analysis, with
the same cutoffs and transformations but the shared site plotting theme.
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d
from scipy.stats import beta, gaussian_kde, weibull_min
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.spazz_plot import CHALK, GOLD, MUTED_DARK, finish_axes, save_figure, spazz_theme

YEARS = range(2007, 2023)
KEEP = [
    "season", "game_id", "goalieIdForShot", "goalieNameForShot", "goal",
    "xGoal", "homeSkatersOnIce", "awaySkatersOnIce",
]
ALIASES = {
    "Cal Petersen": "Calvin Petersen", "Michael DiPietro": "Michael Dipietro",
    "Olie Kolzig": "Olaf Kolzig", "Zach Fucale": "Zachary Fucale",
    "Edward Pasquale": "Eddie Pasquale", "Dan Vladar": "Daniel Vladar",
    "Zach Sawchenko": "Zachary Sawchenko", "Ken Appleby": "Kenneth Appleby",
}
BOUNDARY_EXCEPTIONS = {
    "Carey Price", "Brian Elliott", "Jaroslav Halak", "Jonathan Quick", "Mike Smith",
    "Semyon Varlamov", "Tuukka Rask", "Anton Khudobin", "Jonathan Bernier",
    "Pekka Rinne", "Thomas Greiss", "Corey Crawford", "Cory Schneider",
    "Curtis McElhinney", "Josh Harding", "Matt Keetley", "Daniel Lacosta",
    "Chris Beckford-Tseu", "Daniel Taylor", "Marek Schwarz", "Niklas Backstrom",
    "Peter Budaj", "Alex Stalock", "Fredrik Norrena", "Erik Ersberg",
    "Dimitri Patzold", "Drew MacIntyre", "Tyler Weiman", "Tobias Stephan",
    "Joey MacDonald",
}
NHL_BIRTHDATE_FALLBACK = {
    8474708: "1990-06-04", 8473638: "1985-09-30", 8470751: "1984-06-22",
    8460516: "1976-04-22", 8466290: "1978-02-07", 8469556: "1983-02-03",
    8447687: "1965-01-29", 8469569: "1983-06-24", 8470084: "1984-05-18",
    8462102: "1977-07-19", 8459432: "1975-01-12", 8466303: "1978-05-24",
    8460715: "1975-08-31", 8473632: "1985-01-11", 8480363: "1998-09-23",
    8477356: "1992-07-31", 8479016: "1995-08-24", 8477084: "1994-06-15",
    8471819: "1986-04-27", 8483158: "1998-01-20", 8478559: "1992-02-14",
    8478999: "1991-04-29", 8480925: "1990-06-03", 8479138: "1982-01-17",
    8473461: "1988-05-29", 8480591: "1994-07-25", 8470062: "1984-06-05",
}


def load_shots(data_dir: Path) -> pd.DataFrame:
    frames = []
    for year in YEARS:
        archive = data_dir / f"shots_{year}.zip"
        if not archive.exists():
            raise FileNotFoundError(archive)
        with zipfile.ZipFile(archive) as zf:
            csv_name = next(name for name in zf.namelist() if name.endswith(".csv"))
            with zf.open(csv_name) as handle:
                frame = pd.read_csv(handle, usecols=KEEP, low_memory=False)
        frame = frame.loc[
            (frame.homeSkatersOnIce == 5) & (frame.awaySkatersOnIce == 5),
            ["season", "game_id", "goalieIdForShot", "goalieNameForShot", "goal", "xGoal"],
        ].copy()
        frames.append(frame)
        print(f"loaded {year}: {len(frame):,} attempts")
    shots = pd.concat(frames, ignore_index=True)
    shots.columns = ["season", "game_id", "goalie_id", "goalie_name", "goal", "x_goal"]
    shots = shots.dropna(subset=["goalie_name", "goal", "x_goal"])
    shots["goalie_name"] = shots.goalie_name.replace(ALIASES)
    shots.loc[shots.goalie_name.str.contains("Berube", na=False), "goalie_name"] = "Jean-Francois Berube"
    shots = shots.sort_values(["season", "game_id"], kind="stable").reset_index(drop=True)
    return shots


def career_table(shots: pd.DataFrame, minimum: int = 0) -> pd.DataFrame:
    season_xf = 1 - shots.groupby("season").x_goal.mean()
    season_xf = (season_xf + 2 * season_xf.mean()) / 3
    s = shots.assign(season_xf=shots.season.map(season_xf)).groupby(["goalie_name", "season"]).agg(
        shots=("goal", "size"), goals=("goal", "sum"), exp_g=("x_goal", "sum"),
        season_xf=("season_xf", "mean"),
    )
    s["sv_pct"] = 1 - s.goals / s.shots
    s["exp_f"] = 1 - s.exp_g / s.shots
    s["adj_sv_pct"] = s.season_xf + s.sv_pct - s.exp_f
    s["adj_saves"] = s.adj_sv_pct * s.shots
    career = s.groupby("goalie_name").agg(
        shots=("shots", "sum"), goals=("goals", "sum"), exp_g=("exp_g", "sum"),
        adj_saves=("adj_saves", "sum"), seasons=("shots", "size"),
    )
    career["sv_pct"] = 1 - career.goals / career.shots
    career["adj_sv_pct"] = career.adj_saves / career.shots
    return career.loc[career.shots > minimum].dropna().reset_index()


def bare_hist(ax, values, bins, xlim=None):
    ax.hist(values, bins=bins, histtype="stepfilled", color=GOLD, alpha=.10)
    ax.hist(values, bins=bins, histtype="step", color=GOLD, linewidth=1.8)
    ax.set_yticks([])
    if xlim:
        ax.set_xlim(*xlim)
    finish_axes(ax)


def posterior_panel(ax, grid, prior_ab, careers, adjusted=False):
    a0, b0 = prior_ab
    ax.fill_between(grid, beta.pdf(grid, a0, b0), color=GOLD, alpha=.18)
    styles = [(1, "-"), (.5, "--")]
    for name, (alpha, line) in zip(["Jeremy Swayman", "Jake Oettinger"], styles):
        row = careers.loc[careers.goalie_name == name].iloc[0]
        successes = row.adj_saves if adjusted else row.shots - row.goals
        failures = row.shots - successes
        density = beta.pdf(grid, a0 + successes, b0 + failures)
        ax.plot(grid, density, color=GOLD, alpha=alpha, ls=line, label=name)
    ax.set_yticks([])
    ax.legend(loc="upper center", bbox_to_anchor=(.5, -.20), ncol=2)
    ax.figure.subplots_adjust(bottom=.30)
    finish_axes(ax, xlabel="Fenwick save probability")


def complete_careers(shots: pd.DataFrame) -> tuple[pd.DataFrame, set[str]]:
    boundary = set(shots.loc[shots.season.isin([2007, 2022]), "goalie_name"])
    remove = (boundary - BOUNDARY_EXCEPTIONS) | {"Manny Fernandez"}
    return shots.loc[~shots.goalie_name.isin(remove)].copy(), remove


def attach_age(shots: pd.DataFrame, data_dir: Path) -> pd.DataFrame:
    bios = pd.read_csv(data_dir / "allPlayersLookup.csv", usecols=["playerId", "name", "birthDate"])
    bios = bios.drop_duplicates("playerId").rename(columns={"playerId": "goalie_id", "name": "bio_name", "birthDate": "dob"})
    bios["dob"] = pd.to_datetime(bios.dob, errors="coerce")
    out = shots.merge(bios[["goalie_id", "dob"]], how="left", on="goalie_id")
    fallback = pd.to_datetime(out.goalie_id.map(NHL_BIRTHDATE_FALLBACK), errors="coerce")
    out["dob"] = out.dob.fillna(fallback)
    # Reproduce the original paper's date approximation from within-season game order.
    games = out[["season", "game_id"]].drop_duplicates().sort_values(["season", "game_id"])
    games["game_rank"] = games.groupby("season").cumcount()
    games["game_n"] = games.groupby("season").game_id.transform("size")
    games["day"] = 245 + games.game_rank * 273 / games.game_n
    years = games.season + (games.day > 365).astype(int)
    day = games.day.where(games.day <= 365, games.day - 365)
    games["game_date"] = pd.to_datetime(years.astype(str) + "-01-01") + pd.to_timedelta(day, unit="D")
    out = out.merge(games[["season", "game_id", "game_date"]], on=["season", "game_id"])
    out["age"] = (out.game_date - out.dob).dt.days / 365
    return out


def plot_core(shots: pd.DataFrame, outdir: Path) -> tuple[pd.DataFrame, tuple[float, float]]:
    import matplotlib.pyplot as plt
    raw = career_table(shots, 200)
    raw_ab = beta.fit(raw.sv_pct, floc=0, fscale=1)[:2]
    grid_raw = np.linspace(.915, .957, 500)
    adjusted = career_table(shots, 200)
    adj_ab = beta.fit(adjusted.adj_sv_pct, floc=0, fscale=1)[:2]

    with spazz_theme():
        fig, ax = plt.subplots(); bare_hist(ax, raw.sv_pct, 15, (.915, .957)); save_figure(fig, outdir / "goalie-performance-1-1.png")
        fig, ax = plt.subplots(); bare_hist(ax, raw.sv_pct, 15, (.915, .957)); ax2=ax.twinx(); ax2.plot(grid_raw, beta.pdf(grid_raw,*raw_ab), color=GOLD, alpha=.62); ax2.set_axis_off(); save_figure(fig, outdir / "goalie-performance-1-2.png")
        fig, ax = plt.subplots(); posterior_panel(ax, grid_raw, raw_ab, raw); save_figure(fig, outdir / "goalie-performance-1-3.png")

        grid = np.linspace(adjusted.adj_sv_pct.min(), adjusted.adj_sv_pct.max(), 500)
        fig, ax = plt.subplots(); bare_hist(ax, adjusted.adj_sv_pct, 20)
        ax2=ax.twinx(); ax2.plot(grid, beta.pdf(grid,*adj_ab), color=GOLD, alpha=1, label="beta")
        shape, _, scale = weibull_min.fit(adjusted.adj_sv_pct, floc=0)
        ax2.plot(grid, weibull_min.pdf(grid,shape,scale=scale), color=GOLD, alpha=.9, ls="--", label="Weibull")
        ax2.set_yticks([]); finish_axes(ax2); ax2.legend(loc="upper center", bbox_to_anchor=(.5,-.14), ncol=2)
        fig.subplots_adjust(bottom=.25)
        save_figure(fig, outdir / "goalie-performance-2-1.png")
        fig, ax = plt.subplots(); posterior_panel(ax, grid, adj_ab, adjusted, True); save_figure(fig, outdir / "goalie-performance-2-2.png")

        a0,b0=adj_ab; adjusted["post_sv_pct"]=(a0+adjusted.adj_saves)/(a0+b0+adjusted.shots)
        pairs=[("sv_pct","adj_sv_pct","SV%","AdjSV%"),("adj_sv_pct","post_sv_pct","AdjSV%","Posterior AdjSV%"),("sv_pct","post_sv_pct","SV%","Posterior AdjSV%"),("exp_g","post_sv_pct","xG faced","Posterior AdjSV%")]
        fig, axes=plt.subplots(2,2,figsize=(10,6))
        for ax,(x,y,xl,yl) in zip(axes.flat,pairs):
            ax.scatter(adjusted[x],adjusted[y],s=12,color=GOLD,alpha=.58)
            if x != "exp_g": ax.text(.04,.92,f"r = {adjusted[x].corr(adjusted[y]):.3f}",transform=ax.transAxes,color=GOLD)
            finish_axes(ax,xlabel=xl,ylabel=yl)
        fig.tight_layout(); save_figure(fig,outdir/"goalie-performance-2-3.png")
    return adjusted, adj_ab


def plot_age(shots_age: pd.DataFrame, outdir: Path) -> None:
    import matplotlib.pyplot as plt
    known=shots_age.dropna(subset=["age"]).copy(); known["age_tenth"]=known.age.round(1)
    age=known.groupby("age_tenth").goal.agg(["size","sum"]); age["sv"]=1-age["sum"]/age["size"]
    rounded=known.assign(age_year=known.age.round()).groupby(["goalie_name","age_year"]).agg(shots=("goal","size"),goals=("goal","sum"),xg=("x_goal","sum")).reset_index()
    rounded["adj"]=(1-rounded.goals/rounded.shots)-(1-rounded.xg/rounded.shots)
    rounded=rounded.sort_values(["goalie_name","age_year"]); rounded["lag_shots"]=rounded.groupby("goalie_name").shots.shift(); rounded["delta"]=rounded.groupby("goalie_name").adj.diff()
    d=rounded.loc[(rounded.shots>100)&(rounded.lag_shots>100)].groupby("age_year").apply(lambda g: pd.Series({"occasions":len(g),"delta":np.average(g.delta,weights=g.shots)}),include_groups=False).reset_index()
    d=d.loc[d.age_year.between(22,38)].dropna(); d["curve"]=d.delta.cumsum(); d["curve"]-=d.curve.max(); d["smooth"]=gaussian_filter1d(d.curve.to_numpy(),1.4)
    with spazz_theme():
        fig,ax=plt.subplots(); alpha=np.clip(np.sqrt(age["size"])/np.sqrt(age["size"].max()),.15,1); ax.scatter(age.index,age.sv,c=GOLD,alpha=alpha,s=18); ax.set_ylim(.915,.965); finish_axes(ax,xlabel="Age",ylabel="Fenwick save percentage"); save_figure(fig,outdir/"goalie-performance-3-1.png")
        fig,ax=plt.subplots(); ax.scatter(d.age_year,d.curve,s=14+3*np.sqrt(d.occasions),color=GOLD,alpha=.45); ax.plot(d.age_year,d.smooth,color=GOLD); finish_axes(ax,xlabel="Age",ylabel="Mean observed change in AdjSV%"); save_figure(fig,outdir/"goalie-performance-3-2.png")


def plot_careers(shots: pd.DataFrame, shots_age: pd.DataFrame, outdir: Path) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.ticker import PercentFormatter
    complete, removed=complete_careers(shots); careers=career_table(complete)
    season_xf=1-shots.groupby("season").x_goal.mean(); season_xf=(season_xf+2*season_xf.mean())/3
    ordered=complete.assign(season_xf=complete.season.map(season_xf)).sort_values(["goalie_name","season","game_id"],kind="stable")
    g=ordered.groupby("goalie_name",sort=False); ordered["cml_shots"]=g.cumcount()+1; ordered["cml_xg"]=g.x_goal.cumsum(); ordered["cml_g"]=g.goal.cumsum(); ordered["adj_sv_pct"]=ordered.season_xf+(1-ordered.cml_g/ordered.cml_shots)-(1-ordered.cml_xg/ordered.cml_shots)
    totals=ordered.groupby("goalie_name").cml_shots.max(); ordered["career_shots"]=ordered.goalie_name.map(totals); ordered["long"]=(ordered.career_shots>1500).astype(int)
    short=careers.loc[(careers.shots>50)&(careers.shots<1500)&careers.adj_sv_pct.between(.8,.97)]; long=careers.loc[careers.shots>1500]
    ab_s=beta.fit(short.adj_sv_pct,floc=0,fscale=1)[:2]; ab_l=beta.fit(long.adj_sv_pct,floc=0,fscale=1)[:2]

    model_rows=ordered.loc[ordered.cml_shots<1500]; X=model_rows[["cml_shots","adj_sv_pct"]]; y=model_rows.long
    model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=400)); model.fit(X,y)
    pred=model.predict_proba(X)[:,1]; order=np.argsort(pred); bins=np.arange(len(pred))//100
    calibration=pd.DataFrame({"pred":pred[order],"actual":y.to_numpy()[order],"bin":bins}).groupby("bin").mean()

    # Mixture-posterior trajectory using the same adaptive long-career weight.
    all_pred=model.predict_proba(ordered[["cml_shots","adj_sv_pct"]])[:,1]; all_pred=np.where(ordered.cml_shots>1500,1,all_pred)
    A=ordered.adj_sv_pct*ordered.cml_shots
    good=(ab_l[0]+A)/(sum(ab_l)+ordered.cml_shots); bad=(ab_s[0]+A)/(sum(ab_s)+ordered.cml_shots)
    ordered["post"] = all_pred*good+(1-all_pred)*bad
    ordered["status"]=pd.cut(ordered.career_shots,[-np.inf,299,1499,5999,np.inf],labels=["<300","300–1,499","1,500–5,999","6,000+"])
    trajectory=ordered.groupby(["status","cml_shots"],observed=True).post.agg(["size","median"]).reset_index(); trajectory=trajectory.loc[trajectory["size"]>5]

    age=shots_age.loc[~shots_age.goalie_name.isin(removed)].dropna(subset=["age"]).sort_values(["goalie_name","season","game_id"],kind="stable")
    age["cml_shots"]=age.groupby("goalie_name").cumcount()+1; age["career_shots"]=age.goalie_name.map(totals); age["status"]=pd.cut(age.career_shots,[-np.inf,299,1499,5999,np.inf],labels=["<300","300–1,499","1,500–5,999","6,000+"])
    ages=age.groupby(["status","cml_shots"],observed=True).age.agg(["size","mean"]).reset_index(); ages=ages.loc[(ages["size"]>3)&(ages.cml_shots<5000)]

    with spazz_theme():
        counts=np.sort(careers.shots.to_numpy()); cdf=np.arange(1,len(counts)+1)/len(counts)
        fig,ax=plt.subplots(); ax.plot(counts,cdf,color=GOLD); ax.set_xlim(0,3000); ax.yaxis.set_major_formatter(PercentFormatter(1)); finish_axes(ax,xlabel="Career attempts"); save_figure(fig,outdir/"goalie-six-one.png")
        season_avg=careers.groupby("seasons").adj_sv_pct.mean()
        fig,ax=plt.subplots(); ax.plot(season_avg.index,season_avg.values,color=GOLD); finish_axes(ax,xlabel="Seasons played",ylabel="Mean AdjSV%"); save_figure(fig,outdir/"goalie-six-two.png")
        fig,ax=plt.subplots(); grid=np.linspace(.85,1,500)
        for subset,label,alpha,ls in [(short,"<1,500",1,"-"),(long,"1,500+",.48,"--")]: ax.plot(grid,gaussian_kde(subset.adj_sv_pct)(grid),color=GOLD,alpha=alpha,ls=ls,label=label)
        ax.set_yticks([]); ax.legend(loc="upper center",bbox_to_anchor=(.5,-.20),ncol=2); fig.subplots_adjust(bottom=.30); finish_axes(ax,xlabel="Career AdjSV%"); save_figure(fig,outdir/"goalie-six-three.png")
        fig,ax=plt.subplots(); ax.plot([0,1],[0,1],color=MUTED_DARK,ls="--",alpha=.6); ax.plot(calibration.pred,calibration.actual,color=GOLD); ax.xaxis.set_major_formatter(PercentFormatter(1)); ax.yaxis.set_major_formatter(PercentFormatter(1)); finish_axes(ax,xlabel="Predicted probability of 1,500+ attempts",ylabel="Observed share"); save_figure(fig,outdir/"goalie-six-four.png")
        fig,ax=plt.subplots();
        for i,(label,grp) in enumerate(trajectory.groupby("status",observed=True)): ax.plot(grp.cml_shots,grp["median"],color=GOLD,alpha=1-i*.18,label=str(label))
        ax.axhline(.941,color=MUTED_DARK,ls="--",alpha=.55); ax.set_xlim(0,10000); ax.legend(loc="upper center",bbox_to_anchor=(.5,-.22),ncol=4); fig.subplots_adjust(bottom=.30); finish_axes(ax,xlabel="Cumulative attempts",ylabel="Median pAdjSV%"); save_figure(fig,outdir/"goalie-six-seven.png")
        fig,ax=plt.subplots();
        for i,(label,grp) in enumerate(ages.groupby("status",observed=True)): ax.plot(grp.cml_shots,grp["mean"],color=GOLD,alpha=1-i*.18,label=str(label))
        ax.legend(loc="upper center",bbox_to_anchor=(.5,-.22),ncol=4); fig.subplots_adjust(bottom=.30); finish_axes(ax,xlabel="Cumulative attempts",ylabel="Mean age"); save_figure(fig,outdir/"goalie-six-six.png")


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--data-dir",type=Path,required=True); parser.add_argument("--output-dir",type=Path,default=ROOT/"figs"); args=parser.parse_args()
    shots=load_shots(args.data_dir); plot_core(shots,args.output_dir); shots_age=attach_age(shots,args.data_dir); plot_age(shots_age,args.output_dir); plot_careers(shots,shots_age,args.output_dir)
    print(f"rebuilt goalie figures in {args.output_dir}")


if __name__ == "__main__":
    main()
