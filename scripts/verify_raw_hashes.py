"""Raw CSV Dataset Hash & Provenance Verifier (P2-11).

Asserts SHA-256 integrity of all raw competition dataset files and exits non-zero on mismatch.
"""

import hashlib
import glob
import os
import sys

RAW_DIR = "SupeRR Selector Season 2 _ Problem Statement _ Data Pack/SupeRR Selector Season 2 _ Data Pack"

EXPECTED_HASHES = {
    "ball_by_ball.csv": "a3926f49d2c684dca2a5d2de535a02c5ee46ea654ca1e79dd31c69e7544e9889",
    "competition_team_player_mapping.csv": "1ded4e42a933618572d6e2c3a521c3257eb1844fab4456d567d77cbb2d3bbb12",
    "competitions.csv": "507ceb7189f972d4e4f299ddcfc97f3c3247af1913f6291106f161fa8353fd9b",
    "matches.csv": "bb100ab84b8b9a15160c1f2315cf675210131a30e779ec5079fd5403dcf56eef",
    "playing_eleven.csv": "7517c73722a28d5d61c808ccf0cbed315a8780586d02e946eb9a7f5daf011c27",
    "teams.csv": "a65e5922a9b3bf49247b24fc9471782e700efb31f8dcc5042923238b87c50a5d"
}


def verify_hashes():
    files = sorted(glob.glob(os.path.join(RAW_DIR, "*.csv")))
    if not files:
        print(f"ERROR: No CSV files found in {RAW_DIR}")
        sys.exit(1)
        
    print(f"Verifying {len(files)} raw CSV files against expected SHA-256 provenance hashes:")
    mismatch_count = 0
    
    for f in files:
        basename = os.path.basename(f)
        h = hashlib.sha256()
        with open(f, "rb") as fp:
            while chunk := fp.read(8192 * 1024):
                h.update(chunk)
        digest = h.hexdigest()
        size_mb = os.path.getsize(f) / (1024 * 1024)
        
        expected = EXPECTED_HASHES.get(basename)
        if expected is None:
            print(f"❌ UNEXPECTED FILE: {basename}")
            mismatch_count += 1
        elif digest != expected:
            print(f"❌ HASH MISMATCH for {basename} ({size_mb:.2f} MB)!\n   Expected: {expected}\n   Found:    {digest}")
            mismatch_count += 1
        else:
            print(f"✅ VERIFIED: {basename} ({size_mb:.2f} MB) -> {digest[:16]}...")
            
    if mismatch_count > 0:
        print(f"\nFAILED: {mismatch_count} raw file(s) failed hash verification!")
        sys.exit(1)
        
    print("\nSUCCESS: All raw dataset files match immutable provenance SHA-256 hashes exactly.")
    sys.exit(0)


if __name__ == "__main__":
    verify_hashes()
