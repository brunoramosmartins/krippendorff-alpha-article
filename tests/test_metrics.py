"""Tests for `src.metrics` (Phase 1)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.metrics import (
    expected_agreement_independence,
    observed_agreement,
    observed_agreement_global_with_replacement,
)


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
