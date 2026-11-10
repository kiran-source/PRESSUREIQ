"""Historical player statistics feature generator for PRESSUREIQ.

Strictly temporal: all player metrics for match M are computed using only matches
played PRIOR to match M (chronological lag). Zero future leakage.
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple

# League-level shrinkage priors for cold starts / early matches
PRIOR_BATTER_SR = 132.0
PRIOR_BATTER_AVG = 24.5
PRIOR_BATTER_DOT_PCT = 38.0
PRIOR_BATTER_BOUNDARY_PCT = 17.5
PRIOR_BATTER_PSEUDO_BALLS = 30.0

PRIOR_BOWLER_ECONOMY = 8.25
PRIOR_BOWLER_STRIKE_RATE = 19.5
PRIOR_BOWLER_DOT_PCT = 39.0
PRIOR_BOWLER_PSEUDO_BALLS = 30.0


def compute_historical_batter_stats(deliveries_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute cumulative historical career statistics for each batter prior to each match.
    
    Returns DataFrame indexed by (match_id, striker_id) with strictly pre-match statistics.
    """
    # 1. Match-level aggregates per batter
    match_bat = deliveries_df.groupby(["match_date", "match_id", "striker_id"]).agg(
        match_runs=("batter_runs", "sum"),
        match_balls=("is_batter_ball", "sum"),
        match_dots=("batter_runs", lambda s: (s == 0).sum()),
        match_boundaries=("is_boundary", "sum"),
        match_dismissed=("is_wicket", "max")
    ).reset_index()
    
    # Sort chronologically
    match_bat.sort_values(by=["match_date", "match_id"], inplace=True)
    
    # 2. Expanding window sum per striker
    grp = match_bat.groupby("striker_id")
    
    # Pre-match values = cumulative sum minus current match
    match_bat["prior_balls"] = grp["match_balls"].cumsum() - match_bat["match_balls"]
    match_bat["prior_runs"] = grp["match_runs"].cumsum() - match_bat["match_runs"]
    match_bat["prior_dots"] = grp["match_dots"].cumsum() - match_bat["match_dots"]
    match_bat["prior_boundaries"] = grp["match_boundaries"].cumsum() - match_bat["match_boundaries"]
    match_bat["prior_dismissals"] = grp["match_dismissed"].cumsum() - match_bat["match_dismissed"]
    
    # Bayesian smoothed pre-match metrics
    w = match_bat["prior_balls"] / (match_bat["prior_balls"] + PRIOR_BATTER_PSEUDO_BALLS)
    
    raw_sr = np.where(match_bat["prior_balls"] > 0, (match_bat["prior_runs"] / match_bat["prior_balls"]) * 100.0, PRIOR_BATTER_SR)
    raw_avg = np.where(match_bat["prior_dismissals"] > 0, match_bat["prior_runs"] / match_bat["prior_dismissals"], PRIOR_BATTER_AVG)
    raw_dot_pct = np.where(match_bat["prior_balls"] > 0, (match_bat["prior_dots"] / match_bat["prior_balls"]) * 100.0, PRIOR_BATTER_DOT_PCT)
    raw_bnd_pct = np.where(match_bat["prior_balls"] > 0, (match_bat["prior_boundaries"] / match_bat["prior_balls"]) * 100.0, PRIOR_BATTER_BOUNDARY_PCT)
    
    match_bat["hist_batter_sr"] = w * raw_sr + (1.0 - w) * PRIOR_BATTER_SR
    match_bat["hist_batter_avg"] = w * raw_avg + (1.0 - w) * PRIOR_BATTER_AVG
    match_bat["hist_batter_dot_pct"] = w * raw_dot_pct + (1.0 - w) * PRIOR_BATTER_DOT_PCT
    match_bat["hist_batter_bnd_pct"] = w * raw_bnd_pct + (1.0 - w) * PRIOR_BATTER_BOUNDARY_PCT
    match_bat["hist_batter_balls_exp"] = match_bat["prior_balls"]
    
    cols = [
        "match_id", "striker_id", "hist_batter_sr", "hist_batter_avg",
        "hist_batter_dot_pct", "hist_batter_bnd_pct", "hist_batter_balls_exp"
    ]
    return match_bat[cols]


def compute_historical_bowler_stats(deliveries_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute cumulative historical career statistics for each bowler prior to each match.
    
    Returns DataFrame indexed by (match_id, bowler_id) with strictly pre-match statistics.
    """
    # 1. Match-level aggregates per bowler
    match_bowl = deliveries_df.groupby(["match_date", "match_id", "bowler_id"]).agg(
        match_legal_balls=("is_legal_ball", "sum"),
        match_runs_conceded=("bowler_runs_conceded", "sum"),
        match_wickets=("is_bowler_wicket", "sum"),
        match_dots=("bowler_runs_conceded", lambda s: (s == 0).sum())
    ).reset_index()
    
    # Sort chronologically
    match_bowl.sort_values(by=["match_date", "match_id"], inplace=True)
    
    # 2. Expanding window sum per bowler
    grp = match_bowl.groupby("bowler_id")
    
    match_bowl["prior_balls"] = grp["match_legal_balls"].cumsum() - match_bowl["match_legal_balls"]
    match_bowl["prior_runs"] = grp["match_runs_conceded"].cumsum() - match_bowl["match_runs_conceded"]
    match_bowl["prior_wickets"] = grp["match_wickets"].cumsum() - match_bowl["match_wickets"]
    match_bowl["prior_dots"] = grp["match_dots"].cumsum() - match_bowl["match_dots"]
    
    # Bayesian smoothed pre-match metrics
    w = match_bowl["prior_balls"] / (match_bowl["prior_balls"] + PRIOR_BOWLER_PSEUDO_BALLS)
    
    raw_econ = np.where(match_bowl["prior_balls"] > 0, match_bowl["prior_runs"] / (match_bowl["prior_balls"] / 6.0), PRIOR_BOWLER_ECONOMY)
    raw_sr = np.where(match_bowl["prior_wickets"] > 0, match_bowl["prior_balls"] / match_bowl["prior_wickets"], PRIOR_BOWLER_STRIKE_RATE)
    raw_dot_pct = np.where(match_bowl["prior_balls"] > 0, (match_bowl["prior_dots"] / match_bowl["prior_balls"]) * 100.0, PRIOR_BOWLER_DOT_PCT)
    
    match_bowl["hist_bowler_economy"] = w * raw_econ + (1.0 - w) * PRIOR_BOWLER_ECONOMY
    match_bowl["hist_bowler_strike_rate"] = w * raw_sr + (1.0 - w) * PRIOR_BOWLER_STRIKE_RATE
    match_bowl["hist_bowler_dot_pct"] = w * raw_dot_pct + (1.0 - w) * PRIOR_BOWLER_DOT_PCT
    match_bowl["hist_bowler_balls_exp"] = match_bowl["prior_balls"]
    
    cols = [
        "match_id", "bowler_id", "hist_bowler_economy",
        "hist_bowler_strike_rate", "hist_bowler_dot_pct", "hist_bowler_balls_exp"
    ]
    return match_bowl[cols]

