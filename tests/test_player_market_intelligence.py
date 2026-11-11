"""Unit tests for player-market intelligence module and retention update workflow."""

import os
import hashlib
import subprocess
import pandas as pd
import pytest

from scripts.import_market_retentions import (
    validate_and_import,
    VALID_FRANCHISES,
    VALID_STATUSES,
    REQUIRED_COLUMNS
)

TEMPLATE_PATH = "data/processed/ipl_2027_player_market_template.csv"
LOG_PATH = "data/processed/ipl_2027_market_change_log.csv"
BATTER_PATH = "data/processed/final_batter_rankings.csv"
BOWLER_PATH = "data/processed/final_bowler_rankings.csv"


def test_market_template_schema_and_integrity():
    """Verify market template exists, matches required columns, and has valid statuses."""
    assert os.path.exists(TEMPLATE_PATH), f"Missing {TEMPLATE_PATH}"
    df = pd.read_csv(TEMPLATE_PATH).fillna("None")
    
    # 1. Required columns
    for col in REQUIRED_COLUMNS:
        assert col in df.columns, f"Missing required column: {col}"
        
    # 2. No duplicate player IDs
    assert df["player_id"].nunique() == len(df), "Duplicate player_id detected in market template!"
    
    # 3. Status validation
    for s in df["official_retention_status"]:
        assert s in VALID_STATUSES, f"Invalid status: {s}"
        
    # 4. Franchise validation
    for f in df["current_verified_franchise"]:
        assert f in VALID_FRANCHISES, f"Invalid franchise: {f}"


def test_market_change_log_structure():
    """Verify change log exists and contains valid audit trail events."""
    assert os.path.exists(LOG_PATH), f"Missing {LOG_PATH}"
    df_log = pd.read_csv(LOG_PATH)
    
    req_cols = ["timestamp", "player_id", "player_name", "event_type", "previous_status", "new_status", "verified_by", "source_url"]
    for col in req_cols:
        assert col in df_log.columns, f"Missing column in change log: {col}"
        
    assert len(df_log) >= 4, f"Expected at least 4 change log records, got {len(df_log)}"


def test_duplicate_detection_rejects_invalid_csv(tmp_path):
    """Verify that import workflow raises ValueError when duplicate player IDs exist."""
    bad_data = [
        {
            "player_id": 6059, "player_name": "Ruturaj Gaikwad", "previous_franchise": "CSK",
            "current_verified_franchise": "CSK", "official_retention_status": "Officially retained",
            "official_release_status": "Unknown", "confirmed_trade_status": "Unknown",
            "rumour_status": "None", "source_url": "https://example.com", "source_publication_date": "2024-10-31",
            "verification_timestamp": "2026-11-15 12:00:00", "confidence_classification": "Officially confirmed",
            "conflicting_evidence": "None", "last_updated": "2026-11-15"
        },
        {
            "player_id": 6059, "player_name": "Ruturaj Gaikwad (Duplicate)", "previous_franchise": "CSK",
            "current_verified_franchise": "CSK", "official_retention_status": "Officially retained",
            "official_release_status": "Unknown", "confirmed_trade_status": "Unknown",
            "rumour_status": "None", "source_url": "https://example.com", "source_publication_date": "2024-10-31",
            "verification_timestamp": "2026-11-15 12:00:00", "confidence_classification": "Officially confirmed",
            "conflicting_evidence": "None", "last_updated": "2026-11-15"
        }
    ]
    bad_csv = tmp_path / "duplicate_test.csv"
    pd.DataFrame(bad_data).to_csv(bad_csv, index=False)
    
    with pytest.raises(ValueError, match="Duplicate player_ids detected"):
        validate_and_import(str(bad_csv), apply_update=False)


def test_invalid_status_rejects_import(tmp_path):
    """Verify that import workflow raises ValueError on invalid status enumeration."""
    bad_data = [
        {
            "player_id": 99999, "player_name": "Test Player", "previous_franchise": "RR",
            "current_verified_franchise": "RR", "official_retention_status": "InvalidStatusXYZ",
            "official_release_status": "Unknown", "confirmed_trade_status": "Unknown",
            "rumour_status": "None", "source_url": "https://example.com", "source_publication_date": "2024-10-31",
            "verification_timestamp": "2026-11-15 12:00:00", "confidence_classification": "Officially confirmed",
            "conflicting_evidence": "None", "last_updated": "2026-11-15"
        }
    ]
    bad_csv = tmp_path / "bad_status.csv"
    pd.DataFrame(bad_data).to_csv(bad_csv, index=False)
    
    with pytest.raises(ValueError, match="Status validation error"):
        validate_and_import(str(bad_csv), apply_update=False)


def test_non_interference_rumours_do_not_change_model_a():
    """Verify that market data updates never alter Model A statistical scores or rankings."""
    fb = pd.read_csv(BATTER_PATH)
    fw = pd.read_csv(BOWLER_PATH)
    
    # Batter #1 must be Ruturaj Gaikwad with 97.71
    assert fb.iloc[0]["player_name"] == "Ruturaj Gaikwad"
    assert round(fb.iloc[0]["reliability_score"], 2) == 97.71
    
    # Bowler #1 must be Liam Dawson with 95.39
    assert fw.iloc[0]["player_name"] == "Liam Dawson"
    assert round(fw.iloc[0]["reliability_score"], 2) == 95.39


def test_frozen_baseline_artifacts_unmodified():
    """Verify original submission ZIP checksum and Git HEAD commit are 100% frozen."""
    zip_path = "PRESSUREIQ_Final_Submission.zip"
    h = hashlib.sha256(open(zip_path, "rb").read()).hexdigest()
    assert h == "76059a8f5f8b8de5126a5ed8b2a9378fb6664016989f3125df7ca4bbbe9696db"
    
    git_head = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
    assert git_head == "fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2"

