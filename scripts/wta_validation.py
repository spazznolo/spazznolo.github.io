#!/usr/bin/env python3
"""Validate the frozen off-season WTA model on the 2024-2025 forecasts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


YEARS = (2024, 2025)
# Historical artifact name: "exponential" describes strength after exponentiating
# the rating. On the modeled log-odds scale, curve_power=1 is piecewise linear.
EVALUATION_ARTIFACT_DIRECTORY = "collapsed_wta_market_fixed_peak24_exponential_v1"
EXPECTED_AGE_CURVE = {"peak_age": 24.0, "power": 1.0}


def logistic(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    return np.where(
        values >= 0,
        1.0 / (1.0 + np.exp(-values)),
        np.exp(values) / (1.0 + np.exp(values)),
    )


def logit(probability: np.ndarray) -> np.ndarray:
    probability = np.clip(np.asarray(probability, dtype=float), 1e-9, 1.0 - 1e-9)
    return np.log(probability / (1.0 - probability))


def log_loss_rows(outcome: np.ndarray, probability: np.ndarray) -> np.ndarray:
    probability = np.clip(np.asarray(probability, dtype=float), 1e-12, 1.0 - 1e-12)
    outcome = np.asarray(outcome, dtype=float)
    return -(outcome * np.log(probability) + (1.0 - outcome) * np.log(1.0 - probability))


def calibration_fit(
    outcome: np.ndarray,
    probability: np.ndarray,
    weights: np.ndarray | None = None,
) -> tuple[float, float]:
    outcome = np.asarray(outcome, dtype=float)
    design = np.column_stack([np.ones(len(outcome)), logit(probability)])
    weights = np.ones(len(outcome)) if weights is None else np.asarray(weights, dtype=float)
    coefficient = np.array([0.0, 1.0])
    for _ in range(30):
        fitted = logistic(design @ coefficient)
        variance = np.clip(fitted * (1.0 - fitted), 1e-9, None)
        score = design.T @ (weights * (outcome - fitted))
        information = design.T @ ((weights * variance)[:, None] * design)
        step = np.linalg.solve(information, score)
        coefficient += step
        if float(np.max(np.abs(step))) < 1e-10:
            break
    return float(coefficient[0]), float(coefficient[1])


def percentile_interval(draws: np.ndarray) -> list[float]:
    return [float(value) for value in np.quantile(draws, [0.025, 0.975])]


def day_clustered_mean_interval(
    values: np.ndarray,
    date_codes: np.ndarray,
    cluster_count: int,
    rng: np.random.Generator,
    draws: int,
) -> list[float]:
    cluster_sum = np.bincount(date_codes, weights=values, minlength=cluster_count)
    cluster_n = np.bincount(date_codes, minlength=cluster_count)
    estimates = np.empty(draws)
    probability = np.full(cluster_count, 1.0 / cluster_count)
    for draw in range(draws):
        multiplicity = rng.multinomial(cluster_count, probability)
        estimates[draw] = float(multiplicity @ cluster_sum) / float(multiplicity @ cluster_n)
    return percentile_interval(estimates)


def calibration_interval(
    outcome: np.ndarray,
    probability: np.ndarray,
    date_codes: np.ndarray,
    cluster_count: int,
    rng: np.random.Generator,
    draws: int,
) -> dict[str, list[float]]:
    estimates = np.empty((draws, 2))
    cluster_probability = np.full(cluster_count, 1.0 / cluster_count)
    for draw in range(draws):
        multiplicity = rng.multinomial(cluster_count, cluster_probability)
        estimates[draw] = calibration_fit(outcome, probability, multiplicity[date_codes])
    return {
        "intercept_95": percentile_interval(estimates[:, 0]),
        "slope_95": percentile_interval(estimates[:, 1]),
    }


def correlation_from_sums(sums: np.ndarray) -> float:
    n, sum_x, sum_y, sum_xx, sum_yy, sum_xy = sums
    covariance = sum_xy - sum_x * sum_y / n
    variance_x = sum_xx - sum_x * sum_x / n
    variance_y = sum_yy - sum_y * sum_y / n
    return float(covariance / np.sqrt(variance_x * variance_y))


def player_clustered_correlation_interval(
    pairs: pd.DataFrame,
    rng: np.random.Generator,
    draws: int,
) -> list[float]:
    summaries = []
    for _, group in pairs.groupby("player_id", sort=False):
        x = group["previous_innovation"].to_numpy(dtype=float)
        y = group["innovation"].to_numpy(dtype=float)
        summaries.append(
            [len(group), x.sum(), y.sum(), np.square(x).sum(), np.square(y).sum(), (x * y).sum()]
        )
    summaries = np.asarray(summaries, dtype=float)
    cluster_count = len(summaries)
    probability = np.full(cluster_count, 1.0 / cluster_count)
    estimates = np.empty(draws)
    for draw in range(draws):
        multiplicity = rng.multinomial(cluster_count, probability)
        estimates[draw] = correlation_from_sums(multiplicity @ summaries)
    return percentile_interval(estimates)


def load_predictions(tennis_root: Path) -> pd.DataFrame:
    model_root = tennis_root / "apps/predict/output/models" / EVALUATION_ARTIFACT_DIRECTORY
    frames = []
    for year in YEARS:
        frame = pd.read_csv(model_root / str(year) / "predictions.csv")
        fit = json.loads((model_root / str(year) / "fit.json").read_text(encoding="utf-8"))
        if fit.get("age_curve") != EXPECTED_AGE_CURVE:
            raise ValueError(
                f"{year} evaluation uses {fit.get('age_curve')}, expected {EXPECTED_AGE_CURVE}"
            )
        parameters = fit["system_parameters"]
        interpretation = fit["interpretation"]
        vig_z = (
            frame["vig"].to_numpy(dtype=float) - float(interpretation["training_vig_mean"])
        ) / float(interpretation["training_vig_sd"])
        observation_sd = float(parameters["observation_sd"]) * np.exp(
            float(parameters["vig_log_sd_slope"]) * vig_z
        )
        frame["predictive_market_sd"] = np.sqrt(
            np.square(frame["model_logit_sd"].to_numpy(dtype=float)) + np.square(observation_sd)
        )
        frames.append(frame)
    model = pd.concat(frames, ignore_index=True)
    elo = pd.read_csv(
        tennis_root / "apps/predict/output/models/standard_elo_blog/predictions.csv",
        usecols=["match_id", "elo_prob_home"],
    )
    merged = model.merge(elo, on="match_id", how="inner", validate="one_to_one")
    if len(merged) != len(model):
        raise ValueError("Elo and player-state evaluations do not contain the same matches")
    merged["match_date"] = pd.to_datetime(merged["match_date"])
    merged["match_timestamp"] = pd.to_datetime(merged["match_timestamp"], format="mixed")
    return merged.sort_values(["match_timestamp", "match_id"], kind="stable").reset_index(drop=True)


def serial_pairs(frame: pd.DataFrame) -> pd.DataFrame:
    shared = ["match_id", "tournament_id", "match_timestamp", "match_date"]
    home = frame[shared + ["player_id_home", "standardized_innovation"]].copy()
    home.columns = shared + ["player_id", "innovation"]
    away = frame[shared + ["player_id_away", "standardized_innovation"]].copy()
    away.columns = shared + ["player_id", "innovation"]
    away["innovation"] *= -1.0
    appearances = pd.concat([home, away], ignore_index=True).sort_values(
        ["player_id", "match_timestamp"], kind="stable"
    )
    appearances["previous_innovation"] = appearances.groupby("player_id")["innovation"].shift()
    appearances["previous_date"] = appearances.groupby("player_id")["match_date"].shift()
    appearances["previous_match_id"] = appearances.groupby("player_id")["match_id"].shift()
    appearances["previous_tournament_id"] = appearances.groupby("player_id")["tournament_id"].shift()
    appearances["gap_days"] = (appearances["match_date"] - appearances["previous_date"]).dt.days
    appearances["same_tournament"] = (
        appearances["tournament_id"] == appearances["previous_tournament_id"]
    )
    return appearances.loc[appearances["gap_days"].gt(0)].dropna().reset_index(drop=True)


def main() -> None:
    default_tennis_root = Path(__file__).resolve().parents[2] / "tennis"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tennis-root", type=Path, default=default_tennis_root)
    parser.add_argument("--seed", type=int, default=20260907)
    parser.add_argument("--bootstrap-draws", type=int, default=5000)
    args = parser.parse_args()

    frame = load_predictions(args.tennis_root)
    outcome = frame["winner_is_home"].to_numpy(dtype=float)
    model_probability = frame["model_prob_home"].to_numpy(dtype=float)
    market_probability = frame["market_prob_home"].to_numpy(dtype=float)
    elo_probability = frame["elo_prob_home"].to_numpy(dtype=float)
    date_codes, dates = pd.factorize(frame["match_date"], sort=True)
    cluster_count = len(dates)
    rng = np.random.default_rng(args.seed)

    model_loss = log_loss_rows(outcome, model_probability)
    market_loss = log_loss_rows(outcome, market_probability)
    elo_loss = log_loss_rows(outcome, elo_probability)
    benchmark = {}
    for name, difference in {
        "model_minus_elo": model_loss - elo_loss,
        "model_minus_market": model_loss - market_loss,
    }.items():
        benchmark[name] = {
            "mean": float(np.mean(difference)),
            "day_clustered_95": day_clustered_mean_interval(
                difference, date_codes, cluster_count, rng, args.bootstrap_draws
            ),
        }

    calibration = {}
    for name, probability in {
        "player_state_model": model_probability,
        "market": market_probability,
        "elo": elo_probability,
    }.items():
        intercept, slope = calibration_fit(outcome, probability)
        calibration[name] = {"intercept": intercept, "slope": slope}
    calibration["player_state_model"].update(
        calibration_interval(
            outcome,
            model_probability,
            date_codes,
            cluster_count,
            rng,
            min(args.bootstrap_draws, 2000),
        )
    )
    calibration_by_subset = {}
    for column in ("season", "surface"):
        calibration_by_subset[column] = {}
        for value, subset in frame.groupby(column, sort=True):
            intercept, slope = calibration_fit(
                subset["winner_is_home"].to_numpy(dtype=float),
                subset["model_prob_home"].to_numpy(dtype=float),
            )
            calibration_by_subset[column][str(value)] = {
                "matches": len(subset),
                "intercept": intercept,
                "slope": slope,
            }

    innovation = (
        frame["market_logit_home"].to_numpy(dtype=float)
        - frame["model_logit_mean"].to_numpy(dtype=float)
    )
    frame["standardized_innovation"] = innovation / frame["predictive_market_sd"].to_numpy(dtype=float)
    standardized = frame["standardized_innovation"].to_numpy(dtype=float)
    coverage = {
        "central_50": float(np.mean(np.abs(standardized) <= 0.6744897501960817)),
        "central_80": float(np.mean(np.abs(standardized) <= 1.2815515655446004)),
        "central_95": float(np.mean(np.abs(standardized) <= 1.959963984540054)),
    }
    predictive_uncertainty = {
        "standardized_innovation_mean": float(np.mean(standardized)),
        "standardized_innovation_sd": float(np.std(standardized, ddof=1)),
        "coverage": coverage,
    }
    predictive_uncertainty_by_surface = {}
    for surface, subset in frame.groupby("surface", sort=True):
        values = subset["standardized_innovation"].to_numpy(dtype=float)
        predictive_uncertainty_by_surface[str(surface)] = {
            "matches": len(subset),
            "standardized_innovation_sd": float(np.std(values, ddof=1)),
            "central_50": float(np.mean(np.abs(values) <= 0.6744897501960817)),
            "central_80": float(np.mean(np.abs(values) <= 1.2815515655446004)),
            "central_95": float(np.mean(np.abs(values) <= 1.959963984540054)),
        }

    pairs = serial_pairs(frame)
    dependence = {}
    windows = {
        "all_positive_gaps": pairs,
        "one_to_seven_days": pairs.loc[pairs["gap_days"].le(7)],
        "one_to_seven_days_same_tournament": pairs.loc[
            pairs["gap_days"].le(7) & pairs["same_tournament"]
        ],
        "one_to_seven_days_different_tournament": pairs.loc[
            pairs["gap_days"].le(7) & ~pairs["same_tournament"]
        ],
        "eight_to_thirty_days": pairs.loc[pairs["gap_days"].between(8, 30)],
        "over_thirty_days": pairs.loc[pairs["gap_days"].gt(30)],
    }
    for name, subset in windows.items():
        correlation = float(subset[["previous_innovation", "innovation"]].corr().iloc[0, 1])
        dependence[name] = {
            "pairs": len(subset),
            "lag_one_correlation": correlation,
            "player_clustered_95": player_clustered_correlation_interval(
                subset, rng, args.bootstrap_draws
            ),
        }

    report = {
        "sample": {
            "matches": len(frame),
            "calendar_days": cluster_count,
            "seasons": list(YEARS),
        },
        "benchmark_differences": benchmark,
        "outcome_calibration": calibration,
        "outcome_calibration_by_subset": calibration_by_subset,
        "predictive_market_uncertainty": predictive_uncertainty,
        "predictive_market_uncertainty_by_surface": predictive_uncertainty_by_surface,
        "serial_market_innovation": dependence,
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
