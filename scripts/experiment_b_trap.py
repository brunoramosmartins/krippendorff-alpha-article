#!/usr/bin/env python3
"""Experiment B — high raw agreement vs low chance-corrected reliability (Phase 4)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.experiment_util import apply_plot_style, configure_matplotlib

configure_matplotlib()

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

from src.metrics import fleiss_kappa, krippendorff_alpha, observed_agreement
from src.simulate import SimulatedAnnotation

IMBALANCE_PRESETS: list[tuple[str, np.ndarray]] = [
    ("uniform", np.array([1 / 3, 1 / 3, 1 / 3])),
    ("60/20/20", np.array([0.60, 0.20, 0.20])),
    ("80/10/10", np.array([0.80, 0.10, 0.10])),
    ("90/5/5", np.array([0.90, 0.05, 0.05])),
    ("95/2.5/2.5", np.array([0.95, 0.025, 0.025])),
]
NOISE_LEVELS = [0.01, 0.05, 0.10, 0.20, 0.30]
N_GRID = 8_000


def main() -> None:
    apply_plot_style()

    n_imb, n_eps = len(IMBALANCE_PRESETS), len(NOISE_LEVELS)
    alpha_grid = np.zeros((n_imb, n_eps))
    ao_grid = np.zeros((n_imb, n_eps))
    trap_mask = np.zeros((n_imb, n_eps), dtype=bool)

    for i, (_, pi) in enumerate(IMBALANCE_PRESETS):
        for j, eps in enumerate(NOISE_LEVELS):
            seed = 500 + i * 31 + j * 17
            gen = SimulatedAnnotation(
                n_items=N_GRID,
                n_annotators=5,
                n_classes=3,
                noise_level=eps,
                class_dist=pi,
                pure_random=False,
                seed=seed,
            )
            df = gen.generate()
            ao_grid[i, j] = observed_agreement(df)
            alpha_grid[i, j] = krippendorff_alpha(df, level_of_measurement="nominal")
            trap_mask[i, j] = ao_grid[i, j] > 0.80 and alpha_grid[i, j] < 0.40

    # Spotlight table: first grid cell that matches the "trap" pattern, else fallback
    trap_idx = np.argwhere(trap_mask)
    if trap_idx.size:
        bi, bj = int(trap_idx[0][0]), int(trap_idx[0][1])
        pi_spot = IMBALANCE_PRESETS[bi][1]
        eps_spot = NOISE_LEVELS[bj]
        lbl_spot = IMBALANCE_PRESETS[bi][0]
        gen0 = SimulatedAnnotation(
            n_items=12_000,
            n_annotators=5,
            n_classes=3,
            noise_level=eps_spot,
            class_dist=pi_spot,
            pure_random=False,
            seed=600 + bi * 41 + bj * 13,
        )
    else:
        lbl_spot = "90/5/5"
        pi_spot = np.array([0.90, 0.05, 0.05])
        eps_spot = 0.05
        gen0 = SimulatedAnnotation(
            n_items=12_000,
            n_annotators=5,
            n_classes=3,
            noise_level=eps_spot,
            class_dist=pi_spot,
            pure_random=False,
            seed=404,
        )

    df0 = gen0.generate()
    ao0 = observed_agreement(df0)
    kf0 = fleiss_kappa(df0.to_numpy(dtype=float))
    a0 = krippendorff_alpha(df0, level_of_measurement="nominal")
    print("=== Summary table (article-ready) ===")
    print(f"(spotlight: pi={lbl_spot}, noise={eps_spot})")
    print("| Metric | Value | Short interpretation |")
    print("|--------|-------|----------------------|")
    print(f"| Observed agreement $A_o$ | {ao0:.3f} | High overlap of labels (prevalence-driven). |")
    print(f"| Fleiss $\\kappa_F$ | {kf0:.3f} | Chance-corrected agreement among five raters. |")
    print(f"| Krippendorff $\\alpha$ | {a0:.3f} | Same data, coincidence-based reliability. |")
    print()
    print("=== Interpretation (draft for article) ===")
    print(
        "Under strong class skew and low annotation noise, raw agreement $A_o$ stays "
        "elevated because raters often pick the majority label even when independence "
        "would already yield high overlap. Fleiss $\\kappa$ and Krippendorff $\\alpha$ "
        "subtract a larger chance baseline, so the same surface agreement can map to "
        "a much smaller reliability coefficient - the 'high $A_o$, low $\\alpha$' trap "
        "central to the thesis."
    )
    print()

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), dpi=120)
    labels = [t[0] for t in IMBALANCE_PRESETS]
    noise_lbl = [str(x) for x in NOISE_LEVELS]

    for ax, grid, title in zip(
        axes,
        [alpha_grid, ao_grid],
        [r"Krippendorff $\alpha$ (nominal)", r"Observed agreement $A_o$"],
        strict=True,
    ):
        im = ax.imshow(grid, aspect="auto", cmap="viridis", vmin=0.0, vmax=1.0)
        ax.set_xticks(range(n_eps), labels=noise_lbl, rotation=45, ha="right")
        ax.set_yticks(range(n_imb), labels=labels)
        ax.set_xlabel(r"Noise level $\varepsilon$")
        ax.set_ylabel("Class distribution (latent $\\pi$)")
        ax.set_title(title)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    # outline trap cells on alpha panel
    for i in range(n_imb):
        for j in range(n_eps):
            if trap_mask[i, j]:
                axes[0].add_patch(
                    Rectangle(
                        (j - 0.5, i - 0.5),
                        1,
                        1,
                        fill=False,
                        edgecolor="red",
                        linewidth=2.0,
                    )
                )

    # Add skew direction indicator on y-axis (outside plot area)
    axes[0].annotate(
        "",
        xy=(-0.5, n_imb - 0.3),
        xytext=(-0.5, 0.3),
        xycoords="data",
        arrowprops=dict(arrowstyle="-|>", color="0.35", lw=1.8),
        annotation_clip=False,
    )
    axes[0].text(
        -0.5, n_imb + 0.15,
        "increasing\nskew",
        ha="center",
        va="top",
        fontsize=7,
        color="0.35",
        style="italic",
    )

    fig.suptitle(
        "Experiment B: agreement trap (red box: $A_o>0.80$ and $\\alpha<0.40$)",
        fontsize=11,
    )
    fig.tight_layout()
    out = ROOT / "figures" / "exp_b_agreement_trap_heatmap.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")
    print(f"Trap cells (Ao>0.8 & alpha<0.4): {trap_mask.sum()} / {trap_mask.size}")


if __name__ == "__main__":
    main()
