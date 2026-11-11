"""Tests for Rajasthan Royals IPL 2027 Recommendation Framework and Eligibility Audit."""

from pathlib import Path
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = REPO_ROOT / "data" / "processed"


def test_files_exist():
    assert (PROCESSED_DIR / "player_eligibility_audit.csv").exists()
    assert (PROCESSED_DIR / "rr_2027_candidate_rankings.csv").exists()
    assert (PROCESSED_DIR / "rr_2027_batter_top10.csv").exists()
    assert (PROCESSED_DIR / "rr_2027_bowler_top10.csv").exists()


def test_no_duplicate_players_in_top10():
    bat_df = pd.read_csv(PROCESSED_DIR / "rr_2027_batter_top10.csv")
    bowl_df = pd.read_csv(PROCESSED_DIR / "rr_2027_bowler_top10.csv")
    
    assert len(bat_df) == 10
    assert len(bowl_df) == 10
    assert bat_df["player_name"].nunique() == 10
    assert bowl_df["player_name"].nunique() == 10


def test_pakistani_players_ineligible():
    audit_df = pd.read_csv(PROCESSED_DIR / "player_eligibility_audit.csv")
    cand_df = pd.read_csv(PROCESSED_DIR / "rr_2027_candidate_rankings.csv")
    
    pak_players = ["Fakhar Zaman", "Haris Rauf", "Abbas Afridi", "Sufiyan Muqeem", "Mohammad Rizwan"]
    for p in pak_players:
        sub = audit_df[audit_df["player_name"] == p]
        if len(sub) > 0:
            assert sub.iloc[0]["eligibility_class"] == "D"
            cand_sub = cand_df[cand_df["player_name"] == p]
            assert cand_sub.iloc[0]["rr_priority_score"] == 0.0


def test_franchise_retentions_properly_discounted():
    cand_df = pd.read_csv(PROCESSED_DIR / "rr_2027_candidate_rankings.csv")
    bat_top10 = pd.read_csv(PROCESSED_DIR / "rr_2027_batter_top10.csv")
    bowl_top10 = pd.read_csv(PROCESSED_DIR / "rr_2027_bowler_top10.csv")
    
    # Contracted stars like Gaikwad and Suryakumar should have heavily discounted RR priority score due to Class C (avail_w=0.20)
    # Under additive MCDA (40% Rel + 20% Ev + 25% Avail + 15% Fit), Class C caps availability points to 5/25, keeping scores < 78.0 (well below top targets ~88-94)
    for p in ["Ruturaj Gaikwad", "Suryakumar Yadav", "Rohit Sharma", "Nicholas Pooran"]:
        sub = cand_df[cand_df["player_name"] == p]
        if len(sub) > 0:
            assert sub.iloc[0]["eligibility_class"] == "C"
            assert sub.iloc[0]["rr_priority_score"] < 78.0
            # Ensure none appear in the actionable Top 10 RR recruitment targets
            assert p not in bat_top10["player_name"].values
            
    # Verify Nathan Ellis contracted via CSK-to-SRH trade (Class C) and excluded from RR Top 10 bowler targets
    sub_ellis = cand_df[cand_df["player_name"] == "Nathan Ellis"]
    assert len(sub_ellis) > 0
    assert sub_ellis.iloc[0]["eligibility_class"] == "C"
    assert sub_ellis.iloc[0]["rr_priority_score"] < 78.0
    assert "Nathan Ellis" not in bowl_top10["player_name"].values


def test_rr_role_fit_field_presence():
    bat_df = pd.read_csv(PROCESSED_DIR / "rr_2027_batter_top10.csv")
    bowl_df = pd.read_csv(PROCESSED_DIR / "rr_2027_bowler_top10.csv")
    
    assert "rr_role_need" in bat_df.columns
    assert "rr_role_need" in bowl_df.columns
    assert bat_df["rr_role_need"].notna().all()
    assert bowl_df["rr_role_need"].notna().all()

