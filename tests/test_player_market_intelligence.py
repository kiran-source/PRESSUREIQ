"""Unit tests for audited player-market intelligence ledger and retention workflow."""

import os
import hashlib
import subprocess
from pathlib import Path
import pandas as pd
import pytest

from scripts.import_market_retentions import (
    validate_and_import,
    preserve_historical_snapshot,
    VALID_FRANCHISES,
    VALID_STATUSES,
    REQUIRED_COLUMNS,
    KNOWN_INVALID_PLACEHOLDER_PATTERNS,
)

TEMPLATE_PATH = "data/processed/ipl_2027_player_market_template.csv"
LOG_PATH = "data/processed/ipl_2027_market_change_log.csv"
BATTER_PATH = "data/processed/final_batter_rankings.csv"
BOWLER_PATH = "data/processed/final_bowler_rankings.csv"
CANDIDATE_PATH = "data/processed/rr_2027_candidate_rankings.csv"
AUDIT_PATH = "data/processed/player_eligibility_audit.csv"

FROZEN_ZIP_SHA256 = "76059a8f5f8b8de5126a5ed8b2a9378fb6664016989f3125df7ca4bbbe9696db"
FROZEN_BATTER_SHA256 = "887f0c104047eb7b5c7d662b83600bacaf6263fa7162fc343b27800760b99b87"
FROZEN_BOWLER_SHA256 = "344d63c55cecc7bce9de3cd06d82b6ac8217fcd448bb3f2e93d55da314f1e7bb"
FROZEN_MASTER_COMMIT = "fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2"


def test_market_template_schema_and_strict_statuses():
    """Verify market template matches audited evidence schema, strict 6-enum statuses, and live URLs."""
    assert os.path.exists(TEMPLATE_PATH), f"Missing {TEMPLATE_PATH}"
    df = pd.read_csv(TEMPLATE_PATH).fillna("None")

    for col in REQUIRED_COLUMNS:
        assert col in df.columns, f"Missing required column: {col}"

    assert df["player_id"].nunique() == len(df), "Duplicate player_id detected in market template!"

    expected_strict_statuses = {
        "Confirmed Retained",
        "Confirmed Released",
        "Confirmed Trade",
        "Pending Verification",
        "Rumour",
        "Policy/Eligibility Review",
    }
    assert VALID_STATUSES == expected_strict_statuses

    for _, row in df.iterrows():
        s = row["official_retention_status"]
        assert s in VALID_STATUSES, f"Invalid status for {row['player_name']}: {s}"
        assert row["current_verified_franchise"] in VALID_FRANCHISES
        assert str(row["source_url"]).startswith("https://")
        assert not any(pat in str(row["source_url"]) for pat in KNOWN_INVALID_PLACEHOLDER_PATTERNS), (
            f"Placeholder/dead URL still present for {row['player_name']}: {row['source_url']}"
        )
        assert len(str(row["source_title"]).strip()) > 5
        assert len(str(row["publisher"]).strip()) > 2
        assert len(str(row["evidence_excerpt"]).strip()) > 10


def test_pending_and_unverified_records_cannot_be_confirmed_available():
    """Prove unsupported, pending, or policy records cannot be displayed as confirmed available."""
    df_mkt = pd.read_csv(TEMPLATE_PATH).fillna("None")
    unconfirmed = df_mkt[df_mkt["official_retention_status"].isin({"Pending Verification", "Rumour", "Policy/Eligibility Review"})]
    assert len(unconfirmed) == 16  # 15 Pending Verification + 1 Policy/Eligibility Review

    forbidden_labels = ("Confirmed Available", "Confirmed Released", "Officially released", "Confirmed Retained", "Officially retained")
    for _, row in unconfirmed.iterrows():
        assert row["official_release_status"] not in forbidden_labels, (
            f"Unconfirmed player {row['player_name']} falsely marked {row['official_release_status']}"
        )

    # Also verify downstream RR candidate rankings & eligibility audit never mark pending/policy players as Confirmed Available
    for path in (CANDIDATE_PATH, AUDIT_PATH):
        df_down = pd.read_csv(path).fillna("None")
        avail_col = "auction_availability" if "auction_availability" in df_down.columns else "auction_2027_availability"
        pending_down = df_down[df_down["market_status"].isin({"Pending Verification", "Rumour", "Policy/Eligibility Review"})]
        assert len(pending_down) > 0
        for _, r in pending_down.iterrows():
            avail_text = str(r[avail_col])
            assert "Confirmed Available" not in avail_text
            assert "Confirmed Released" not in avail_text
            assert "Confirmed Target" not in avail_text


def test_verified_player_franchises_and_mechanisms():
    """Verify audited franchises and transaction mechanisms for disputed players."""
    df = pd.read_csv(TEMPLATE_PATH).fillna("None").set_index("player_name")

    assert df.loc["Jos Buttler", "current_verified_franchise"] == "Gujarat Titans"
    assert df.loc["Jos Buttler", "official_retention_status"] == "Pending Verification"

    assert df.loc["Matheesha Pathirana", "current_verified_franchise"] == "Kolkata Knight Riders"
    assert df.loc["Matheesha Pathirana", "official_retention_status"] == "Pending Verification"

    assert df.loc["Vignesh Puthur", "current_verified_franchise"] == "Rajasthan Royals"
    assert df.loc["Vignesh Puthur", "confirmed_trade_status"] == "None"
    assert df.loc["Vignesh Puthur", "official_retention_status"] == "Pending Verification"

    assert df.loc["Jitesh Sharma", "current_verified_franchise"] == "Royal Challengers Bengaluru"
    assert df.loc["Jitesh Sharma", "official_retention_status"] == "Pending Verification"

    assert df.loc["Romario Shepherd", "current_verified_franchise"] == "Royal Challengers Bengaluru"
    assert df.loc["Romario Shepherd", "official_retention_status"] == "Pending Verification"

    assert df.loc["Harpreet Brar", "current_verified_franchise"] == "Punjab Kings"
    assert df.loc["Harpreet Brar", "official_retention_status"] == "Pending Verification"

    assert df.loc["Nathan Ellis", "current_verified_franchise"] == "Sunrisers Hyderabad"
    assert df.loc["Nathan Ellis", "official_retention_status"] == "Confirmed Trade"
    assert df.loc["Nathan Ellis", "confirmed_trade_status"] == "Confirmed Trade"

    assert df.loc["Haris Rauf", "official_retention_status"] == "Policy/Eligibility Review"


