"""Coincidence and expected-coincidence matrices for Krippendorff's :math:`\\alpha`.

The construction follows the aggregation used in Krippendorff (2004, Ch. 11) and the
reference implementation in the ``krippendorff`` package: for each unit, pairable
judgments are weighted by :math:`1/(m-1)` where :math:`m` is the number of valid
ratings on that unit.

Reliability data layout in this repository: **rows = units (items), columns = raters**.
"""

from __future__ import annotations

import numpy as np


def value_counts_matrix(data: np.ndarray, value_domain: np.ndarray) -> np.ndarray:
    r"""Count assignments per unit and category.

    Parameters
    ----------
    data
        Shape ``(n_units, n_raters)``. Missing values must be ``np.nan`` (they do
        not match any category in ``value_domain``).
    value_domain
        Shape ``(V,)``. All possible values, **ordered** for ordinal/interval/ratio.

    Returns
    -------
    ndarray
        Integer array ``(n_units, V)`` with :math:`n_{iv}` = number of raters who
        assigned ``value_domain[v]`` to unit :math:`i`.
    """
    if data.ndim != 2:
        raise ValueError("data must be 2D (units × raters).")
    vd = np.asarray(value_domain)
    if vd.ndim != 1:
        raise ValueError("value_domain must be 1D.")
    return (data[..., np.newaxis] == vd[np.newaxis, np.newaxis, :]).sum(axis=1).astype(
        np.int64, copy=False
    )


def build_coincidence_matrix(value_counts: np.ndarray) -> np.ndarray:
    r"""Aggregate **observed** coincidence matrix :math:`\mathbf{O}`.

    For unit :math:`i` with counts :math:`n_{i\cdot}` (row of ``value_counts``),
    let :math:`m_i=\sum_v n_{iv}` and define the pairable count
    :math:`\tilde m_i=\max(m_i,2)` (so division by :math:`\tilde m_i-1` is safe).

    The unnormalised coincidence for that unit is
    :math:`\mathbf{n}_i\mathbf{n}_i^\top` with diagonal entries
    :math:`n_{iv}(n_{iv}-1)` removed (no self-pairs for the same rater). Each row
    is scaled by :math:`1/(\tilde m_i-1)`. Summing over units yields
    :math:`\mathbf{O}\in\mathbb{R}^{V\times V}`.

    Parameters
    ----------
    value_counts
        Shape ``(n_units, V)``, non-negative integers.

    Returns
    -------
    ndarray
        Symmetric :math:`\mathbf{O}`, shape ``(V, V)``.
    """
    vc = np.asarray(value_counts, dtype=np.int64)
    if vc.ndim != 2:
        raise ValueError("value_counts must be 2D (units × categories).")
    n_units, v = vc.shape
    if v < 2:
        raise ValueError("Need at least two categories in the domain.")

    pairable = np.maximum(vc.sum(axis=1), 2)
    diagonals = vc[:, np.newaxis, :] * np.eye(v, dtype=np.int64)[np.newaxis, ...]
    unnormalized = vc[..., np.newaxis] * vc[:, np.newaxis, :] - diagonals
    scaled = np.divide(
        unnormalized,
        (pairable - 1).reshape(-1, 1, 1),
        dtype=np.float64,
    )
    return scaled.sum(axis=0).astype(np.float64, copy=False)


def marginal_totals(coincidence: np.ndarray) -> np.ndarray:
    r"""Marginal :math:`n_v = \sum_{c} O_{cv}` (column sums of :math:`\mathbf{O}`)."""
    o = np.asarray(coincidence, dtype=float)
    return o.sum(axis=0)


def random_coincidence_matrix(n_v: np.ndarray) -> np.ndarray:
    r"""Expected coincidence under random pairing preserving marginals :math:`n_v`.

    .. math::

        E_{cc'} = \frac{n_c n_{c'} - n_c\,\delta_{cc'}}{N-1},
        \quad N = \sum_v n_v.

    Parameters
    ----------
    n_v
        Shape ``(V,)``, non-negative, sum at least 2.

    Returns
    -------
    ndarray
        Symmetric :math:`\mathbf{E}`, shape ``(V, V)``.
    """
    nv = np.asarray(n_v, dtype=np.float64).ravel()
    ntot = float(nv.sum())
    if ntot <= 1.0:
        raise ValueError("Total pairable assignments must exceed 1.")
    return (np.outer(nv, nv) - np.diagflat(nv)) / (ntot - 1.0)
