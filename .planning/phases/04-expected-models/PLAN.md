# PHASE 04: Expected Performance Models Plan

## Goal
Build expected-outcome machine learning models on chronological validation splits to predict expected runs, dismissal probability, and boundary probability.

## Tasks
1. Dataset split:
   - Chronological: Train ($\le 2024$), Validation ($2025$), Test ($2026$).
2. Multi-target model training:
   - Batting targets: $E[\text{runs}]$, $P(\text{dismissal})$, $P(\text{boundary})$.
   - Bowling targets: $E[\text{runs conceded}]$, $P(\text{bowler wicket})$.
3. Algorithms benchmarked:
   - Baseline historical mean.
   - LightGBM Regressor / Classifier.
   - XGBoost Regressor / Classifier.
   - CatBoost Regressor / Classifier.
4. Calibration and metrics:
   - Brier score, ROC-AUC, MAE, RMSE evaluated.
   - Prevent artificial class weighting distortion on rare events.
   - Save report to `docs/MODEL_BENCHMARK_REPORT.json`.

## Acceptance Criteria
- LightGBM selected based on best test calibration and speed.
- Natural wicket calibration preserved ($Brier \approx 0.052$).
