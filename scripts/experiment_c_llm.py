#!/usr/bin/env python3
"""Experiment C — synthetic LLM vs human panel (Phase 4)."""

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

from src.metrics import cohens_kappa, fleiss_kappa, krippendorff_alpha, observed_agreement
from src.simulate import SimulatedAnnotation

N_ITEMS = 10_000
HUMAN_NOISE = 0.10
DEFAULT_LLM_NOISE = 0.15
BASE_SEED = 700


def panel(llm_noise: float, seed: int) -> pd.DataFrame:
    eps = [HUMAN_NOISE, HUMAN_NOISE, HUMAN_NOISE, llm_noise]
    gen = SimulatedAnnotation(
        n_items=N_ITEMS,
        n_annotators=4,
        n_classes=3,
        noise_level=eps,
        class_dist="uniform",
        pure_random=False,
        seed=seed,
    )
    return gen.generate()


def main() -> None:
    apply_plot_style()

    df = panel(DEFAULT_LLM_NOISE, BASE_SEED)
    arr = df.to_numpy(dtype=float)

    ao = observed_agreement(df)
    kf = fleiss_kappa(arr)
    alpha_all = krippendorff_alpha(df, level_of_measurement="nominal")
    alpha_hum = krippendorff_alpha(df.iloc[:, :3], level_of_measurement="nominal")

    print("=== Default scenario (LLM noise=0.15, humans=0.10) ===")
    print(f"Observed agreement A_o (all four): {ao:.4f}")
    print(f"Fleiss kappa (all four): {kf:.4f}")
    print(f"Krippendorff alpha (humans only): {alpha_hum:.4f}")
    print(f"Krippendorff alpha (humans + LLM): {alpha_all:.4f}")
    print("Pairwise Cohen kappa (human vs LLM, column r3):")
    for h in range(3):
        ck = cohens_kappa(df.iloc[:, h], df.iloc[:, 3])
        print(f"  r{h} vs LLM: {ck:.4f}")
    # Negative => panel reliability drops when the LLM joins (alpha_all < alpha_hum).
    print(f"Alpha change when adding LLM (all minus humans-only): {alpha_all - alpha_hum:+.4f}")

    llm_grid = np.linspace(0.0, 0.5, 21)
    alphas_all: list[float] = []
    alphas_hum: list[float] = []
    for idx, ln in enumerate(llm_grid):
        dfp = panel(ln, BASE_SEED + idx)
        alphas_all.append(krippendorff_alpha(dfp, level_of_measurement="nominal"))
        alphas_hum.append(krippendorff_alpha(dfp.iloc[:, :3], level_of_measurement="nominal"))

    fig, ax = plt.subplots(figsize=(8, 5), dpi=120)
    ax.plot(llm_grid, alphas_all, "o-", label=r"$\alpha$ (humans + LLM)")
    ax.plot(llm_grid, alphas_hum, "s--", label=r"$\alpha$ (humans only)")
    ax.axvline(DEFAULT_LLM_NOISE, color="gray", linestyle=":", label="default LLM noise")
    # annotate largest drop in alpha_all between consecutive points
    dalpha = np.diff(alphas_all)
    j = int(np.argmin(dalpha))
    ax.annotate(
        "steepest drop\n(in this grid)",
        xy=(float(llm_grid[j + 1]), alphas_all[j + 1]),
        xytext=(0.35, min(alphas_all) + 0.05),
        arrowprops=dict(arrowstyle="->", color="0.3", lw=1.5),
        fontsize=11,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.7", alpha=0.85),
    )
    ax.set_xlabel(r"LLM noise level $\varepsilon_{\mathrm{LLM}}$")
    ax.set_ylabel(r"Krippendorff $\alpha$ (nominal)")
    ax.set_title("Experiment C: sensitivity of $\\alpha$ to simulated LLM noise")
    ax.legend(loc="best", fontsize=9)
    ax.set_ylim(bottom=min(0.0, min(alphas_all) - 0.05))
    fig.tight_layout()
    out = ROOT / "figures" / "exp_c_llm_vs_humans.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
