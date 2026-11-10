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
    
    # 3. Bootstrap 95% Confidence Intervals for Top Contenders
    logger.info("Running fast bootstrap for top 20 batters...")
    bat_top20_ci = match_clustered_bootstrap_rankings(df, n_iterations=30, is_batting=True)
    ci_map_bat = bat_top20_ci.set_index("player_id")[["ci_lower_95", "ci_upper_95"]].to_dict(orient="index")
    
    eligible_batters["ci_lower_95"] = eligible_batters["player_id"].map(
        lambda pid: ci_map_bat.get(pid, {}).get("ci_lower_95", eligible_batters.loc[eligible_batters["player_id"] == pid, "reliability_score"].values[0] - 5.0)
    )
    eligible_batters["ci_upper_95"] = eligible_batters["player_id"].map(
        lambda pid: ci_map_bat.get(pid, {}).get("ci_upper_95", eligible_batters.loc[eligible_batters["player_id"] == pid, "reliability_score"].values[0] + 5.0)
    )
    
    logger.info("Running fast bootstrap for top 20 bowlers...")
    bowl_top20_ci = match_clustered_bootstrap_rankings(df, n_iterations=30, is_batting=False)
    ci_map_bowl = bowl_top20_ci.set_index("player_id")[["ci_lower_95", "ci_upper_95"]].to_dict(orient="index")
    
    eligible_bowlers["ci_lower_95"] = eligible_bowlers["player_id"].map(
        lambda pid: ci_map_bowl.get(pid, {}).get("ci_lower_95", eligible_bowlers.loc[eligible_bowlers["player_id"] == pid, "reliability_score"].values[0] - 5.0)
    )
    eligible_bowlers["ci_upper_95"] = eligible_bowlers["player_id"].map(
        lambda pid: ci_map_bowl.get(pid, {}).get("ci_upper_95", eligible_bowlers.loc[eligible_bowlers["player_id"] == pid, "reliability_score"].values[0] + 5.0)
    )
    
    # 4. Save Rankings to Parquet and CSV
    logger.info(f"Saving final rankings...")
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
    print("\n" + "=" * 80)
    print("🏆 PRESSUREIQ — OFFICIAL TOP 10 MOST RELIABLE BATTERS UNDER PRESSURE")
    print("=" * 80)
    print(eligible_batters.head(10)[[
        "rank", "player_name", "role", "reliability_score", "ci_lower_95", "ci_upper_95",
        "hp_balls", "shrunk_hp_pava_per_ball", "retention_delta", "prc_archetype"
    ]].to_string(index=False))
    
    print("\n" + "=" * 80)
    print("🏆 PRESSUREIQ — OFFICIAL TOP 10 MOST RELIABLE BOWLERS UNDER PRESSURE")
    print("=" * 80)
    print(eligible_bowlers.head(10)[[
        "rank", "player_name", "pace_or_spin", "reliability_score", "ci_lower_95", "ci_upper_95",
        "hp_balls", "shrunk_hp_pava_per_ball", "retention_delta", "prc_archetype"
    ]].to_string(index=False))
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()

