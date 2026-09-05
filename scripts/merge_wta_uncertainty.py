"""Merge exact player-week uncertainty into a published WTA ranking archive."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


SURFACES = ("overall", "hard", "clay", "grass")
KEYS = ["week_ending", "player_id"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--history", type=Path, required=True)
    parser.add_argument("--uncertainty", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    history = pd.read_csv(args.history, dtype={"player_id": str})
    uncertainty = pd.read_csv(args.uncertainty, dtype={"player_id": str})
    if history.duplicated(KEYS).any() or uncertainty.duplicated(KEYS).any():
        raise ValueError("player-week keys must be unique in both inputs")

    uncertainty_columns = {
        f"{surface}_sd": f"conditional_{surface}_sd_backfill"
        for surface in SURFACES
    }
    backfill = uncertainty[KEYS + list(uncertainty_columns)].rename(
        columns=uncertainty_columns
    )
    merged = history.merge(backfill, on=KEYS, how="left", validate="one_to_one")
    for surface in SURFACES:
        column = f"conditional_{surface}_sd"
        backfill_column = f"{column}_backfill"
        merged[column] = merged[backfill_column].combine_first(merged[column])
        merged = merged.drop(columns=backfill_column)

    missing = merged[[f"conditional_{surface}_sd" for surface in SURFACES]].isna().any(axis=1)
    if missing.any():
        raise ValueError(f"uncertainty remains missing for {int(missing.sum()):,} player-weeks")

    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    merged.to_csv(temporary, index=False, float_format="%.10g")
    temporary.replace(args.output)
    print(f"Merged exact uncertainty for {len(merged):,} player-weeks into {args.output}")


if __name__ == "__main__":
    main()
