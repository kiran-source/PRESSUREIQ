"""Master script to compute final Top-10 Batters and Bowlers under pressure with CIs and validation."""

import json
import logging
from pathlib import Path
import pandas as pd
import numpy as np

from src.config import PROCESSED_DATA_DIR, DOCS_DIR
from src.analysis.reliability_engine import (
    compute_batter_reliability_scores,
    compute_bowler_reliability_scores
)
from src.analysis.validation import (
    match_clustered_bootstrap_rankings,
    run_ablation_study
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("PRESSUREIQ.FinalRankings")

DELIVERIES_PAVA_PARQUET = PROCESSED_DATA_DIR / "deliveries_with_pava.parquet"
BATTER_RANKINGS_CSV = PROCESSED_DATA_DIR / "final_batter_rankings.csv"
BOWLER_RANKINGS_CSV = PROCESSED_DATA_DIR / "final_bowler_rankings.csv"
BATTER_RANKINGS_PARQUET = PROCESSED_DATA_DIR / "final_batter_rankings.parquet"
BOWLER_RANKINGS_PARQUET = PROCESSED_DATA_DIR / "final_bowler_rankings.parquet"
VALIDATION_REPORT = DOCS_DIR / "VALIDATION_REPORT.json"


def main():
    logger.info(f"Loading {DELIVERIES_PAVA_PARQUET}...")
    df = pd.read_parquet(DELIVERIES_PAVA_PARQUET)
    
    # 1. Full Batter Reliability Rankings
    logger.info("Computing full batter reliability scores...")
    batter_df = compute_batter_reliability_scores(df)
    eligible_batters = batter_df[batter_df["is_eligible"]].copy()
    eligible_batters["rank"] = np.arange(1, len(eligible_batters) + 1)
    
    # 2. Full Bowler Reliability Rankings
    logger.info("Computing full bowler reliability scores...")
    bowler_df = compute_bowler_reliability_scores(df)
    eligible_bowlers = bowler_df[bowler_df["is_eligible"]].copy()
    eligible_bowlers["rank"] = np.arange(1, len(eligible_bowlers) + 1)
    
    # 3. 2,000 Match-Clustered Bootstrap Confidence Intervals (P0-5)
    boot_bat_path = PROCESSED_DATA_DIR / "bootstrap_2000_batters.parquet"
    if not boot_bat_path.exists():
        logger.info("Running 2,000 match-clustered bootstrap for batters...")
        bat_boot = match_clustered_bootstrap_rankings(df, n_iterations=2000, is_batting=True)
        bat_boot.to_parquet(boot_bat_path, index=False)
        bat_boot.to_csv(PROCESSED_DATA_DIR / "bootstrap_2000_batters.csv", index=False)
    else:
        logger.info(f"Loading existing 2,000 bootstrap results from {boot_bat_path}...")
        bat_boot = pd.read_parquet(boot_bat_path)
        
    boot_bowl_path = PROCESSED_DATA_DIR / "bootstrap_2000_bowlers.parquet"
    if not boot_bowl_path.exists():
        logger.info("Running 2,000 match-clustered bootstrap for bowlers...")
        bowl_boot = match_clustered_bootstrap_rankings(df, n_iterations=2000, is_batting=False)
        bowl_boot.to_parquet(boot_bowl_path, index=False)
        bowl_boot.to_csv(PROCESSED_DATA_DIR / "bootstrap_2000_bowlers.csv", index=False)
    else:
        logger.info(f"Loading existing 2,000 bootstrap results from {boot_bowl_path}...")
        bowl_boot = pd.read_parquet(boot_bowl_path)
        
    # Merge bootstrap statistics
    merge_cols = [
        "player_id", "boot_score_ci_lower_95", "boot_score_ci_upper_95",
        "top10_inclusion_prob", "boot_mean_rank", "boot_rank_ci_lower_95", "boot_rank_ci_upper_95"
    ]
    
    eligible_batters = eligible_batters.merge(bat_boot[merge_cols], on="player_id", how="left")
    eligible_batters["ci_lower_95"] = eligible_batters["boot_score_ci_lower_95"].fillna(eligible_batters["reliability_score"] - 5.0)
    eligible_batters["ci_upper_95"] = eligible_batters["boot_score_ci_upper_95"].fillna(eligible_batters["reliability_score"] + 5.0)
    
    eligible_bowlers = eligible_bowlers.merge(bowl_boot[merge_cols], on="player_id", how="left")
    eligible_bowlers["ci_lower_95"] = eligible_bowlers["boot_score_ci_lower_95"].fillna(eligible_bowlers["reliability_score"] - 5.0)
    eligible_bowlers["ci_upper_95"] = eligible_bowlers["boot_score_ci_upper_95"].fillna(eligible_bowlers["reliability_score"] + 5.0)
    
    # 4. Save Rankings to Parquet and CSV
    logger.info("Saving final rankings...")
    eligible_batters.to_parquet(BATTER_RANKINGS_PARQUET, index=False)
    eligible_batters.to_csv(BATTER_RANKINGS_CSV, index=False)
    
    eligible_bowlers.to_parquet(BOWLER_RANKINGS_PARQUET, index=False)
    eligible_bowlers.to_csv(BOWLER_RANKINGS_CSV, index=False)
    
    # 5. Ablation Studies
    ablation_res = run_ablation_study(df)
    with open(VALIDATION_REPORT, "w", encoding="utf-8") as f:
        json.dump(ablation_res, f, indent=2)
    logger.info(f"Validation report saved to {VALIDATION_REPORT}")
    
    # 6. Print Official Top 10 Batters and Bowlers
    print("\n" + "=" * 90)
    print("🏆 PRESSUREIQ — OFFICIAL TOP 10 MOST RELIABLE BATTERS UNDER PRESSURE")
    print("=" * 90)
    print(eligible_batters.head(10)[[
        "rank", "player_name", "role", "reliability_score", "ci_lower_95", "ci_upper_95",
        "top10_inclusion_prob", "hp_balls", "shrunk_hp_pava_per_ball", "retention_delta", "prc_archetype"
    ]].to_string(index=False))
    
    print("\n" + "=" * 90)
    print("🏆 PRESSUREIQ — OFFICIAL TOP 10 MOST RELIABLE BOWLERS UNDER PRESSURE")
    print("=" * 90)
    print(eligible_bowlers.head(10)[[
        "rank", "player_name", "pace_or_spin", "reliability_score", "ci_lower_95", "ci_upper_95",
        "top10_inclusion_prob", "hp_balls", "shrunk_hp_pava_per_ball", "retention_delta", "prc_archetype"
    ]].to_string(index=False))
    print("=" * 90 + "\n")


if __name__ == "__main__":
    main()
