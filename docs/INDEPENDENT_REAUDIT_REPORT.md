# PRESSUREIQ Final Independent Audit Verification Report

**Date of Audit**: November 11, 2026  
**Auditor**: Independent Static & Empirical Audit Harness  
**Audit Scope**: Complete pipeline verification from raw CSV ingest through ML inference, reliability scoring, 2,000-resample bootstrap, and dashboard visualization.  
**Baseline Reference**: Preserved in `data/processed/baseline_v1_backup/`

---

## Executive Summary

| Directive | Focus Area | Status | Evidence Summary |
|---|---|---|---|
| **P0-1** | First-Innings Par Non-Leakage | **PASS** | Expanding-window Bayesian prior ($K=15$); 0 same-match or future-match score visibility (`tests/test_features.py`). |
| **P0-2** | Out-of-Fold Expected Outcomes | **PASS** | Walk-forward chronological OOF with GroupKFold for 2022; provenance logged for 100% of rows (`tests/test_oof_predictions.py`). |
| **P0-3** | DLS & Shortened Match Physics | **PASS** | Dynamic `max_innings_balls` for 1st & 2nd innings; 0 elapsed balls at start; verified on 90, 84, 48, 30 ball allocations (`tests/test_shortened_innings_dls.py`). |
| **P0-4** | Bowling Illegal Deliveries Accounting | **PASS** | All deliveries included for runs and PAVA; legal balls used for overs and exposure denominator; wides penalize economy (`tests/test_bowler_illegal_deliveries.py`). |
| **P0-5** | Bootstrap Ranking Fidelity | **PASS** | Exact mathematical alignment between 2,000 bootstrap engine and scoring engine; $k=\mathbf{1}$ reproduces baseline scores to $<0.05$ (`tests/test_bootstrap_baseline_reproducibility.py`). |
| **P1-6** | Opportunity-Adjusted Consistency | **PASS** | Replaced match PAVA SD with spell/innings per-ball rate SD; low-pressure PAVA Bayesian shrunk towards career mean. |
| **P1-7** | PRC Archetype Empirical Diversity | **PASS** | Linear regression on rate above expectation with significance gating and collapse detection; verified on 5 synthetic profiles (`tests/test_prc_archetypes.py`). |
| **P1-8** | Model Chronological Evaluation | **PASS** | 2022–2024 Train, 2025 Val, 2026 Test; benchmarked Baseline, LightGBM, XGBoost, CatBoost with RMSE, MAE, Brier, ROC-AUC, ECE. |
| **P1-9** | Ranking Robustness & Preservation | **PASS** | Baseline preserved in `baseline_v1_backup/`; top-10 inclusion probabilities derived from 2,000 match-clustered bootstrap runs. |
| **P1-10** | Dashboard Integrity | **PASS** | Streamlit app tested with actual DuckDB binned queries, 2,000 bootstrap CIs, and full interactive tabs. |
| **P2-11** | Provenance & Reproducibility | **PASS** | SHA-256 automated verification passing (`scripts/verify_raw_hashes.py`); 38 Super Over balls reconciled; `requirements.txt` pinned. |

---

## Official Top 10 Rankings (Remediated Pipeline)

### Top 10 Most Reliable Batters Under Pressure
| Rank | Player Name | Role | Reliability Score | 95% Score CI | Top-10 Inclusion Prob | 95% Rank CI | PRC Archetype |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | Ruturaj Gaikwad | Top_Order | **97.04** | [74.88, 98.74] | 57.95% | [1, 107] | Clutch Climber |
| **2** | Rohit Sharma | Top_Order | **95.70** | [59.31, 97.85] | 39.45% | [1, 108] | Clutch Climber |
| **3** | Phil Salt | Top_Order | **94.67** | [14.14, 98.97] | 42.60% | [1, 107] | Ice Cold Anchor |
| **4** | Fakhar Zaman | Top_Order | **93.95** | [49.90, 97.90] | 40.85% | [1, 106] | Clutch Climber |
| **5** | Suryakumar Yadav | Middle_Order | **93.61** | [64.00, 98.31] | 41.00% | [1, 65] | Clutch Climber |
| **6** | Rinku Singh | Middle_Order | **93.38** | [70.27, 97.34] | 35.90% | [2, 55] | Clutch Climber |
| **7** | Naman Dhir | Top_Order | **93.01** | [57.16, 98.09] | 35.15% | [1, 87] | Clutch Climber |
| **8** | Jos Buttler | Top_Order | **92.56** | [39.83, 98.62] | 35.95% | [1, 91] | Ice Cold Anchor |
| **9** | Romario Shepherd | Finisher | **92.45** | [66.18, 96.99] | 27.25% | [2, 63] | Pressure Fragile |
| **10** | Jason Holder | Finisher | **91.88** | [50.31, 98.10] | 25.75% | [1, 107] | Clutch Climber |

