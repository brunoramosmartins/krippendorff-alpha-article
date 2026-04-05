"""Agreement metrics: observed agreement, Kappa family, Krippendorff's Alpha.

Phase 1: :func:`observed_agreement`, :func:`expected_agreement_independence`.
Phase 2: :func:`cohens_kappa`, :func:`fleiss_kappa`.
Phase 3: :func:`krippendorff_alpha`.
See `notes/phase1-theory.md`, `notes/phase2-kappa.md`, and `notes/phase3-alpha.md`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import numpy as np
import pandas as pd

from .coincidence import (
    build_coincidence_matrix,
    marginal_totals,
    random_coincidence_matrix,
    value_counts_matrix,
)
from .distances import distance_matrix

if TYPE_CHECKING:
    from collections.abc import Sequence

AlphaLevel = Literal["nominal", "ordinal", "interval", "ratio"]


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
    p = np.asarray(probs, dtype=float).ravel()
    if np.any(p < 0) or not np.isclose(p.sum(), 1.0, atol=1e-6):
        raise ValueError("probs must be non-negative and sum to 1.")
    return float(np.dot(p, p))


def cohens_kappa(rater_a: np.ndarray | pd.Series, rater_b: np.ndarray | pd.Series) -> float:
    r"""Cohen's :math:`\kappa` for **two** raters on the same :math:`n` items.

    .. math::

        \kappa = \frac{A_o - A_e}{1 - A_e},

    where :math:`A_o = \frac{1}{n}\sum_i \mathbf{1}\{X_{i1}=X_{i2}\}` and
    :math:`A_e = \sum_k p_{k\cdot} p_{\cdot k}` with :math:`p_{k\cdot}` the
    proportion of class :math:`k` among rater 1's labels and :math:`p_{\cdot k}`
    for rater 2.

    Rows with a missing value in either rater are dropped.

    Parameters
    ----------
    rater_a, rater_b
        Same shape, integer labels in ``{0,\ldots,K-1}`` (or any consecutive
        integers — category set is inferred from observed values).

    Returns
    -------
    float
        Cohen's :math:`\kappa`, or ``nan`` if :math:`1 - A_e` is numerically zero
        or no paired items remain.
    """
    a = np.asarray(rater_a, dtype=float).ravel()
    b = np.asarray(rater_b, dtype=float).ravel()
    if a.shape != b.shape:
        raise ValueError("rater_a and rater_b must have the same shape.")
    mask = ~(np.isnan(a) | np.isnan(b))
    a = a[mask]
    b = b[mask]
    if a.size == 0:
        return float("nan")
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):
        raise ValueError("Labels must be finite (non-NaN after masking).")
    if np.any(a != np.floor(a)) or np.any(b != np.floor(b)):
        raise ValueError("Cohen's kappa expects integer category codes.")
    ai = a.astype(np.int64, copy=False)
    bi = b.astype(np.int64, copy=False)

    k_min = int(min(ai.min(), bi.min()))
    k_max = int(max(ai.max(), bi.max()))
    k = k_max - k_min + 1
    a0 = ai - k_min
    b0 = bi - k_min
    n = int(a0.size)
    p_o = float((a0 == b0).mean())
    p_row = np.bincount(a0, minlength=k).astype(float) / n
    p_col = np.bincount(b0, minlength=k).astype(float) / n
    p_e = float(np.dot(p_row, p_col))
    denom = 1.0 - p_e
    if denom <= 1e-15:
        return float("nan")
    return (p_o - p_e) / denom


def fleiss_kappa(data: pd.DataFrame | np.ndarray) -> float:
    r"""Fleiss' :math:`\kappa` for **multiple** raters and nominal categories.

    Each row is one item; each column is one rater. All entries must be observed
    (no ``NaN``) and integer codes ``0,\ldots,K-1``.

    Let :math:`n_{ik}` be the number of raters who assigned category :math:`k` to
    item :math:`i`, and :math:`m` the number of raters (constant across items).

    .. math::

        P_i = \frac{1}{m(m-1)} \sum_{k=1}^K n_{ik}(n_{ik}-1), \quad
        \bar P = \frac{1}{n}\sum_i P_i, \quad
        p_k = \frac{1}{nm}\sum_i n_{ik}, \quad
        \bar P_e = \sum_k p_k^2.

    .. math::

        \kappa_F = \frac{\bar P - \bar P_e}{1 - \bar P_e}.

    Parameters
    ----------
    data
        Shape ``(n_items, n_raters)``.

    Returns
    -------
    float
        Fleiss' :math:`\kappa`, or ``1.0`` when :math:`\bar P=1` (perfect within-item
        agreement), or ``nan`` if :math:`1-\bar P_e` vanishes otherwise.

    Raises
    ------
    ValueError
        If there is any missing data, fewer than two raters, or non-integer labels.
    """
    if isinstance(data, pd.DataFrame):
        arr = data.to_numpy(dtype=float, copy=False)
    else:
        arr = np.asarray(data, dtype=float)
    if arr.ndim != 2:
        raise ValueError("Fleiss' kappa expects a 2D array (items × raters).")
    n, m = arr.shape
    if m < 2:
        raise ValueError("Fleiss' kappa requires at least two raters per item.")
    if np.any(np.isnan(arr)):
        raise ValueError("Fleiss' kappa requires complete ratings (no NaN).")
    if np.any(arr != np.floor(arr)):
        raise ValueError("All labels must be integer category codes.")
    lab = arr.astype(np.int64, copy=False)
    if lab.min() < 0:
        raise ValueError("Category codes must be non-negative integers.")
    k = int(lab.max()) + 1
    if k == 0:
        return float("nan")

    p_rows = np.empty(n, dtype=float)
    for i in range(n):
        row = lab[i]
        counts = np.bincount(row, minlength=k)
        p_rows[i] = float(np.dot(counts, counts - 1)) / (m * (m - 1))

    p_bar = float(p_rows.mean())
    flat = lab.ravel()
    p_cat = np.bincount(flat, minlength=k).astype(float) / float(n * m)
    p_e = float(np.dot(p_cat, p_cat))
    if np.isclose(p_bar, 1.0):
        return 1.0
    denom = 1.0 - p_e
    if denom <= 1e-15:
        return float("nan")
    return (p_bar - p_e) / denom


def krippendorff_alpha(
    data: pd.DataFrame | np.ndarray,
    *,
    level_of_measurement: AlphaLevel = "interval",
    value_domain: np.ndarray | None = None,
    dtype: np.dtype | None = None,
) -> float:
    r"""Krippendorff's :math:`\alpha` from reliability data (items × raters).

    .. math::

        \alpha = 1 - \frac{\sum_{c,c'} O_{cc'}\,\delta_{cc'}}
                         {\sum_{c,c'} E_{cc'}\,\delta_{cc'}},

    where :math:`\mathbf{O}` is the observed coincidence matrix,
    :math:`\mathbf{E}` the expected coincidence under random pairing preserving
    marginals, and :math:`\delta` the metric for the chosen scale.

    **Layout:** each **row** is a unit (item), each **column** a rater. Missing
    entries are ``NaN``. This matches :func:`observed_agreement` / Fleiss inputs;
    the ``krippendorff`` reference package uses the **transposed** layout
    (raters × items).

    Parameters
    ----------
    data
        Shape ``(n_units, n_raters)``.
    level_of_measurement
        ``"nominal"``, ``"ordinal"``, ``"interval"``, or ``"ratio"``.
    value_domain
        Shape ``(V,)``, all admissible values **in order** (required for ordinal
        and for non-numeric categories). If ``None``, taken as sorted unique
        non-missing values in ``data`` (strings allowed only for nominal unless
        you pass an explicit order).
    dtype
        Inexact numpy dtype for weighted sums (default ``float64``).

    Returns
    -------
    float
        :math:`\alpha`, or ``nan`` if the denominator vanishes.

    Raises
    ------
    ValueError
        If the domain or pairability conditions for :math:`\alpha` are not met.
    """
    dt = np.dtype(np.float64) if dtype is None else np.dtype(dtype)
    if not np.issubdtype(dt, np.inexact):
        raise ValueError("dtype must be a floating-point dtype.")

    if isinstance(data, pd.DataFrame):
        arr = data.to_numpy()
    else:
        arr = np.asarray(data)

    if arr.ndim != 2:
        raise ValueError("data must be 2D (units × raters).")

    kind = arr.dtype.kind
    if kind in {"i", "u", "f"}:
        arr_f = arr.astype(np.float64, copy=False)
        flat = arr_f.ravel()
        observed = flat[~np.isnan(flat)]
        computed_domain = np.unique(observed)
        work = arr_f
    elif kind in {"U", "S"}:
        if level_of_measurement != "nominal":
            raise ValueError("String arrays require level_of_measurement='nominal'.")
        observed = arr[np.asarray(arr != "nan")]
        computed_domain = np.unique(observed)
        work = arr
    else:
        raise ValueError(f"Unsupported array dtype kind {kind!r}; use numeric codes.")

    if value_domain is None:
        vd = computed_domain
    else:
        vd = np.asarray(value_domain)

    if vd.ndim != 1 or vd.size <= 1:
        raise ValueError("value_domain must be 1D with at least two categories.")

    if not np.isin(computed_domain, vd).all():
        raise ValueError("data contains values outside value_domain.")

    vc = value_counts_matrix(work, vd)
    if not np.any(vc.sum(axis=1) >= 2):
        raise ValueError("At least one unit must have two or more valid ratings.")

    o_mat = build_coincidence_matrix(vc)
    n_v = marginal_totals(o_mat)
    e_mat = random_coincidence_matrix(n_v)
    d_mat = distance_matrix(vd, n_v, level_of_measurement, dtype=dt)

    num = float((o_mat * d_mat).sum())
    den = float((e_mat * d_mat).sum())
    if den <= 1e-15:
        return float("nan")
    return 1.0 - num / den
