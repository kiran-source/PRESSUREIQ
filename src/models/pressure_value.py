"""Pressure-Adjusted Value Added (PAVA) calculation module for PRESSUREIQ.

Calculates delivery-level contextual value above expectation for batters and bowlers,
weighted continuously by pressure indices, with aggregation to innings and spell levels.
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple

# Run-equivalent value of a wicket by innings phase
WICKET_VALUE_BY_PHASE = {
    "Powerplay": 5.2,
    "Middle": 4.5,
    "Death": 3.6
}


def compute_pressure_adjusted_value(
    deliveries_df: pd.DataFrame,
    expected_outcomes_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Compute delivery-level PAVA for batting and bowling.
    
    All units are expressed in Runs Added Above Expectation.
    """
    df = pd.concat([deliveries_df, expected_outcomes_df], axis=1).copy()
    
    # 1. Phase-based wicket run equivalence
    phase = df["phase"].fillna("Middle")
    wkt_val = phase.map(WICKET_VALUE_BY_PHASE).fillna(4.5).values
    
    # 2. Batting Raw Value Added (Runs)
    # delta_runs: runs off bat - expected runs
    delta_bat_runs = df["batter_runs"].values - df["exp_batter_runs"].values
    # delta_wkt: avoided expected dismissal (positive), or conceded wicket (negative)
    # Strictly evaluate striker dismissal (avoids penalizing striker on non-striker run-outs)
    striker_out = df["is_striker_out"].astype(int).values if "is_striker_out" in df.columns else df["is_wicket"].astype(int).values
    delta_bat_wkt = df["prob_dismissal"].values - striker_out
    # delta_boundary: boundary scored above probability
    delta_bat_bnd = df["is_boundary"].astype(int).values - df["prob_boundary"].values
    
    raw_bat_value = delta_bat_runs + (wkt_val * delta_bat_wkt) + (0.5 * delta_bat_bnd)
    
    # Pressure multiplier: linear scaling anchored at 1.0 (neutral), reaching 3.0 at BPI=100
    bpi = df["bpi"].fillna(35.0).values
    bat_pressure_mult = 1.0 + (bpi / 50.0)
    pava_bat = raw_bat_value * bat_pressure_mult
    
    # 3. Bowling Raw Value Added (Runs)
    # delta_bowl_runs: expected runs conceded - actual runs conceded (positive is good)
    delta_bowl_runs = df["exp_bowler_runs"].values - df["bowler_runs_conceded"].values
    # delta_bowl_wkt: wickets taken above expectation
    delta_bowl_wkt = df["is_bowler_wicket"].astype(int).values - df["prob_bowler_wicket"].values
    
    raw_bowl_value = delta_bowl_runs + (wkt_val * delta_bowl_wkt)
    
    bopi = df["bopi"].fillna(45.0).values
    bowl_pressure_mult = 1.0 + (bopi / 50.0)
    pava_bowl = raw_bowl_value * bowl_pressure_mult
    
    df["raw_bat_value"] = np.round(raw_bat_value, 3)
    df["pava_bat"] = np.round(pava_bat, 3)
    df["raw_bowl_value"] = np.round(raw_bowl_value, 3)
    df["pava_bowl"] = np.round(pava_bowl, 3)
    
    return df


def aggregate_innings_batting_pava(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate delivery-level batting PAVA to innings level."""
    # Filter to players who faced at least 1 legal/batting delivery
    d_col = "is_striker_out" if "is_striker_out" in df.columns else "is_wicket"
    batters = df[df["is_batter_ball"]].groupby(
        ["match_id", "innings", "striker_id", "striker_name", "comp_category"]
    ).agg(
        balls_faced=("is_batter_ball", "sum"),
        runs=("batter_runs", "sum"),
        dismissed=(d_col, "max"),
        avg_bpi=("bpi", "mean"),
        high_pressure_balls=("bpi", lambda s: (s >= 65.0).sum()),
        total_pava=("pava_bat", "sum"),
        raw_value=("raw_bat_value", "sum")
    ).reset_index()
    
    batters["pava_per_ball"] = np.round(batters["total_pava"] / batters["balls_faced"], 3)
    return batters


def aggregate_spell_bowling_pava(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate delivery-level bowling PAVA to match/spell level."""
    bowlers = df[df["is_legal_ball"]].groupby(
        ["match_id", "innings", "bowler_id", "bowler_name", "comp_category"]
    ).agg(
        legal_balls=("is_legal_ball", "sum"),
        runs_conceded=("bowler_runs_conceded", "sum"),
        wickets=("is_bowler_wicket", "sum"),
        avg_bopi=("bopi", "mean"),
        high_pressure_balls=("bopi", lambda s: (s >= 65.0).sum()),
        total_pava=("pava_bowl", "sum"),
        raw_value=("raw_bowl_value", "sum")
    ).reset_index()
    
    bowlers["pava_per_ball"] = np.round(bowlers["total_pava"] / bowlers["legal_balls"], 3)
    return bowlers

