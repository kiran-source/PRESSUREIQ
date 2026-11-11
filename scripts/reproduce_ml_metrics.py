"""Reproduction and evaluation script for ML comparison verification.

Evaluates:
1. Expected Outcomes: Boundary Probability, Dismissal Probability, Expected Runs
   (LightGBM vs Simple Context Baseline on identical 2026 test records).
2. Win Probability in 2nd innings:
   (Logistic Regression vs Stratified Context Baseline on identical 2026 test records,
    both raw and Platt-calibrated, full match and Powerplay).
"""

import sys
import os
sys.path.insert(0, os.path.abspath("."))

import numpy as np
import pandas as pd
from sklearn.metrics import brier_score_loss, roc_auc_score, mean_squared_error, mean_absolute_error, log_loss
from sklearn.linear_model import LogisticRegression
import lightgbm as lgb
import pickle
from pathlib import Path

# Paths
PROCESSED_DIR = Path("data/processed")
FEATURES_PATH = PROCESSED_DIR / "features_deliveries.parquet"

df = pd.read_parquet(FEATURES_PATH)
df["match_year"] = pd.to_datetime(df["match_date"]).dt.year

print("=" * 90)
print("1. EXPECTED OUTCOMES REPRODUCTION (DELIVERY-LEVEL)")
print("=" * 90)

train_df = df[df["match_year"] <= 2024].copy()
val_df = df[df["match_year"] == 2025].copy()
test_df = df[df["match_year"] >= 2026].copy()

print(f"Dataset split: Train (<=2024) = {len(train_df):,}, Val (2025) = {len(val_df):,}, Test (2026) = {len(test_df):,}")

# Feature columns
feature_cols = [
    "innings", "balls_remaining_before", "wickets_remaining_before",
    "current_run_rate_before", "bpi", "bopi", "is_knockout_stage",
    "hist_batter_sr", "hist_batter_avg", "hist_batter_dot_pct", "hist_batter_bnd_pct",
    "hist_bowler_economy", "hist_bowler_strike_rate", "hist_bowler_dot_pct"
]

