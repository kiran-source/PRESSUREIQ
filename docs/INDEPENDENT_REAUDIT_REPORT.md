# PRESSUREIQ Final Independent Audit Verification Report

**Date of Audit**: November 11, 2026  
**Auditor**: Independent Static & Empirical Audit Harness  
**Audit Scope**: Complete pipeline verification from raw CSV ingest through ML inference, reliability scoring, 2,000-resample bootstrap, and dashboard visualization.  
**Baseline Reference**: Preserved in `data/processed/baseline_v1_backup/`

---

## Executive Summary

| Directive | Focus Area | Status | Evidence Summary |
|---|---|---|---|
| **P0** | PAVA Pressure Double-Counting Resolution | **PASS** | PAVA defined as pure unamplified execution surplus ($V_{\text{raw}}$ in runs/ball); eliminates artificial retention inflation (`tests/test_pava_pressure_amplification.py`). |
| **P0-1** | First-Innings Par Non-Leakage | **PASS** | Expanding-window Bayesian prior ($K=15$); 0 same-match or future-match score visibility (`tests/test_features.py`). |
| **P0-2** | Out-of-Fold Expected Outcomes | **PASS** | Walk-forward chronological OOF with GroupKFold for 2022; provenance logged for 100% of rows (`tests/test_oof_predictions.py`). |
| **P0-3** | DLS & Shortened Match Physics | **PASS** | Dynamic `max_innings_balls` for 1st & 2nd innings; 0 elapsed balls at start; verified on 90, 84, 48, 30 ball allocations (`tests/test_shortened_innings_dls.py`). |
| **P0-4** | Bowling Illegal Deliveries Accounting | **PASS** | All deliveries included for runs and PAVA; legal balls used for overs and exposure denominator; wides penalize economy (`tests/test_bowler_illegal_deliveries.py`). |
| **P0-5** | Bootstrap Ranking Fidelity | **PASS** | Exact mathematical alignment between 2,000 bootstrap engine and scoring engine; $k=\mathbf{1}$ reproduces baseline scores to $<0.05$ (`tests/test_bootstrap_baseline_reproducibility.py`). |
| **P1** | Categorical Encoder OOF Isolation | **PASS** | Categorical encoders fit strictly on training splits; unseen categories mapped to `-1` with 0 NaNs across all 5 prediction columns (`tests/test_oof_predictions.py`). |
| **P1-6** | Opportunity-Adjusted Consistency | **PASS** | Replaced match PAVA SD with spell/innings per-ball rate SD; low-pressure PAVA Bayesian shrunk towards career mean. |
| **P1-7** | PRC Archetype Empirical Diversity | **PASS** | Linear regression on rate above expectation with significance gating and collapse detection; verified on 5 synthetic profiles (`tests/test_prc_archetypes.py`). |
| **P1-8** | Model Chronological Evaluation | **PASS** | 2022–2024 Train, 2025 Val, 2026 Test; benchmarked Baseline, LightGBM, XGBoost, CatBoost with RMSE, MAE, Brier, ROC-AUC, ECE. |
| **P1-9** | Ranking Robustness & Preservation | **PASS** | Baseline preserved in `baseline_v1_backup/`; top-10 inclusion probabilities derived from 2,000 match-clustered bootstrap runs. |
| **P1-10** | Dashboard Integrity | **PASS** | Streamlit app tested with actual DuckDB binned queries, 2,000 bootstrap CIs, and full interactive tabs (`scripts/test_streamlit_headless.py`). |
| **P2-11** | Provenance & Reproducibility | **PASS** | SHA-256 automated verification passing (`scripts/verify_raw_hashes.py`); 38 Super Over balls reconciled; `requirements.txt` pinned (`pyarrow==23.0.1`). |

---

## Official Top 10 Rankings (Remediated Pipeline)

