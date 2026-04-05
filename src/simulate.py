"""Synthetic annotation matrix generator.

Specification: `docs/dataset-design.md`.

Two sampling regimes:

1. **Truth + noise** (`pure_random=False`): latent
   :math:`Y_i \\sim \\mathrm{Categorical}(\\pi)`, then each annotator copies :math:`Y_i` with
   probability :math:`1-\\varepsilon`, else a uniform
   error among the other :math:`K-1` labels.

2. **Pure independence / chance benchmark** (`pure_random=True`): each cell is i.i.d.
   :math:`\\mathrm{Categorical}(\\pi)` (no shared latent truth). Use this for validating
   :math:`A_o \\to \\sum_k \\pi_k^2` under independent labelling.
"""

from __future__ import annotations

from typing import Literal

import numpy as np
import pandas as pd

ClassDistName = Literal["uniform", "imbalanced", "extreme"]


def _distribution_vector(name_or_probs: ClassDistName | np.ndarray, n_classes: int) -> np.ndarray:
    if isinstance(name_or_probs, np.ndarray):
        pi = np.asarray(name_or_probs, dtype=float).reshape(-1)
        if pi.shape[0] != n_classes:
            raise ValueError(f"Custom pi length {pi.shape[0]} must equal n_classes={n_classes}.")
        if np.any(pi < 0) or not np.isclose(pi.sum(), 1.0, atol=1e-6):
            raise ValueError("Custom pi must be non-negative and sum to 1.")
        return pi / pi.sum()

    if name_or_probs == "uniform":
        return np.full(n_classes, 1.0 / n_classes, dtype=float)

    if n_classes != 3:
        raise ValueError(
            f'Named presets "imbalanced" and "extreme" require n_classes=3 (got {n_classes}).'
        )

    if name_or_probs == "imbalanced":
        return np.array([0.70, 0.20, 0.10], dtype=float)
    if name_or_probs == "extreme":
        return np.array([0.90, 0.05, 0.05], dtype=float)

    raise ValueError(f"Unknown class_dist: {name_or_probs!r}")


class SimulatedAnnotation:
    """Generate a synthetic :math:`n \\times m` annotation matrix.

    Labels are integers in ``{0, ..., n_classes - 1}``. Missing values are ``NaN``.

    Example
    -------
    >>> gen = SimulatedAnnotation(
    ...     n_items=1000,
    ...     n_annotators=5,
    ...     n_classes=3,
    ...     noise_level=1.0,
    ...     class_dist="uniform",
    ...     pure_random=True,
    ...     seed=42,
    ... )
    >>> df = gen.generate()
    >>> df.shape
    (1000, 5)
    """

    __slots__ = (
        "n_items",
        "n_annotators",
        "n_classes",
        "noise_level",
        "class_dist",
        "missing_rate",
        "seed",
        "pure_random",
        "_pi",
        "_rng",
    )

    def __init__(
        self,
        n_items: int,
        n_annotators: int,
        n_classes: int,
        *,
        noise_level: float = 0.0,
        class_dist: ClassDistName | np.ndarray | list[float] = "uniform",
        missing_rate: float = 0.0,
        seed: int | None = None,
        pure_random: bool = False,
    ) -> None:
        if n_items < 1 or n_annotators < 2 or n_classes < 2:
            raise ValueError("Require n_items >= 1, n_annotators >= 2, n_classes >= 2.")
        if not 0.0 <= noise_level <= 1.0:
            raise ValueError("noise_level must be in [0, 1].")
        if not 0.0 <= missing_rate <= 0.5:
            raise ValueError("missing_rate must be in [0, 0.5].")

        if isinstance(class_dist, list):
            dist_arg: ClassDistName | np.ndarray = np.asarray(class_dist, dtype=float)
        else:
            dist_arg = class_dist

        pi = _distribution_vector(dist_arg, n_classes)

        self.n_items = n_items
        self.n_annotators = n_annotators
        self.n_classes = n_classes
        self.noise_level = float(noise_level)
        self.class_dist = class_dist
        self.missing_rate = float(missing_rate)
        self.seed = seed
        self.pure_random = bool(pure_random)
        self._pi = pi
        self._rng = np.random.default_rng(seed)

    def generate(self) -> pd.DataFrame:
        """Build the annotation matrix (new draw; uses RNG state)."""
        rng = self._rng
        n, m, k = self.n_items, self.n_annotators, self.n_classes
        eps = self.noise_level

        if self.pure_random:
            # i.i.d. labels ~ Categorical(pi) — independent across items and annotators
            flat = rng.choice(k, size=n * m, p=self._pi)
            x = flat.reshape(n, m)
        else:
            truths = rng.choice(k, size=n, p=self._pi)
            noise = rng.random((n, m)) < eps
            # Uniform error among the K-1 classes different from the latent truth
            aux = rng.integers(0, k - 1, size=(n, m))
            t_col = truths[:, None]
            wrong_labels = np.where(aux < t_col, aux, aux + 1)
            x = np.where(noise, wrong_labels, t_col)

        if self.missing_rate > 0:
            miss = rng.random(size=x.shape) < self.missing_rate
            x_float = x.astype(float)
            x_float[miss] = np.nan
            data = x_float
        else:
            data = x.astype(float)

        cols = [f"r{j}" for j in range(m)]
        return pd.DataFrame(data, columns=cols)

    def reset_rng(self) -> None:
        """Reset the RNG to ``seed`` (repeatable multi-step workflows)."""
        self._rng = np.random.default_rng(self.seed)
