#!/usr/bin/env python3
"""Experiment A — random i.i.d. annotators (Phase 4).

Metrics: observed agreement :math:`A_o`, Fleiss :math:`\\kappa`, Krippendorff :math:`\\alpha`.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.experiment_util import apply_plot_style, configure_matplotlib

configure_matplotlib()

import matplotlib.pyplot as plt

from src.metrics import fleiss_kappa, krippendorff_alpha, observed_agreement
from src.simulate import SimulatedAnnotation

N_ITEMS = 10_000
N_RATERS = 5
TOL = 0.02


def main() -> None:
    apply_plot_style()
    ks = list(range(2, 11))
    ao_list: list[float] = []
    kf_list: list[float] = []
    alpha_list: list[float] = []
    one_over_k: list[float] = []

    for k in ks:
        seed = 42 if k == 3 else 42 + k * 997
        gen = SimulatedAnnotation(
            n_items=N_ITEMS,
            n_annotators=N_RATERS,
            n_classes=k,
            class_dist="uniform",
            pure_random=True,
            seed=seed,
        )
        df = gen.generate()
        arr = df.to_numpy(dtype=float)
        ao_list.append(observed_agreement(df))
        kf_list.append(fleiss_kappa(arr))
        alpha_list.append(krippendorff_alpha(df, level_of_measurement="nominal"))
        one_over_k.append(1.0 / k)

    i3 = ks.index(3)
    if abs(ao_list[i3] - 1 / 3) >= TOL:
        raise SystemExit(f"A_o for K=3 out of tolerance: {ao_list[i3]}")
    if abs(kf_list[i3]) >= TOL:
        raise SystemExit(f"Fleiss kappa for K=3 out of tolerance: {kf_list[i3]}")
    if abs(alpha_list[i3]) >= TOL:
        raise SystemExit(f"alpha for K=3 out of tolerance: {alpha_list[i3]}")

    fig, ax = plt.subplots(figsize=(8.4, 5.2), dpi=120)

    # Shade the whole story: the gap between raw agreement and zero is agreement
    # that is *pure chance* — no shared signal produced any of it.
    ax.fill_between(
        ks, 0.0, ao_list, color="#1f77b4", alpha=0.10, zorder=0,
    )
    ax.annotate(
        "everything below the curve is\nagreement produced by pure chance",
        xy=(4, ao_list[2] / 2),
        xytext=(5.2, 0.30),
        fontsize=9,
        color="#1f4e79",
        arrowprops=dict(arrowstyle="->", color="#1f4e79", lw=1.1),
    )

    # Empirical A_o is the star; 1/K is a faint reference it lands exactly on.
    ax.plot(ks, one_over_k, color="gray", linestyle="--", linewidth=1.0, alpha=0.7,
            zorder=1, label=r"$1/K$ (chance baseline it lands on)")
    ax.plot(ks, ao_list, "o-", color="#1f77b4", zorder=3,
            label=r"Empirical $A_o$ (raw agreement)")

    # Fleiss and alpha coincide near zero by design — both see through the chance.
    ax.plot(ks, kf_list, "s-", color="#d95f02", zorder=3, label=r"Fleiss $\kappa_F$")
    ax.plot(ks, alpha_list, "^-", color="#2ca02c", zorder=3,
            label=r"Krippendorff $\alpha$ (nominal)")
    ax.axhline(0.0, color="gray", linewidth=0.8, linestyle=":")

    # Call out the two ends of the argument.
    ax.annotate(
        r"$K=2$: raters agree 50% of the time" + "\nwith zero shared signal",
        xy=(2, ao_list[0]),
        xytext=(2.15, 0.40),
        fontsize=9,
        arrowprops=dict(arrowstyle="->", lw=1.0),
    )
    ax.annotate(
        r"$\kappa_F$ and $\alpha$ collapse to $\approx 0$",
        xy=(7, kf_list[5]),
        xytext=(6.1, 0.10),
        fontsize=9,
        arrowprops=dict(arrowstyle="->", lw=1.0),
    )

    ax.set_xlabel("Number of categories $K$")
    ax.set_ylabel("Metric value")
    ax.set_title("Experiment A: random i.i.d. raters (uniform categories)")
    ax.set_xticks(ks)
    ax.set_ylim(-0.05, 0.55)
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    out = ROOT / "figures" / "exp_a_random_metrics.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")
    ao3, kf3, a3 = ao_list[i3], kf_list[i3], alpha_list[i3]
    print(f"K=3 (seed=42): Ao={ao3:.4f}, kappa_F={kf3:.4f}, alpha={a3:.4f}")


if __name__ == "__main__":
    main()
