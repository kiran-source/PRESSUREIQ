"""Match state and score trajectory reconstruction module for PRESSUREIQ."""

import numpy as np
import pandas as pd
from typing import Dict, Optional


def reconstruct_match_states(
    deliveries_df: pd.DataFrame,
    matches_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Reconstruct delivery-level match states, innings scores, and chase dynamics.
    
    Guarantees strict temporal validity:
    All 'before' features represent the state prior to that ball being bowled.
    """
    df = deliveries_df.sort_values(
        by=["match_id", "innings", "overid", "over_ball_num", "innings_ball_num"]
    ).copy()
    
    # 1. Intra-innings cumulative counters
    grp = df.groupby(["match_id", "innings"], sort=False)
    
    # Cumulative legal balls bowled (including current delivery)
    df["cum_legal_balls"] = grp["is_legal_ball"].cumsum()
    # Legal balls bowled prior to this delivery
    df["legal_balls_before"] = grp["is_legal_ball"].cumsum() - df["is_legal_ball"].astype(int)
    
    # Cumulative team runs (estimated)
    df["cum_team_runs"] = grp["est_total_runs"].cumsum()
    df["team_runs_before"] = grp["est_total_runs"].cumsum() - df["est_total_runs"]
    
    # Cumulative wickets lost
    df["cum_wickets"] = grp["is_wicket"].cumsum()
    df["wickets_lost_before"] = grp["is_wicket"].cumsum() - df["is_wicket"].astype(int)
    df["wickets_remaining_before"] = np.clip(10 - df["wickets_lost_before"], 0, 10)
    
    # Standard T20 overs (default 120 balls)
    total_innings_balls = 120
    df["balls_remaining_before"] = np.clip(total_innings_balls - df["legal_balls_before"], 0, total_innings_balls)
    
    # Match Phase before delivery
    # Powerplay: balls 0 to 35 (overs 0.1 to 6.0)
    # Middle: balls 36 to 89 (overs 6.1 to 15.0)
    # Death: balls 90 to 119 (overs 15.1 to 20.0)
    df["phase"] = np.where(
        df["legal_balls_before"] < 36, "Powerplay",
        np.where(df["legal_balls_before"] < 90, "Middle", "Death")
    )
    
    # Current Run Rate before delivery
    df["current_run_rate_before"] = np.where(
        df["legal_balls_before"] > 0,
        (df["team_runs_before"] / (df["legal_balls_before"] / 6.0)),
        0.0
    )
    
    # 2. Chase dynamics (Innings 2)
    # Compute 1st innings total score for each match
    inn1 = df[df["innings"] == 1].groupby("match_id")["est_total_runs"].sum().reset_index()
    inn1.columns = ["match_id", "inn1_final_score"]
    
    # Merge matches meta for revised targets (e.g. DLS)
    revised_meta = matches_df[["match_id", "revised_target", "second_inn_revised_overs", "is_dls_or_revised"]].copy()
    
    df = df.merge(inn1, on="match_id", how="left")
    df = df.merge(revised_meta, on="match_id", how="left")
    
    # Target score definition:
    # If revised target is specified, use that; otherwise 1st innings score + 1
    has_revised = df["revised_target"].notna()
    df["target_score"] = np.where(
        df["innings"] == 2,
        np.where(has_revised, df["revised_target"], df["inn1_final_score"] + 1),
        np.nan
    )
    
    # Revised total balls for innings 2 if shortened
    # Note: 'second_inn_revised_overs' column in raw data actually stores the total revised BALLS (e.g., 90 = 15 overs)
    inn2_max_balls = df["second_inn_revised_overs"].fillna(120).astype(int)
    
    df["balls_remaining_before"] = np.where(
        df["innings"] == 2,
        np.clip(inn2_max_balls - df["legal_balls_before"], 0, inn2_max_balls),
        df["balls_remaining_before"]
    )
    
    # Runs required before delivery in 2nd innings
    df["runs_required_before"] = np.where(
        df["innings"] == 2,
        np.maximum(0, df["target_score"] - df["team_runs_before"]),
        np.nan
    )
    
    # Required Run Rate before delivery in 2nd innings
    df["required_run_rate_before"] = np.where(
        (df["innings"] == 2) & (df["balls_remaining_before"] > 0),
        df["runs_required_before"] / (df["balls_remaining_before"] / 6.0),
        np.where((df["innings"] == 2) & (df["runs_required_before"] <= 0), 0.0, np.nan)
    )
    
    # 3. Individual Batter state before delivery
    # Batter balls faced: legal balls + noballs (excludes wides)
    df["is_batter_ball"] = ~df["is_wide"]
    bat_grp = df.groupby(["match_id", "innings", "striker_id"], sort=False)
    df["batter_balls_faced_before"] = bat_grp["is_batter_ball"].cumsum() - df["is_batter_ball"].astype(int)
    df["batter_runs_before"] = bat_grp["batter_runs"].cumsum() - df["batter_runs"]
    df["batter_strike_rate_before"] = np.where(
        df["batter_balls_faced_before"] > 0,
        (df["batter_runs_before"] / df["batter_balls_faced_before"]) * 100.0,
        0.0
    )
    
    # 4. Individual Bowler spell state before delivery
    bowl_grp = df.groupby(["match_id", "innings", "bowler_id"], sort=False)
    df["bowler_legal_balls_before"] = bowl_grp["is_legal_ball"].cumsum() - df["is_legal_ball"].astype(int)
    df["bowler_runs_conceded_before"] = bowl_grp["bowler_runs_conceded"].cumsum() - df["bowler_runs_conceded"]
    df["bowler_wickets_before"] = bowl_grp["is_bowler_wicket"].cumsum() - df["is_bowler_wicket"].astype(int)
    df["bowler_economy_before"] = np.where(
        df["bowler_legal_balls_before"] > 0,
        (df["bowler_runs_conceded_before"] / (df["bowler_legal_balls_before"] / 6.0)),
        0.0
    )
    
    return df
