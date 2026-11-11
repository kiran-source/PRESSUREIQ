"""
Comprehensive Pressure Methodology Research Engine for PRESSUREIQ.

Implements and evaluates:
1. Current BPI & BoPI (Baseline)
2. Resource-Adjusted Required Run Rate & Par Velocity (Model B)
3. Pre-Delivery Win Probability & Leverage Index (WPL) (Model C)
4. Context-Aware Decoupled Pressure Index (CDPI) (Model D)
5. Pressure Tier experiments (Fixed vs Quantile vs Context vs Continuous)
6. Directionality monotonicity validation
7. Batting and bowling fairness & opportunity distribution
8. Full sensitivity & ranking impact analysis
"""

import sys
import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.models.pressure_index import compute_batting_pressure_index, compute_bowling_pressure_index
from src.analysis.reliability_engine import (
    compute_batter_reliability_scores,
    compute_bowler_reliability_scores,
    MIN_BATTER_CAREER_BALLS,
    MIN_BATTER_PRESSURE_BALLS,
    MIN_BATTER_MATCHES,
    MIN_BOWLER_CAREER_BALLS,
    MIN_BOWLER_PRESSURE_BALLS,
    MIN_BOWLER_MATCHES
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("PRESSUREIQ.Research")

DELIVERIES_PAVA_PATH = REPO_ROOT / "data" / "processed" / "deliveries_with_pava.parquet"
RESULTS_DIR = REPO_ROOT / "data" / "processed" / "research_pressure"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -15.0, 15.0)))


