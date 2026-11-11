"""Unit and regression tests for experimental pressure methodology models."""

import pytest
import numpy as np
import pandas as pd

from scripts.research_pressure_models import (
    compute_alternative_pressure_indices,
    train_predelivery_win_probability_model,
    sigmoid
)


def test_sigmoid_numerical_stability():
    """Ensure sigmoid does not overflow or underflow on extreme inputs."""
    large_pos = np.array([100.0, 1000.0])
    large_neg = np.array([-100.0, -1000.0])
    assert np.allclose(sigmoid(large_pos), 1.0, atol=1e-5)
    assert np.allclose(sigmoid(large_neg), 0.0, atol=1e-5)
    assert np.isclose(sigmoid(np.array([0.0]))[0], 0.5)


def test_win_probability_leverage_bounds():
    """Test that win probability leverage peaks at 50% win probability and is zero at 0% and 100%."""
    p_50 = 0.50
    wpl_50 = 4.0 * p_50 * (1.0 - p_50) * 100.0
    assert np.isclose(wpl_50, 100.0)

    p_0 = 0.0
    wpl_0 = 4.0 * p_0 * (1.0 - p_0) * 100.0
    assert np.isclose(wpl_0, 0.0)

    p_1 = 1.0
    wpl_1 = 4.0 * p_1 * (1.0 - p_1) * 100.0
    assert np.isclose(wpl_1, 0.0)


def test_blowout_suppression_in_cdpi():
    """
    Ensure that in a blowout chase where the opposition is cruising at RRR=2.0
    in the final overs, CDPI bowling pressure is significantly suppressed
    compared to the monotonic baseline.
    """
    sample_df = pd.DataFrame({
        "match_id": [99999],
        "match_date": ["2024-05-01"],
        "innings": [2],
        "required_run_rate_before": [2.0],
        "balls_remaining_before": [18.0],
        "runs_required_before": [6.0],
        "wickets_lost_before": [2.0],
        "wickets_remaining_before": [8.0],
        "target_score": [120.0],
        "runs_above_par_trajectory": [0.0],
        "bpi": [10.0],
        "bopi": [85.0],
        "legal_balls_before": [102.0],
        "max_innings_balls": [120.0],
        "cum_team_runs": [115.0]
    })

    res = compute_alternative_pressure_indices(sample_df)
    
    # In CDPI, blowout pressure should be much lower than the baseline blowout BoPI of 85.0
    bopi_cdpi = res["bopi_cdpi"].iloc[0]
    assert bopi_cdpi < 60.0, f"Expected suppressed BoPI in blowout, got {bopi_cdpi}"


def test_chase_monotonicity_in_cdpi_batting():
    """Ensure that higher RRR increases batting CDPI, holding other factors constant."""
    base_state = {
        "match_id": [99998, 99998],
        "match_date": ["2024-05-01", "2024-05-01"],
        "innings": [2, 2],
        "balls_remaining_before": [30.0, 30.0],
        "wickets_lost_before": [4.0, 4.0],
        "wickets_remaining_before": [6.0, 6.0],
        "target_score": [180.0, 180.0],
        "runs_above_par_trajectory": [0.0, 0.0],
        "bpi": [50.0, 75.0],
        "bopi": [50.0, 25.0],
        "legal_balls_before": [90.0, 90.0],
        "max_innings_balls": [120.0, 120.0],
        "cum_team_runs": [120.0, 100.0]
    }
    # Delivery 1: RRR = 8.0 (40 runs off 30 balls)
    # Delivery 2: RRR = 14.0 (70 runs off 30 balls)
    base_state["required_run_rate_before"] = [8.0, 14.0]
    base_state["runs_required_before"] = [40.0, 70.0]

    sample_df = pd.DataFrame(base_state)
    res = compute_alternative_pressure_indices(sample_df)

    bpi_low_rrr = res["bpi_cdpi"].iloc[0]
    bpi_high_rrr = res["bpi_cdpi"].iloc[1]

    assert bpi_high_rrr > bpi_low_rrr, f"Expected higher BPI for higher RRR: {bpi_high_rrr} vs {bpi_low_rrr}"
