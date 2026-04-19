#!/usr/bin/env python3
"""Generate `figures/kappa_paradox.png` — Fleiss kappa vs imbalance for fixed noise."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.metrics import fleiss_kappa, observed_agreement  # noqa: E402
from src.simulate import SimulatedAnnotation  # noqa: E402


def _symmetric_pi(p0: float) -> np.ndarray:
    rest = (1.0 - p0) / 2.0
    return np.array([p0, rest, rest], dtype=float)


def main() -> None:
    try:
        plt.style.use("seaborn-v0_8-whitegrid")
    except OSError:
        plt.style.use("ggplot")

    n_items = 6_000
    n_annotators = 5
    n_classes = 3
    p0_grid = np.linspace(1 / 3 + 0.02, 0.95, 18)
    noise_levels = [0.01, 0.05, 0.10]

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), dpi=120)

    for eps in noise_levels:
        kappas: list[float] = []
        aos: list[float] = []
        for p0 in p0_grid:
            pi = _symmetric_pi(float(p0))
            seed = int(10_000 * eps + 1_000 * p0)
            gen = SimulatedAnnotation(
                n_items=n_items,
                n_annotators=n_annotators,
                n_classes=n_classes,
                noise_level=eps,
                class_dist=pi,
                pure_random=False,
                seed=seed,
            )
            df = gen.generate()
            arr = df.to_numpy(dtype=float)
            kappas.append(fleiss_kappa(arr))
            aos.append(observed_agreement(df))

        axes[0].plot(p0_grid, kappas, marker="o", markersize=3, label=rf"$\varepsilon={eps}$")
        axes[1].plot(p0_grid, aos, marker="o", markersize=3, label=rf"$\varepsilon={eps}$")

    axes[0].set_xlabel(r"Dominant class mass $\pi_1$ (symmetric tail $(1-\pi_1)/2$)")
    axes[0].set_ylabel(r"Fleiss $\kappa_F$")
    axes[0].set_title("Kappa vs imbalance (fixed noise)")
    axes[0].legend(loc="best", fontsize=8)
    axes[0].set_ylim(bottom=-0.05)

    axes[1].set_xlabel(r"Dominant class mass $\pi_1$")
    axes[1].set_ylabel(r"Pairwise $A_o$")
    axes[1].set_title("Raw agreement vs imbalance (same draws)\n(note narrower y-axis scale)")
    axes[1].legend(loc="best", fontsize=8)

    fig.suptitle(
        "Paradox region: high $A_o$ can coexist with low $\\kappa_F$ under skew + low noise",
        fontsize=11,
    )
    fig.tight_layout()

    out = ROOT / "figures" / "kappa_paradox.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
