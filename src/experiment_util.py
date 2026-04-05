"""Shared setup for Phase 4 experiment scripts (non-interactive figures)."""

from __future__ import annotations


def configure_matplotlib() -> None:
    """Select Agg backend; call **before** ``import matplotlib.pyplot``."""
    import matplotlib

    matplotlib.use("Agg")


def apply_plot_style() -> None:
    import matplotlib.pyplot as plt

    try:
        plt.style.use("seaborn-v0_8-whitegrid")
    except OSError:
        plt.style.use("ggplot")
