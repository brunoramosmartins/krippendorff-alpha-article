"""Agreement metrics: observed agreement, Kappa family, Krippendorff's Alpha.

Phase 1: :func:`observed_agreement`, :func:`expected_agreement_independence`.
See `notes/phase1-theory.md` for notation and derivations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from collections.abc import Sequence


def observed_agreement(data: pd.DataFrame | np.ndarray) -> float:
    r"""Pairwise observed agreement :math:`A_o` across all items.

    For each item (row), consider all **unordered** pairs of annotators whose
    labels are present (non-missing). Count pairs that use the same category.

    .. math::

        A_o = \frac{\sum_i \text{agreeing pairs on item } i}
                   {\sum_i \text{total pairs on item } i}.

    Parameters
    ----------
    data
        Shape ``(n_items, n_annotators)``. Missing values should be ``NaN``
        (for :class:`~pandas.DataFrame` or float array).

    Returns
    -------
    float
        Observed agreement in :math:`[0,1]`, or ``nan`` if no valid pair exists.
    """
    if isinstance(data, pd.DataFrame):
        arr = data.to_numpy(dtype=float, copy=False)
    else:
        arr = np.asarray(data, dtype=float)

    agree_pairs = 0
    total_pairs = 0
    for row in arr:
        vals = row[~np.isnan(row)].astype(np.int64, copy=False)
        mloc = int(vals.size)
        if mloc < 2:
            continue
        for i in range(mloc):
            vi = vals[i]
            for j in range(i + 1, mloc):
                total_pairs += 1
                if vi == vals[j]:
                    agree_pairs += 1

    if total_pairs == 0:
        return float("nan")
    return agree_pairs / total_pairs


def observed_agreement_global_with_replacement(data: pd.DataFrame | np.ndarray) -> float:
    r"""Alternative :math:`A_o` view: draw two judgments uniformly **with replacement**.

    Pool all non-missing cells. Let :math:`N` be their count and :math:`n_k` the
    count of category :math:`k`. If two judgments are drawn i.i.d. uniformly from
    the pool,

    .. math::

        P(\text{agree}) = \sum_k \Bigl(\frac{n_k}{N}\Bigr)^2.

    For large :math:`m` this is close to the pairwise (without replacement)
    :func:`observed_agreement` when items are exchangeable.

    Parameters
    ----------
    data
        Annotation matrix as for :func:`observed_agreement`.

    Returns
    -------
    float
        :math:`\sum_k (n_k/N)^2`, or ``nan`` if :math:`N < 2`.
    """
    if isinstance(data, pd.DataFrame):
        flat = data.to_numpy(dtype=float, copy=False).ravel()
    else:
        flat = np.asarray(data, dtype=float).ravel()
    vals = flat[~np.isnan(flat)].astype(np.int64, copy=False)
    n = int(vals.size)
    if n < 2:
        return float("nan")
    k = int(vals.max()) + 1 if vals.size else 0
    counts = np.bincount(vals, minlength=k)
    p = counts.astype(float) / n
    return float(np.dot(p, p))


def expected_agreement_independence(probs: Sequence[float] | np.ndarray) -> float:
    r"""Expected agreement if two raters pick categories **independently** from :math:`\pi`.

    .. math::

        A_e = \sum_{k=1}^K \pi_k^2.

    For a uniform distribution, :math:`A_e = 1/K`.
    """
    p = np.asarray(list(probs), dtype=float)
    if np.any(p < 0) or not np.isclose(p.sum(), 1.0, atol=1e-6):
        raise ValueError("probs must be non-negative and sum to 1.")
    return float(np.dot(p, p))