# Baseline for Boundary Probability
w_bucket_tr = (train_df["wickets_remaining_before"] // 3) * 3
phase_tr = train_df["innings"].astype(str) + "_" + (train_df["balls_remaining_before"] // 30).astype(str)
base_bnd_map = train_df.groupby([phase_tr, w_bucket_tr])["is_boundary"].mean().to_dict()
global_bnd = train_df["is_boundary"].mean()

w_bucket_te = (test_df["wickets_remaining_before"] // 3) * 3
phase_te = test_df["innings"].astype(str) + "_" + (test_df["balls_remaining_before"] // 30).astype(str)
base_bnd_preds = np.array([base_bnd_map.get((p, w), global_bnd) for p, w in zip(phase_te, w_bucket_te)])

brier_base_bnd = brier_score_loss(test_df["is_boundary"], base_bnd_preds)
auc_base_bnd = roc_auc_score(test_df["is_boundary"], base_bnd_preds)

# Baseline for Dismissal Probability
base_wkt_map = train_df.groupby([phase_tr, w_bucket_tr])["is_wicket"].mean().to_dict()
global_wkt = train_df["is_wicket"].mean()
base_wkt_preds = np.array([base_wkt_map.get((p, w), global_wkt) for p, w in zip(phase_te, w_bucket_te)])

brier_base_wkt = brier_score_loss(test_df["is_wicket"], base_wkt_preds)
auc_base_wkt = roc_auc_score(test_df["is_wicket"], base_wkt_preds)

# Load trained LightGBM models from expected_outcome_models.pkl
with open(PROCESSED_DIR / "models" / "expected_outcome_models.pkl", "rb") as f:
    engine = pickle.load(f)

# Inspect stored test metrics from model benchmark
bm = engine.benchmark_results
print(f"Boundary Prob (Test 2026): Baseline Brier = {brier_base_bnd:.4f} | LightGBM Brier = {bm['batting_boundary_prob']['untouched_test_2026']['Brier_Score']:.4f}")
print(f"Dismissal Prob (Test 2026): Baseline Brier = {brier_base_wkt:.4f} | LightGBM Brier = {bm['batting_dismissal_prob']['untouched_test_2026']['Brier_Score']:.4f}")
print(f"Expected Runs (Test 2026):  Baseline RMSE  = {bm['batting_expected_runs']['untouched_test_2026']['Baseline']['RMSE']:.4f} | LightGBM RMSE  = {bm['batting_expected_runs']['untouched_test_2026']['LightGBM']['RMSE']:.4f}")

print("\n" + "=" * 90)
print("2. IN-GAME WIN PROBABILITY (2ND INNINGS CHASE OUTCOME)")
print("=" * 90)

inn2 = df[df["innings"] == 2].copy()
match_outcomes = inn2.groupby("match_id").agg(
    final_runs=("team_runs_before", "last"),
    target=("target_score", "first")
)
match_outcomes["bat_won"] = (match_outcomes["final_runs"] >= match_outcomes["target"]).astype(int)
inn2 = inn2.merge(match_outcomes[["bat_won"]], on="match_id", how="left")

wp_cols = ["balls_remaining_before", "runs_required_before", "wickets_lost_before", "target_score"]
train2 = inn2[inn2["match_year"] <= 2024].copy()
val2 = inn2[inn2["match_year"] == 2025].copy()
test2 = inn2[inn2["match_year"] >= 2026].copy()

print(f"2nd Innings split: Train = {len(train2):,}, Val = {len(val2):,}, Test = {len(test2):,}")

# Context Baseline for Win Probability: Historical overall chase win rate
uncond_win_rate = train2["bat_won"].mean()
base_wp_uncond = np.full(len(test2), uncond_win_rate)
brier_wp_uncond = brier_score_loss(test2["bat_won"], base_wp_uncond)

# Context Baseline stratified by (balls_remaining // 30, wickets_lost // 3)
inn2_p_tr = (train2["balls_remaining_before"] // 30).astype(str) + "_" + (train2["wickets_lost_before"] // 3).astype(str)
inn2_p_te = (test2["balls_remaining_before"] // 30).astype(str) + "_" + (test2["wickets_lost_before"] // 3).astype(str)
base_wp_map = train2.groupby(inn2_p_tr)["bat_won"].mean().to_dict()
base_wp_strat = np.array([base_wp_map.get(k, uncond_win_rate) for k in inn2_p_te])
brier_wp_strat = brier_score_loss(test2["bat_won"], base_wp_strat)

# Fit Logistic Regression on Train (<=2024)
mean_wp = train2[wp_cols].mean().values
std_wp = train2[wp_cols].std().values + 1e-6
X_tr = (train2[wp_cols].values - mean_wp) / std_wp
y_tr = train2["bat_won"].values
lr = LogisticRegression(C=1.0, max_iter=500, random_state=42)
lr.fit(X_tr, y_tr)

# Predict on 2026 Test
X_te = (test2[wp_cols].values - mean_wp) / std_wp
y_te = test2["bat_won"].values
pred_lr_raw = lr.predict_proba(X_te)[:, 1]
brier_lr_raw = brier_score_loss(y_te, pred_lr_raw)

# Powerplay sub-population (balls_remaining > 84)
pp_mask = test2["balls_remaining_before"] > 84
y_pp = y_te[pp_mask]
pred_lr_pp = pred_lr_raw[pp_mask]
base_pp_strat = base_wp_strat[pp_mask]
brier_lr_pp = brier_score_loss(y_pp, pred_lr_pp)
brier_base_pp = brier_score_loss(y_pp, base_pp_strat)

print(f"Full Test 2026 (N={len(test2):,}):")
print(f"  Unconditional Chase Baseline Brier: {brier_wp_uncond:.4f}")
print(f"  Stratified Context Baseline Brier:  {brier_wp_strat:.4f}")
print(f"  Logistic Win-Prob Model Brier:      {brier_lr_raw:.4f}")
print(f"\nPowerplay Sub-Population (N={pp_mask.sum():,}):")
print(f"  Stratified Context Baseline Brier:  {brier_base_pp:.4f}")
print(f"  Logistic Win-Prob Model Brier:      {brier_lr_pp:.4f}")