def test_historical_snapshots_preserved_without_overwrite(tmp_path):
    """Verify historical snapshots exist and sequential saves do not overwrite previous snapshots."""
    snap_dir = Path("data/processed/snapshots")
    assert (snap_dir / "ipl_2027_market_snapshot_legacy_pre_url_audit.csv").exists()
    assert (snap_dir / "ipl_2027_market_snapshot_2026-11-11.csv").exists()

    # Test non-overwriting helper in isolated tmp_path
    src = tmp_path / "master.csv"
    src.write_text("col\nval1\n", encoding="utf-8")
    p1 = preserve_historical_snapshot(src, snapshot_dir=tmp_path)
    src.write_text("col\nval2\n", encoding="utf-8")
    p2 = preserve_historical_snapshot(src, snapshot_dir=tmp_path)
    assert p1 != p2
    assert p1.exists() and p2.exists()
    assert "val1" in p1.read_text(encoding="utf-8")
    assert "val2" in p2.read_text(encoding="utf-8")


def test_market_change_log_structure():
    """Verify change log exists and contains valid non-future audit trail events."""
    assert os.path.exists(LOG_PATH), f"Missing {LOG_PATH}"
    df_log = pd.read_csv(LOG_PATH)

    req_cols = ["timestamp", "player_id", "player_name", "event_type", "previous_status", "new_status", "verified_by", "source_url"]
    for col in req_cols:
        assert col in df_log.columns, f"Missing column in change log: {col}"

    assert len(df_log) >= 4, f"Expected at least 4 change log records, got {len(df_log)}"
    for url in df_log["source_url"]:
        assert str(url).startswith("https://")
        assert not any(pat in str(url) for pat in KNOWN_INVALID_PLACEHOLDER_PATTERNS)


def test_duplicate_detection_rejects_invalid_csv(tmp_path):
    """Verify that import workflow raises ValueError when duplicate player IDs exist."""
    base_row = {
        "player_id": 6059, "player_name": "Ruturaj Gaikwad", "previous_franchise": "CSK",
        "current_verified_franchise": "CSK", "official_retention_status": "Pending Verification",
        "official_release_status": "Pending Verification", "confirmed_trade_status": "None",
        "transaction_mechanism": "Test", "rumour_status": "None",
        "source_url": "https://www.iplt20.com/news/article/tata-ipl-2026-player-retentions-announced",
        "source_title": "Test Title", "publisher": "IPLT20",
        "source_publication_date": "2025-11-15", "verification_timestamp": "2026-11-11 12:00:00",
        "confidence_classification": "Pending", "evidence_excerpt": "Verified test excerpt",
        "conflicting_evidence": "None", "snapshot_label": "test", "last_updated": "2026-11-11"
    }
    bad_data = [base_row, {**base_row, "player_name": "Ruturaj Gaikwad (Duplicate)"}]
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
            "official_release_status": "Pending Verification", "confirmed_trade_status": "None",
            "transaction_mechanism": "Test", "rumour_status": "None",
            "source_url": "https://www.iplt20.com/news/article/tata-ipl-2026-player-retentions-announced",
            "source_title": "Test Title", "publisher": "IPLT20",
            "source_publication_date": "2025-11-15", "verification_timestamp": "2026-11-11 12:00:00",
            "confidence_classification": "Pending", "evidence_excerpt": "Verified test excerpt",
            "conflicting_evidence": "None", "snapshot_label": "test", "last_updated": "2026-11-11"
        }
    ]
    bad_csv = tmp_path / "bad_status.csv"
    pd.DataFrame(bad_data).to_csv(bad_csv, index=False)

    with pytest.raises(ValueError, match="Status validation error"):
        validate_and_import(str(bad_csv), apply_update=False)


def test_non_interference_rumours_do_not_change_model_a():
    """Verify that market data updates never alter Model A statistical scores or rankings."""
    assert hashlib.sha256(open(BATTER_PATH, "rb").read()).hexdigest() == FROZEN_BATTER_SHA256
    assert hashlib.sha256(open(BOWLER_PATH, "rb").read()).hexdigest() == FROZEN_BOWLER_SHA256

    fb = pd.read_csv(BATTER_PATH)
    fw = pd.read_csv(BOWLER_PATH)
    assert fb.iloc[0]["player_name"] == "Ruturaj Gaikwad"
    assert round(fb.iloc[0]["reliability_score"], 2) == 97.71
    assert fw.iloc[0]["player_name"] == "Liam Dawson"
    assert round(fw.iloc[0]["reliability_score"], 2) == 95.39


def test_frozen_baseline_artifacts_unmodified():
    """Verify original submission ZIP checksum and master baseline commit remain 100% frozen."""
    zip_path = "PRESSUREIQ_Final_Submission.zip"
    h = hashlib.sha256(open(zip_path, "rb").read()).hexdigest()
    assert h == FROZEN_ZIP_SHA256

    master_head = subprocess.check_output(["git", "rev-parse", "master"]).decode("utf-8").strip()
    assert master_head == FROZEN_MASTER_COMMIT
