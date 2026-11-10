"""Validation, Bootstrap Confidence Intervals, and Ablation Study Engine for PRESSUREIQ."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from src.config import PROCESSED_DATA_DIR, DOCS_DIR
from src.analysis.reliability_engine import (
    compute_batter_reliability_scores,
    compute_bowler_reliability_scores
)
from src.analysis.bootstrap_engine import run_match_clustered_bootstrap

logger = logging.getLogger("PRESSUREIQ.Validation")
VALIDATION_REPORT = DOCS_DIR / "VALIDATION_REPORT.json"


def match_clustered_bootstrap_rankings(
    deliveries_df: pd.DataFrame,
    n_iterations: int = 2000,
    is_batting: bool = True
) -> pd.DataFrame:
    """
    Perform match-clustered bootstrap resampling to compute 95% confidence intervals
    for player reliability scores, ranks, and top-10 inclusion probabilities.
    """
    logger.info(f"Running match-clustered bootstrap (N={n_iterations}, is_batting={is_batting})...")
    return run_match_clustered_bootstrap(
        deliveries_df=deliveries_df,
        n_iterations=n_iterations,
        seed=42,
        is_batting=is_batting
    )


def run_ablation_study(deliveries_df: pd.DataFrame) -> Dict:
    """
    Ablation study evaluating ranking stability when omitting individual framework components (P1-8).
    """
    logger.info("Running Ablation Studies...")
    bat_full = compute_batter_reliability_scores(deliveries_df)
    eligible_full = bat_full[bat_full["is_eligible"]].copy()
    top10_full = set(eligible_full.head(10)["player_name"])
    
    # 1. Ablation: Raw SR only (No contextual expected outcome)
    raw_sr_top10 = set(eligible_full.sort_values(by="career_sr", ascending=False).head(10)["player_name"])
    
    # 2. Ablation: No Empirical Bayes Shrinkage (raw PAVA)
    no_shrink_top10 = set(eligible_full.sort_values(by="raw_hp_pava_per_ball", ascending=False).head(10)["player_name"])
    
    # 3. Ablation: No Retention Delta
    no_ret_comp = (
        0.70 * eligible_full["shrunk_hp_pava_per_ball"] +
        0.15 * (eligible_full["consistency_score"] / 50.0) +
        0.15 * (eligible_full["adaptability_score"] / 50.0)
    )
    eligible_full["no_ret_score"] = no_ret_comp
    no_ret_top10 = set(eligible_full.sort_values(by="no_ret_score", ascending=False).head(10)["player_name"])
    
    # 4. Ablation: No Consistency Pillar
    no_cons_comp = (
        0.60 * eligible_full["shrunk_hp_pava_per_ball"] +
        0.25 * eligible_full["retention_delta"] +
        0.15 * (eligible_full["adaptability_score"] / 50.0)
    )
    eligible_full["no_cons_score"] = no_cons_comp
    no_cons_top10 = set(eligible_full.sort_values(by="no_cons_score", ascending=False).head(10)["player_name"])
    
    # 5. Ablation: No Adaptability Pillar
    no_adapt_comp = (
        0.60 * eligible_full["shrunk_hp_pava_per_ball"] +
        0.25 * eligible_full["retention_delta"] +
        0.15 * (eligible_full["consistency_score"] / 50.0)
    )
    eligible_full["no_adapt_score"] = no_adapt_comp
    no_adapt_top10 = set(eligible_full.sort_values(by="no_adapt_score", ascending=False).head(10)["player_name"])
    
    return {
        "full_model_top10": list(top10_full),
        "ablations": {
            "raw_strike_rate_only": {
                "top10": list(raw_sr_top10),
                "top10_overlap_with_full": len(top10_full.intersection(raw_sr_top10)),
                "jaccard_similarity": round(len(top10_full.intersection(raw_sr_top10)) / len(top10_full.union(raw_sr_top10)), 3)
            },
            "no_empirical_bayes_shrinkage": {
                "top10": list(no_shrink_top10),
                "top10_overlap_with_full": len(top10_full.intersection(no_shrink_top10)),
                "jaccard_similarity": round(len(top10_full.intersection(no_shrink_top10)) / len(top10_full.union(no_shrink_top10)), 3)
            },
            "no_retention_delta": {
                "top10": list(no_ret_top10),
                "top10_overlap_with_full": len(top10_full.intersection(no_ret_top10)),
                "jaccard_similarity": round(len(top10_full.intersection(no_ret_top10)) / len(top10_full.union(no_ret_top10)), 3)
            },
            "no_consistency_pillar": {
                "top10": list(no_cons_top10),
                "top10_overlap_with_full": len(top10_full.intersection(no_cons_top10)),
                "jaccard_similarity": round(len(top10_full.intersection(no_cons_top10)) / len(top10_full.union(no_cons_top10)), 3)
            },
            "no_adaptability_pillar": {
                "top10": list(no_adapt_top10),
                "top10_overlap_with_full": len(top10_full.intersection(no_adapt_top10)),
                "jaccard_similarity": round(len(top10_full.intersection(no_adapt_top10)) / len(top10_full.union(no_adapt_top10)), 3)
            }
        }
    }
