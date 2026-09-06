"""Shared plotting style for spazznolo.github.io.

The theme keeps figures close to the site's visual language: one warm signal
colour, quiet supporting marks, no grid, no tick marks, and no title duplicated
inside the image. Article prose should supply the figure title and explanation.
"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


GOLD = "#DDB85C"
NIGHT = "#090908"
PAPER = "#F4F0E7"
INK = "#211D17"
CHALK = "#EEEAE2"
MUTED_DARK = "#938D84"
MUTED_LIGHT = "#665F54"
FONT_PATH = Path(__file__).resolve().parents[1] / "assets/fonts/IBMPlexSans.ttf"


def _matplotlib() -> tuple[Any, Any]:
    try:
        import matplotlib as mpl
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Plotting requires matplotlib; install the plotting environment first."
        ) from exc
    if FONT_PATH.exists():
        mpl.font_manager.fontManager.addfont(FONT_PATH)
    return mpl, plt


def _rc(dark: bool) -> dict[str, object]:
    mpl, _ = _matplotlib()
    foreground = CHALK if dark else INK
    muted = MUTED_DARK if dark else MUTED_LIGHT
    return {
        "figure.facecolor": "none",
        "figure.dpi": 140,
        "figure.figsize": (7.5, 4.5),
        "savefig.facecolor": "none",
        "savefig.edgecolor": "none",
        "savefig.transparent": True,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.08,
        "axes.facecolor": "none",
        "axes.edgecolor": muted,
        "axes.labelcolor": foreground,
        "axes.titlecolor": GOLD,
        "axes.titlelocation": "left",
        "axes.titlesize": 11,
        "axes.titleweight": 600,
        "axes.grid": False,
        "axes.prop_cycle": mpl.cycler(
            color=[GOLD, GOLD, GOLD, GOLD],
            alpha=[1.0, 0.78, 0.56, 0.36],
        ),
        "font.family": "sans-serif",
        "font.sans-serif": ["IBM Plex Sans", "DejaVu Sans"],
        "font.size": 11,
        "xtick.color": muted,
        "ytick.color": muted,
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        "xtick.minor.size": 0,
        "ytick.minor.size": 0,
        "legend.facecolor": "none",
        "legend.edgecolor": "none",
        "legend.frameon": False,
        "legend.labelcolor": foreground,
        "lines.color": GOLD,
        "lines.linewidth": 1.8,
        "patch.edgecolor": "none",
        "patch.facecolor": GOLD,
        "text.color": foreground,
    }


@contextmanager
def spazz_theme(*, dark: bool = True) -> Iterator[None]:
    """Apply the site theme within a temporary matplotlib context."""

    mpl, _ = _matplotlib()
    with mpl.rc_context(rc=_rc(dark)):
        yield


def finish_axes(
    ax: Any,
    *,
    xlabel: str | None = None,
    ylabel: str | None = None,
) -> Any:
    """Remove chart furniture and retain only useful labels."""

    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(which="both", length=0)
    if xlabel is not None:
        ax.set_xlabel(xlabel, labelpad=12)
    if ylabel is not None:
        ax.set_ylabel(ylabel, labelpad=12)
    return ax


def save_figure(
    fig: Any,
    path: str | Path,
    *,
    dpi: int = 240,
) -> Path:
    """Save a web-ready figure with stable dimensions and close it."""

    _, plt = _matplotlib()
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=dpi)
    plt.close(fig)
    return output
