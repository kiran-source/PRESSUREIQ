"""Unit tests for Batting and Bowling Pressure Indices (BPI & BoPI)."""

import numpy as np
import pandas as pd
import pytest

from src.models.pressure_index import (
    compute_batting_pressure_index,
    compute_bowling_pressure_index
)


@pytest.fixture
def sample_scenarios():
    """Create distinct match situations to test pressure calibration."""
    df = pd.DataFrame([
        # Scenario 1: Low pressure (Over 2, chase RRR 5.0, 10 wickets in hand)
        {
            "innings": 2, "balls_remaining_before": 110, "wickets_lost_before": 0,
            "wickets_remaining_before": 10, "required_run_rate_before": 5.0,
            "runs_required_before": 90, "runs_above_par_trajectory": 0.0,
            "is_knockout_stage": False
        },
        # Scenario 2: Moderate pressure (Over 10, chase RRR 8.5, 7 wickets in hand)
        {
            "innings": 2, "balls_remaining_before": 60, "wickets_lost_before": 3,
            "wickets_remaining_before": 7, "required_run_rate_before": 8.5,
            "runs_required_before": 85, "runs_above_par_trajectory": 0.0,
            "is_knockout_stage": False
        },
        # Scenario 3: High pressure (Over 18, chase RRR 14.0, 5 wickets in hand)
        {
            "innings": 2, "balls_remaining_before": 12, "wickets_lost_before": 5,
            "wickets_remaining_before": 5, "required_run_rate_before": 14.0,
            "runs_required_before": 28, "runs_above_par_trajectory": 0.0,
            "is_knockout_stage": False
        },
        # Scenario 4: Extreme pressure (Over 20, chase RRR 20.0, 2 wickets in hand, Knockout)
        {
            "innings": 2, "balls_remaining_before": 3, "wickets_lost_before": 8,
            "wickets_remaining_before": 2, "required_run_rate_before": 20.0,
            "runs_required_before": 10, "runs_above_par_trajectory": 0.0,
            "is_knockout_stage": True
        }
    ])
    return df


def test_bpi_monotonicity_and_bounds(sample_scenarios):
    bpi_df = compute_batting_pressure_index(sample_scenarios)
    
    # Range check [0, 100]
    assert (bpi_df["bpi"] >= 0.0).all()
    assert (bpi_df["bpi"] <= 100.0).all()
    
    # Monotonicity: Scenario 1 < Scenario 2 < Scenario 3 < Scenario 4
    scores = bpi_df["bpi"].tolist()
    assert scores[0] < scores[1] < scores[2] < scores[3]
    
    # Tiers check
    assert bpi_df.loc[0, "bpi_tier"] in ["Low", "Medium"]
    assert bpi_df.loc[3, "bpi_tier"] in ["High", "Extreme"]


def test_bopi_monotonicity_and_bounds(sample_scenarios):
    bopi_df = compute_bowling_pressure_index(sample_scenarios)
    
    # Range check [0, 100]
    assert (bopi_df["bopi"] >= 0.0).all()
    assert (bopi_df["bopi"] <= 100.0).all()
    
    # Component explainability check
    assert "bopi_defend_comp" in bopi_df.columns
    assert "bopi_resource_comp" in bopi_df.columns
    assert "bopi_climax_comp" in bopi_df.columns

