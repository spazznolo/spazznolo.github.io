#!/usr/bin/env python3
"""Audit filtered WTA player-state uncertainty against later smoothed estimates."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd


QUANTITIES = ("overall", "played_surface")


def central_coverage(values: np.ndarray) -> dict[str, float]:
    absolute = np.abs(values)
    return {
        "central_50": float(np.mean(absolute <= 0.6744897501960817)),
        "central_80": float(np.mean(absolute <= 1.2815515655446004)),
        "central_95": float(np.mean(absolute <= 1.959963984540054)),
    }


def clustered_moment_intervals(
    frame: pd.DataFrame,
    column: str,
    cluster_column: str,
    rng: np.random.Generator,
    draws: int,
) -> dict[str, list[float]]:
    summaries = []
    for _, group in frame.groupby(cluster_column, sort=False):
        values = group[column].to_numpy(dtype=float)
        summaries.append([len(values), values.sum(), np.square(values).sum()])
    summaries = np.asarray(summaries, dtype=float)
    cluster_count = len(summaries)
    probability = np.full(cluster_count, 1.0 / cluster_count)
    estimates = np.empty((draws, 2))
    for draw in range(draws):
        multiplicity = rng.multinomial(cluster_count, probability)
        n, total, total_square = multiplicity @ summaries
        estimates[draw, 0] = total / n
        estimates[draw, 1] = np.sqrt((total_square - total * total / n) / (n - 1.0))
    return {
        "mean_95": [float(value) for value in np.quantile(estimates[:, 0], [0.025, 0.975])],
        "sd_95": [float(value) for value in np.quantile(estimates[:, 1], [0.025, 0.975])],
    }


def summarize(
    frame: pd.DataFrame,
    matchup_frame: pd.DataFrame,
    seed: int,
    draws: int,
) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    report: dict[str, object] = {
        "states": len(frame),
        "players": int(frame["player_id"].nunique()),
        "dates": int(frame["match_date"].nunique()),
        "quantities": {},
    }
    for quantity in QUANTITIES:
        column = f"{quantity}_revision_z"
        values = frame[column].to_numpy(dtype=float)
        intervals = clustered_moment_intervals(
            frame, column, "player_id", rng, draws
        )
        report["quantities"][quantity] = {
            "mean": float(np.mean(values)),
            "player_clustered_mean_95": intervals["mean_95"],
            "sd": float(np.std(values, ddof=1)),
            "player_clustered_sd_95": intervals["sd_95"],
            **central_coverage(values),
        }
    report["played_surface"] = {
        str(surface): {
            "states": len(group),
            "mean": float(group["played_surface_revision_z"].mean()),
            "sd": float(group["played_surface_revision_z"].std(ddof=1)),
            **central_coverage(group["played_surface_revision_z"].to_numpy(dtype=float)),
        }
        for surface, group in frame.groupby("surface", sort=True)
    }
    matchup_values = matchup_frame["matchup_revision_z"].to_numpy(dtype=float)
    matchup_intervals = clustered_moment_intervals(
        matchup_frame, "matchup_revision_z", "match_date", rng, draws
    )
    report["matchup_contrast"] = {
        "matches": len(matchup_frame),
        "mean": float(np.mean(matchup_values)),
        "day_clustered_mean_95": matchup_intervals["mean_95"],
        "sd": float(np.std(matchup_values, ddof=1)),
        "day_clustered_sd_95": matchup_intervals["sd_95"],
        **central_coverage(matchup_values),
        "by_surface": {
            str(surface): {
                "matches": len(group),
                "mean": float(group["matchup_revision_z"].mean()),
                "sd": float(group["matchup_revision_z"].std(ddof=1)),
                **central_coverage(group["matchup_revision_z"].to_numpy(dtype=float)),
            }
            for surface, group in matchup_frame.groupby("surface", sort=True)
        },
    }
    return report


def _linear_moments(problem, solution, records: pd.DataFrame) -> dict[str, np.ndarray]:
    from predict.models.collapsed_market import SURFACE_CONTRAST

    means = {quantity: np.empty(len(records), dtype=float) for quantity in QUANTITIES}
    variances = {quantity: np.empty(len(records), dtype=float) for quantity in QUANTITIES}
    rows = list(records.itertuples(index=False))
    for start in range(0, len(rows), 16):
        batch = rows[start : start + 16]
        right_hand_sides = np.zeros((problem.latent_count, 2 * len(batch)), dtype=float)
        specifications = []
        for position, row in enumerate(batch):
            player_id = str(row.player_id)
            state_index = int(row.state_index)
            surface_offset = problem.dynamic_state_count + 2 * problem.player_index[player_id]
            indices = np.asarray([state_index, surface_offset, surface_offset + 1])
            contrast = SURFACE_CONTRAST[str(row.surface).upper()]
            weights = {
                "overall": np.asarray([1.0, 0.0, 0.0]),
                "played_surface": np.asarray([1.0, contrast[0], contrast[1]]),
            }
            for quantity_index, quantity in enumerate(QUANTITIES):
                column = 2 * position + quantity_index
                right_hand_sides[indices, column] = weights[quantity]
                specifications.append((position, quantity, indices, weights[quantity], column))
        columns = problem._solve(solution.factor, right_hand_sides)
        for position, quantity, indices, weights, column in specifications:
            output_index = start + position
            means[quantity][output_index] = float(weights @ solution.mean[indices])
            variances[quantity][output_index] = float(weights @ columns[indices, column])
    return {
        **{f"{quantity}_mean": means[quantity] for quantity in QUANTITIES},
        **{
            f"{quantity}_variance": np.maximum(variances[quantity], 0.0)
            for quantity in QUANTITIES
        },
    }


def build_revision_data(
    tennis_root: Path,
    output_path: Path,
    matchup_output_path: Path,
    audit_season: int,
    smoothing_end_season: int,
) -> pd.DataFrame:
    sys.path.insert(0, str(tennis_root / "apps/predict/src"))
    sys.path.insert(0, str(tennis_root / "packages"))
    from predict.audit_player_uncertainty import _load_fit
    from predict.evaluate_collapsed_market import apply_reference_attributes
    from predict.models.collapsed_market import CollapsedMarketProblem

    model_root = (
        tennis_root
        / "apps/predict/output/models/collapsed_wta_market_fixed_peak24_exponential_v1"
    )
    dataset_path = (
        tennis_root
        / "apps/predict/output/datasets/wta_market_context_2019_2025_v1/matches.csv"
    )
    parameters, interpretation = _load_fit(model_root / str(audit_season) / "fit.json")
    dataset = pd.read_csv(dataset_path)
    dataset["match_timestamp"] = pd.to_datetime(dataset["match_timestamp"], format="mixed")
    dataset["match_date"] = dataset["match_timestamp"].dt.normalize()
    dataset = dataset.loc[dataset["season"].le(smoothing_end_season)].copy()
    dataset = dataset.sort_values(["match_timestamp", "match_id"], kind="stable").reset_index(drop=True)
    model_frame = dataset.copy()
    apply_reference_attributes(
        model_frame,
        float(interpretation["training_vig_mean"]),
        float(interpretation["training_vig_sd"]),
        {str(key): float(value) for key, value in interpretation["context_references"].items()},
    )
    problem = CollapsedMarketProblem.from_frame(model_frame)

    shared = ["match_id", "match_date", "surface"]
    player_1 = dataset.loc[dataset["season"].eq(audit_season), shared + ["player_id_home"]].rename(
        columns={"player_id_home": "player_id"}
    )
    player_2 = dataset.loc[dataset["season"].eq(audit_season), shared + ["player_id_away"]].rename(
        columns={"player_id_away": "player_id"}
    )
    candidates = pd.concat([player_1, player_2], ignore_index=True)
    candidates["player_id"] = candidates["player_id"].astype(str)
    candidates = candidates.sort_values(["match_date", "match_id"], kind="stable")
    candidates = candidates.drop_duplicates(["player_id", "match_date"])
    candidates["month"] = candidates["match_date"].dt.to_period("M")
    candidates = candidates.groupby(["player_id", "month"], as_index=False, sort=False).first()

    metadata = problem.dynamic_state_metadata.copy()
    metadata["player_id"] = metadata["player_id"].astype(str)
    metadata["match_date"] = pd.to_datetime(metadata["state_date"]).dt.normalize()
    candidates = candidates.merge(
        metadata[["player_id", "match_date", "state_index"]],
        on=["player_id", "match_date"],
        how="left",
        validate="one_to_one",
    )
    if candidates["state_index"].isna().any():
        raise ValueError("Could not map every audit appearance to a latent state")

    dates = dataset["match_date"]
    initial_mask = dates.lt(pd.Timestamp(f"{audit_season}-01-01")).to_numpy()
    smoothing_mask = dataset["season"].le(smoothing_end_season).to_numpy()
    filtered = problem.solve_posterior(parameters, observation_mask=initial_mask)
    smoothed = problem.solve_posterior(parameters, observation_mask=smoothing_mask)

    audit_indices = dataset.index[dataset["season"].eq(audit_season)].to_numpy(dtype=np.int64)
    smoothed_matchup_mean, smoothed_matchup_variance = problem.linear_predictive_moments(
        smoothed, audit_indices
    )
    prediction = pd.read_csv(
        model_root / str(audit_season) / "predictions.csv",
        usecols=["match_id", "model_logit_mean", "model_logit_sd"],
    )
    matchup = dataset.loc[audit_indices, ["match_id", "match_date", "surface"]].copy()
    matchup["smoothed_matchup_mean"] = smoothed_matchup_mean
    matchup["smoothed_matchup_sd"] = np.sqrt(smoothed_matchup_variance)
    matchup = matchup.merge(prediction, on="match_id", how="left", validate="one_to_one")
    matchup = matchup.rename(
        columns={
            "model_logit_mean": "filtered_matchup_mean",
            "model_logit_sd": "filtered_matchup_sd",
        }
    )
    matchup_revision_variance = (
        np.square(matchup["filtered_matchup_sd"])
        - np.square(matchup["smoothed_matchup_sd"])
    )
    if (matchup_revision_variance <= 1e-10).any():
        raise ValueError("Non-positive matchup revision variance")
    matchup["matchup_revision_z"] = (
        matchup["smoothed_matchup_mean"] - matchup["filtered_matchup_mean"]
    ) / np.sqrt(matchup_revision_variance)
    matchup_output_path.parent.mkdir(parents=True, exist_ok=True)
    matchup.to_csv(matchup_output_path, index=False, float_format="%.10g")

    records = []
    audit_rows = dataset.loc[dataset["season"].eq(audit_season)]
    for match_date, day in audit_rows.groupby("match_date", sort=True):
        selected = candidates.loc[candidates["match_date"].eq(match_date)].copy()
        if not selected.empty:
            filtered_moments = _linear_moments(problem, filtered, selected)
            smoothed_moments = _linear_moments(problem, smoothed, selected)
            for column, values in filtered_moments.items():
                selected[f"filtered_{column}"] = values
            for column, values in smoothed_moments.items():
                selected[f"smoothed_{column}"] = values
            records.append(selected)
        filtered = problem.update_posterior(
            filtered,
            parameters,
            day.index.to_numpy(dtype=np.int64),
        )

    result = pd.concat(records, ignore_index=True)
    for quantity in QUANTITIES:
        revision_variance = (
            result[f"filtered_{quantity}_variance"]
            - result[f"smoothed_{quantity}_variance"]
        )
        if (revision_variance <= 1e-10).any():
            raise ValueError(f"Non-positive revision variance for {quantity}")
        result[f"{quantity}_revision_z"] = (
            result[f"smoothed_{quantity}_mean"] - result[f"filtered_{quantity}_mean"]
        ) / np.sqrt(revision_variance)
        result[f"filtered_{quantity}_sd"] = np.sqrt(
            result.pop(f"filtered_{quantity}_variance")
        )
        result[f"smoothed_{quantity}_sd"] = np.sqrt(
            result.pop(f"smoothed_{quantity}_variance")
        )
    output_columns = [
        "match_id",
        "match_date",
        "surface",
        "player_id",
        "filtered_overall_mean",
        "filtered_overall_sd",
        "smoothed_overall_mean",
        "smoothed_overall_sd",
        "overall_revision_z",
        "filtered_played_surface_mean",
        "filtered_played_surface_sd",
        "smoothed_played_surface_mean",
        "smoothed_played_surface_sd",
        "played_surface_revision_z",
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result[output_columns].to_csv(output_path, index=False, float_format="%.10g")
    return result[output_columns]


def main() -> None:
    repository_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data",
        type=Path,
        default=repository_root / "assets/data/wta-state-revision-audit.csv",
    )
    parser.add_argument(
        "--matchup-data",
        type=Path,
        default=repository_root / "assets/data/wta-matchup-revision-audit.csv",
    )
    parser.add_argument("--rebuild-from-tennis-root", type=Path)
    parser.add_argument("--audit-season", type=int, default=2024)
    parser.add_argument("--smoothing-end-season", type=int, default=2025)
    parser.add_argument("--seed", type=int, default=20260907)
    parser.add_argument("--bootstrap-draws", type=int, default=5000)
    args = parser.parse_args()

    if args.rebuild_from_tennis_root is not None:
        build_revision_data(
            args.rebuild_from_tennis_root,
            args.data,
            args.matchup_data,
            args.audit_season,
            args.smoothing_end_season,
        )
    frame = pd.read_csv(args.data)
    matchup_frame = pd.read_csv(args.matchup_data)
    print(
        json.dumps(
            summarize(frame, matchup_frame, args.seed, args.bootstrap_draws),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
