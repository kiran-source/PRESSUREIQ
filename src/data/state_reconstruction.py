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
    Fully accounts for shortened matches and DLS revised overs in both innings.
    """
    df = deliveries_df.sort_values(
        by=["match_id", "innings", "overid", "over_ball_num", "innings_ball_num"]
    ).copy()
    
    # 0. Early merge of matches metadata for revised overs / targets
    revised_cols = [
        "match_id", "first_inn_revised_overs", "second_inn_revised_overs",
        "revised_target", "is_dls_or_revised"
    ]
    cols_to_merge = [c for c in revised_cols if c in matches_df.columns]
    cols_to_drop = [c for c in cols_to_merge if c != "match_id" and c in df.columns]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
    df = df.merge(matches_df[cols_to_merge], on="match_id", how="left")
    
    # Determine maximum legal ball allocation for the innings
    # Note: first_inn_revised_overs and second_inn_revised_overs store total balls (e.g., 90, 84, 48, 30)
    inn1_max = df["first_inn_revised_overs"].fillna(120).astype(int) if "first_inn_revised_overs" in df.columns else 120
    inn2_max = df["second_inn_revised_overs"].fillna(120).astype(int) if "second_inn_revised_overs" in df.columns else 120
    
    df["max_innings_balls"] = np.where(
        df["innings"] == 1, inn1_max,
        np.where(df["innings"] == 2, inn2_max, 120)
    ).astype(int)
    
    # 1. Intra-innings cumulative counters
    grp = df.groupby(["match_id", "innings"], sort=False)
    
    # Cumulative legal balls bowled (including current delivery)
    df["cum_legal_balls"] = grp["is_legal_ball"].cumsum()
    # Legal balls bowled prior to this delivery (elapsed balls)
    df["legal_balls_before"] = grp["is_legal_ball"].cumsum() - df["is_legal_ball"].astype(int)
    
    # Cumulative team runs (estimated)
    df["cum_team_runs"] = grp["est_total_runs"].cumsum()
    df["team_runs_before"] = grp["est_total_runs"].cumsum() - df["est_total_runs"]
    
    # Cumulative wickets lost
    df["cum_wickets"] = grp["is_wicket"].cumsum()
    df["wickets_lost_before"] = grp["is_wicket"].cumsum() - df["is_wicket"].astype(int)
    df["wickets_remaining_before"] = np.clip(10 - df["wickets_lost_before"], 0, 10)
    
    # Balls remaining before delivery, strictly respecting shortened match allocations
    df["balls_remaining_before"] = np.clip(
        df["max_innings_balls"] - df["legal_balls_before"], 0, df["max_innings_balls"]
    )
    
    # Match Phase before delivery (adapted for standard and shortened matches)
    # Powerplay: first ~30% of scheduled innings (36 balls for 120; 14 for 48; 9 for 30)
    # Death: last ~25% of scheduled innings (90+ for 120; 36+ for 48; 23+ for 30)
    pp_cutoff = np.floor(df["max_innings_balls"] * 0.30).astype(int)
    death_cutoff = np.floor(df["max_innings_balls"] * 0.75).astype(int)
    
    df["phase"] = np.where(
        df["legal_balls_before"] < pp_cutoff, "Powerplay",
        np.where(df["legal_balls_before"] < death_cutoff, "Middle", "Death")
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
    if "inn1_final_score" in df.columns:
        df = df.drop(columns=["inn1_final_score"])
    df = df.merge(inn1, on="match_id", how="left")
    
    # Target score definition:
    # If revised target is specified, use that; otherwise 1st innings score + 1
    has_revised = df["revised_target"].notna() if "revised_target" in df.columns else pd.Series(False, index=df.index)
    df["target_score"] = np.where(
        df["innings"] == 2,
        np.where(has_revised, df["revised_target"], df["inn1_final_score"] + 1),
        np.nan
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
