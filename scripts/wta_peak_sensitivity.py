#!/usr/bin/env python3
"""Compare fixed WTA peak ages on the same 2024-2025 forecast panel."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


PEAKS = (22, 24, 26, 28)


def log_loss_rows(outcome: np.ndarray, probability: np.ndarray) -> np.ndarray:
    probability = np.clip(np.asarray(probability, dtype=float), 1e-12, 1.0 - 1e-12)
    outcome = np.asarray(outcome, dtype=float)
    return -(outcome * np.log(probability) + (1.0 - outcome) * np.log(1.0 - probability))


def clustered_interval(
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
    return [float(value) for value in np.quantile(estimates, [0.025, 0.975])]


def main() -> None:
    repository_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data",
        type=Path,
        default=repository_root / "assets/data/wta-peak-sensitivity.csv",
    )
    parser.add_argument("--seed", type=int, default=20260907)
    parser.add_argument("--bootstrap-draws", type=int, default=5000)
    args = parser.parse_args()

    frame = pd.read_csv(args.data)
    expected = {"match_id", "match_date", "player_1_won"} | {
        f"probability_peak_{peak}" for peak in PEAKS
    }
    missing = sorted(expected - set(frame.columns))
    if missing:
        raise ValueError(f"Sensitivity data is missing columns: {missing}")
    if frame["match_id"].duplicated().any():
        raise ValueError("Sensitivity data contains duplicate matches")

    outcome = frame["player_1_won"].to_numpy(dtype=float)
    date_codes, dates = pd.factorize(pd.to_datetime(frame["match_date"]), sort=True)
    rng = np.random.default_rng(args.seed)
    losses = {
        peak: log_loss_rows(outcome, frame[f"probability_peak_{peak}"].to_numpy(dtype=float))
        for peak in PEAKS
    }
    report = {"matches": len(frame), "calendar_days": len(dates), "candidates": {}}
    for peak in PEAKS:
        difference = losses[peak] - losses[24]
        report["candidates"][str(peak)] = {
            "log_loss": float(np.mean(losses[peak])),
            "difference_from_peak_24": float(np.mean(difference)),
            "day_clustered_95": clustered_interval(
                difference,
                date_codes,
                len(dates),
                rng,
                args.bootstrap_draws,
            ),
        }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
