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
    DOCS_DIR / "UNSTOP_SUBMISSION_GUIDE.md",
    DOCS_DIR / "EXECUTIVE_SUMMARY.md",
    DOCS_DIR / "FINAL_READINESS_REPORT.md",
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


def create_and_verify_submission_zip():
    import subprocess
    import tempfile
    import zipfile
    import os

    print("=" * 80)
    print("📦 PACKAGING SUBMISSION ZIP ARCHIVE...")
    print("=" * 80)
    
    zip_path = REPO_ROOT / "PRESSUREIQ_Final_Submission.zip"
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True).strip()
    tracked_files = subprocess.check_output(["git", "ls-files"], cwd=REPO_ROOT, text=True).splitlines()
    
    print(f"Commit HEAD: {commit}")
    print(f"Tracked Git files to pack: {len(tracked_files)}")
    
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        # 1. Add all tracked files
        for tf in tracked_files:
            p = REPO_ROOT / tf
            if p.exists():
                zf.write(p, arcname=tf)
                
        # 2. Add processed data directory (Parquets, final CSVs, 2000-bootstrap, baseline backup)
        proc_dir = REPO_ROOT / "data" / "processed"
        for root, _, files in os.walk(proc_dir):
            for f in files:
                full_p = Path(root) / f
                rel_p = full_p.relative_to(REPO_ROOT)
                zf.write(full_p, arcname=str(rel_p))
                
        # 3. Add .git repository metadata
        git_dir = REPO_ROOT / ".git"
        for root, _, files in os.walk(git_dir):
            for f in files:
                full_p = Path(root) / f
                rel_p = full_p.relative_to(REPO_ROOT)
                zf.write(full_p, arcname=str(rel_p))
                
        # 4. Add raw CSV dataset files
        raw_dir = REPO_ROOT / "SupeRR Selector Season 2 _ Problem Statement _ Data Pack" / "SupeRR Selector Season 2 _ Data Pack"
        if raw_dir.exists():
            for f in raw_dir.glob("*.csv"):
                rel_p = f.relative_to(REPO_ROOT)
                zf.write(f, arcname=str(rel_p))
                
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    import hashlib
    h = hashlib.sha256()
    with open(zip_path, "rb") as fp:
        while chunk := fp.read(8192 * 1024):
            h.update(chunk)
    zip_sha256 = h.hexdigest()
    
    with zipfile.ZipFile(zip_path, "r") as zf:
        file_count = len(zf.namelist())
        
    print(f"✅ Generated {zip_path.name}")
    print(f"   Size:       {size_mb:.2f} MB ({zip_path.stat().st_size:,} bytes)")
    print(f"   File Count: {file_count} files")
    print(f"   SHA-256:    {zip_sha256}")
    
    print("\n🔍 REOPENING AND VERIFYING EXTRACTED ARCHIVE INTEGRITY...")
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(zip_path, "r") as zf:
            bad_crc = zf.testzip()
            assert bad_crc is None, f"Corrupted file in ZIP: {bad_crc}"
            zf.extractall(td)
            
        res_status = subprocess.run(["git", "status", "--short"], cwd=td, capture_output=True, text=True)
        res_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=td, text=True).strip()
        res_raw = subprocess.run([sys.executable, "scripts/verify_raw_hashes.py"], cwd=td, capture_output=True, text=True)
        
        print(f"Extracted Git HEAD: {res_head}")
        status_out = res_status.stdout.strip()
        print(f"Extracted Git status: {status_out if status_out else '(working tree clean)'}")
        print(f"Extracted Raw Hash Verification: {'PASSED (exit code 0)' if res_raw.returncode == 0 else 'FAILED'}")
        
        assert res_head == commit, f"Commit mismatch: {res_head} vs {commit}"
        assert status_out == "", f"Extracted archive has dirty git status:\n{status_out}"
        assert res_raw.returncode == 0, f"Raw hash verification failed in extracted archive:\n{res_raw.stdout}\n{res_raw.stderr}"
        
        # Verify critical files in extracted archive
        for req_f in REQUIRED_DATA_FILES + REQUIRED_DOC_FILES:
            rel = req_f.relative_to(REPO_ROOT)
            assert (Path(td) / rel).exists(), f"Missing extracted file: {rel}"
            
    print("🎉 ARCHIVE VERIFICATION PASSED: Clean Git status, exact commit match, all critical files intact!\n")


if __name__ == "__main__":
    verify_files()
    print_unstop_dropdown_table()
    create_and_verify_submission_zip()

