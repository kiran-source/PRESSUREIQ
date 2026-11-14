"""Unit tests for Model B RR IPL 2027 Recruitment Intelligence."""

import hashlib
from pathlib import Path
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = REPO_ROOT / "data" / "processed"

FROZEN_BATTER_SHA256 = "887f0c104047eb7b5c7d662b83600bacaf6263fa7162fc343b27800760b99b87"
FROZEN_BOWLER_SHA256 = "344d63c55cecc7bce9de3cd06d82b6ac8217fcd448bb3f2e93d55da314f1e7bb"


def test_model_b_deliverable_files_exist():
    """Verify all 7 Model B CSV deliverables exist in data/processed/."""
    expected_files = [
        "rr_model_b_candidates.csv",
        "rr_model_b_eligible.csv",
        "rr_model_b_targetable.csv",
        "rr_model_b_target_batters.csv",
        "rr_model_b_target_bowlers.csv",
        "rr_model_b_watchlist.csv",
        "rr_model_b_exclusions.csv",
        "RR_IPL_2027_RECRUITMENT_INTELLIGENCE.pdf",
    ]
    for fname in expected_files:
        fpath = PROCESSED_DIR / fname
        assert fpath.exists(), f"Missing required Model B deliverable: {fname}"


def test_model_a_hashes_remain_strictly_frozen():
    """Guarantee Model B pipeline has caused 0.00 drift in Model A frozen baseline hashes."""
    bat_path = PROCESSED_DIR / "final_batter_rankings.csv"
    bowl_path = PROCESSED_DIR / "final_bowler_rankings.csv"

    bat_hash = hashlib.sha256(bat_path.read_bytes()).hexdigest()
    bowl_hash = hashlib.sha256(bowl_path.read_bytes()).hexdigest()

    assert bat_hash == FROZEN_BATTER_SHA256, "Model A Batters hash modified!"
    assert bowl_hash == FROZEN_BOWLER_SHA256, "Model A Bowlers hash modified!"


def test_traded_and_contracted_stars_excluded_from_target_rankings():
    """Ensure rival-retained and confirmed-traded players are strictly barred from target lists."""
    targetable_df = pd.read_csv(PROCESSED_DIR / "rr_model_b_targetable.csv")
    target_bat = pd.read_csv(PROCESSED_DIR / "rr_model_b_target_batters.csv")
    target_bowl = pd.read_csv(PROCESSED_DIR / "rr_model_b_target_bowlers.csv")
    exclusions_df = pd.read_csv(PROCESSED_DIR / "rr_model_b_exclusions.csv")

    rival_stars = [
        "Ruturaj Gaikwad", "Rohit Sharma", "Suryakumar Yadav", "Jasprit Bumrah",
        "Nicholas Pooran", "Heinrich Klaasen", "Hardik Pandya", "Arshdeep Singh",
        "Rishabh Pant", "Kuldeep Yadav", "Nathan Ellis", "Khaleel Ahmed", "Liam Livingstone"
    ]

    for star in rival_stars:
        assert star not in targetable_df["player_name"].values, f"{star} illegally present in targetable pool!"
        assert star not in target_bat["player_name"].values, f"{star} illegally present in target batters!"
        assert star not in target_bowl["player_name"].values, f"{star} illegally present in target bowlers!"
        assert star in exclusions_df["player_name"].values, f"{star} missing from exclusions ledger!"


def test_policy_restricted_pakistani_players_zero_score():
    """Verify Pakistani passport holders have Policy Review status and zero recruitment score."""
    cand_df = pd.read_csv(PROCESSED_DIR / "rr_model_b_candidates.csv")
    exclusions_df = pd.read_csv(PROCESSED_DIR / "rr_model_b_exclusions.csv")

    pak_stars = ["Fakhar Zaman", "Haris Rauf", "Abbas Afridi", "Sufiyan Muqeem", "Mohammad Rizwan"]
    for star in pak_stars:
        sub = cand_df[cand_df["player_name"] == star]
        if len(sub) > 0:
            assert sub.iloc[0]["eligibility_status"] == "Policy Review"
            assert sub.iloc[0]["eligibility_class"] == "D"
            assert sub.iloc[0]["model_b_target_score"] == 0.0
            assert star in exclusions_df["player_name"].values


def test_targetable_bowlers_lead_with_liam_dawson():
    """Verify Liam Dawson is the #1 target bowler addressing the SMS Jaipur spin squeeze."""
    target_bowl = pd.read_csv(PROCESSED_DIR / "rr_model_b_target_bowlers.csv")
    assert not target_bowl.empty
    assert target_bowl.iloc[0]["player_name"] == "Liam Dawson"
    assert "Jaipur" in target_bowl.iloc[0]["addressed_gap"]
    assert target_bowl.iloc[0]["model_b_target_score"] > 90.0
    assert target_bowl.iloc[0]["is_targetable"] is True or target_bowl.iloc[0]["is_targetable"] == 1


