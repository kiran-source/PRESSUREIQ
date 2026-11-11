"""Unit tests for final competition deliverables."""

import os
import hashlib
import subprocess
import pandas as pd
import pytest

try:
    import pymupdf as fitz
except ImportError:
    import fitz


def test_final_top10_csvs():
    """Verify final competition top 10 batters and bowlers CSVs."""
    fb_path = "data/processed/final_competition_batter_top10.csv"
    fw_path = "data/processed/final_competition_bowler_top10.csv"
    
    assert os.path.exists(fb_path), f"Missing {fb_path}"
    assert os.path.exists(fw_path), f"Missing {fw_path}"
    
    fb = pd.read_csv(fb_path)
    fw = pd.read_csv(fw_path)
    
    assert len(fb) == 10, f"Expected 10 batters, got {len(fb)}"
    assert len(fw) == 10, f"Expected 10 bowlers, got {len(fw)}"
    
    assert fb["player_name"].nunique() == 10, "Duplicate batters in top 10"
    assert fw["player_name"].nunique() == 10, "Duplicate bowlers in top 10"
    
    # Check key columns
    for col in ["rank", "player_name", "reliability_score", "strategic_category", "rr_strategic_utility"]:
        assert col in fb.columns, f"Missing column {col} in batters CSV"
        assert col in fw.columns, f"Missing column {col} in bowlers CSV"


def test_player_evidence_dossier():
    """Verify player evidence dossier contains 30 players with full analytical data."""
    dos_path = "data/processed/player_evidence_dossier.csv"
    assert os.path.exists(dos_path), f"Missing {dos_path}"
    
    dos = pd.read_csv(dos_path)
    assert len(dos) == 30, f"Expected 30 players (20 top + 10 near misses), got {len(dos)}"
    
    assert (dos["discipline"] == "Batting").sum() == 15
    assert (dos["discipline"] == "Bowling").sum() == 15
    
    req_cols = [
        "rank", "player_name", "discipline", "role", "selection_status",
        "reliability_score", "matches", "hp_balls", "prc_archetype",
        "boot_ci_lower_95", "boot_ci_upper_95", "top10_inclusion_prob"
    ]
    for c in req_cols:
        assert c in dos.columns, f"Missing column {c} in dossier"


def test_emerging_talent_watchlist():
    """Verify dedicated emerging talent watchlist."""
    em_path = "data/processed/emerging_talent_watchlist.csv"
    assert os.path.exists(em_path), f"Missing {em_path}"
    
    em = pd.read_csv(em_path)
    assert len(em) >= 10, f"Expected at least 10 emerging profiles, got {len(em)}"
    assert "Vaibhav Sooryavanshi" in em["player_name"].values
    assert "Vignesh Puthur" in em["player_name"].values
    assert "Prince Yadav" in em["player_name"].values


def test_final_methodology_pdf():
    """Verify final methodology report PDF exists and meets 12-16 page target."""
    pdf_path = "docs/PRESSUREIQ_FINAL_METHODOLOGY_REPORT.pdf"
    assert os.path.exists(pdf_path), f"Missing {pdf_path}"
    
    doc = fitz.open(pdf_path)
    page_count = len(doc)
    assert 12 <= page_count <= 16, f"Expected 12-16 pages, got {page_count}"
    assert page_count == 14, f"Expected exactly 14 pages, got {page_count}"


def test_frozen_baseline_integrity():
    """Verify original submission ZIP and Git HEAD remain completely frozen."""
    zip_path = "PRESSUREIQ_Final_Submission.zip"
    assert os.path.exists(zip_path), f"Missing {zip_path}"
    
    h = hashlib.sha256(open(zip_path, "rb").read()).hexdigest()
    assert h == "76059a8f5f8b8de5126a5ed8b2a9378fb6664016989f3125df7ca4bbbe9696db", "Frozen ZIP checksum mismatch!"
    
    master_head = subprocess.check_output(["git", "rev-parse", "master"]).decode("utf-8").strip()
    assert master_head == "fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2", "Frozen master Git HEAD modified!"