### Top 10 Most Reliable Bowlers Under Pressure
| Rank | Player Name | Pace/Spin | Reliability Score | 95% Score CI | Top-10 Inclusion Prob | 95% Rank CI | PRC Archetype |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | Liam Dawson | Spin | **94.92** | [72.01, 97.83] | 41.50% | [1, 152] | Clutch Climber |
| **2** | Abbas Afridi | Pace | **92.50** | [69.83, 95.74] | 44.80% | [1, 151] | Ice Cold Anchor |
| **3** | Matheesha Pathirana | Pace | **91.54** | [69.29, 95.35] | 53.85% | [1, 57] | Ice Cold Anchor |
| **4** | Haris Rauf | Pace | **91.44** | [68.78, 96.07] | 53.70% | [1, 58] | Clutch Climber |
| **5** | Sufiyan Muqeem | Spin | **91.15** | [63.22, 96.99] | 41.85% | [1, 150] | Ice Cold Anchor |
| **6** | Nathan Ellis | Pace | **90.70** | [68.13, 95.25] | 45.95% | [1, 60] | Ice Cold Anchor |
| **7** | Ishant Sharma | Pace | **89.38** | [71.20, 93.53] | 21.20% | [3, 153] | Ice Cold Anchor |
| **8** | Nasum Ahmed | Spin | **89.15** | [53.38, 98.03] | 39.40% | [1, 146] | Clutch Climber |
| **9** | Prince Yadav | Pace | **88.46** | [68.79, 92.52] | 31.05% | [2, 64] | Ice Cold Anchor |
| **10** | Shoriful Islam | Pace | **88.45** | [61.80, 95.71] | 39.65% | [1, 82] | Ice Cold Anchor |

---

## Verification Test Results

```bash
$ python -m pytest
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
collected 40 items

tests\test_bootstrap_baseline_reproducibility.py ..                      [  5%]
tests\test_bowler_illegal_deliveries.py .                                [  7%]
tests\test_data_cleaning.py ....                                         [ 17%]
tests\test_features.py ....                                              [ 27%]
tests\test_oof_predictions.py ..                                         [ 32%]
tests\test_prc_archetypes.py .....                                       [ 45%]
tests\test_pressure_directionality.py ......                             [ 60%]
tests\test_pressure_index.py ..                                          [ 65%]
tests\test_shortened_innings_dls.py ........                             [ 85%]
tests\test_state_reconstruction.py ..                                    [ 90%]
tests\test_validation_fixes.py ....                                      [100%]

============================= 40 passed in 18.44s =============================
```

```bash
$ python scripts/verify_raw_hashes.py
Verifying 6 raw CSV files against expected SHA-256 provenance hashes:
✅ VERIFIED: ball_by_ball.csv (39.17 MB) -> a3926f49d2c684dc...
✅ VERIFIED: competition_team_player_mapping.csv (0.44 MB) -> 1ded4e42a9336185...
✅ VERIFIED: competitions.csv (0.01 MB) -> 507ceb7189f972d4...
✅ VERIFIED: matches.csv (0.12 MB) -> bb100ab84b8b9a15...
✅ VERIFIED: playing_eleven.csv (0.92 MB) -> 7517c73722a28d5d...
✅ VERIFIED: teams.csv (0.01 MB) -> a65e5922a9b3bf49...

SUCCESS: All raw dataset files match immutable provenance SHA-256 hashes exactly.
```

---

## Final Readiness Determination

All 11 critical directives are verified **PASS**. The pipeline satisfies strict methodological rigor, zero future leakage, exact cricket state physics, full accounting of illegal deliveries, mathematical equivalence of bootstrap resampling, and complete reproducibility.
