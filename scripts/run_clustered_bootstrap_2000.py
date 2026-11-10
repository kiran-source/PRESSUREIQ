"""Master execution script for 2,000 Match-Clustered Bootstrap Analysis (P0-5).

Guarantees 100% mathematical fidelity to the canonical reliability engine.
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.abspath("."))

import logging
import time
import pandas as pd
from src.analysis.bootstrap_engine import run_match_clustered_bootstrap

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("PRESSUREIQ.RunBootstrap2000")

PROCESSED_DATA_DIR = Path("data/processed")
DELIVERIES_PAVA_PATH = PROCESSED_DATA_DIR / "deliveries_with_pava.parquet"


def main():
    logger.info(f"Loading deliveries from {DELIVERIES_PAVA_PATH}...")
    df = pd.read_parquet(DELIVERIES_PAVA_PATH)
    logger.info(f"Loaded {len(df):,} deliveries across {df['match_id'].nunique()} matches.")
    
    # 1. Batting 2,000 Match-Clustered Resamples
    t0 = time.time()
    logger.info("Executing 2,000 match-clustered bootstrap iterations for Batters...")
    bat_summary = run_match_clustered_bootstrap(df, n_iterations=2000, seed=42, is_batting=True)
    logger.info(f"Batting bootstrap finished in {time.time() - t0:.2f}s")
    
    bat_parquet = PROCESSED_DATA_DIR / "bootstrap_2000_batters.parquet"
    bat_csv = PROCESSED_DATA_DIR / "bootstrap_2000_batters.csv"
    bat_summary.to_parquet(bat_parquet, index=False)
    bat_summary.to_csv(bat_csv, index=False)
    logger.info(f"Saved {bat_parquet} and {bat_csv}")
    
    # 2. Bowling 2,000 Match-Clustered Resamples
    t0 = time.time()
    logger.info("Executing 2,000 match-clustered bootstrap iterations for Bowlers...")
    bowl_summary = run_match_clustered_bootstrap(df, n_iterations=2000, seed=42, is_batting=False)
    logger.info(f"Bowling bootstrap finished in {time.time() - t0:.2f}s")
    
    bowl_parquet = PROCESSED_DATA_DIR / "bootstrap_2000_bowlers.parquet"
    bowl_csv = PROCESSED_DATA_DIR / "bootstrap_2000_bowlers.csv"
    bowl_summary.to_parquet(bowl_parquet, index=False)
    bowl_summary.to_csv(bowl_csv, index=False)
    logger.info(f"Saved {bowl_parquet} and {bowl_csv}")
    
    # 3. Print Top 10 Stability Summaries
    print("\n" + "=" * 90)
    print("🏏 TOP 10 BATTERS: 2,000 MATCH-CLUSTERED BOOTSTRAP STABILITY (P0-5 HARMONIZED)")
    print("=" * 90)
    print(bat_summary.head(10)[[
        "baseline_rank", "player_name", "baseline_score", "boot_mean_score",
        "boot_score_ci_lower_95", "boot_score_ci_upper_95", "top10_inclusion_prob",
        "boot_mean_rank", "boot_rank_ci_lower_95", "boot_rank_ci_upper_95"
    ]].to_string(index=False))
    
    print("\n" + "=" * 90)
    print("🎯 TOP 10 BOWLERS: 2,000 MATCH-CLUSTERED BOOTSTRAP STABILITY (P0-5 HARMONIZED)")
    print("=" * 90)
    print(bowl_summary.head(10)[[
        "baseline_rank", "player_name", "baseline_score", "boot_mean_score",
        "boot_score_ci_lower_95", "boot_score_ci_upper_95", "top10_inclusion_prob",
        "boot_mean_rank", "boot_rank_ci_lower_95", "boot_rank_ci_upper_95"
    ]].to_string(index=False))
    print("=" * 90 + "\n")


if __name__ == "__main__":
    main()
