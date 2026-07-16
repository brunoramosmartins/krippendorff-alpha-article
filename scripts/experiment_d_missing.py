#!/usr/bin/env python3
"""Experiment D — missing data: Fleiss vs Krippendorff (Phase 4).

Three curves make the contrast explicit under MCAR missingness:

* Krippendorff ``alpha`` — uses every pairable judgment, stays stable.
* Fleiss ``kappa`` on the **full** matrix — defined only at 0% missing, then NaN.
* Fleiss ``kappa`` with **complete-case deletion** — the naive workaround: drop any
  item with a missing cell, then run Fleiss on what remains. Under MCAR the mean is
  ~unbiased, but the retained sample collapses like ``(1 - rate) ** n_raters`` and the
  error bars blow up. A twin axis shows the shrinking share of items kept.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.experiment_util import apply_plot_style, configure_matplotlib

configure_matplotlib()

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.metrics import fleiss_kappa_or_nan, krippendorff_alpha
from src.simulate import SimulatedAnnotation

BASE_SEED = 800
MISSING_RATES = [0.0, 0.10, 0.20, 0.30, 0.40, 0.50]
N_SEEDS = 10  # number of seeds for confidence intervals

ALPHA_COLOR = "#1f77b4"
FLEISS_COLOR = "#d95f02"
DELETION_COLOR = "#2ca02c"
RETAINED_COLOR = "#7f7f7f"


def fleiss_complete_case(arr: np.ndarray) -> tuple[float, float]:
    """Fleiss on complete rows only. Returns (kappa, retained_fraction)."""
    complete = arr[~np.isnan(arr).any(axis=1)]
    retained = complete.shape[0] / arr.shape[0]
    if complete.shape[0] < 2:
        return float("nan"), retained
    return fleiss_kappa_or_nan(pd.DataFrame(complete)), retained


def main() -> None:
    apply_plot_style()

    gen = SimulatedAnnotation(
        n_items=10_000,
        n_annotators=5,
        n_classes=3,
        noise_level=0.15,
        class_dist="uniform",
        pure_random=False,
        seed=BASE_SEED,
    )
    base = gen.generate().to_numpy(dtype=float)

    alpha_runs = np.zeros((len(MISSING_RATES), N_SEEDS))
    deletion_runs = np.full((len(MISSING_RATES), N_SEEDS), np.nan)
    retained_runs = np.zeros((len(MISSING_RATES), N_SEEDS))
    fleiss_full: list[float] = []

    for idx, rate in enumerate(MISSING_RATES):
        for s in range(N_SEEDS):
            rng = np.random.default_rng(BASE_SEED + 11 + idx * 97 + s * 7)
            arr = base.copy()
            if rate > 0:
                miss = rng.random(arr.shape) < rate
                arr[miss] = np.nan
            df = pd.DataFrame(arr)
            alpha_runs[idx, s] = krippendorff_alpha(df, level_of_measurement="nominal")
            deletion_runs[idx, s], retained_runs[idx, s] = fleiss_complete_case(arr)
        # Fleiss on the full matrix: NaN as soon as any cell is missing.
        rng0 = np.random.default_rng(BASE_SEED + 11 + idx * 97)
        arr0 = base.copy()
        if rate > 0:
            arr0[rng0.random(arr0.shape) < rate] = np.nan
        fleiss_full.append(fleiss_kappa_or_nan(pd.DataFrame(arr0)))

    alpha_mean = alpha_runs.mean(axis=1)
    alpha_std = alpha_runs.std(axis=1)
    deletion_mean = np.nanmean(deletion_runs, axis=1)
    deletion_std = np.nanstd(deletion_runs, axis=1)
    retained_mean = retained_runs.mean(axis=1)

    x_pct = [int(round(100 * r)) for r in MISSING_RATES]
    fig, ax = plt.subplots(figsize=(8.4, 5.2), dpi=120)

    # --- alpha: the stable hero, uses all pairable data --------------------
    ax.errorbar(
        x_pct,
        alpha_mean,
        yerr=alpha_std,
        fmt="o-",
        color=ALPHA_COLOR,
        capsize=4,
        capthick=1.5,
        zorder=5,
        label=r"Krippendorff $\alpha$ — all pairable data (mean $\pm$ 1 SD)",
    )

    # --- Fleiss, complete-case deletion: unbiased but exploding variance ---
    ax.errorbar(
        x_pct,
        deletion_mean,
        yerr=deletion_std,
        fmt="^--",
        color=DELETION_COLOR,
        capsize=4,
        capthick=1.5,
        zorder=4,
        label=r"Fleiss $\kappa_F$ — complete-case deletion (mean $\pm$ 1 SD)",
    )

    # --- Fleiss on the full matrix: one valid point, then undefined --------
    ax.plot(
        x_pct[0],
        fleiss_full[0],
        "s",
        color=FLEISS_COLOR,
        markersize=9,
        zorder=6,
        label=r"Fleiss $\kappa_F$ — full matrix (defined only at 0% missing)",
    )
    y_undef = 0.05
    ax.scatter(
        x_pct[1:],
        [y_undef] * (len(x_pct) - 1),
        marker="x",
        s=70,
        color=FLEISS_COLOR,
        linewidths=2,
        zorder=6,
    )
    ax.annotate(
        "Fleiss on the full matrix is undefined\nas soon as any cell is missing (NaN)",
        xy=(x_pct[1], y_undef),
        xytext=(16, 0.235),
        fontsize=8.5,
        color=FLEISS_COLOR,
        arrowprops=dict(arrowstyle="->", color=FLEISS_COLOR, lw=1.1),
    )

    ax.set_xlabel("MCAR missing rate (% of cells)")
    ax.set_ylabel("Coefficient value")
    ax.set_title("Experiment D: robustness to missing annotations")
    ax.set_xticks(x_pct)
    ax.set_ylim(0.0, 0.8)

    # --- twin axis: share of items retained by complete-case deletion ------
    ax2 = ax.twinx()
    ax2.plot(
        x_pct,
        100 * retained_mean,
        ":",
        color=RETAINED_COLOR,
        linewidth=1.6,
        label="Items retained by deletion (right axis)",
    )
    ax2.set_ylabel("% of items kept (complete-case)", color=RETAINED_COLOR)
    ax2.tick_params(axis="y", labelcolor=RETAINED_COLOR)
    ax2.set_ylim(0, 105)
    ax2.grid(False)
    ax2.annotate(
        f"only {100 * retained_mean[-1]:.0f}% of items survive at 50% missing",
        xy=(x_pct[-1], 100 * retained_mean[-1]),
        xytext=(-205, 40),
        textcoords="offset points",
        fontsize=8.5,
        color=RETAINED_COLOR,
        arrowprops=dict(arrowstyle="->", color=RETAINED_COLOR, lw=1.1),
    )

    # merged legend, parked in the empty upper band (curves sit near 0.60)
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(
        lines1 + lines2, labels1 + labels2, loc="upper center", fontsize=8.0,
        framealpha=0.92,
    )

    fig.tight_layout()
    out = ROOT / "figures" / "exp_d_missing_robustness.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")
    for idx, r in enumerate(MISSING_RATES):
        ks = "nan" if np.isnan(fleiss_full[idx]) else f"{fleiss_full[idx]:.4f}"
        print(
            f"  missing={r:.0%}: alpha={alpha_mean[idx]:.4f} (±{alpha_std[idx]:.4f}), "
            f"fleiss_full={ks}, "
            f"fleiss_deletion={deletion_mean[idx]:.4f} (±{deletion_std[idx]:.4f}), "
            f"retained={retained_mean[idx]:.1%}"
        )


if __name__ == "__main__":
    main()