def train_predelivery_win_probability_model(df: pd.DataFrame) -> LogisticRegression:
    """
    Train a strictly pre-delivery win probability model on historical chases (Innings 2).
    Features: balls_remaining_before, runs_required_before, wickets_lost_before, target_score.
    Target: 1 if batting team won, 0 otherwise.
    Zero post-delivery leakage.
    """
    chases = df[df["innings"] == 2].copy()
    
    # Determine match winner for each match
    # A batting team won if outcome is win_by_wickets, or if team_runs >= target_score
    match_outcomes = chases.groupby("match_id").agg(
        final_runs=("cum_team_runs", "max"),
        target=("target_score", "first")
    ).reset_index()
    match_outcomes["bat_won"] = (match_outcomes["final_runs"] >= match_outcomes["target"]).astype(int)
    
    chases = chases.merge(match_outcomes[["match_id", "bat_won"]], on="match_id", how="left")
    
    # Use chronological train split (<= 2024) to train model
    chases["match_year"] = pd.to_datetime(chases["match_date"]).dt.year
    train_mask = chases["match_year"] <= 2024
    
    X_cols = ["balls_remaining_before", "runs_required_before", "wickets_lost_before", "target_score"]
    
    X_train = chases.loc[train_mask, X_cols].fillna(0).values
    y_train = chases.loc[train_mask, "bat_won"].values
    
    # Standardize features
    mean = X_train.mean(axis=0)
    std = X_train.std(axis=0) + 1e-6
    
    X_train_scaled = (X_train - mean) / std
    
    model = LogisticRegression(C=1.0, max_iter=500, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Validate on 2025-2026
    val_mask = ~train_mask
    if val_mask.sum() > 0:
        X_val_scaled = (chases.loc[val_mask, X_cols].fillna(0).values - mean) / std
        y_val = chases.loc[val_mask, "bat_won"].values
        probs_val = model.predict_proba(X_val_scaled)[:, 1]
        brier = brier_score_loss(y_val, probs_val)
        auc = roc_auc_score(y_val, probs_val)
        logger.info(f"Win Probability Model Validation: Brier={brier:.4f}, AUC={auc:.4f}")
        
    return model, mean, std, X_cols


def compute_alternative_pressure_indices(
    df: pd.DataFrame,
    wp_model: Optional[LogisticRegression] = None,
    mean: Optional[np.ndarray] = None,
    std: Optional[np.ndarray] = None,
    X_cols: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Computes 4 alternative pressure formulations:
    1. BPI_baseline / BoPI_baseline (Current production)
    2. BPI_resource / BoPI_resource (Model B: Resource-Adjusted Required Run Rate)
    3. BPI_winprob / BoPI_winprob (Model C: Win-Probability Leverage WPL)
    4. BPI_cdpi / BoPI_cdpi (Model D: Context-Aware Decoupled Pressure Index with Critical Leverage)
    """
    res = df.copy()
    
    # 1. Baseline Current
    res["bpi_baseline"] = res["bpi"]
    res["bopi_baseline"] = res["bopi"]
    
    # --- MODEL B: Resource-Adjusted Required Run Rate (RRRR) ---
    b_rem = res["balls_remaining_before"].fillna(120.0).values
    w_lost = res["wickets_lost_before"].fillna(0.0).values
    w_rem = np.clip(10.0 - w_lost, 1.0, 10.0)
    
    resource_pct = np.clip((w_rem / 10.0) ** 0.8 * (b_rem / 120.0) ** 0.65, 0.01, 1.0)
    
    runs_req = res["runs_required_before"].fillna(100.0).values
    exp_runs_from_resources = resource_pct * 165.0
    resource_deficit = runs_req - exp_runs_from_resources
    
    bpi_res_inn2 = sigmoid(resource_deficit / 25.0) * 100.0
    runs_above_par = res["runs_above_par_trajectory"].fillna(0.0).values
    bpi_res_inn1 = sigmoid((-runs_above_par) / 16.0) * 100.0
    
    inn_mask = (res["innings"] == 1).values
    bpi_res = np.where(inn_mask, bpi_res_inn1, bpi_res_inn2)
    res["bpi_resource"] = np.round(np.clip(bpi_res, 0.0, 100.0), 2)
    
    bopi_res_inn2 = sigmoid((-resource_deficit) / 25.0) * 100.0
    bopi_res_inn1 = sigmoid(runs_above_par / 16.0) * 100.0
    bopi_res = np.where(inn_mask, bopi_res_inn1, bopi_res_inn2)
    res["bopi_resource"] = np.round(np.clip(bopi_res, 0.0, 100.0), 2)
    
    # --- MODEL C: Pre-Delivery Win Probability & Leverage (WPL) ---
    chase_mask = res["innings"] == 2
    p_win_bat = np.full(len(res), 0.50)
    
    if wp_model is None:
        if len(res) >= 100 and res["innings"].nunique() > 1:
            wp_model, mean, std, X_cols = train_predelivery_win_probability_model(res)
            X_chase = (res.loc[chase_mask, X_cols].fillna(0).values - mean) / std
            p_win_bat[chase_mask] = wp_model.predict_proba(X_chase)[:, 1]
        else:
            # Analytical baseline win probability for small samples/tests
            # Higher RRR -> lower bat win prob
            rrr_vals = res.loc[chase_mask, "required_run_rate_before"].fillna(8.5).values
            p_win_bat[chase_mask] = sigmoid((9.0 - rrr_vals) / 2.5)
    else:
        X_chase = (res.loc[chase_mask, X_cols].fillna(0).values - mean) / std
        p_win_bat[chase_mask] = wp_model.predict_proba(X_chase)[:, 1]
    
    # In 1st innings: Win probability estimated from runs above par trajectory
    p_win_bat[~chase_mask] = sigmoid(runs_above_par[~chase_mask] / 18.0)
    
    res["predeliv_win_prob_bat"] = np.round(p_win_bat, 4)
    wpl = 4.0 * p_win_bat * (1.0 - p_win_bat) * 100.0
    res["win_prob_leverage"] = np.round(wpl, 2)
    
    bpi_wp = (1.0 - p_win_bat) * 70.0 + (wpl / 100.0) * 30.0
    res["bpi_winprob"] = np.round(np.clip(bpi_wp, 0.0, 100.0), 2)
    
    bopi_wp = p_win_bat * 50.0 + (wpl / 100.0) * 50.0
    res["bopi_winprob"] = np.round(np.clip(bopi_wp, 0.0, 100.0), 2)
    
    # --- MODEL D: Context-Aware Decoupled Pressure Index (CDPI) ---
    rrr = res["required_run_rate_before"].fillna(8.5).values
    rrr_clean = np.clip(rrr, 1.0, 24.0)
    
    critical_balance_bell = np.exp(-0.5 * ((rrr_clean - 10.5) / 3.8) ** 2)
    
    cdpi_defend_inn2 = (
        0.55 * (critical_balance_bell * 100.0) +
        0.45 * (sigmoid((12.0 - rrr_clean) / 2.5) * (w_rem / 10.0) * 100.0)
    )
    blowout_discount = np.where((~inn_mask) & (rrr < 4.5) & (b_rem < 36), 0.25, 1.0)
    cdpi_defend_inn2 = cdpi_defend_inn2 * blowout_discount
    
    cdpi_defend_inn1 = sigmoid(runs_above_par / 14.0) * 100.0
    cdpi_defend = np.where(inn_mask, cdpi_defend_inn1, cdpi_defend_inn2)
    
    max_balls = res["max_innings_balls"].fillna(120.0).values if "max_innings_balls" in res.columns else 120.0
    completion_ratio = np.clip(res["legal_balls_before"].fillna(0.0).values / max_balls, 0.0, 1.0)
    climax_comp = (completion_ratio ** 1.35) * 100.0
    
    res["bopi_cdpi"] = np.round(np.clip(
        0.42 * cdpi_defend +
        0.28 * ((w_rem / 10.0) * 100.0) +
        0.20 * climax_comp +
        0.10 * res["win_prob_leverage"].values,
        0.0, 100.0
    ), 2)
    
    bpi_rate_inn2 = sigmoid((rrr_clean - 8.5) / 2.2) * 100.0
    bpi_rate_inn1 = sigmoid((-runs_above_par) / 14.0) * 100.0
    cdpi_rate = np.where(inn_mask, bpi_rate_inn1, bpi_rate_inn2)
    
    res["bpi_cdpi"] = np.round(np.clip(
        0.45 * cdpi_rate * (0.6 + 0.4 * completion_ratio) +
        0.25 * ((w_lost / 9.0) ** 1.2 * 100.0) +
        0.18 * climax_comp +
        0.12 * res["win_prob_leverage"].values,
        0.0, 100.0
    ), 2)
    
    return res


def run_pressure_experiments():
    logger.info(f"Loading deliveries dataset from {DELIVERIES_PAVA_PATH}...")
    df = pd.read_parquet(DELIVERIES_PAVA_PATH)
    logger.info(f"Loaded {len(df):,} deliveries across {df['match_id'].nunique()} matches.")
    
    # 1. Compute Alternative Indices
    logger.info("Computing Alternative Pressure Indices (Models A, B, C, D)...")
    res_df = compute_alternative_pressure_indices(df)
    
    # Save enriched research parquet for subsequent analysis
    enriched_path = RESULTS_DIR / "deliveries_with_research_pressure.parquet"
    res_df.to_parquet(enriched_path, index=False)
    logger.info(f"Saved enriched research dataset to {enriched_path}")
    
    # 2. Evaluate Pressure Distributions & Monotonicity
    models = ["baseline", "resource", "winprob", "cdpi"]
    dist_stats = {}
    for m in models:
        dist_stats[f"bpi_{m}"] = {
            "mean": float(res_df[f"bpi_{m}"].mean()),
            "median": float(res_df[f"bpi_{m}"].median()),
            "std": float(res_df[f"bpi_{m}"].std()),
            "pct_ge_50": float((res_df[f"bpi_{m}"] >= 50.0).mean() * 100.0),
            "pct_ge_65": float((res_df[f"bpi_{m}"] >= 65.0).mean() * 100.0)
        }
        dist_stats[f"bopi_{m}"] = {
            "mean": float(res_df[f"bopi_{m}"].mean()),
            "median": float(res_df[f"bopi_{m}"].median()),
            "std": float(res_df[f"bopi_{m}"].std()),
            "pct_ge_50": float((res_df[f"bopi_{m}"] >= 50.0).mean() * 100.0),
            "pct_ge_65": float((res_df[f"bopi_{m}"] >= 65.0).mean() * 100.0)
        }
        
    with open(RESULTS_DIR / "pressure_distribution_stats.json", "w") as fp:
        json.dump(dist_stats, fp, indent=2)
    logger.info("Saved pressure_distribution_stats.json")
    
    # 3. Monotonicity & Directionality Correlation with RRR and Wickets
    chases = res_df[res_df["innings"] == 2]
    mono_corrs = {}
    for m in models:
        mono_corrs[m] = {
            "bpi_corr_rrr": float(stats.spearmanr(chases["required_run_rate_before"].fillna(8.5), chases[f"bpi_{m}"])[0]),
            "bpi_corr_wkts_lost": float(stats.spearmanr(chases["wickets_lost_before"], chases[f"bpi_{m}"])[0]),
            "bopi_corr_rrr": float(stats.spearmanr(chases["required_run_rate_before"].fillna(8.5), chases[f"bopi_{m}"])[0]),
            "bopi_corr_wkts_rem": float(stats.spearmanr(chases["wickets_remaining_before"], chases[f"bopi_{m}"])[0]),
            "bopi_corr_leverage": float(stats.spearmanr(chases["win_prob_leverage"], chases[f"bopi_{m}"])[0])
        }
        
    with open(RESULTS_DIR / "monotonicity_correlations.json", "w") as fp:
        json.dump(mono_corrs, fp, indent=2)
    logger.info("Saved monotonicity_correlations.json")
    
    # 4. Blowout Anomaly Test
    # Inspect deliveries in extreme blowouts (RRR <= 4.0, balls_rem <= 30)
    blowout_delivs = chases[(chases["required_run_rate_before"] <= 4.0) & (chases["balls_remaining_before"] <= 30)]
    blowout_comparison = {
        "count": len(blowout_delivs),
        "mean_bopi_baseline": float(blowout_delivs["bopi_baseline"].mean()),
        "mean_bopi_cdpi": float(blowout_delivs["bopi_cdpi"].mean()),
        "mean_win_prob_leverage": float(blowout_delivs["win_prob_leverage"].mean())
    }
    with open(RESULTS_DIR / "blowout_anomaly_stats.json", "w") as fp:
        json.dump(blowout_comparison, fp, indent=2)
    logger.info(f"Blowout deliveries: {len(blowout_delivs)}. Mean BoPI Baseline: {blowout_comparison['mean_bopi_baseline']:.2f} vs CDPI: {blowout_comparison['mean_bopi_cdpi']:.2f}")
    
    # 5. Ranking Sensitivity Grid Across Pressure Models
    logger.info("Running player ranking sensitivity across pressure models...")
    ranking_comparisons = {}
    
    for m in models:
        logger.info(f"Computing reliability rankings under Model: {m}...")
        tmp_df = res_df.copy()
        tmp_df["bpi"] = tmp_df[f"bpi_{m}"]
        tmp_df["bopi"] = tmp_df[f"bopi_{m}"]
        
        bat_ranks = compute_batter_reliability_scores(tmp_df)
        bowl_ranks = compute_bowler_reliability_scores(tmp_df)
        
        # Filter eligible
        bat_elig = bat_ranks[bat_ranks["is_eligible"]].head(15).copy()
        bowl_elig = bowl_ranks[bowl_ranks["is_eligible"]].head(15).copy()
        
        bat_elig["rank"] = range(1, len(bat_elig) + 1)
        bowl_elig["rank"] = range(1, len(bowl_elig) + 1)
        
        ranking_comparisons[m] = {
            "top10_batters": bat_elig["player_name"].tolist()[:10],
            "top10_bowlers": bowl_elig["player_name"].tolist()[:10],
            "top10_bat_scores": bat_elig["reliability_score"].tolist()[:10],
            "top10_bowl_scores": bowl_elig["reliability_score"].tolist()[:10]
        }
        
    with open(RESULTS_DIR / "model_ranking_comparisons.json", "w") as fp:
        json.dump(ranking_comparisons, fp, indent=2)
    logger.info("Saved model_ranking_comparisons.json")
    
    # 6. Pressure Threshold Sensitivity Experiments (Fixed vs Quantile vs Continuous)
    logger.info("Evaluating pressure tier threshold sensitivity...")
    threshold_results = {}
    
    for p_thresh in [35.0, 40.0, 45.0, 50.0, 55.0, 60.0]:
        tmp_df = res_df.copy()
        # Override threshold in reliability calculation by shifting BPI
        # We simulate threshold by adjusting what counts as hp_group
        bat_deliv = tmp_df[tmp_df["is_batter_ball"]].copy()
        counts = bat_deliv.groupby("striker_name").agg(
            total_balls=("is_batter_ball", "sum"),
            hp_balls=("bpi", lambda s: (s >= p_thresh).sum())
        )
        eligible_players = (counts["total_balls"] >= MIN_BATTER_CAREER_BALLS) & (counts["hp_balls"] >= MIN_BATTER_PRESSURE_BALLS)
        
        threshold_results[f"thresh_{int(p_thresh)}"] = {
            "eligible_batters_count": int(eligible_players.sum()),
            "median_hp_balls": float(counts.loc[eligible_players, "hp_balls"].median()) if eligible_players.sum() > 0 else 0,
            "mean_hp_balls": float(counts.loc[eligible_players, "hp_balls"].mean()) if eligible_players.sum() > 0 else 0,
            "ruturaj_hp_balls": int(counts.loc["Ruturaj Gaikwad", "hp_balls"]) if "Ruturaj Gaikwad" in counts.index else 0,
            "rohit_hp_balls": int(counts.loc["Rohit Sharma", "hp_balls"]) if "Rohit Sharma" in counts.index else 0,
            "surya_hp_balls": int(counts.loc["Suryakumar Yadav", "hp_balls"]) if "Suryakumar Yadav" in counts.index else 0,
            "rinku_hp_balls": int(counts.loc["Rinku Singh", "hp_balls"]) if "Rinku Singh" in counts.index else 0
        }
        
    with open(RESULTS_DIR / "threshold_sensitivity_stats.json", "w") as fp:
        json.dump(threshold_results, fp, indent=2)
    logger.info("Saved threshold_sensitivity_stats.json")
    
    print("\n" + "=" * 80)
    print("🏆 PRESSURE RESEARCH COMPLETE — SUMMARY FINDINGS")
    print("=" * 80)
    for m in models:
        print(f"\n[{m.upper()}] Top 5 Batters: {', '.join(ranking_comparisons[m]['top10_batters'][:5])}")
        print(f"[{m.upper()}] Top 5 Bowlers: {', '.join(ranking_comparisons[m]['top10_bowlers'][:5])}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    run_pressure_experiments()
