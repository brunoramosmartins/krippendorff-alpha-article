"""Distance metrics for Krippendorff's :math:`\\alpha` (Stevens scales).

Scalar helpers are useful for intuition; :func:`distance_matrix` builds the full
:math:`V\\times V` matrix needed with the coincidence machinery (ordinal uses
category frequencies :math:`n_v` from the data, per Krippendorff 2004, §11.4).
"""

from __future__ import annotations

from typing import Literal

import numpy as np

DEFAULT_DTYPE = np.dtype(np.float64)

LevelOfMeasurement = Literal["nominal", "ordinal", "interval", "ratio"]


def nominal_distance(c: float, c_prime: float) -> float:
    r"""Nominal: :math:`\delta(c,c')=0` if :math:`c=c'`, else :math:`1`."""
    return 0.0 if c == c_prime else 1.0


def interval_distance(c: float, c_prime: float) -> float:
    r"""Interval: :math:`\delta(c,c')=(c-c')^2`."""
    d = float(c) - float(c_prime)
    return d * d


def ratio_distance(c: float, c_prime: float) -> float:
    r"""Ratio: :math:`\delta(c,c')=\bigl((c-c')/(c+c')\bigr)^2`, :math:`0` if :math:`c+c'=0`."""
    s = float(c) + float(c_prime)
    if s == 0.0:
        return 0.0
    return ((float(c) - float(c_prime)) / s) ** 2


def _nominal_metric(
    v1: np.ndarray,
    v2: np.ndarray,
    i1: np.ndarray,
    i2: np.ndarray,
    n_v: np.ndarray,
    dtype: np.dtype = DEFAULT_DTYPE,
) -> np.ndarray:
    del i1, i2, n_v
    return (v1 != v2).astype(dtype)


def _interval_metric(
    v1: np.ndarray,
    v2: np.ndarray,
    i1: np.ndarray,
    i2: np.ndarray,
    n_v: np.ndarray,
    dtype: np.dtype = DEFAULT_DTYPE,
) -> np.ndarray:
    del i1, i2, n_v
    return (v1.astype(dtype) - v2.astype(dtype)) ** 2


def _ratio_metric(
    v1: np.ndarray,
    v2: np.ndarray,
    i1: np.ndarray,
    i2: np.ndarray,
    n_v: np.ndarray,
    dtype: np.dtype = DEFAULT_DTYPE,
) -> np.ndarray:
    del i1, i2, n_v
    s = v1 + v2
    return np.divide(
        v1 - v2,
        s,
        out=np.zeros(np.broadcast(v1, v2).shape, dtype=dtype),
        where=s != 0,
        dtype=dtype,
    ) ** 2


def _ordinal_metric(
    v1: np.ndarray,
    v2: np.ndarray,
    i1: np.ndarray,
    i2: np.ndarray,
    n_v: np.ndarray,
    dtype: np.dtype = DEFAULT_DTYPE,
) -> np.ndarray:
    del v1, v2
    lo = np.minimum(i1, i2)
    hi = np.maximum(i1, i2)
    ranges = np.dstack((lo, hi + 1))
    nv_app = np.append(n_v.astype(dtype), 0)
    sums_between = np.add.reduceat(nv_app, ranges.reshape(-1))[::2].reshape(*lo.shape)
    mid = np.divide(n_v[lo] + n_v[hi], 2, dtype=dtype)
    return (sums_between - mid) ** 2


_METRICS = {
    "nominal": _nominal_metric,
    "ordinal": _ordinal_metric,
    "interval": _interval_metric,
    "ratio": _ratio_metric,
}


def distance_matrix(
    value_domain: np.ndarray,
    n_v: np.ndarray,
    level_of_measurement: LevelOfMeasurement,
    dtype: np.dtype = DEFAULT_DTYPE,
) -> np.ndarray:
    r"""Pairwise distances :math:`\delta_{cc'}` on the **value domain** rows.

    Ordinal distances use sorted domain indices and the observed category totals
    :math:`n_v` (Krippendorff, 2004).

    Parameters
    ----------
    value_domain
        Shape ``(V,)``, ordered for non-nominal scales.
    n_v
        Shape ``(V,)``, marginal counts from :func:`~src.coincidence.marginal_totals`.
    level_of_measurement
        One of ``"nominal"``, ``"ordinal"``, ``"interval"``, ``"ratio"``.
    dtype
        Floating dtype for the matrix.

    Returns
    -------
    ndarray
        Shape ``(V, V)``, symmetric non-negative.
    """
    vd = np.asarray(value_domain)
    nv = np.asarray(n_v, dtype=dtype)
    v = len(vd)
    if nv.shape != (v,):
        raise ValueError("n_v must have length equal to value_domain.")
    idx = np.arange(v)
    metric = _METRICS[level_of_measurement]
    return metric(
        vd[:, np.newaxis],
        vd[np.newaxis, :],
        i1=idx[:, np.newaxis],
        i2=idx[np.newaxis, :],
        n_v=nv,
        dtype=dtype,
    )
