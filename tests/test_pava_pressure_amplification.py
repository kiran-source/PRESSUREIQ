"""Tests for PAVA Pressure Amplification Resolution (P0).

Verifies that:
1. Positive and negative outcomes at low, medium, high, and extreme pressure
   have pure unamplified units (Runs Added Above Expectation per ball).
2. Multiplying by 1 + BPI/50 is not applied to PAVA (which eliminates double counting).
3. A player with identical raw surplus in HP and LP achieves an exact 0.00 Retention Delta.
4. Symmetrical execution surplus (+x vs -x) produces equal and opposite value.
"""

import numpy as np
import pandas as pd
import pytest

from src.models.pressure_value import compute_pressure_adjusted_value


def make_delivery_row(
    bpi: float,
    bopi: float,
    batter_runs: int,
    is_boundary: int,
    is_striker_out: int,
    bowler_runs: int,
    is_bowler_wicket: int,
    exp_batter_runs: float = 1.2,
    prob_dismissal: float = 0.05,
    prob_boundary: float = 0.18,
    exp_bowler_runs: float = 1.2,
    prob_bowler_wicket: float = 0.05,
    phase: str = "Middle"
):
    return {
        "delivery_id": "test_1",
        "match_id": 1,
        "innings": 1,
        "phase": phase,
        "bpi": bpi,
        "bopi": bopi,
        "batter_runs": batter_runs,
        "is_boundary": is_boundary,
        "is_striker_out": is_striker_out,
        "is_wicket": is_striker_out,
        "bowler_runs_conceded": bowler_runs,
        "is_bowler_wicket": is_bowler_wicket,
        "is_batter_ball": True,
        "is_legal_ball": True,
        "bowler_id": 100,
        "striker_id": 200,
        "exp_batter_runs": exp_batter_runs,
        "prob_dismissal": prob_dismissal,
        "prob_boundary": prob_boundary,
        "exp_bowler_runs": exp_bowler_runs,
        "prob_bowler_wicket": prob_bowler_wicket
    }


def test_positive_and_negative_outcomes_across_pressure_tiers():
    """Verify positive and negative batting & bowling outcomes across Low, Med, High, Extreme BPI."""
    tiers = [
        ("Low", 20.0),
        ("Medium", 50.0),
        ("High", 70.0),
        ("Extreme", 95.0)
    ]
    
    for name, p_val in tiers:
        # 1. Positive Batting Outcome (Six hit: 6 runs, 1 boundary, 0 out)
        row_pos = make_delivery_row(
            bpi=p_val, bopi=p_val,
            batter_runs=6, is_boundary=1, is_striker_out=0,
            bowler_runs=6, is_bowler_wicket=0
        )
        df_pos = pd.DataFrame([row_pos])
        pava_pos = compute_pressure_adjusted_value(df_pos, df_pos[[
            "exp_batter_runs", "prob_dismissal", "prob_boundary", "exp_bowler_runs", "prob_bowler_wicket"
        ]])
        
        # Expected raw surplus: (6 - 1.2) + 4.5 * (0.05 - 0) + 0.5 * (1 - 0.18)
        # = 4.8 + 0.225 + 0.41 = 5.435 runs
        expected_surplus = round((6 - 1.2) + 4.5 * 0.05 + 0.5 * (1 - 0.18), 3)
        assert np.isclose(pava_pos["pava_bat"].iloc[0], expected_surplus), \
            f"Failed at {name} pressure: pava_bat must equal raw_bat_value without multiplier"
        assert pava_pos["pava_bat"].iloc[0] == pava_pos["raw_bat_value"].iloc[0]
        
        # 2. Negative Batting Outcome (Dismissed for dot: 0 runs, 0 boundary, 1 out)
        row_neg = make_delivery_row(
            bpi=p_val, bopi=p_val,
            batter_runs=0, is_boundary=0, is_striker_out=1,
            bowler_runs=0, is_bowler_wicket=1
        )
        df_neg = pd.DataFrame([row_neg])
        pava_neg = compute_pressure_adjusted_value(df_neg, df_neg[[
            "exp_batter_runs", "prob_dismissal", "prob_boundary", "exp_bowler_runs", "prob_bowler_wicket"
        ]])
        
        # Expected raw deficit: (0 - 1.2) + 4.5 * (0.05 - 1) + 0.5 * (0 - 0.18)
        # = -1.2 + 4.5 * (-0.95) - 0.09 = -1.2 - 4.275 - 0.09 = -5.565 runs
        expected_deficit = round((0 - 1.2) + 4.5 * (0.05 - 1.0) + 0.5 * (0 - 0.18), 3)
        assert np.isclose(pava_neg["pava_bat"].iloc[0], expected_deficit)
        assert pava_neg["pava_bat"].iloc[0] == pava_neg["raw_bat_value"].iloc[0]
        
        # 3. Bowling Wicket (Positive for bowler)
        # Bowler value: (1.2 - 0) + 4.5 * (1 - 0.05) = 1.2 + 4.275 = +5.475 runs
        expected_bowl_val = round((1.2 - 0) + 4.5 * (1.0 - 0.05), 3)
        assert np.isclose(pava_neg["pava_bowl"].iloc[0], expected_bowl_val)
        assert pava_neg["pava_bowl"].iloc[0] == pava_neg["raw_bowl_value"].iloc[0]


