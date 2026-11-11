"""Tests for Chronological Out-of-Fold expected outcome predictions (P0-2)."""

import numpy as np
import pandas as pd
import pytest
from src.models.expected_outcomes import ExpectedOutcomeEngine, expected_calibration_error


def test_expected_calibration_error():
    y_true = np.array([0, 0, 1, 1])
    y_prob = np.array([0.1, 0.2, 0.8, 0.9])
    ece = expected_calibration_error(y_true, y_prob, n_bins=5)
    assert 0.0 <= ece <= 1.0


def test_oof_predictions_chronology_and_provenance():
    """Verify OOF predictions contain proper provenance and do not leak future matches."""
    # Create synthetic dataset across 3 years (2022, 2023, 2024)
    rows = []
    match_id = 1
    for year in [2022, 2023, 2024]:
        for m in range(5):
            m_id = match_id
            match_id += 1
            for b in range(10):
                rows.append({
                    "match_id": m_id,
                    "match_date": f"{year}-04-{10+m:02d}",
                    "innings": 1,
                    "legal_balls_before": b,
                    "balls_remaining_before": 120 - b,
                    "wickets_remaining_before": 10,
                    "current_score_before": b,
                    "crr_before": 6.0,
                    "current_run_rate_before": 6.0,
                    "rrr_before": 0.0,
                    "target_runs": 0,
                    "bpi": 40.0,
                    "bopi": 45.0,
                    "is_powerplay": 1,
                    "is_death_overs": 0,
                    "is_knockout_stage": 0,
                    "hist_batter_sr": 130.0,
                    "hist_batter_avg": 28.0,
                    "hist_batter_dot_pct": 35.0,
                    "hist_batter_bnd_pct": 18.0,
                    "hist_bowler_economy": 7.8,
                    "hist_bowler_strike_rate": 18.0,
                    "hist_bowler_dot_pct": 40.0,
                    "batting_type": "RHB",
                    "pace_or_spin": "Pace",
                    "bowling_type": "Fast",
                    "batting_role": "Top_Order",
                    "batter_runs": 1,
                    "is_striker_out": 0,
                    "is_boundary": 0,
                    "bowler_runs_conceded": 1,
                    "is_bowler_wicket": 0,
                    "is_batter_ball": True,
                    "is_legal_ball": True
                })
    df = pd.DataFrame(rows)
    
    engine = ExpectedOutcomeEngine()
    oof = engine.generate_chronological_oof_predictions(df)
    
    # Assert output shape and required provenance columns
    assert len(oof) == len(df)
    assert "pred_provenance" in oof.columns
    assert "pred_model_cutoff" in oof.columns
    assert not oof["exp_batter_runs"].isna().any()
    assert not oof["prob_dismissal"].isna().any()
    
    # Check 2022 used GroupKFold
    mask_2022 = df["match_date"].str.startswith("2022")
    assert oof.loc[mask_2022, "pred_provenance"].str.contains("GroupKFold").all()
    assert (oof.loc[mask_2022, "pred_model_cutoff"] == "2022-GroupKFold").all()
    
    # Check 2023 used walk-forward with cutoff 2022-12-31
    mask_2023 = df["match_date"].str.startswith("2023")
    assert (oof.loc[mask_2023, "pred_model_cutoff"] == "2022-12-31").all()
    assert (oof.loc[mask_2023, "pred_provenance"] == "walk_forward_2023").all()
    
    # Check 2024 used walk-forward with cutoff 2023-12-31
    mask_2024 = df["match_date"].str.startswith("2024")
    assert (oof.loc[mask_2024, "pred_model_cutoff"] == "2023-12-31").all()
    assert (oof.loc[mask_2024, "pred_provenance"] == "walk_forward_2024").all()


def test_future_category_isolation_and_completeness():
    """Verify unseen future categories in test year do not leak into historical training."""
    rows = []
    # 2022: known categories
    for m in range(5):
        for b in range(6):
            rows.append({
                "match_id": m + 1,
                "match_date": f"2022-04-{10+m:02d}",
                "innings": 1,
                "legal_balls_before": b,
                "balls_remaining_before": 120 - b,
                "wickets_remaining_before": 10,
                "current_score_before": b,
                "crr_before": 6.0,
                "current_run_rate_before": 6.0,
                "rrr_before": 0.0,
                "target_runs": 0,
                "bpi": 40.0,
                "bopi": 45.0,
                "is_powerplay": 1,
                "is_death_overs": 0,
                "is_knockout_stage": 0,
                "hist_batter_sr": 130.0,
                "hist_batter_avg": 28.0,
                "hist_batter_dot_pct": 35.0,
                "hist_batter_bnd_pct": 18.0,
                "hist_bowler_economy": 7.8,
                "hist_bowler_strike_rate": 18.0,
                "hist_bowler_dot_pct": 40.0,
                "batting_type": "RHB",
                "pace_or_spin": "Pace",
                "bowling_type": "Fast",
                "batting_role": "Top_Order",
                "batter_runs": 1,
                "is_striker_out": 0,
                "is_boundary": 0,
                "bowler_runs_conceded": 1,
                "is_bowler_wicket": 0,
                "is_batter_ball": True,
                "is_legal_ball": True
            })
            
    # 2023: brand new future unseen categories!
    for b in range(6):
        rows.append({
            "match_id": 99,
            "match_date": "2023-04-10",
            "innings": 1,
            "legal_balls_before": b,
            "balls_remaining_before": 120 - b,
            "wickets_remaining_before": 10,
            "current_score_before": b,
            "crr_before": 6.0,
            "current_run_rate_before": 6.0,
            "rrr_before": 0.0,
            "target_runs": 0,
            "bpi": 40.0,
            "bopi": 45.0,
            "is_powerplay": 1,
            "is_death_overs": 0,
            "is_knockout_stage": 0,
            "hist_batter_sr": 130.0,
            "hist_batter_avg": 28.0,
            "hist_batter_dot_pct": 35.0,
            "hist_batter_bnd_pct": 18.0,
            "hist_bowler_economy": 7.8,
            "hist_bowler_strike_rate": 18.0,
            "hist_bowler_dot_pct": 40.0,
            # UNSEEN FUTURE CATEGORIES:
            "batting_type": "BrandNewFutureGrip",
            "pace_or_spin": "FutureHybrid",
            "bowling_type": "MysteryCarrom",
            "batting_role": "PinchHitter2023",
            "batter_runs": 2,
            "is_striker_out": 0,
            "is_boundary": 0,
            "bowler_runs_conceded": 2,
            "is_bowler_wicket": 0,
            "is_batter_ball": True,
            "is_legal_ball": True
        })
        
    df = pd.DataFrame(rows)
    engine = ExpectedOutcomeEngine()
    oof = engine.generate_chronological_oof_predictions(df)
    
    # 1. Assert completeness: all 5 columns have zero missing values
    pred_cols = ["exp_batter_runs", "prob_dismissal", "prob_boundary", "exp_bowler_runs", "prob_bowler_wicket"]
    for c in pred_cols:
        assert not oof[c].isna().any(), f"Prediction column {c} has NaN!"
        
    # 2. Check that future unseen rows executed cleanly without error
    mask_2023 = df["match_date"].str.startswith("2023")
    assert len(oof[mask_2023]) == 6
    assert (oof.loc[mask_2023, "pred_provenance"] == "walk_forward_2023").all()
