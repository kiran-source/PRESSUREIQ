"""Submission packaging, verification, and Unstop dropdown exporter script."""

import sys
from pathlib import Path
import pandas as pd

# Paths
REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
DOCS_DIR = REPO_ROOT / "docs"

BATTER_CSV = PROCESSED_DIR / "final_batter_rankings.csv"
BOWLER_CSV = PROCESSED_DIR / "final_bowler_rankings.csv"

REQUIRED_DATA_FILES = [
    PROCESSED_DIR / "matches.parquet",
    PROCESSED_DIR / "deliveries.parquet",
    PROCESSED_DIR / "features_deliveries.parquet",
    PROCESSED_DIR / "deliveries_with_pava.parquet",
    BATTER_CSV,
    BOWLER_CSV,
]

REQUIRED_DOC_FILES = [
    REPO_ROOT / "README.md",
    DOCS_DIR / "METHODOLOGY_REPORT.md",
    DOCS_DIR / "PLAYER_DECISION_DOSSIERS.md",
    DOCS_DIR / "DATA_INVENTORY_AND_FEASIBILITY.md",
    DOCS_DIR / "DATA_DICTIONARY.md",
    DOCS_DIR / "DECISION_LOG.md",
    DOCS_DIR / "ROLE_AND_FORMAT_BREAKDOWNS.md",
    DOCS_DIR / "MODEL_BENCHMARK_REPORT.json",
    DOCS_DIR / "VALIDATION_REPORT.json",
]


def verify_files():
    print("=" * 80)
    print("🔍 VERIFYING ARTIFACTS AND DATASETS...")
    print("=" * 80)
    
    missing = []
    for f in REQUIRED_DATA_FILES + REQUIRED_DOC_FILES:
        if not f.exists():
            print(f"❌ MISSING: {f.relative_to(REPO_ROOT)}")
            missing.append(f)
        else:
            size_kb = round(f.stat().st_size / 1024, 1)
            print(f"✅ FOUND: {f.relative_to(REPO_ROOT)} ({size_kb} KB)")
            
    if missing:
        print(f"\n❌ FAILED: {len(missing)} required files missing.")
        sys.exit(1)
    else:
        print(f"\n🎉 ALL {len(REQUIRED_DATA_FILES) + len(REQUIRED_DOC_FILES)} FILES VERIFIED!")


def print_unstop_dropdown_table():
    bat_df = pd.read_csv(BATTER_CSV)
    bowl_df = pd.read_csv(BOWLER_CSV)
    
    print("\n" + "=" * 90)
    print("📋 UNSTOP SUBMISSION DROPDOWN: 10 MOST RELIABLE BATTERS UNDER PRESSURE")
    print("=" * 90)
    print(f"{'Rank':<6} | {'Player Name':<24} | {'Role':<14} | {'Reliability':<11} | {'95% CI':<14} | {'HP Deliveries':<13} | {'Archetype':<16}")
    print("-" * 90)
    for idx, row in bat_df.head(10).iterrows():
        rank = row['rank']
        name = row['player_name']
        role = row['role']
        rel = f"{row['reliability_score']:.2f}"
        ci = f"[{row['ci_lower_95']:.1f}, {row['ci_upper_95']:.1f}]"
        hp = int(row['hp_balls'])
        arch = row['prc_archetype']
        print(f"{rank:<6} | {name:<24} | {role:<14} | {rel:<11} | {ci:<14} | {hp:<13} | {arch:<16}")
        
    print("\n" + "=" * 90)
    print("📋 UNSTOP SUBMISSION DROPDOWN: 10 MOST RELIABLE BOWLERS UNDER PRESSURE")
    print("=" * 90)
    print(f"{'Rank':<6} | {'Player Name':<24} | {'Discipline':<14} | {'Reliability':<11} | {'95% CI':<14} | {'HP Deliveries':<13} | {'Archetype':<16}")
    print("-" * 90)
    for idx, row in bowl_df.head(10).iterrows():
        rank = row['rank']
        name = row['player_name']
        disc = row['pace_or_spin']
        rel = f"{row['reliability_score']:.2f}"
        ci = f"[{row['ci_lower_95']:.1f}, {row['ci_upper_95']:.1f}]"
        hp = int(row['hp_balls'])
        arch = row['prc_archetype']
        print(f"{rank:<6} | {name:<24} | {disc:<14} | {rel:<11} | {ci:<14} | {hp:<13} | {arch:<16}")
        
    print("=" * 90 + "\n")


if __name__ == "__main__":
    verify_files()
    print_unstop_dropdown_table()
