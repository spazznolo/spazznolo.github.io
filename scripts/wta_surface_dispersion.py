#!/usr/bin/env python3
"""Summarize the cross-player spread in the published WTA ranking states."""

from __future__ import annotations

import argparse
import csv
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "assets/data/wta-rankings-latest.csv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--top", type=int, default=500)
    args = parser.parse_args()

    with args.input.open(newline="", encoding="utf-8") as handle:
        rows = sorted(csv.DictReader(handle), key=lambda row: int(row["rank"]))[: args.top]

    if len(rows) < 2:
        raise ValueError("At least two ranking rows are required")

    columns = (
        ("Overall strength", "overall_mean"),
        ("Hard effect", "hard_effect_mean"),
        ("Clay effect", "clay_effect_mean"),
        ("Grass effect", "grass_effect_mean"),
    )
    overall_sd = statistics.stdev(float(row["overall_mean"]) for row in rows)

    print(f"Snapshot: {rows[0]['as_of_date']}; players: {len(rows)}")
    print("| Quantity | Cross-player SD | Share of overall SD |")
    print("|:--|--:|--:|")
    for label, column in columns:
        sd = statistics.stdev(float(row[column]) for row in rows)
        print(f"| {label} | {sd:.3f} | {sd / overall_sd:.1%} |")


if __name__ == "__main__":
    main()
