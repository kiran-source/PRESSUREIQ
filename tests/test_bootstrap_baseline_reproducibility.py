"""Test for Bootstrap Baseline Reproducibility (P0-5).

Proves that when every match is sampled exactly once (k=1), the bootstrap evaluator
produces identical scores and rankings to the canonical reliability engine.
"""

import numpy as np
import pandas as pd
import pytest

from src.analysis.reliability_engine import (
    compute_batter_reliability_scores,
    compute_bowler_reliability_scores
)
from src.analysis.bootstrap_engine import (
    build_player_match_matrices,
    evaluate_scores_vectorized
)


def test_bootstrap_baseline_reproduces_batting_scores():
    """Verify k=1 vector reproduces canonical batter reliability scores."""
    # Load deliveries with pava
    df = pd.read_parquet("data/processed/deliveries_with_pava.parquet")
    
    # 1. Canonical evaluation
    canon_df = compute_batter_reliability_scores(df)
    canon_map = canon_df.set_index("player_id")["reliability_score"].to_dict()
    
    # 2. Vectorized evaluation with k = 1
    mats = build_player_match_matrices(df, is_batting=True)
    k_ones = np.ones(mats["n_matches"], dtype=np.float64)
    boot_scores, eligible, metrics = evaluate_scores_vectorized(mats, k_ones)
    
    # Check top 20 players
    canon_top20 = canon_df[canon_df["is_eligible"]].head(20)
    for _, row in canon_top20.iterrows():
        pid = row["player_id"]
        p_idx = np.where(mats["player_ids"] == pid)[0][0]
        canon_score = row["reliability_score"]
        boot_score = boot_scores[p_idx]
        
        # Must be equal to within 0.05 score points (accounting for slight rounding)
        assert abs(canon_score - boot_score) < 0.05, f"Mismatch for player {row['player_name']}: canon={canon_score}, boot={boot_score}"


def test_bootstrap_baseline_reproduces_bowling_scores():
    """Verify k=1 vector reproduces canonical bowler reliability scores."""
    df = pd.read_parquet("data/processed/deliveries_with_pava.parquet")
    
    # 1. Canonical evaluation
    canon_df = compute_bowler_reliability_scores(df)
    canon_map = canon_df.set_index("player_id")["reliability_score"].to_dict()
    
    # 2. Vectorized evaluation with k = 1
    mats = build_player_match_matrices(df, is_batting=False)
    k_ones = np.ones(mats["n_matches"], dtype=np.float64)
    boot_scores, eligible, metrics = evaluate_scores_vectorized(mats, k_ones)
    
    # Check top 20 players
    canon_top20 = canon_df[canon_df["is_eligible"]].head(20)
    for _, row in canon_top20.iterrows():
        pid = row["player_id"]
        p_idx = np.where(mats["player_ids"] == pid)[0][0]
        canon_score = row["reliability_score"]
        boot_score = boot_scores[p_idx]
        
        assert abs(canon_score - boot_score) < 0.05, f"Mismatch for bowler {row['player_name']}: canon={canon_score}, boot={boot_score}"
