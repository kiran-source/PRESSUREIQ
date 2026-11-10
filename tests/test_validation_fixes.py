"""Regression and validation unit tests for CodeRabbit review fixes."""

import numpy as np
import pandas as pd
import pytest

from src.data.cleaner import clean_deliveries
from src.features.first_innings_par import FirstInningsParModel
from src.analysis.reliability_engine import K_SHRINK
from src.models.pressure_value import compute_pressure_adjusted_value, aggregate_innings_batting_pava


def test_striker_out_attribution_on_runout():
    """Verify that when the non-striker is run out, striker is NOT marked as out."""
    df = pd.DataFrame([
        # Ball 1: Non-striker is run out
        {
            "match_id": 1, "innings": 1, "overid": 1, "over_ball_num": 1, "innings_ball_num": 1,
            "batting_team_id": 1, "bowling_team_id": 2,
            "striker_id": 101, "striker_name": "Striker A",
            "non_striker_id": 102, "non_striker_name": "NonStriker B",
            "bowler_id": 201, "bowler_name": "Bowler X",
            "batting_type": "RHB", "bowling_type": "Pace", "batting_order": 1, "runs": 1,
            "is_four": False, "is_six": False, "is_wicket": True,
            "dismissal_type_id": 4.0, "dismissal_type": "RunOut",
            "dismissed_player_id": 102.0,  # Non-striker dismissed!
            "extras_type": np.nan, "extras1_runs": 6, "extras_2_runs": 0, "pace_or_spin": "Pace",
            "bowl_speed": 135.0, "stroke": "Push", "delivery_style": "Straight",
            "over_or_around": "Over", "on_or_off": "Off-side",
            "delivery_ist_time": "2024-04-01 00:00:00 UTC"
        },
        # Ball 2: Striker is caught
        {
            "match_id": 1, "innings": 1, "overid": 1, "over_ball_num": 2, "innings_ball_num": 2,
            "batting_team_id": 1, "bowling_team_id": 2,
            "striker_id": 101, "striker_name": "Striker A",
            "non_striker_id": 103, "non_striker_name": "NonStriker C",
            "bowler_id": 201, "bowler_name": "Bowler X",
            "batting_type": "RHB", "bowling_type": "Pace", "batting_order": 1, "runs": 0,
            "is_four": False, "is_six": False, "is_wicket": True,
            "dismissal_type_id": 1.0, "dismissal_type": "Caught",
            "dismissed_player_id": 101.0,  # Striker dismissed!
            "extras_type": np.nan, "extras1_runs": 6, "extras_2_runs": 0, "pace_or_spin": "Pace",
            "bowl_speed": 136.0, "stroke": "Slog", "delivery_style": "Straight",
            "over_or_around": "Over", "on_or_off": "Off-side",
            "delivery_ist_time": "2024-04-01 00:00:00 UTC"
        }
    ])
    
    cleaned = clean_deliveries(df)
    
    # Ball 1: Wicket fell, but striker was NOT out
    assert bool(cleaned.loc[0, "is_wicket"]) is True
    assert bool(cleaned.loc[0, "is_striker_out"]) is False
    
    # Ball 2: Wicket fell, and striker WAS out
    assert bool(cleaned.loc[1, "is_wicket"]) is True
    assert bool(cleaned.loc[1, "is_striker_out"]) is True


def test_first_innings_par_model_final_score_accounting():
    """Verify that FirstInningsParModel accounts for runs on the final delivery."""
    # 2 deliveries in Innings 1:
    # Ball 1: 1 run (score_before = 0, est_runs = 1)
    # Ball 2: 6 runs (score_before = 1, est_runs = 6) -> Final Score = 7
    df = pd.DataFrame([
        {
            "match_id": 10, "innings": 1, "balls_remaining_before": 2,
            "wickets_remaining_before": 10, "team_runs_before": 0,
            "est_total_runs": 1, "comp_category": "IPL"
        },
        {
            "match_id": 10, "innings": 1, "balls_remaining_before": 1,
            "wickets_remaining_before": 10, "team_runs_before": 1,
            "est_total_runs": 6, "comp_category": "IPL"
        }
    ])
    
    model = FirstInningsParModel()
    model.fit(df)
    
    # With both balls falling into over_bucket=0 (balls remaining 2 and 1):
    # Ball 1 had remaining runs = 7 - 0 = 7
    # Ball 2 had remaining runs = 7 - 1 = 6
    # The expected remaining runs across the bucket is the mean: (7 + 6) / 2 = 6.5
    key = ("IPL", 0, 10)
    assert key in model.lookup_table
    assert model.lookup_table[key] == 6.5


def test_empirical_bayes_shrinkage_extremes():
    """Verify shrinkage behavior for low-volume vs high-volume pressure samples."""
    # Low exposure: 5 balls, raw PAVA = +2.0
    n_low = 5.0
    weight_low = n_low / (n_low + K_SHRINK)
    shrunk_low = weight_low * 2.0 + (1.0 - weight_low) * 0.0
    # Must be heavily regressed to 0 (< 0.3)
    assert shrunk_low < 0.30
    assert weight_low == pytest.approx(5.0 / 50.0, rel=1e-3)
    
    # High exposure: 450 balls, raw PAVA = +2.0
    n_high = 450.0
    weight_high = n_high / (n_high + K_SHRINK)
    shrunk_high = weight_high * 2.0 + (1.0 - weight_high) * 0.0
    # Must retain >= 90% of raw performance (> 1.80)
    assert shrunk_high > 1.80
    assert weight_high == pytest.approx(450.0 / 495.0, rel=1e-3)


def test_pava_aggregation_consistency():
    """Verify that delivery-level PAVA properly rolls up into innings-level PAVA."""
    deliv_df = pd.DataFrame([
        {
            "match_id": 1, "innings": 1, "striker_id": 50, "striker_name": "Batter Z",
            "comp_category": "IPL", "is_batter_ball": True, "is_wide": False,
            "batter_runs": 4, "bowler_runs_conceded": 4, "is_wicket": False,
            "is_striker_out": False, "is_bowler_wicket": False,
            "is_boundary": True, "phase": "Middle", "bpi": 70.0, "bopi": 50.0
        },
        {
            "match_id": 1, "innings": 1, "striker_id": 50, "striker_name": "Batter Z",
            "comp_category": "IPL", "is_batter_ball": True, "is_wide": False,
            "batter_runs": 6, "bowler_runs_conceded": 6, "is_wicket": False,
            "is_striker_out": False, "is_bowler_wicket": False,
            "is_boundary": True, "phase": "Death", "bpi": 80.0, "bopi": 60.0
        }
    ])
    
    exp_df = pd.DataFrame([
        {
            "exp_batter_runs": 1.2, "prob_dismissal": 0.05, "prob_boundary": 0.20,
            "exp_bowler_runs": 1.2, "prob_bowler_wicket": 0.05
        },
        {
            "exp_batter_runs": 1.5, "prob_dismissal": 0.08, "prob_boundary": 0.25,
            "exp_bowler_runs": 1.5, "prob_bowler_wicket": 0.08
        }
    ])
    
    pava_df = compute_pressure_adjusted_value(deliv_df, exp_df)
    inn_pava = aggregate_innings_batting_pava(pava_df)
    
    assert len(inn_pava) == 1
    assert inn_pava.loc[0, "balls_faced"] == 2
    assert inn_pava.loc[0, "runs"] == 10
    assert np.isclose(inn_pava.loc[0, "total_pava"], pava_df["pava_bat"].sum())
