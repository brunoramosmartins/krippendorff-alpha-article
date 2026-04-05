#!/usr/bin/env python3
"""Generate `figures/random_agreement_convergence.png` for Phase 1.

Empirical pairwise :math:`A_o` for independent random labellers vs
:math:`A_e = \\sum_k \\pi_k^2` (horizontal lines).
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.metrics import expected_agreement_independence, observed_agreement  # noqa: E402
from src.simulate import SimulatedAnnotation  # noqa: E402


def main() -> None:
    try:
        plt.style.use("seaborn-v0_8-whitegrid")
    except OSError:
        plt.style.use("ggplot")
    fig, ax = plt.subplots(figsize=(8, 5), dpi=120)

    n_annotators = 5
    n_classes = 3
    n_grid = [100, 500, 1000, 5000, 10_000]

    # Uniform i.i.d. labels -> A_e = 1/K
    aes_uniform: list[float] = []
    aos_uniform: list[float] = []
    pi_imb = np.array([0.70, 0.20, 0.10])
    aes_imb: list[float] = []
    aos_imb: list[float] = []

    ae_u = expected_agreement_independence(np.full(n_classes, 1.0 / n_classes))
    ae_i = expected_agreement_independence(pi_imb)

    for idx, n_items in enumerate(n_grid):
        gen_u = SimulatedAnnotation(
            n_items=n_items,
            n_annotators=n_annotators,
            n_classes=n_classes,
            class_dist="uniform",
            pure_random=True,
            seed=42 + idx,
        )
        df_u = gen_u.generate()
        aos_uniform.append(observed_agreement(df_u))
        aes_uniform.append(ae_u)

        gen_i = SimulatedAnnotation(
            n_items=n_items,
            n_annotators=n_annotators,
            n_classes=n_classes,
            class_dist=pi_imb,
            pure_random=True,
            seed=100 + idx,
        )
        df_i = gen_i.generate()
        aos_imb.append(observed_agreement(df_i))
        aes_imb.append(ae_i)

    ax.plot(
        n_grid,
        aos_uniform,
        "o-",
        color="#1f77b4",
        label=r"Empirical $A_o$ (uniform i.i.d.)",
    )
    ax.axhline(
        ae_u,
        color="#1f77b4",
        linestyle="--",
        linewidth=1.5,
        label=rf"$A_e = 1/K = {ae_u:.4f}$",
    )

    ax.plot(
        n_grid,
        aos_imb,
        "s-",
        color="#d95f02",
        label=r"Empirical $A_o$ (i.i.d. $\pi=(0.7,0.2,0.1)$)",
    )
    ax.axhline(
        ae_i,
        color="#d95f02",
        linestyle="--",
        linewidth=1.5,
        label=rf"$A_e = \sum \pi_k^2 = {ae_i:.4f}$",
    )

    ax.set_xscale("log")
    ax.set_xticks(n_grid)
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    ax.set_xlabel("Number of items $n$")
    ax.set_ylabel(r"Observed agreement $A_o$")
    ax.set_title("Convergence of empirical $A_o$ under independent random labelling")
    ax.legend(loc="best", frameon=True)
    fig.tight_layout()

    out = ROOT / "figures" / "random_agreement_convergence.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
