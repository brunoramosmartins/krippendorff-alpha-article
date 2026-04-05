"""Tests for `src.coincidence`."""

from __future__ import annotations

import numpy as np
import pytest

from src.coincidence import (
    build_coincidence_matrix,
    marginal_totals,
    random_coincidence_matrix,
    value_counts_matrix,
)


def test_value_counts_with_missing() -> None:
    domain = np.array([0, 1, 2])
    # 2 items × 3 raters; NaNs ignored
    data = np.array([[0.0, 0.0, 1.0], [1.0, 1.0, 1.0]])
    vc = value_counts_matrix(data, domain)
    np.testing.assert_array_equal(vc[0], [2, 1, 0])
    np.testing.assert_array_equal(vc[1], [0, 3, 0])


def test_coincidence_symmetric_single_unit() -> None:
    """One unit, counts [2,1,0] on domain (0,1,2) — hand check vs reference formula."""
    vc = np.array([[2, 1, 0]], dtype=np.int64)
    o = build_coincidence_matrix(vc)
    assert np.allclose(o, o.T)
    # pairable=max(3,2)=3, (m-1)=2; unnormalized off-diagonal [2,2,0; 2,0,0; 0,0,0] / 2
    expect = np.array([[1.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
    np.testing.assert_allclose(o, expect)


def test_coincidence_missing_column_in_counts() -> None:
    vc = np.array([[1, 0, 0], [0, 1, 1]], dtype=np.int64)
    o = build_coincidence_matrix(vc)
    assert o.shape == (3, 3)
    nv = marginal_totals(o)
    assert nv.shape == (3,)
    e = random_coincidence_matrix(nv)
    assert np.allclose(e, e.T)


def test_random_coincidence_row_sums() -> None:
    n_v = np.array([3.0, 2.0, 1.0])
    e = random_coincidence_matrix(n_v)
    row_sums = e.sum(axis=1)
    # Each row c: sum_{c'} E_{cc'} = n_c (N - n_c) / (N-1) + (n_c(n_c-1))/(N-1) = n_c
    np.testing.assert_allclose(row_sums, n_v)


def test_build_coincidence_raises_small_domain() -> None:
    with pytest.raises(ValueError, match="at least two"):
        build_coincidence_matrix(np.ones((4, 1), dtype=np.int64))


def test_random_coincidence_raises_total_one() -> None:
    with pytest.raises(ValueError):
        random_coincidence_matrix(np.array([1.0]))
