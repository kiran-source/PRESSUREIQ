"""Feature engineering orchestrator for PRESSUREIQ.

Combines match state, par trajectories, historical player statistics,
and matchup context into ML-ready delivery-level feature matrices.
"""

import logging
import numpy as np
import pandas as pd
from pathlib import Path

from src.config import DELIVERIES_PARQUET, PROCESSED_DATA_DIR
from src.features.first_innings_par import (
    compute_chronological_first_innings_par,
    FirstInningsParModel
)
from src.features.player_history import (
    compute_historical_batter_stats,
    compute_historical_bowler_stats
)

logger = logging.getLogger("PRESSUREIQ.FeatureBuilder")
FEATURES_PARQUET = PROCESSED_DATA_DIR / "features_deliveries.parquet"


def build_delivery_features(deliveries_df: pd.DataFrame) -> pd.DataFrame:
    """Build all delivery-level features with strict temporal ordering."""
    logger.info("Building delivery features...")
    df = deliveries_df.copy()
    
    # Exclude super overs from feature training / pressure rankings
    df = df[df["innings"].isin([1, 2])].copy()
    
    # 1. First innings par score trajectory estimation (strictly chronological expanding window)
    logger.info("Computing strictly chronological 1st innings par trajectories...")
    df = compute_chronological_first_innings_par(df)
    
    # 2. Historical player statistics (strictly pre-match lag)
    logger.info("Computing pre-match historical batter statistics...")
    bat_stats = compute_historical_batter_stats(df)
    df = df.merge(bat_stats, on=["match_id", "striker_id"], how="left")
    
    logger.info("Computing pre-match historical bowler statistics...")
    bowl_stats = compute_historical_bowler_stats(df)
    df = df.merge(bowl_stats, on=["match_id", "bowler_id"], how="left")
    
    # 3. Role and position encodings
    df["batting_role"] = np.where(
        df["batting_order"] <= 3, "Top_Order",
        np.where(df["batting_order"] <= 6, "Middle_Order", "Finisher")
    )
    
    # 4. Stage context & Knockout leverage
    # Playoff/Knockout matches have higher psychological leverage
    stage_lower = df["stage"].astype(str).str.lower()
    is_knockout = (
        (df["knock_out"] == 1) | 
        stage_lower.str.contains("final|qualifier|eliminator|semi", regex=True)
    )
    df["is_knockout_stage"] = is_knockout
    df["match_importance_weight"] = np.where(is_knockout, 1.25, 1.0)
    
    # 5. Handedness matchup interaction
    df["matchup_interaction"] = df["batting_type"] + "_vs_" + df["pace_or_spin"]
    
    # 6. Pressure Indices (BPI and BoPI)
    logger.info("Computing Batting Pressure Index (BPI)...")
    from src.models.pressure_index import compute_batting_pressure_index, compute_bowling_pressure_index
    bpi_df = compute_batting_pressure_index(df)
    for col in bpi_df.columns:
        df[col] = bpi_df[col].values
        
    logger.info("Computing Bowling Pressure Index (BoPI)...")
    bopi_df = compute_bowling_pressure_index(df)
    for col in bopi_df.columns:
        df[col] = bopi_df[col].values
    
    # Fill remaining numerical NaNs with appropriate domain neutrals
    df["hist_batter_sr"] = df["hist_batter_sr"].fillna(130.0)
    df["hist_batter_avg"] = df["hist_batter_avg"].fillna(24.0)
    df["hist_batter_dot_pct"] = df["hist_batter_dot_pct"].fillna(38.0)
    df["hist_batter_bnd_pct"] = df["hist_batter_bnd_pct"].fillna(17.5)
    df["hist_batter_balls_exp"] = df["hist_batter_balls_exp"].fillna(0)
    
    df["hist_bowler_economy"] = df["hist_bowler_economy"].fillna(8.2)
    df["hist_bowler_strike_rate"] = df["hist_bowler_strike_rate"].fillna(19.0)
    df["hist_bowler_dot_pct"] = df["hist_bowler_dot_pct"].fillna(39.0)
    df["hist_bowler_balls_exp"] = df["hist_bowler_balls_exp"].fillna(0)
    
    logger.info(f"Feature matrix built successfully: {len(df)} deliveries, {len(df.columns)} columns.")
    return df


def generate_and_save_features():
    """Load deliveries parquet, compute features, and save enriched parquet."""
    logger.info(f"Loading {DELIVERIES_PARQUET}...")
    deliveries_df = pd.read_parquet(DELIVERIES_PARQUET)
    feat_df = build_delivery_features(deliveries_df)
    logger.info(f"Writing {FEATURES_PARQUET}...")
    feat_df.to_parquet(FEATURES_PARQUET, index=False)
    logger.info("Feature engineering complete!")
    return feat_df


if __name__ == "__main__":
    generate_and_save_features()
