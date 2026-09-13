"""Rebuild the Post-regulation scatterplots in the shared site theme.

The original analysis data are no longer available in this repository. The two
small CSV files contain points digitized from the published figures, preserving
the evidence while allowing the presentation to remain reproducible.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.spazz_plot import GOLD, MUTED_DARK, finish_axes, save_figure, spazz_theme

DATA = ROOT / "assets" / "data"
OUT = ROOT / "figs"


def read_points(name: str) -> tuple[np.ndarray, np.ndarray]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    columns = list(rows[0])
    x = np.asarray([float(row[columns[0]]) for row in rows])
    y = np.asarray([float(row[columns[1]]) for row in rows])
    return x, y


def scatter(ax, x: np.ndarray, y: np.ndarray) -> None:
    ax.scatter(
        x,
        y,
        s=25,
        facecolor=GOLD,
        edgecolor=GOLD,
        linewidth=0.7,
        alpha=0.58,
    )


def main() -> None:
    import matplotlib.pyplot as plt
    from matplotlib.ticker import PercentFormatter

    with spazz_theme():
        x, y = read_points("post-regulation-overtime-frequency.csv")
        fig, ax = plt.subplots()
        scatter(ax, x, y)
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        finish_axes(
            ax,
            xlabel="Regulation points per game",
            ylabel="Share of games reaching overtime",
        )
        save_figure(fig, OUT / "post-regulation-zero-one.png")

        x, y = read_points("post-regulation-overtime-results.csv")
        fig, ax = plt.subplots()
        scatter(ax, x, y)
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        ax.text(
            0.04,
            0.08,
            "r = 0.10",
            color=MUTED_DARK,
            transform=ax.transAxes,
        )
        finish_axes(
            ax,
            xlabel="Regulation points per game",
            ylabel="Overtime points share",
        )
        save_figure(fig, OUT / "post-regulation-two-one.png")

    print(f"rebuilt Post-regulation figures in {OUT}")


if __name__ == "__main__":
    main()
