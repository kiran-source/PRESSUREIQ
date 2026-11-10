"""Tests for Bowling Illegal Deliveries Accounting (P0-4).

Proves that an expensive wide or no-ball worsens bowler value and economy
without increasing legal-ball count.
"""

import numpy as np
import pandas as pd
import pytest

from src.models.pressure_value import compute_pressure_adjusted_value, aggregate_spell_bowling_pava
from src.analysis.reliability_engine import compute_bowler_reliability_scores


def test_illegal_deliveries_worsen_economy_and_pava_without_increasing_legal_balls():
    """Verify wide/no-ball penalizes bowler runs/PAVA while legal balls remain unchanged."""
    # Create baseline match deliveries for Bowler A (6 legal balls, 6 runs conceded)
    base_rows = []
    for i in range(6):
        base_rows.append({
            "delivery_id": f"m1_inn1_{i+1}",
            "match_id": 1,
            "match_date": "2023-04-10",
            "innings": 1,
            "phase": "Death",
            "bpi": 70.0,
            "bopi": 70.0,
            "comp_category": "IPL",
            "bowler_id": 999,
            "bowler_name": "Test Bowler",
            "bowling_type": "Fast",
            "pace_or_spin": "Pace",
            "is_legal_ball": True,
            "is_batter_ball": True,
            "batter_runs": 1,
            "is_boundary": 0,
            "bowler_runs_conceded": 1,
            "is_bowler_wicket": 0,
            "is_striker_out": 0,
            # Model expectations
            "exp_batter_runs": 1.2,
            "prob_dismissal": 0.05,
            "prob_boundary": 0.15,
            "exp_bowler_runs": 1.2,
            "prob_bowler_wicket": 0.05
        })
    df_clean = pd.DataFrame(base_rows)
    pava_clean = compute_pressure_adjusted_value(df_clean, df_clean[[
        "exp_batter_runs", "prob_dismissal", "prob_boundary", "exp_bowler_runs", "prob_bowler_wicket"
    ]])
    spell_clean = aggregate_spell_bowling_pava(pava_clean)
    
    assert spell_clean["legal_balls"].iloc[0] == 6
    assert spell_clean["runs_conceded"].iloc[0] == 6
    clean_pava = spell_clean["total_pava"].iloc[0]
    
    # Now create dirty version with 1 expensive wide (conceding 5 runs: 1 wide + 4 boundary)
    dirty_rows = list(base_rows)
    dirty_rows.append({
        "delivery_id": "m1_inn1_wide",
        "match_id": 1,
        "match_date": "2023-04-10",
        "innings": 1,
        "phase": "Death",
        "bpi": 70.0,
        "bopi": 70.0,
        "comp_category": "IPL",
        "bowler_id": 999,
        "bowler_name": "Test Bowler",
        "bowling_type": "Fast",
        "pace_or_spin": "Pace",
        "is_legal_ball": False,   # WIDE BALL
        "is_batter_ball": False,
        "batter_runs": 0,
        "is_boundary": 0,
        "bowler_runs_conceded": 5, # 5 runs conceded on wide
        "is_bowler_wicket": 0,
        "is_striker_out": 0,
        "exp_batter_runs": 1.2,
        "prob_dismissal": 0.05,
        "prob_boundary": 0.15,
        "exp_bowler_runs": 1.2,
        "prob_bowler_wicket": 0.05
    })
    df_dirty = pd.DataFrame(dirty_rows)
    pava_dirty = compute_pressure_adjusted_value(df_dirty, df_dirty[[
        "exp_batter_runs", "prob_dismissal", "prob_boundary", "exp_bowler_runs", "prob_bowler_wicket"
    ]])
    spell_dirty = aggregate_spell_bowling_pava(pava_dirty)
    
    # Legal balls MUST remain 6
    assert spell_dirty["legal_balls"].iloc[0] == 6
    # Total balls bowled increments to 7
    assert spell_dirty["total_balls_bowled"].iloc[0] == 7
    # Conceded runs must increase from 6 to 11
    assert spell_dirty["runs_conceded"].iloc[0] == 11
    # PAVA must be strictly worse (lower)
    dirty_pava = spell_dirty["total_pava"].iloc[0]
    assert dirty_pava < clean_pava
