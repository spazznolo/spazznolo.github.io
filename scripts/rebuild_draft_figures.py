"""Rebuild the illustrative NHL Pick Probability figures.

The values reproduce the assumptions stated in the article. Figures use the
shared site theme and a fixed seed so future renders remain stable.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.stats import gaussian_kde

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.spazz_plot import GOLD, MUTED_DARK, finish_axes, save_figure, spazz_theme

OUT = ROOT / "figs"
RNG = np.random.default_rng(2023)
PROSPECTS = {
    "Bedard": (24.0, 3.0),
    "Fantilli": (19.0, 4.0),
    "Michkov": (17.5, 7.0),
    "Carlsson": (14.0, 4.5),
    "Smith": (10.0, 5.0),
}
PICK_WEIGHTS = {
    1: [1.0, 0.0, 0.0, 0.0, 0.0],
    2: [0.0019, 0.9981, 0.0, 0.0, 0.0],
    3: [0.0, 0.2098, 0.7902, 0.0, 0.0],
    4: [0.0, 0.0278, 0.4204, 0.5518, 0.0],
    5: [0.0, 0.0021, 0.1113, 0.2687, 0.6179],
}


def density(values: np.ndarray, grid: np.ndarray) -> np.ndarray:
    return gaussian_kde(values)(grid)


def draw_ridges(ax, samples: list[np.ndarray], labels: list[str]) -> None:
    grid = np.linspace(0, 43, 500)
    for index, (values, label) in enumerate(zip(samples, labels, strict=True)):
        baseline = len(samples) - index
        curve = density(values, grid)
        curve /= curve.max()
        alpha = 1.0 - index * 0.13
        ax.fill_between(grid, baseline, baseline + 0.78 * curve, color=GOLD, alpha=0.12 + 0.05 * alpha)
        ax.plot(grid, baseline + 0.78 * curve, color=GOLD, alpha=alpha)
    ax.set_yticks(range(1, len(labels) + 1), labels[::-1])
    ax.set_xlim(0, 43)
    finish_axes(ax, xlabel="7-year predicted WAR")


def prospect_samples(n: int = 100_000) -> dict[str, np.ndarray]:
    return {name: RNG.normal(mean, sd, n) for name, (mean, sd) in PROSPECTS.items()}


def pick_samples(n: int = 100_000) -> dict[int, np.ndarray]:
    names = list(PROSPECTS)
    values = {}
    for pick, weights in PICK_WEIGHTS.items():
        choice = RNG.choice(len(names), size=n, p=np.asarray(weights) / np.sum(weights))
        draw = np.empty(n)
        for index, name in enumerate(names):
            mask = choice == index
            mean, sd = PROSPECTS[name]
            draw[mask] = RNG.normal(mean, sd, mask.sum())
        values[pick] = draw
    return values


def main() -> None:
    import matplotlib.pyplot as plt
    from matplotlib.ticker import PercentFormatter

    prospects = prospect_samples()
    picks = pick_samples()

    with spazz_theme():
        grid = np.linspace(10, 40, 500)
        bedard = prospects["Bedard"]
        curve = density(bedard, grid)
        fig, ax = plt.subplots()
        ax.fill_between(grid, curve, color=GOLD, alpha=0.16)
        ax.plot(grid, curve, color=GOLD)
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        finish_axes(ax, xlabel="7-year predicted WAR")
        save_figure(fig, OUT / "draft-probabilities-4-1.png")

        fig, ax = plt.subplots(figsize=(7.5, 5.0))
        draw_ridges(ax, list(prospects.values()), list(prospects))
        save_figure(fig, OUT / "draft-probabilities-4-2.png")

        fig, ax = plt.subplots(figsize=(7.5, 5.0))
        draw_ridges(ax, list(picks.values()), [f"Pick {pick}" for pick in picks])
        save_figure(fig, OUT / "draft-probabilities-4-3.png")

        difference = picks[4] - RNG.permutation(picks[5])
        grid = np.linspace(np.quantile(difference, 0.002), np.quantile(difference, 0.998), 500)
        curve = density(difference, grid)
        mean = difference.mean()
        fig, ax = plt.subplots()
        ax.fill_between(grid, curve, color=GOLD, alpha=0.16)
        ax.plot(grid, curve, color=GOLD)
        ax.axvline(mean, color=GOLD, linestyle="--", alpha=0.62)
        ax.text(
            0.98,
            0.92,
            f"mean difference  {mean:.2f} WAR",
            color=MUTED_DARK,
            ha="right",
            transform=ax.transAxes,
        )
        ax.set_yticks([])
        finish_axes(ax, xlabel="Value difference, pick 4 − pick 5 (WAR)")
        save_figure(fig, OUT / "draft-probabilities-4-4.png")

    print(f"rebuilt draft figures in {OUT}")
    print(f"pick 4 mean: {picks[4].mean():.3f}")
    print(f"pick 5 mean: {picks[5].mean():.3f}")
    print(f"difference mean: {difference.mean():.3f}")
    print(f"P(pick 4 > pick 5): {(difference > 0).mean():.3f}")


if __name__ == "__main__":
    main()
