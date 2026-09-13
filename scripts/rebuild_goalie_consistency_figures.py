"""Rebuild the canonical Goalie consistency figures in the shared site theme.

The original simulation and NHL inputs are no longer stored in this repository.
The retained CSV files contain points digitized from the published figures; the
inter-game distributions are reconstructed from their published means and SDs.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.spazz_plot import GOLD, MUTED_DARK, finish_axes, save_figure, spazz_theme

DATA = ROOT / "assets" / "data"
OUT = ROOT / "figs"

GOALIES = {
    "A": (89.05, 8.38),
    "B": (89.63, 8.31),
    "C": (91.01, 7.95),
    "D": (92.68, 7.29),
    "E": (94.70, 6.26),
}


def read_points(name: str) -> tuple[np.ndarray, np.ndarray]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    columns = list(rows[0])
    x = np.asarray([float(row[columns[0]]) for row in rows])
    y = np.asarray([float(row[columns[1]]) for row in rows])
    return x, y


def draw_scatter(ax, x: np.ndarray, y: np.ndarray, correlation: str) -> None:
    ax.scatter(
        x,
        y,
        s=20,
        facecolor=GOLD,
        edgecolor=GOLD,
        linewidth=0.6,
        alpha=0.48,
    )
    ax.text(
        0.04,
        0.08,
        correlation,
        color=MUTED_DARK,
        transform=ax.transAxes,
    )


def main() -> None:
    import matplotlib.pyplot as plt

    with spazz_theme():
        grid = np.linspace(58, 120, 500)
        fig, ax = plt.subplots(figsize=(7.5, 5.0))
        for index, (label, (mean, sd)) in enumerate(GOALIES.items()):
            baseline = len(GOALIES) - index
            density = norm.pdf(grid, mean, sd)
            density /= density.max()
            alpha = 1.0 - index * 0.13
            ax.fill_between(
                grid,
                baseline,
                baseline + 0.72 * density,
                color=GOLD,
                alpha=0.08 + 0.025 * alpha,
            )
            ax.plot(
                grid,
                baseline + 0.72 * density,
                color=GOLD,
                alpha=alpha,
            )
        ax.set_yticks(range(1, 6), list(GOALIES)[::-1])
        finish_axes(ax, xlabel="Standing points")
        save_figure(fig, OUT / "goalie-consistency-intergame.png")

        x, y = read_points("goalie-consistency-simulated-shots.csv")
        fig, ax = plt.subplots()
        draw_scatter(ax, x, y, "r = 0.061")
        finish_axes(
            ax,
            xlabel="Streakiness percentile",
            ylabel="Expected standing points",
        )
        save_figure(fig, OUT / "goalie-consistency-intershot-simulation.png")

        x, y = read_points("goalie-consistency-season-performance.csv")
        fig, ax = plt.subplots()
        draw_scatter(ax, x, y, "r = −0.044")
        finish_axes(
            ax,
            xlabel="Streakiness percentile",
            ylabel="Season GSAx / xG",
        )
        save_figure(fig, OUT / "goalie-consistency-performance.png")

        x, y = read_points("goalie-consistency-career-persistence.csv")
        fig, ax = plt.subplots()
        draw_scatter(ax, x, y, "r = −0.029")
        finish_axes(
            ax,
            xlabel="Career average streakiness percentile",
            ylabel="Career average year-over-year change in GSAx / xG",
        )
        save_figure(fig, OUT / "goalie-consistency-persistence.png")

    print(f"rebuilt Goalie consistency figures in {OUT}")


if __name__ == "__main__":
    main()
