# PHASE 08: Validation & Bootstrap Uncertainty Plan

## Goal
Quantify ranking stability and uncertainty via match-clustered bootstrap resampling ($N=30$) and conduct ablation studies.

## Tasks
1. Match-Clustered Bootstrap Resampling:
   - Resample entire matches with replacement ($N=30$ iterations).
   - Recompute full reliability scores for top 20 contenders in each iteration.
   - Compute empirical 95% Confidence Intervals (`[ci_lower_95, ci_upper_95]`).
2. Ablation Studies:
   - Full Model vs Raw Strike Rate (Overlap = 10%).
   - Full Model vs No Empirical Bayes Shrinkage.
   - Full Model vs No Retention Delta.
   - Save report to `docs/VALIDATION_REPORT.json`.

## Acceptance Criteria
- 95% Confidence Intervals populated in final rankings.
- Ablation report confirms all 5 pillars provide measurable ranking stability benefits.

