import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.abspath("."))

import numpy as np
import pandas as pd
from scipy import stats

bat_rankings = pd.read_parquet("data/processed/final_batter_rankings.parquet")
bowl_rankings = pd.read_parquet("data/processed/final_bowler_rankings.parquet")

print(f"Loaded final rankings: {len(bat_rankings)} eligible batters, {len(bowl_rankings)} eligible bowlers.")

# 1. Pillar Correlations
bat_pillars = bat_rankings[[
    "shrunk_hp_pava_per_ball",
    "retention_delta",
    "consistency_score",
    "adaptability_score",
    "evidence_weight"
]]

bowl_pillars = bowl_rankings[[
    "shrunk_hp_pava_per_ball",
    "retention_delta",
    "consistency_score",
    "adaptability_score",
    "evidence_weight"
]]

print("\n--- BATTER PILLAR CORRELATION MATRIX ---")
print(bat_pillars.corr().round(3))

print("\n--- BOWLER PILLAR CORRELATION MATRIX ---")
print(bowl_pillars.corr().round(3))

# 2. Score Saturation & Distributions
print("\n--- BATTER SCORE DISTRIBUTION METRICS ---")
b_scores = bat_rankings["reliability_score"]
print(f"Mean: {b_scores.mean():.2f}, Std: {b_scores.std():.2f}")
print(f"Min: {b_scores.min():.2f}, 25%: {b_scores.quantile(0.25):.2f}, Median: {b_scores.median():.2f}, 75%: {b_scores.quantile(0.75):.2f}, Max: {b_scores.max():.2f}")
print(f"Skewness: {stats.skew(b_scores):.3f}, Kurtosis: {stats.kurtosis(b_scores):.3f}")
print(f"Players with score >= 95.0: {(b_scores >= 95.0).sum()} / {len(b_scores)}")
print(f"Players with score <= 5.0: {(b_scores <= 5.0).sum()} / {len(b_scores)}")

print("\n--- BOWLER SCORE DISTRIBUTION METRICS ---")
w_scores = bowl_rankings["reliability_score"]
print(f"Mean: {w_scores.mean():.2f}, Std: {w_scores.std():.2f}")
print(f"Min: {w_scores.min():.2f}, 25%: {w_scores.quantile(0.25):.2f}, Median: {w_scores.median():.2f}, 75%: {w_scores.quantile(0.75):.2f}, Max: {w_scores.max():.2f}")
print(f"Skewness: {stats.skew(w_scores):.3f}, Kurtosis: {stats.kurtosis(w_scores):.3f}")
print(f"Players with score >= 95.0: {(w_scores >= 95.0).sum()} / {len(w_scores)}")
print(f"Players with score <= 5.0: {(w_scores <= 5.0).sum()} / {len(w_scores)}")

# 3. Weight Sensitivity & Ablation
weights_baseline = np.array([0.50, 0.20, 0.15, 0.15])

# Standardized pillars for batters
pava_norm = (bat_rankings["shrunk_hp_pava_per_ball"] - bat_rankings["shrunk_hp_pava_per_ball"].mean()) / bat_rankings["shrunk_hp_pava_per_ball"].std()
ret_norm = (bat_rankings["retention_delta"] - bat_rankings["retention_delta"].mean()) / bat_rankings["retention_delta"].std()
cons_norm = bat_rankings["consistency_score"] / 50.0
adapt_norm = bat_rankings["adaptability_score"] / 50.0

X_bat = np.column_stack([pava_norm, ret_norm, cons_norm, adapt_norm])
base_top10 = set(bat_rankings.head(10)["player_id"])

perturbations = {
    "Baseline (0.50, 0.20, 0.15, 0.15)": weights_baseline,
    "+20% Absolute PAVA (0.60, 0.15, 0.125, 0.125)": np.array([0.60, 0.15, 0.125, 0.125]),
    "+20% Retention (0.40, 0.35, 0.125, 0.125)": np.array([0.40, 0.35, 0.125, 0.125]),
    "+20% Consistency (0.45, 0.15, 0.25, 0.15)": np.array([0.45, 0.15, 0.25, 0.15]),
    "Ablate Consistency (0.55, 0.25, 0.00, 0.20)": np.array([0.55, 0.25, 0.00, 0.20]),
    "Ablate Adaptability (0.55, 0.25, 0.20, 0.00)": np.array([0.55, 0.25, 0.20, 0.00]),
}

print("\n--- BATTER TOP 10 WEIGHT SENSITIVITY & ABLATION ---")
for name, w in perturbations.items():
    comp = X_bat @ w
    ranked_indices = np.argsort(-comp)
    top10_pids = set(bat_rankings.iloc[ranked_indices[:10]]["player_id"])
    overlap = len(base_top10 & top10_pids)
    spearman_corr, _ = stats.spearmanr(bat_rankings["reliability_score"], comp)
    print(f"{name:45s} | Top-10 Overlap: {overlap}/10 | Rank Spearman: {spearman_corr:.4f}")

# 4. Eligibility Threshold Sensitivity
deliv_pava = pd.read_parquet("data/processed/deliveries_with_pava.parquet")
bat_deliv = deliv_pava[deliv_pava["is_batter_ball"]]

bat_agg = bat_deliv.groupby("striker_id").agg(
    player_name=("striker_name", "first"),
    matches=("match_id", "nunique"),
    total_balls=("is_batter_ball", "count"),
    hp_balls=("bpi", lambda s: (s >= 50.0).sum())
).reset_index()

threshold_scenarios = [
    ("Relaxed (B>=300, HP>=20, M>=10)", 300, 20, 10),
    ("Baseline (B>=400, HP>=30, M>=15)", 400, 30, 15),
    ("Strict (B>=500, HP>=40, M>=20)", 500, 40, 20),
    ("High-Exposure (B>=600, HP>=50, M>=25)", 600, 50, 25),
]

print("\n--- BATTER ELIGIBILITY THRESHOLD SENSITIVITY ---")
shortlisted_top10_names = bat_rankings.head(10)["player_name"].tolist()

for sc_name, min_b, min_hp, min_m in threshold_scenarios:
    eligible = bat_agg[
        (bat_agg["total_balls"] >= min_b) &
        (bat_agg["hp_balls"] >= min_hp) &
        (bat_agg["matches"] >= min_m)
    ]
    el_names = set(eligible["player_name"])
    retained = [p for p in shortlisted_top10_names if p in el_names]
    dropped = [p for p in shortlisted_top10_names if p not in el_names]
    print(f"{sc_name:38s} -> Qualifying Batters: {len(eligible):3d} | Top 10 Retained: {len(retained)}/10")
    if dropped:
        print(f"   Dropped from Top 10: {', '.join(dropped)}")

