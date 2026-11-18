"""
Phase 7: Model A Rankings & Integrity Verification Script.
Compares final_batter_rankings.csv and final_bowler_rankings.csv
against prompt specification and cryptographic hashes.
"""
import hashlib
from pathlib import Path
import pandas as pd

def sha256_file(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def verify_rankings():
    bat_path = Path("data/processed/final_batter_rankings.csv")
    bowl_path = Path("data/processed/final_bowler_rankings.csv")
    zip_path = Path("PRESSUREIQ_Final_Submission.zip")

    # Hashes
    assert bat_path.exists(), "Batter rankings CSV missing!"
    assert bowl_path.exists(), "Bowler rankings CSV missing!"
    assert zip_path.exists(), "Submission ZIP missing!"

    bat_hash = sha256_file(bat_path)
    bowl_hash = sha256_file(bowl_path)
    zip_hash = sha256_file(zip_path)

    expected_bat_hash = "887f0c104047eb7b5c7d662b83600bacaf6263fa7162fc343b27800760b99b87"
    expected_bowl_hash = "344d63c55cecc7bce9de3cd06d82b6ac8217fcd448bb3f2e93d55da314f1e7bb"
    expected_zip_hash = "76059a8f5f8b8de5126a5ed8b2a9378fb6664016989f3125df7ca4bbbe9696db"

    print("=== Cryptographic Hash Verification ===")
    print(f"Batter CSV: {bat_hash} [{'MATCH' if bat_hash == expected_bat_hash else 'FAIL'}]")
    print(f"Bowler CSV: {bowl_hash} [{'MATCH' if bowl_hash == expected_bowl_hash else 'FAIL'}]")
    print(f"ZIP Bundle: {zip_hash} [{'MATCH' if zip_hash == expected_zip_hash else 'FAIL'}]")

    assert bat_hash == expected_bat_hash, "Batter hash mismatch!"
    assert bowl_hash == expected_bowl_hash, "Bowler hash mismatch!"
    assert zip_hash == expected_zip_hash, "ZIP hash mismatch!"

    # Top 10 Batters
    bat_df = pd.read_csv(bat_path)
    expected_batters = [
        (1, "Ruturaj Gaikwad", 97.71),
        (2, "Rohit Sharma", 95.27),
        (3, "Fakhar Zaman", 95.25),
        (4, "Suryakumar Yadav", 94.68),
        (5, "Romario Shepherd", 93.69),
        (6, "Naman Dhir", 93.30),
        (7, "Phil Salt", 93.01),
        (8, "Jitesh Sharma", 92.79),
        (9, "Nicholas Pooran", 92.58),
        (10, "Jos Buttler", 92.45),
    ]

    print("\n=== Model A: Top 10 Batters Verification ===")
    all_bat_ok = True
    for rank, name, score in expected_batters:
        row = bat_df.iloc[rank - 1]
        actual_name = row["player_name"]
        actual_score = round(float(row["reliability_score"]), 2)
        match = (actual_name == name and abs(actual_score - score) < 0.05)
        status = "OK" if match else "MISMATCH"
        print(f"  Rank {rank:2d}: Expected {name} ({score:.2f}) | Actual: {actual_name} ({actual_score:.2f}) -> {status}")
        if not match:
            all_bat_ok = False

    # Top 10 Bowlers
    bowl_df = pd.read_csv(bowl_path)
    expected_bowlers = [
        (1, "Liam Dawson", 95.39),
        (2, "Haris Rauf", 92.36),
        (3, "Abbas Afridi", 91.88),
        (4, "Nathan Ellis", 91.84),
        (5, "Sufiyan Muqeem", 91.41),
        (6, "Matheesha Pathirana", 91.11),
        (7, "Nasum Ahmed", 90.77),
        (8, "Ishant Sharma", 90.42),
        (9, "Shoriful Islam", 90.36),
        (10, "Tim Southee", 89.16),
    ]

    print("\n=== Model A: Top 10 Bowlers Verification ===")
    all_bowl_ok = True
    for rank, name, score in expected_bowlers:
        row = bowl_df.iloc[rank - 1]
        actual_name = row["player_name"]
        actual_score = round(float(row["reliability_score"]), 2)
        match = (actual_name == name and abs(actual_score - score) < 0.05)
        status = "OK" if match else "MISMATCH"
        print(f"  Rank {rank:2d}: Expected {name} ({score:.2f}) | Actual: {actual_name} ({actual_score:.2f}) -> {status}")
        if not match:
            all_bowl_ok = False

    return all_bat_ok and all_bowl_ok

if __name__ == "__main__":
    ok = verify_rankings()
    print(f"\nModel A Rankings Verification: {'ALL PASSED' if ok else 'FAILED'}")
