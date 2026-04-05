"""Tests for `src.simulate.SimulatedAnnotation`."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.metrics import expected_agreement_independence, observed_agreement
from src.simulate import SimulatedAnnotation, _distribution_vector


def test_distribution_vector_uniform() -> None:
    pi = _distribution_vector("uniform", 4)
    assert pi.shape == (4,)
    np.testing.assert_allclose(pi, 0.25)


def test_distribution_vector_custom() -> None:
    pi = _distribution_vector(np.array([0.2, 0.3, 0.5]), 3)
    np.testing.assert_allclose(pi, [0.2, 0.3, 0.5])


def test_noise_zero_perfect_rowwise_agreement() -> None:
    gen = SimulatedAnnotation(
        n_items=200,
        n_annotators=5,
        n_classes=4,
        noise_level=0.0,
        class_dist="uniform",
        seed=7,
    )
    df = gen.generate()
    assert (df.nunique(axis=1) == 1).all()
    assert observed_agreement(df) == pytest.approx(1.0)


def test_pure_random_uniform_approaches_chance() -> None:
    gen = SimulatedAnnotation(
        n_items=20_000,
        n_annotators=5,
        n_classes=3,
        noise_level=0.0,
        class_dist="uniform",
        pure_random=True,
        seed=42,
    )
    df = gen.generate()
    ao = observed_agreement(df)
    ae = expected_agreement_independence([1 / 3, 1 / 3, 1 / 3])
    assert abs(ao - ae) < 0.01


def test_pure_random_imbalanced_matches_sum_pi_squared() -> None:
    pi = np.array([0.70, 0.20, 0.10])
    gen = SimulatedAnnotation(
        n_items=25_000,
        n_annotators=5,
        n_classes=3,
        class_dist=pi,
        pure_random=True,
        seed=99,
    )
    df = gen.generate()
    ao = observed_agreement(df)
    ae = expected_agreement_independence(pi)
    assert abs(ao - ae) < 0.01


def test_missing_rate_mcar() -> None:
    gen = SimulatedAnnotation(
        n_items=8_000,
        n_annotators=5,
        n_classes=3,
        missing_rate=0.30,
        pure_random=True,
        class_dist="uniform",
        seed=123,
    )
    df = gen.generate()
    frac = df.isna().to_numpy().mean()
    assert abs(frac - 0.30) < 0.02


def test_empirical_marginal_matches_pi() -> None:
    pi = np.array([0.70, 0.20, 0.10])
    gen = SimulatedAnnotation(
        n_items=12_000,
        n_annotators=6,
        n_classes=3,
        class_dist=pi,
        pure_random=True,
        seed=5,
    )
    df = gen.generate()
    vals = df.to_numpy(dtype=float).ravel()
    vals = vals[~np.isnan(vals)].astype(int)
    counts = np.bincount(vals, minlength=3)
    p_hat = counts / counts.sum()
    np.testing.assert_allclose(p_hat, pi, atol=0.02)


def test_invalid_constructor() -> None:
    with pytest.raises(ValueError):
        SimulatedAnnotation(10, 1, 3, seed=0)
    with pytest.raises(ValueError):
        SimulatedAnnotation(10, 3, 1, seed=0)
    with pytest.raises(ValueError):
        SimulatedAnnotation(10, 3, 3, noise_level=1.5, seed=0)
    with pytest.raises(ValueError):
        SimulatedAnnotation(10, 3, 3, missing_rate=0.6, seed=0)


def test_reset_rng_reproducible() -> None:
    gen = SimulatedAnnotation(50, 3, 3, pure_random=True, seed=10)
    a = gen.generate().to_numpy()
    gen.reset_rng()
    b = gen.generate().to_numpy()
    np.testing.assert_array_equal(a, b)


def test_list_class_dist() -> None:
    gen = SimulatedAnnotation(
        20,
        3,
        3,
        class_dist=[1 / 3, 1 / 3, 1 / 3],
        pure_random=True,
        seed=0,
    )
    assert isinstance(gen.generate(), pd.DataFrame)
