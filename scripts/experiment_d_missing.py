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

    alphas: list[float] = []
    fleiss_vals: list[float] = []

    for idx, rate in enumerate(MISSING_RATES):
        rng = np.random.default_rng(BASE_SEED + 11 + idx * 97)
        arr = base.copy()
        if rate > 0:
            miss = rng.random(arr.shape) < rate
            arr[miss] = np.nan
        df = pd.DataFrame(arr)
        alphas.append(krippendorff_alpha(df, level_of_measurement="nominal"))
        fleiss_vals.append(fleiss_kappa_or_nan(df))

    fig, ax = plt.subplots(figsize=(8, 5), dpi=120)
    ax.plot(
        [int(round(100 * r)) for r in MISSING_RATES],
        alphas,
        "o-",
        color="#1f77b4",
        label=r"Krippendorff $\alpha$ (handles missing cells)",
    )
    # Fleiss: plot valid points, leave gaps for nan
    x_pct = [int(round(100 * r)) for r in MISSING_RATES]
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
    fig.tight_layout()
    out = ROOT / "figures" / "exp_d_missing_robustness.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")
    for r, a, k in zip(MISSING_RATES, alphas, fleiss_vals, strict=True):
        ks = "nan" if np.isnan(k) else f"{k:.4f}"
        print(f"  missing={r:.0%}: alpha={a:.4f}, fleiss={ks}")


if __name__ == "__main__":
    main()
