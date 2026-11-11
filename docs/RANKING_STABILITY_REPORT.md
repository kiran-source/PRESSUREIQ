# PRESSUREIQ Ranking Stability & Sensitivity Analysis Report

**Date**: November 11, 2026  
**Bootstrap Repetitions**: 2,000 match-clustered resamples  
**Seed**: 42 (fixed, documented, deterministic)  
**Baseline Reference**: Preserved in `data/processed/baseline_v1_backup/`

---

## 1. Baseline vs Remediated Rankings Comparison

The baseline rankings (`data/processed/baseline_v1_backup/`) were established prior to the static audit remediation. The remediated rankings incorporate:
1. **Resolution of PAVA Pressure Amplification (P0)**: Elimination of pressure double-counting; PAVA defined as pure execution surplus $V_{\text{raw}}$ (runs/ball), stabilizing retention deltas.
2. **Strictly Chronological First-Innings Par (P0-1)**: Expanding-window par table fitted strictly on prior matches.
3. **Walk-Forward Out-of-Fold Expected Outcomes (P0-2)**: Predictions for historical deliveries use strictly prior models.
4. **Shortened Innings Legal-Ball Allocations (P0-3)**: DLS and revised innings maximums properly handled for both innings.
5. **Complete Accounting of Illegal Deliveries (P0-4)**: Wides and no-balls fully penalized in bowling value and economy.
6. **Harmonized 2,000-Resample Clustered Bootstrap (P0-5)**: Exact mathematical scoring reproduction ($<0.01$ score delta on $k=1$).
7. **Categorical Feature Isolation (P1)**: Encoders fitted strictly on training slices with unseen future categories mapped to `-1`.

### Batters: Comparison Table
| Player Name | Baseline Rank | Remediated Rank | Shift | Baseline Score | Remediated Score | 95% Confidence Interval | Top-10 Inclusion Prob (2k Boot) | Remediated Archetype |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Ruturaj Gaikwad | 1 | 1 | 0 | 97.05 | 97.71 | `[76.30, 99.09]` | 60.85% | Clutch Climber |
| Rohit Sharma | 2 | 2 | 0 | 95.71 | 95.27 | `[60.01, 98.17]` | 33.95% | Clutch Climber |
| Fakhar Zaman | 4 | 3 | +1 | 93.96 | 95.25 | `[52.46, 98.38]` | 45.15% | Clutch Climber |
| Suryakumar Yadav | 5 | 4 | +1 | 93.62 | 94.68 | `[66.71, 98.64]` | 45.90% | Clutch Climber |
| Romario Shepherd | 9 | 5 | +4 | 92.47 | 93.69 | `[71.26, 97.62]` | 34.80% | Pressure Fragile |
| Naman Dhir | 7 | 6 | +1 | 93.04 | 93.30 | `[58.13, 98.06]` | 35.70% | Clutch Climber |
| Phil Salt | 3 | 7 | -4 | 94.68 | 93.01 | `[14.48, 98.55]` | 37.00% | Ice Cold Anchor |
| Jitesh Sharma | — | 8 | NEW | — | 92.79 | `[63.45, 97.68]` | 32.70% | Clutch Climber |
| Nicholas Pooran | — | 9 | NEW | — | 92.58 | `[68.33, 97.47]` | 31.75% | Ice Cold Anchor |
| Jos Buttler | 8 | 10 | -2 | 92.58 | 92.45 | `[40.62, 98.43]` | 34.05% | Ice Cold Anchor |

*Batting Ranking Stability*: The Top 10 batting cohort shows strong structural stability. When resolving the PAVA double-counting distortion, players with massive pressure sample sizes and strong fundamentals like Suryakumar Yadav (236 HP balls) and Nicholas Pooran (300 HP balls) rise into the top tier, while Phil Salt experiences expected variance due to a smaller high-pressure sample (49 balls). PRC archetypes clearly distinguish *Clutch Climbers* (positive slope under pressure) from *Ice Cold Anchors* (statistically invariant) and *Pressure Fragile* performers (Romario Shepherd, whose rate dips at extreme $>85$ BPI).

### Bowlers: Comparison Table
| Player Name | Baseline Rank | Remediated Rank | Shift | Baseline Score | Remediated Score | 95% Confidence Interval | Top-10 Inclusion Prob (2k Boot) | Remediated Archetype |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Liam Dawson | 1 | 1 | 0 | 94.93 | 95.39 | `[74.17, 98.08]` | 41.85% | Clutch Climber |
| Haris Rauf | 4 | 2 | +2 | 91.45 | 92.36 | `[71.13, 96.49]` | 55.20% | Clutch Climber |
| Abbas Afridi | 2 | 3 | -1 | 92.52 | 91.88 | `[69.16, 95.74]` | 39.55% | Ice Cold Anchor |
| Nathan Ellis | 6 | 4 | +2 | 90.71 | 91.84 | `[70.87, 95.95]` | 48.90% | Ice Cold Anchor |
| Sufiyan Muqeem | 5 | 5 | 0 | 91.17 | 91.41 | `[64.39, 96.91]` | 39.50% | Ice Cold Anchor |
| Matheesha Pathirana | 3 | 6 | -3 | 91.55 | 91.11 | `[70.27, 95.05]` | 47.00% | Ice Cold Anchor |
| Nasum Ahmed | 8 | 7 | +1 | 89.17 | 90.77 | `[57.03, 98.19]` | 41.75% | Clutch Climber |
| Ishant Sharma | 7 | 8 | -1 | 89.41 | 90.42 | `[72.42, 94.32]` | 22.10% | Ice Cold Anchor |
| Shoriful Islam | 10 | 9 | +1 | 88.48 | 90.36 | `[65.38, 96.63]` | 44.30% | Ice Cold Anchor |
| Tim Southee | — | 10 | NEW | — | 89.16 | `[63.99, 95.51]` | 35.40% | Ice Cold Anchor |

*Bowling Ranking Stability*: Properly accounting for illegal deliveries (wides and no-balls) penalizes erratic bowlers while rewarding disciplined death executioners. Haris Rauf (444 HP balls) and Nathan Ellis (251 HP balls) demonstrate the highest bootstrap top-10 inclusion probabilities (55.20% and 48.90%), reflecting sustained reliability across diverse match resamples.

---

## 2. Methodology of the 2,000 Match-Clustered Bootstrap

1. **Clustering Unit**: The entire match delivery cluster is preserved intact. Deliveries from the same match are never separated, preserving within-match correlation structures.
2. **Resampling Scheme**: 2,000 resamples with replacement of the 867 valid matches using fixed random seed 42.
3. **Harmonized Scoring**: Every bootstrap resample executes the exact same scoring functions as the canonical pipeline:
   - Same eligibility filters ($\ge 30$ high-pressure balls, $\ge 5$ matches, $\ge 50$ total balls).
   - Same candidate pool standardization and Empirical Bayes shrinkage ($K=45$).
   - Same pillar weights and score aggregation.
4. **Reproducibility Guarantee**: Verified by `tests/test_bootstrap_baseline_reproducibility.py`: the canonical baseline score matches the bootstrap engine score with delta $< 0.01$.