def test_death_seam_targets_present():
    """Verify Spencer Johnson and Fazalhaq Farooqi are qualified death pace targets."""
    target_bowl = pd.read_csv(PROCESSED_DIR / "rr_model_b_target_bowlers.csv")
    bowler_names = target_bowl["player_name"].values
    assert "Spencer Johnson" in bowler_names
    assert "FazalHaq Farooqi" in bowler_names


def test_target_batters_contain_no7_finishers():
    """Verify Jamie Smith and Ashutosh Sharma appear in top target batters addressing No. 7 deficit."""
    target_bat = pd.read_csv(PROCESSED_DIR / "rr_model_b_target_batters.csv")
    batter_names = target_bat["player_name"].values
    assert "Jamie Smith" in batter_names or "Ashutosh Sharma" in batter_names
    for _, r in target_bat.iterrows():
        assert pd.notna(r["addressed_gap"])
        assert r["model_b_target_score"] > 50.0


def test_remediated_nationalities_are_correctly_classified_as_overseas():
    """Verify that the 5 remediated defect players are accurately mapped to their true home nations and overseas status."""
    from src.recruitment.eligibility import resolve_player_nationality
    
    expected_remediations = {
        "Sikandar Raza": ("Zimbabwe", True),
        "Sherfane Rutherford": ("West Indies", True),
        "Moeen Ali": ("England", True),
        "Dasun Shanaka": ("Sri Lanka", True),
        "Glenn Phillips": ("New Zealand", True),
    }

    # 1. Unit check against resolve_player_nationality
    for name, (exp_nat, exp_ov) in expected_remediations.items():
        nat, is_ov = resolve_player_nationality(player_name=name)
        assert nat == exp_nat, f"{name} nationality expected {exp_nat}, got {nat}"
        assert is_ov is exp_ov, f"{name} is_overseas expected {exp_ov}, got {is_ov}"

    # 2. Check in regenerated CSV deliverables
    cand_df = pd.read_csv(PROCESSED_DIR / "rr_model_b_candidates.csv")
    for name, (exp_nat, exp_ov) in expected_remediations.items():
        sub = cand_df[cand_df["player_name"] == name]
        assert not sub.empty, f"{name} missing from candidates CSV!"
        for _, row in sub.iterrows():
            assert row["nationality"] == exp_nat, f"{name} in CSV has nationality {row['nationality']} instead of {exp_nat}"
            assert bool(row["is_overseas"]) is exp_ov, f"{name} in CSV has is_overseas {row['is_overseas']} instead of {exp_ov}"


def test_unknown_nationality_handling_never_defaults_to_domestic_india():
    """Verify that unverified player names NEVER default to India or is_overseas=False."""
    from src.recruitment.eligibility import resolve_player_nationality

    nat, is_ov = resolve_player_nationality(player_name="Completely Unknown Mystery Entrant 2027")
    assert nat == "Unknown / Requires Verification"
    assert is_ov is None
    assert is_ov is not False


def test_overseas_flag_strictly_equals_nationality_not_india():
    """Verify mathematical consistency: is_overseas == (nationality != 'India') across all candidates."""
    cand_df = pd.read_csv(PROCESSED_DIR / "rr_model_b_candidates.csv")
    assert (cand_df["nationality"] == "Unknown / Requires Verification").sum() == 0, "Found unverified nationality in candidate pool!"

    mismatches = cand_df[(cand_df["nationality"] != "India") != (cand_df["is_overseas"] == True)]
    assert len(mismatches) == 0, f"Found overseas flag mismatches: {mismatches[['player_name', 'nationality', 'is_overseas']]}"


def test_canonical_availability_vocabulary():
    """Verify all candidate availability statuses strictly follow the canonical 6-status vocabulary."""
    cand_df = pd.read_csv(PROCESSED_DIR / "rr_model_b_candidates.csv")
    canonical_statuses = {
        "Confirmed Retained",
        "Confirmed Released",
        "Confirmed Trade",
        "Pending Verification",
        "Rumour",
        "Policy/Eligibility Review"
    }

    observed_statuses = set(cand_df["auction_availability"].unique())
    invalid_statuses = observed_statuses - canonical_statuses
    assert len(invalid_statuses) == 0, f"Found non-canonical availability statuses: {invalid_statuses}"


def test_target_boards_consistency_and_dual_qualified_allrounders():
    """Verify dual-qualified all-rounders appear in both batting and bowling target boards without corruption."""
    target_bat = pd.read_csv(PROCESSED_DIR / "rr_model_b_target_batters.csv")
    target_bowl = pd.read_csv(PROCESSED_DIR / "rr_model_b_target_bowlers.csv")

    dual_allrounders = ["Sikandar Raza", "Moeen Ali", "Dasun Shanaka", "Jason Holder", "Mohammad Nabi"]
    for p in dual_allrounders:
        assert p in target_bat["player_name"].values, f"Dual all-rounder {p} missing from target batters!"
        assert p in target_bowl["player_name"].values, f"Dual all-rounder {p} missing from target bowlers!"

    # Ensure all targets are eligible
    assert (target_bat["eligibility_status"] == "Eligible").all()
    assert (target_bowl["eligibility_status"] == "Eligible").all()
    assert (target_bat["is_targetable"] == True).all()
    assert (target_bowl["is_targetable"] == True).all()

