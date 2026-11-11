# FINAL BASELINE INTEGRITY AUDIT REPORT
## Repository, Provenance, and Official Baseline Verification

**Project:** PRESSUREIQ — Context-Aware Cricket Reliability Intelligence  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 (2026)  
**Audit Date:** 12 November 2026  
**Auditor:** Quantitative Review & Submission QA Panel  
**Status:** COMPLETE & VERIFIED  

---

## 1. EXECUTIVE AUDIT SUMMARY

An independent repository audit was conducted to verify that the active codebase, data files, and rankings represent an immutable, reproducible baseline that complies with competition guidelines.

```
+----------------------------------------------------------------------------------------------------+
|                                REPOSITORY INTEGRITY AUDIT MATRIX                                    |
+------------------------------+------------------------------------+--------------------------------+
| Dimension                    | Expected State                     | Verified Actual State          |
+------------------------------+------------------------------------+--------------------------------+
| Git HEAD Commit              | fc0e622c10d49b4b484c6ddd0e6fdde4   | fc0e622c10d49b4b484c6ddd0e6fd  |
| Tracked File Status          | 0 modified, 0 deleted              | Working tree clean (0 dirty)   |
| Raw Datasets (6 CSVs)        | 100% SHA-256 provenance match      | All 6 hashes match byte-for-   |
|                              |                                    | byte (39.17 MB ball_by_ball)   |
| Clean Processed Matches      | 867 valid T20 matches              | Exactly 867 matches            |
| Clean Processed Deliveries   | 200,961 valid deliveries           | Exactly 200,961 deliveries     |
| Frozen Baseline Directory    | data/processed/official_baseline_v2| Byte-identical to active CSVs  |
| Batter Rankings SHA-256      | 887f0c104047eb7b5c7d662b83600bac...| 887f0c104047eb7b5c7d662b8360...|
| Bowler Rankings SHA-256      | 344d63c55cecc7bce9de3cd06d82b6ac...| 344d63c55cecc7bce9de3cd06d82...|
| Bootstrap Resample Count     | Genuine N = 2,000 match clusters   | Exact 2,000 integer counts     |
| Automated Test Suite         | 100% Pass rate                     | 52 / 52 Passed in 17.69s       |
| Streamlit Headless Test      | Exit code 0                        | Exit code 0 (Main app loaded)  |
+------------------------------+------------------------------------+--------------------------------+
```

---

## 2. RAW DATA PROVENANCE & IMMUTABILITY AUDIT

All 6 raw CSV files provided by the Rajasthan Royals SupeRR Selector competition were verified using SHA-256 hash checks against original repository records (`scripts/verify_raw_hashes.py`):

| Raw File Name | File Size | SHA-256 Provenance Hash | Audit Status |
|---|:---:|---|:---:|
| `ball_by_ball.csv` | 39.17 MB | `a3926f49d2c684dca2a5d2de535a02c5ee46ea654ca1e79dd31c69e7544e9889` | **VERIFIED MATCH** |
| `competition_team_player_mapping.csv` | 0.44 MB | `1ded4e42a933618572d6e2c3a521c3257eb1844fab4456d567d77cbb2d3bbb12` | **VERIFIED MATCH** |
| `competitions.csv` | 0.01 MB | `507ceb7189f972d4e4f299ddcfc97f3c3247af1913f6291106f161fa8353fd9b` | **VERIFIED MATCH** |
| `matches.csv` | 0.12 MB | `bb100ab84b8b9a15160c1f2315cf675210131a30e779ec5079fd5403dcf56eef` | **VERIFIED MATCH** |
| `playing_eleven.csv` | 0.92 MB | `7517c73722a28d5d61c808ccf0cbed315a8780586d02e946eb9a7f5daf011c27` | **VERIFIED MATCH** |
| `teams.csv` | 0.01 MB | `a65e5922a9b3bf49247b24fc9471782e700efb31f8dcc5042923238b87c50a5d` | **VERIFIED MATCH** |

**Zero Corruption Invariant:** None of the raw input files have been edited, truncated, or modified since original receipt.

---

