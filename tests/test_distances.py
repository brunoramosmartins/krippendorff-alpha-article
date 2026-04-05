"""Tests for `src.distances`."""

from __future__ import annotations

import numpy as np
import pytest

from src.distances import (
    distance_matrix,
    interval_distance,
    nominal_distance,
    ratio_distance,
)


def test_nominal_distance() -> None:
    assert nominal_distance(0, 0) == 0.0
    assert nominal_distance(1, 2) == 1.0


def test_interval_distance() -> None:
    assert interval_distance(3.0, 1.0) == pytest.approx(4.0)


def test_ratio_distance_zero_sum() -> None:
    assert ratio_distance(0.0, 0.0) == 0.0


def test_ratio_distance_positive() -> None:
    d = ratio_distance(1.0, 3.0)
    assert d == pytest.approx(((1 - 3) / 4) ** 2)


def test_distance_matrices_symmetric() -> None:
    vd = np.array([0.0, 1.0, 2.0])
    n_v = np.array([4.0, 2.0, 1.0])
    for level in ("nominal", "ordinal", "interval", "ratio"):
        d = distance_matrix(vd, n_v, level)
        assert d.shape == (3, 3)
        np.testing.assert_allclose(d, d.T)


def test_nominal_distance_matrix_zero_diagonal() -> None:
    vd = np.array([0, 1, 2])
    n_v = np.array([1.0, 1.0, 1.0])
    d = distance_matrix(vd, n_v, "nominal")
    assert np.all(np.diag(d) == 0)
    assert d[0, 1] == 1.0


def test_interval_distance_matrix_matches_pairwise() -> None:
    vd = np.array([1.0, 4.0, 5.0])
    n_v = np.array([2.0, 1.0, 3.0])
    d = distance_matrix(vd, n_v, "interval")
    assert d[0, 1] == pytest.approx(interval_distance(vd[0], vd[1]))


def test_ordinal_matches_krippendorff_reference() -> None:
    krippendorff = pytest.importorskip("krippendorff")
    kk = krippendorff.krippendorff
    vd = np.array([1.0, 2.0, 3.0, 4.0])
    n_v = np.array([5.0, 3.0, 2.0, 1.0])
    d_ref = kk._distances(vd, kk._ordinal_metric, n_v.astype(np.int64))
    d_ours = distance_matrix(vd, n_v, "ordinal")
    np.testing.assert_allclose(d_ours, d_ref, rtol=1e-12)
