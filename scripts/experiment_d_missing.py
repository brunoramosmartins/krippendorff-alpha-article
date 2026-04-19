#!/usr/bin/env python3
"""Experiment D — missing data: Fleiss vs Krippendorff (Phase 4)."""

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

    # Collect alpha across multiple seeds per missing rate
    alpha_runs = np.zeros((len(MISSING_RATES), N_SEEDS))
    fleiss_vals: list[float] = []

    for idx, rate in enumerate(MISSING_RATES):
        for s in range(N_SEEDS):
            rng = np.random.default_rng(BASE_SEED + 11 + idx * 97 + s * 7)
            arr = base.copy()
            if rate > 0:
                miss = rng.random(arr.shape) < rate
                arr[miss] = np.nan
            df = pd.DataFrame(arr)
            alpha_runs[idx, s] = krippendorff_alpha(df, level_of_measurement="nominal")
        # Fleiss: use first seed only (it's NaN for any missing rate > 0 anyway)
        rng0 = np.random.default_rng(BASE_SEED + 11 + idx * 97)
        arr0 = base.copy()
        if rate > 0:
            miss0 = rng0.random(arr0.shape) < rate
            arr0[miss0] = np.nan
        fleiss_vals.append(fleiss_kappa_or_nan(pd.DataFrame(arr0)))

    alpha_mean = alpha_runs.mean(axis=1)
    alpha_std = alpha_runs.std(axis=1)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=120)
    x_pct = [int(round(100 * r)) for r in MISSING_RATES]
    ax.errorbar(
        x_pct,
        alpha_mean,
        yerr=alpha_std,
        fmt="o-",
        color="#1f77b4",
        capsize=4,
        capthick=1.5,
        label=r"Krippendorff $\alpha$ (mean $\pm$ 1 SD, 10 seeds)",
    )
    # Fleiss: plot valid points, leave gaps for nan
    kf_y = np.array(fleiss_vals, dtype=float)
    ax.plot(
        x_pct,
        kf_y,
        "s--",
        color="#d95f02",
        label=r"Fleiss $\kappa_F$ (complete matrix only; else NaN)",
    )
    ax.set_xlabel("MCAR missing rate (% of cells)")
    ax.set_ylabel("Coefficient value")
    ax.set_title("Experiment D: robustness to missing annotations")
    ax.legend(loc="best", fontsize=9)
    ax.set_xticks(x_pct)
    ax.set_ylim(0.0, max(alpha_mean) + 0.15)
    fig.tight_layout()
    out = ROOT / "figures" / "exp_d_missing_robustness.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")
    for idx, (r, k) in enumerate(zip(MISSING_RATES, fleiss_vals, strict=True)):
        ks = "nan" if np.isnan(k) else f"{k:.4f}"
        print(f"  missing={r:.0%}: alpha={alpha_mean[idx]:.4f} (±{alpha_std[idx]:.4f}), fleiss={ks}")


if __name__ == "__main__":
    main()