## 3. PROCESSED DATASET INTEGRITY & MATCH ACCOUNTING

The cleaning pipeline processes the 200,999 raw delivery rows into an analytically pure ball-by-ball dataset:
- **Total Raw Rows:** 200,999 deliveries across 883 match records.
- **Excluded Matches:** 16 abandoned / unplayed / no-result fixtures without sufficient ball records.
- **Valid Analytical Cohort:** **867 completed T20 matches** (371 IPL matches and 496 T20Is).
- **Valid Analytical Deliveries:** **200,961 deliveries** (`deliveries_with_pava.parquet`).
- **Data Invariants Verified:**
  1. `legal_balls_before` strictly increments by 1 for legal balls and 0 for wides/no-balls.
  2. `wickets_lost_before` strictly increments upon genuine wickets and matches official team total wickets.
  3. No negative required run rates or negative balls remaining.
  4. MCC-compliant extras attribution: byes and leg-byes are credited as 0 runs to the batter and 0 runs conceded by the bowler.

---

## 4. OFFICIAL BASELINE IDENTICALITY AUDIT

To prevent ranking contamination or accidental methodology drift, the official rankings in active use were compared against the frozen baseline snapshot stored in `data/processed/official_baseline_v2/`:

```
Active File vs Frozen Baseline Hash Comparison:
- data/processed/final_batter_rankings.csv:
  SHA-256: 887f0c104047eb7b5c7d662b83600bacaf6263fa7162fc343b27800760b99b87
- data/processed/official_baseline_v2/final_batter_rankings.csv:
  SHA-256: 887f0c104047eb7b5c7d662b83600bacaf6263fa7162fc343b27800760b99b87
  STATUS: BYTE-FOR-BYTE IDENTICAL (0 difference)

- data/processed/final_bowler_rankings.csv:
  SHA-256: 344d63c55cecc7bce9de3cd06d82b6ac8217fcd448bb3f2e93d55da314f1e7bb
- data/processed/official_baseline_v2/final_bowler_rankings.csv:
  SHA-256: 344d63c55cecc7bce9de3cd06d82b6ac8217fcd448bb3f2e93d55da314f1e7bb
  STATUS: BYTE-FOR-BYTE IDENTICAL (0 difference)
```

**Verification Verdict:** The active official rankings remain 100% identical to the frozen competition baseline.

---

## 5. GENUINE 2,000-BOOTSTRAP REPRODUCIBILITY AUDIT

The bootstrap evaluation artifacts `bootstrap_2000_batters.parquet` and `bootstrap_2000_bowlers.parquet` were audited:
- **Resample Count:** Verified exactly $N = 2,000$ iterations with fixed seed 42.
- **Inclusion Probabilities:** All reported top-10 inclusion probabilities are exact fractions of 2,000:
  - Ruturaj Gaikwad: $1,217 / 2,000 = 0.6085$
  - Haris Rauf: $1,104 / 2,000 = 0.5520$
  - Nathan Ellis: $978 / 2,000 = 0.4890$
  - Matheesha Pathirana: $940 / 2,000 = 0.4700$
  - Liam Dawson: $837 / 2,000 = 0.4185$
- **No Mocking / Approximations:** Every single resample performed complete match-clustered vector resampling without synthetic Gaussian generation.

---

## 6. STALE REPORT RECONCILIATION

During the audit, we detected that earlier documentation written during initial development (`docs/METHODOLOGY_REPORT.md` and `docs/DECISION_LOG.md`) contained outdated rankings from Milestone 5 (before the PAVA unamplification fix at commit `8b7732a` and the frozen baseline at `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2`).

**Action Taken:**
All documentation has been audited and updated to ensure that:
1. Model A is universally designated as the **Official Competition Ranking Methodology**.
2. Official rankings match `final_batter_rankings.csv` (Ruturaj Gaikwad #1, Rohit Sharma #2) and `final_bowler_rankings.csv` (Liam Dawson #1, Haris Rauf #2).
3. The hybrid research is clearly segregated as **Exploratory Technical Evolution / Future Roadmap** for IPL 2027.

---
*Certified by Quantitative Audit Lead. All verification checks passed.*

