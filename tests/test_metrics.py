"""Tests for `src.metrics` (Phases 1–2)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import cohen_kappa_score

from src.metrics import (
    cohens_kappa,
    expected_agreement_independence,
    fleiss_kappa,
    fleiss_kappa_or_nan,
    krippendorff_alpha,
    observed_agreement,
    observed_agreement_global_with_replacement,
)
from src.simulate import SimulatedAnnotation


def test_observed_agreement_hand_computed_matrix() -> None:
    # 3 items, 2 annotators — roadmap-style toy example (integer labels)
    # pairs: agree, disagree, agree -> A_o = 2/3
    df = pd.DataFrame([[0, 0], [1, 0], [2, 2]])
    assert observed_agreement(df) == pytest.approx(2.0 / 3.0)


def test_observed_agreement_respects_nan() -> None:
    df = pd.DataFrame([[0, 0, np.nan], [1, np.nan, 1]])
    # row0: one pair (0,0) agree; row1: only one label -> no pairs
    assert observed_agreement(df) == pytest.approx(1.0)


def test_observed_agreement_no_pairs_returns_nan() -> None:
    df = pd.DataFrame([[0, np.nan], [np.nan, 1]])
    assert np.isnan(observed_agreement(df))


def test_global_with_replacement_matches_square_sum() -> None:
    # Pool: two 0, one 1 -> N=3, A_o = (2/3)^2 + (1/3)^2 = 5/9
    df = pd.DataFrame([[0, 0, 1]])
    assert observed_agreement_global_with_replacement(df) == pytest.approx(5.0 / 9.0)


def test_expected_uniform() -> None:
    assert expected_agreement_independence([0.5, 0.5]) == pytest.approx(0.50)
    assert expected_agreement_independence([1 / 3, 1 / 3, 1 / 3]) == pytest.approx(1 / 3)
    ae = expected_agreement_independence([0.7, 0.2, 0.1])
    assert ae == pytest.approx(0.7**2 + 0.2**2 + 0.1**2)
    assert ae == pytest.approx(0.54)


def test_expected_invalid_probs() -> None:
    with pytest.raises(ValueError):
        expected_agreement_independence([0.5, 0.8])
    with pytest.raises(ValueError):
        expected_agreement_independence([-0.1, 1.1])


def test_cohens_kappa_worked_example() -> None:
    # notes/phase2-kappa.md: A_o=2/3, kappa=0.4
    y1 = np.array([0, 0, 1])
    y2 = np.array([0, 1, 1])
    assert cohens_kappa(y1, y2) == pytest.approx(0.4)
    assert cohens_kappa(y1, y2) == pytest.approx(cohen_kappa_score(y1, y2))


def test_cohens_kappa_matches_sklearn_random() -> None:
    rng = np.random.default_rng(11)
    y1 = rng.integers(0, 4, size=500)
    y2 = rng.integers(0, 4, size=500)
    assert cohens_kappa(y1, y2) == pytest.approx(cohen_kappa_score(y1, y2))


def test_cohens_kappa_drops_nan_pairs() -> None:
    y1 = np.array([0.0, np.nan, 2.0])
    y2 = np.array([0.0, 1.0, 2.0])
    clean1 = np.array([0.0, 2.0])
    clean2 = np.array([0.0, 2.0])
    assert cohens_kappa(y1, y2) == pytest.approx(cohen_kappa_score(clean1, clean2))


def test_fleiss_kappa_hand_computed() -> None:
    # notes/phase2-kappa.md: kappa_F = 0.25
    x = np.array([[0, 0, 1], [1, 1, 1]], dtype=int)
    assert fleiss_kappa(x) == pytest.approx(0.25)


def test_fleiss_kappa_perfect_agreement() -> None:
    x = np.zeros((10, 4), dtype=int)
    assert fleiss_kappa(x) == pytest.approx(1.0)


def test_fleiss_kappa_rejects_nan() -> None:
    x = np.array([[0, 0], [0, np.nan]])
    with pytest.raises(ValueError, match="complete"):
        fleiss_kappa(x)


def test_fleiss_kappa_rejects_non_integer() -> None:
    with pytest.raises(ValueError, match="integer"):
        fleiss_kappa(np.array([[0.0, 0.5]]))


def test_fleiss_kappa_dataframe() -> None:
    df = pd.DataFrame([[0, 0, 1], [1, 1, 1]])
    assert fleiss_kappa(df) == pytest.approx(0.25)


def test_fleiss_kappa_or_nan_complete_matches_fleiss() -> None:
    df = pd.DataFrame([[0, 0, 1], [1, 1, 1]])
    assert fleiss_kappa_or_nan(df) == pytest.approx(fleiss_kappa(df))


def test_fleiss_kappa_or_nan_missing_returns_nan() -> None:
    df = pd.DataFrame([[0, 0], [0, np.nan]])
    assert np.isnan(fleiss_kappa_or_nan(df))


def test_krippendorff_alpha_matches_reference_nominal_interval() -> None:
    krippendorff = pytest.importorskip("krippendorff")
    ka = krippendorff.alpha

    rel = np.array(
        [
            [np.nan, np.nan, np.nan, np.nan, np.nan, 3, 4, 1, 2, 1, 1, 3, 3, np.nan, 3],
            [1, np.nan, 2, 1, 3, 3, 4, 3, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            [np.nan, np.nan, 2, 1, 3, 4, 4, np.nan, 2, 1, 1, 3, 3, np.nan, 4],
        ],
        dtype=float,
    )
    data = rel.T
    assert krippendorff_alpha(data, level_of_measurement="nominal") == pytest.approx(
        ka(reliability_data=rel, level_of_measurement="nominal"),
        abs=1e-5,
    )
    assert krippendorff_alpha(data, level_of_measurement="interval") == pytest.approx(
        ka(reliability_data=rel, level_of_measurement="interval"),
        abs=1e-5,
    )


def test_krippendorff_alpha_matches_reference_ordinal_ratio() -> None:
    krippendorff = pytest.importorskip("krippendorff")
    ka = krippendorff.alpha

    rel = np.array(
        [
            [1, 2, 3, 3, 2, 1, 4, 1, 2, np.nan, np.nan, np.nan],
            [1, 2, 3, 3, 2, 2, 4, 1, 2, 5, np.nan, 3],
            [np.nan, 3, 3, 3, 2, 3, 4, 2, 2, 5, 1, np.nan],
            [1, 2, 3, 3, 2, 4, 4, 1, 2, 5, 1, np.nan],
        ],
        dtype=float,
    )
    data = rel.T
    vd = np.array([1, 2, 3, 4, 5], dtype=float)
    ord_ours = krippendorff_alpha(data, level_of_measurement="ordinal", value_domain=vd)
    ord_ref = ka(rel, value_domain=[1, 2, 3, 4, 5], level_of_measurement="ordinal")
    assert ord_ours == pytest.approx(ord_ref, abs=1e-5)
    ratio_ours = krippendorff_alpha(data, level_of_measurement="ratio", value_domain=vd)
    assert ratio_ours == pytest.approx(ka(rel, level_of_measurement="ratio"), abs=1e-5)


def test_krippendorff_alpha_perfect_agreement() -> None:
    x = np.array([[0, 0], [0, 0], [1, 1], [1, 1]], dtype=float)
    assert krippendorff_alpha(x, level_of_measurement="nominal") == pytest.approx(1.0)


def test_krippendorff_alpha_two_raters_matches_package() -> None:
    krippendorff = pytest.importorskip("krippendorff")
    x = np.array([[0, 0], [1, 1], [0, 1], [1, 0], [2, 2]], dtype=float)
    ka = krippendorff_alpha(x, level_of_measurement="nominal")
    assert ka == pytest.approx(
        krippendorff.alpha(x.T, level_of_measurement="nominal"),
        abs=1e-9,
    )


def test_krippendorff_alpha_raises_no_pairable_unit() -> None:
    x = np.array([[0, np.nan], [np.nan, 1]], dtype=float)
    with pytest.raises(ValueError, match="two or more"):
        krippendorff_alpha(x, level_of_measurement="nominal")


def test_krippendorff_alpha_raises_single_category_domain() -> None:
    x = np.ones((4, 3))
    with pytest.raises(ValueError, match="at least two"):
        krippendorff_alpha(x, level_of_measurement="nominal")


def test_kappa_paradox_ordering_extreme_noise() -> None:
    gen = SimulatedAnnotation(
        n_items=18_000,
        n_annotators=5,
        n_classes=3,
        noise_level=0.05,
        class_dist="extreme",
        seed=21,
    )
    df = gen.generate()
    ao = observed_agreement(df)
    kf = fleiss_kappa(df.to_numpy(dtype=float))
    assert ao > 0.80
    assert kf < 0.70
    assert ao - kf > 0.25