def test_baseline_retention_invariance():
    """Verify that a player with identical raw execution in HP and LP has Retention Delta = 0.00."""
    # Suppose a batter executes with raw surplus of +0.30 runs/ball in both LP (BPI=20) and HP (BPI=80)
    lp_row = make_delivery_row(bpi=20.0, bopi=20.0, batter_runs=2, is_boundary=0, is_striker_out=0, bowler_runs=2, is_bowler_wicket=0, exp_batter_runs=1.7, prob_dismissal=0.0)
    hp_row = make_delivery_row(bpi=80.0, bopi=80.0, batter_runs=2, is_boundary=0, is_striker_out=0, bowler_runs=2, is_bowler_wicket=0, exp_batter_runs=1.7, prob_dismissal=0.0)
    
    df = pd.DataFrame([lp_row, hp_row])
    pava_df = compute_pressure_adjusted_value(df, df[[
        "exp_batter_runs", "prob_dismissal", "prob_boundary", "exp_bowler_runs", "prob_bowler_wicket"
    ]])
    
    lp_pava = pava_df.loc[0, "pava_bat"]
    hp_pava = pava_df.loc[1, "pava_bat"]
    
    # Retention delta MUST be 0.00
    retention_delta = hp_pava - lp_pava
    assert np.isclose(retention_delta, 0.0, atol=1e-5), \
        f"Retention delta must be 0.00 for identical execution across pressure regimes, got {retention_delta}"


def test_symmetric_execution_surplus():
    """Verify that +x runs surplus and -x runs deficit produce equal and opposite PAVA."""
    exp_r = 1.0
    row_plus = make_delivery_row(bpi=60.0, bopi=60.0, batter_runs=2, is_boundary=0, is_striker_out=0, bowler_runs=2, is_bowler_wicket=0, exp_batter_runs=exp_r, prob_dismissal=0.0, prob_boundary=0.0)
    row_minus = make_delivery_row(bpi=60.0, bopi=60.0, batter_runs=0, is_boundary=0, is_striker_out=0, bowler_runs=0, is_bowler_wicket=0, exp_batter_runs=exp_r, prob_dismissal=0.0, prob_boundary=0.0)
    
    df = pd.DataFrame([row_plus, row_minus])
    pava_df = compute_pressure_adjusted_value(df, df[[
        "exp_batter_runs", "prob_dismissal", "prob_boundary", "exp_bowler_runs", "prob_bowler_wicket"
    ]])
    
    assert np.isclose(pava_df.loc[0, "pava_bat"], -pava_df.loc[1, "pava_bat"])
