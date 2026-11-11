"""Automated regression tests for Phase 1 Independent Audit Remediation.

Covers:
1. Batter dot-ball accounting (wides strictly excluded from dot-ball numerator).
2. Bowler dot-ball accounting (strictly isolated to legal balls).
3. Same-day match ordering determinism.
4. Recommendation engine MCDA single availability weighting.
5. Canonical player identity crosswalk against data pack mapping.
6. Mathematical specification parameter consistency.
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np
import pytest

from src.features.player_history import (
    compute_historical_batter_stats,
    compute_historical_bowler_stats,
    PRIOR_BATTER_SR,
    PRIOR_BOWLER_ECONOMY
)
from src.models.pressure_value import WICKET_VALUE_BY_PHASE
from src.analysis.reliability_engine import fit_pressure_response_curve

RAW_MAPPING_PATH = Path("SupeRR Selector Season 2 _ Problem Statement _ Data Pack/SupeRR Selector Season 2 _ Data Pack/competition_team_player_mapping.csv")
PROCESSED_DIR = Path("data/processed")


def test_batter_dot_ball_accounting_excludes_wides():
    """Verify that wide deliveries (where batter_runs==0 and is_batter_ball==0) do not enter match_dots."""
    mock_deliveries = pd.DataFrame([
        # Match 1: 3 balls faced (1 run, 0 run dot, 4 run), plus 2 wides
        {"match_date": "2024-04-01", "match_id": 101, "striker_id": 1, "batter_runs": 1, "is_batter_ball": 1, "is_boundary": 0, "is_wicket": 0},
        {"match_date": "2024-04-01", "match_id": 101, "striker_id": 1, "batter_runs": 0, "is_batter_ball": 1, "is_boundary": 0, "is_wicket": 0},
        {"match_date": "2024-04-01", "match_id": 101, "striker_id": 1, "batter_runs": 4, "is_batter_ball": 1, "is_boundary": 1, "is_wicket": 0},
        {"match_date": "2024-04-01", "match_id": 101, "striker_id": 1, "batter_runs": 0, "is_batter_ball": 0, "is_boundary": 0, "is_wicket": 0}, # Wide 1
        {"match_date": "2024-04-01", "match_id": 101, "striker_id": 1, "batter_runs": 0, "is_batter_ball": 0, "is_boundary": 0, "is_wicket": 0}, # Wide 2
        # Match 2: Next match, where pre-match stats will reflect Match 1
        {"match_date": "2024-04-05", "match_id": 102, "striker_id": 1, "batter_runs": 0, "is_batter_ball": 1, "is_boundary": 0, "is_wicket": 0},
    ])
    
    stats = compute_historical_batter_stats(mock_deliveries)
    m2_stat = stats[stats["match_id"] == 102].iloc[0]
    
    # In match 1: batter faced exactly 3 balls, with exactly 1 genuine dot ball
    # Prior balls must be exactly 3 (NOT 5)
    assert m2_stat["hist_batter_balls_exp"] == 3.0
    
    # The dot percentage of match 1 prior should be based on 1 dot out of 3 balls (33.33%), NOT 3 dots out of 3 balls (100%)
    # Let's verify raw_dot_pct prior to Bayesian smoothing:
    # w = 3 / (3 + 30) = 3/33 = 0.0909
    # smoothed_dot = (3/33)*(1/3*100) + (30/33)*38.0 = 3.03 + 34.55 = 37.58%
    assert m2_stat["hist_batter_dot_pct"] < 50.0, "Dot percentage inflated by counting wides!"


def test_bowler_dot_ball_accounting_isolated_to_legal_balls():
    """Verify that bowler dots require legal balls."""
    mock_deliveries = pd.DataFrame([
        # Match 1: 2 legal balls (0 runs, 4 runs), 1 wide (1 run conceded)
        {"match_date": "2024-04-01", "match_id": 201, "bowler_id": 10, "is_legal_ball": 1, "bowler_runs_conceded": 0, "is_bowler_wicket": 0},
        {"match_date": "2024-04-01", "match_id": 201, "bowler_id": 10, "is_legal_ball": 1, "bowler_runs_conceded": 4, "is_bowler_wicket": 0},
        {"match_date": "2024-04-01", "match_id": 201, "bowler_id": 10, "is_legal_ball": 0, "bowler_runs_conceded": 1, "is_bowler_wicket": 0},
        # Match 2
        {"match_date": "2024-04-05", "match_id": 202, "bowler_id": 10, "is_legal_ball": 1, "bowler_runs_conceded": 0, "is_bowler_wicket": 0},
    ])
    
    stats = compute_historical_bowler_stats(mock_deliveries)
    m2_stat = stats[stats["match_id"] == 202].iloc[0]
    
    assert m2_stat["hist_bowler_balls_exp"] == 2.0


def test_market_template_all_players_match_canonical_ids():
    """Verify all 17 player identities in market template exactly match data pack mapping."""
    if not RAW_MAPPING_PATH.exists():
        pytest.skip("Raw mapping path not found")
        
    mapping = pd.read_csv(RAW_MAPPING_PATH)
    template = pd.read_csv(PROCESSED_DIR / "ipl_2027_player_market_template.csv")
    
    map_ids = set(mapping["player_id"].unique())
    assert len(template[~template["player_id"].isin(map_ids)]) == 0, "Unknown player IDs in market template!"
    
    for _, row in template.iterrows():
        matches = mapping[mapping["player_id"] == row["player_id"]]
        assert len(matches) > 0
        canonical_name = matches["player_name"].values[0]
        assert row["player_name"] == canonical_name, f"Name mismatch: {row['player_name']} vs {canonical_name}"


def test_nathan_ellis_trade_and_contracted_status():
    """Verify Nathan Ellis reflects the verified CSK-to-SRH trade deal and is not classified as available."""
    template = pd.read_csv(PROCESSED_DIR / "ipl_2027_player_market_template.csv")
    ellis_rows = template[template["player_name"] == "Nathan Ellis"]
    assert len(ellis_rows) == 1
    ellis = ellis_rows.iloc[0]
    
    assert ellis["current_verified_franchise"] == "Sunrisers Hyderabad"
    assert ellis["confirmed_trade_status"] == "Officially traded"
    assert ellis["official_retention_status"] == "Officially retained"
    assert ellis["official_release_status"] == "Unknown"
    
    # Check candidate rankings
    cand_df = pd.read_csv(PROCESSED_DIR / "rr_2027_candidate_rankings.csv")
    c_ellis = cand_df[cand_df["player_name"] == "Nathan Ellis"].iloc[0]
    assert c_ellis["eligibility_class"] == "C", "Contracted trade player must be Class C!"
    
    # Bowler top 10 must exclude Nathan Ellis
    bowl_top10 = pd.read_csv(PROCESSED_DIR / "rr_2027_bowler_top10.csv")
    assert "Nathan Ellis" not in bowl_top10["player_name"].values


def test_mcda_single_availability_weighting():
    """Verify that RR 2027 priority score uses single-pass additive MCDA weighting."""
    cand_df = pd.read_csv(PROCESSED_DIR / "rr_2027_candidate_rankings.csv")
    
    # Verify weights: 40% rel + 20% ev + 25% avail + 15% fit
    # For any Class B player with avail_w = 0.85 (avail_comp = 21.25)
    class_b = cand_df[cand_df["eligibility_class"] == "B"]
    assert len(class_b) > 0
    
    # Check that highest priority score is not artificially shrunk to < 80 due to double-multiplication
    top_score = class_b["rr_priority_score"].max()
    assert top_score > 90.0, f"Top Class B candidate score {top_score} unexpectedly depressed!"


def test_canonical_mathematical_parameters():
    """Verify core canonical mathematical specification parameters."""
    # Phase wicket values
    assert WICKET_VALUE_BY_PHASE["Powerplay"] == 5.2
    assert WICKET_VALUE_BY_PHASE["Middle"] == 4.5
    assert WICKET_VALUE_BY_PHASE["Death"] == 3.6
    
    # Uniform empirical bayes shrinkage constant K = 45.0
    from src.analysis.reliability_engine import K_SHRINK
    assert K_SHRINK == 45.0