### Top 10 Most Reliable Batters Under Pressure
| Rank | Player Name | Role | Reliability Score | 95% Score CI | Top-10 Inclusion Prob | 95% Rank CI | PRC Archetype |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | Ruturaj Gaikwad | Top_Order | **97.71** | [76.30, 99.09] | 60.85% | [1, 107] | Clutch Climber |
| **2** | Rohit Sharma | Top_Order | **95.27** | [60.01, 98.17] | 33.95% | [1, 108] | Clutch Climber |
| **3** | Fakhar Zaman | Top_Order | **95.25** | [52.46, 98.38] | 45.15% | [1, 106] | Clutch Climber |
| **4** | Suryakumar Yadav | Middle_Order | **94.68** | [66.71, 98.64] | 45.90% | [1, 63] | Clutch Climber |
| **5** | Romario Shepherd | Finisher | **93.69** | [71.26, 97.62] | 34.80% | [2, 56] | Pressure Fragile |
| **6** | Naman Dhir | Top_Order | **93.30** | [58.13, 98.06] | 35.70% | [1, 87] | Clutch Climber |
| **7** | Phil Salt | Top_Order | **93.01** | [14.48, 98.55] | 37.00% | [1, 107] | Ice Cold Anchor |
| **8** | Jitesh Sharma | Middle_Order | **92.79** | [63.45, 97.68] | 32.70% | [2, 68] | Clutch Climber |
| **9** | Nicholas Pooran | Middle_Order | **92.58** | [68.33, 97.47] | 31.75% | [2, 61] | Ice Cold Anchor |
| **10** | Jos Buttler | Top_Order | **92.45** | [40.62, 98.43] | 34.05% | [1, 92] | Ice Cold Anchor |

### Top 10 Most Reliable Bowlers Under Pressure
| Rank | Player Name | Pace/Spin | Reliability Score | 95% Score CI | Top-10 Inclusion Prob | 95% Rank CI | PRC Archetype |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | Liam Dawson | Spin | **95.39** | [74.17, 98.08] | 41.85% | [1, 152] | Clutch Climber |
| **2** | Haris Rauf | Pace | **92.36** | [71.13, 96.49] | 55.20% | [1, 56] | Clutch Climber |
| **3** | Abbas Afridi | Pace | **91.88** | [69.16, 95.74] | 39.55% | [1, 151] | Ice Cold Anchor |
| **4** | Nathan Ellis | Pace | **91.84** | [70.87, 95.95] | 48.90% | [1, 57] | Ice Cold Anchor |
| **5** | Sufiyan Muqeem | Spin | **91.41** | [64.39, 96.91] | 39.50% | [1, 150] | Ice Cold Anchor |
| **6** | Matheesha Pathirana | Pace | **91.11** | [70.27, 95.05] | 47.00% | [1, 59] | Ice Cold Anchor |
| **7** | Nasum Ahmed | Spin | **90.77** | [57.03, 98.19] | 41.75% | [1, 146] | Clutch Climber |
| **8** | Ishant Sharma | Pace | **90.42** | [72.42, 94.32] | 22.10% | [3, 153] | Ice Cold Anchor |
| **9** | Shoriful Islam | Pace | **90.36** | [65.38, 96.63] | 44.30% | [1, 79] | Ice Cold Anchor |
| **10** | Tim Southee | Pace | **89.16** | [63.99, 95.51] | 35.40% | [1, 80] | Ice Cold Anchor |

---

## Verification Test Results

All 44 automated unit tests passed in 24.75s:
- `test_bootstrap_baseline_reproducibility.py`: 2 passed
- `test_bowler_illegal_deliveries.py`: 1 passed
- `test_data_cleaning.py`: 4 passed
- `test_features.py`: 4 passed
- `test_oof_predictions.py`: 3 passed
- `test_pava_pressure_amplification.py`: 3 passed
- `test_prc_archetypes.py`: 5 passed
- `test_pressure_directionality.py`: 6 passed
- `test_pressure_index.py`: 2 passed
- `test_shortened_innings_dls.py`: 8 passed
- `test_state_reconstruction.py`: 2 passed
- `test_validation_fixes.py`: 4 passed
- **Total: 44 passed, 0 failed, 100% pass rate**
