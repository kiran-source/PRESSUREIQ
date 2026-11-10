"""Unit tests for Phase 2 feature engineering and no-leakage guarantees."""

import numpy as np
import pandas as pd
import pytest

from src.features.first_innings_par import FirstInningsParModel
from src.features.player_history import (
    compute_historical_batter_stats,
    compute_historical_bowler_stats,
    PRIOR_BATTER_SR,
    PRIOR_BOWLER_ECONOMY
)


def test_first_innings_par_model():
    model = FirstInningsParModel()
    # At start of match (120 balls remaining, 10 wickets, 0 score)
    par_score, runs_above = model.estimate_par_trajectory("IPL", 120, 10, 0)
    assert 140 <= par_score <= 210
    assert runs_above == 0.0
    
    # At 90 balls remaining, score 40, 9 wickets
    par_score, runs_above = model.estimate_par_trajectory("IPL", 90, 9, 40)
    assert 140 <= par_score <= 210


def test_player_history_zero_future_leakage():
    """Verify that player statistics before match M only depend on matches < M."""
    # Match 1: Player scores 50 off 20 balls on 2024-04-01 (SR = 250)
    # Match 2: Player scores 10 off 20 balls on 2024-04-05 (SR = 50)
    df = pd.DataFrame([
        # Match 1
        {"match_date": "2024-04-01", "match_id": 1, "striker_id": 99,
         "batter_runs": 50, "is_batter_ball": 20, "is_boundary": 8, "is_wicket": 1},
        # Match 2
        {"match_date": "2024-04-05", "match_id": 2, "striker_id": 99,
         "batter_runs": 10, "is_batter_ball": 20, "is_boundary": 1, "is_wicket": 1},
    ])
    
    # Expand to individual rows mock
    rows = []
    # Match 1: 20 balls
    for i in range(20):
        rows.append({
            "match_date": "2024-04-01", "match_id": 1, "striker_id": 99,
            "batter_runs": 2 if i < 15 else 4, "is_batter_ball": True,
            "is_boundary": i >= 15, "is_wicket": i == 19
        })
    # Match 2: 20 balls
    for i in range(20):
        rows.append({
            "match_date": "2024-04-05", "match_id": 2, "striker_id": 99,
            "batter_runs": 0 if i < 15 else 2, "is_batter_ball": True,
            "is_boundary": False, "is_wicket": i == 19
        })
    df_deliv = pd.DataFrame(rows)
    
    bat_stats = compute_historical_batter_stats(df_deliv)
    
    # Match 1: Prior balls must be 0, strike rate equal to baseline prior
    m1_stats = bat_stats[bat_stats["match_id"] == 1].iloc[0]
    assert m1_stats["hist_batter_balls_exp"] == 0
    assert np.isclose(m1_stats["hist_batter_sr"], PRIOR_BATTER_SR)
    
    # Match 2: Prior balls must be 20 (from Match 1 only)
    m2_stats = bat_stats[bat_stats["match_id"] == 2].iloc[0]
    assert m2_stats["hist_batter_balls_exp"] == 20
    # Match 2 strike rate must be influenced by Match 1 performance, NOT Match 2 itself
    assert m2_stats["hist_batter_sr"] != PRIOR_BATTER_SR
    assert m2_stats["hist_batter_sr"] > 140.0  # High score in Match 1 pulled it up

