"""Match-Clustered Bootstrap Engine for PRESSUREIQ (P0-5).

Guarantees exact mathematical equivalence between bootstrap evaluation and the
canonical reliability ranking engine.

Key Features:
- Exact scoring alignment: identical 5-pillar formulas, shrinkage, Bayesian retention,
  opportunity-adjusted consistency, and eligibility rules.
- Reproducibility test: When every match is sampled exactly once (k=1), baseline
  scores reproduce canonical ranking scores exactly.
- Statistically defensible absent handling: ineligible or absent players in any resample
  are assigned tail rank (N_eligible + 1) rather than arbitrary score 50.
"""

import logging
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from scipy import stats

from src.analysis.reliability_engine import (
    MIN_BATTER_CAREER_BALLS,
    MIN_BATTER_PRESSURE_BALLS,
    MIN_BATTER_MATCHES,
    MIN_BOWLER_CAREER_BALLS,
    MIN_BOWLER_PRESSURE_BALLS,
    MIN_BOWLER_MATCHES,
    K_SHRINK
)

logger = logging.getLogger("PRESSUREIQ.BootstrapEngine")


def build_player_match_matrices(deliveries_df: pd.DataFrame, is_batting: bool = True) -> Dict:
    """
    Pre-aggregate delivery data into match-by-player matrices for ultra-fast vectorized resampling.
    """
    unique_matches = np.sort(deliveries_df["match_id"].unique())
    n_matches = len(unique_matches)
    match_to_idx = {mid: idx for idx, mid in enumerate(unique_matches)}
    
    if is_batting:
        sub_df = deliveries_df[deliveries_df["is_batter_ball"]].copy()
        pid_col = "striker_id"
        pname_col = "striker_name"
        
        sub_df["is_hp"] = (sub_df["bpi"] >= 50.0).astype(np.float64)
        sub_df["is_lp"] = (sub_df["bpi"] < 35.0).astype(np.float64)
        sub_df["hp_pava"] = np.where(sub_df["bpi"] >= 50.0, sub_df["pava_bat"], 0.0)
        sub_df["lp_pava"] = np.where(sub_df["bpi"] < 35.0, sub_df["pava_bat"], 0.0)
        sub_df["is_ipl"] = (sub_df["comp_category"] == "IPL").astype(np.float64)
        sub_df["is_t20i"] = (sub_df["comp_category"] == "T20I").astype(np.float64)
        sub_df["ipl_pava"] = np.where(sub_df["comp_category"] == "IPL", sub_df["pava_bat"], 0.0)
        sub_df["t20i_pava"] = np.where(sub_df["comp_category"] == "T20I", sub_df["pava_bat"], 0.0)
        sub_df["ball_cnt"] = 1.0
        
        grouped = sub_df.groupby(["match_id", pid_col]).agg(
            player_name=(pname_col, "first"),
            n_balls=("ball_cnt", "sum"),
            n_hp=("is_hp", "sum"),
            n_lp=("is_lp", "sum"),
            sum_hp=("hp_pava", "sum"),
            sum_lp=("lp_pava", "sum"),
            sum_pava=("pava_bat", "sum"),
            n_ipl=("is_ipl", "sum"),
            sum_ipl=("ipl_pava", "sum"),
            n_t20i=("is_t20i", "sum"),
            sum_t20i=("t20i_pava", "sum")
        ).reset_index()
        
        # Filter to players with at least 50 balls overall for candidate tracking
        career = grouped.groupby(pid_col)["n_balls"].sum()
        valid_pids = career[career >= 50].index.values
        
    else:
        # P0-4: Include all deliveries bowled by bowler
        sub_df = deliveries_df[deliveries_df["bowler_id"].notna()].copy()
        pid_col = "bowler_id"
        pname_col = "bowler_name"
        
        is_legal = sub_df["is_legal_ball"].astype(np.float64)
        sub_df["is_legal_cnt"] = is_legal
        sub_df["is_hp"] = np.where(sub_df["bopi"] >= 50.0, is_legal, 0.0)
        sub_df["is_lp"] = np.where(sub_df["bopi"] < 35.0, is_legal, 0.0)
        sub_df["hp_pava"] = np.where(sub_df["bopi"] >= 50.0, sub_df["pava_bowl"], 0.0)
        sub_df["lp_pava"] = np.where(sub_df["bopi"] < 35.0, sub_df["pava_bowl"], 0.0)
        sub_df["is_ipl"] = np.where(sub_df["comp_category"] == "IPL", is_legal, 0.0)
        sub_df["is_t20i"] = np.where(sub_df["comp_category"] == "T20I", is_legal, 0.0)
        sub_df["ipl_pava"] = np.where(sub_df["comp_category"] == "IPL", sub_df["pava_bowl"], 0.0)
        sub_df["t20i_pava"] = np.where(sub_df["comp_category"] == "T20I", sub_df["pava_bowl"], 0.0)
        
        grouped = sub_df.groupby(["match_id", pid_col]).agg(
            player_name=(pname_col, "first"),
            n_balls=("is_legal_cnt", "sum"),
            n_hp=("is_hp", "sum"),
            n_lp=("is_lp", "sum"),
            sum_hp=("hp_pava", "sum"),
            sum_lp=("lp_pava", "sum"),
            sum_pava=("pava_bowl", "sum"),
            n_ipl=("is_ipl", "sum"),
            sum_ipl=("ipl_pava", "sum"),
            n_t20i=("is_t20i", "sum"),
            sum_t20i=("t20i_pava", "sum")
        ).reset_index()
        
        career = grouped.groupby(pid_col)["n_balls"].sum()
        valid_pids = career[career >= 50].index.values

    grouped = grouped[grouped[pid_col].isin(valid_pids)].copy()
    player_ids = np.sort(valid_pids)
    n_players = len(player_ids)
    player_to_idx = {pid: idx for idx, pid in enumerate(player_ids)}
    
    # Pre-allocate sparse/dense (n_matches, n_players) matrices
    m_idx = grouped["match_id"].map(match_to_idx).values
    p_idx = grouped[pid_col].map(player_to_idx).values
    
    def make_mat(col_name: str) -> np.ndarray:
        mat = np.zeros((n_matches, n_players), dtype=np.float64)
        mat[m_idx, p_idx] = grouped[col_name].values
        return mat
        
    mat_balls = make_mat("n_balls")
    mat_hp = make_mat("n_hp")
    mat_lp = make_mat("n_lp")
    mat_pava = make_mat("sum_pava")
    mat_hp_pava = make_mat("sum_hp")
    mat_lp_pava = make_mat("sum_lp")
    mat_ipl_balls = make_mat("n_ipl")
    mat_ipl_pava = make_mat("sum_ipl")
    mat_t20i_balls = make_mat("n_t20i")
    mat_t20i_pava = make_mat("sum_t20i")
    mat_match_presence = (mat_balls > 0).astype(np.float64)
    
    # Pre-compute per-match rates for consistency evaluation
    min_innings_balls = 5 if is_batting else 6
    mat_valid_spell = (mat_balls >= min_innings_balls).astype(np.float64)
    mat_rates = np.zeros((n_matches, n_players), dtype=np.float64)
    mask_valid = mat_valid_spell > 0
    mat_rates[mask_valid] = mat_pava[mask_valid] / mat_balls[mask_valid]
    
    name_map = grouped.drop_duplicates(pid_col).set_index(pid_col)["player_name"].to_dict()
    
    return {
        "n_matches": n_matches,
        "n_players": n_players,
        "player_ids": player_ids,
        "unique_matches": unique_matches,
        "name_map": name_map,
        "is_batting": is_batting,
        "mat_balls": mat_balls,
        "mat_hp": mat_hp,
        "mat_lp": mat_lp,
        "mat_pava": mat_pava,
        "mat_hp_pava": mat_hp_pava,
        "mat_lp_pava": mat_lp_pava,
        "mat_ipl_balls": mat_ipl_balls,
        "mat_ipl_pava": mat_ipl_pava,
        "mat_t20i_balls": mat_t20i_balls,
        "mat_t20i_pava": mat_t20i_pava,
        "mat_match_presence": mat_match_presence,
        "mat_valid_spell": mat_valid_spell,
        "mat_rates": mat_rates
    }


def evaluate_scores_vectorized(mats: Dict, k_vec: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Evaluate 5-pillar scores, composite reliability, and eligibility for all players under resample vector k.
    
    Returns:
    - scores: (n_players,) composite reliability score (0-100)
    - is_eligible: (n_players,) boolean eligibility indicator
    - metrics_dict: dict of intermediate pillar values
    """
    is_bat = mats["is_batting"]
    min_balls = MIN_BATTER_CAREER_BALLS if is_bat else MIN_BOWLER_CAREER_BALLS
    min_hp = MIN_BATTER_PRESSURE_BALLS if is_bat else MIN_BOWLER_PRESSURE_BALLS
    min_matches = MIN_BATTER_MATCHES if is_bat else MIN_BOWLER_MATCHES
    
    # Weighted sums across matches: (n_players,)
    tot_balls = k_vec @ mats["mat_balls"]
    tot_hp_balls = k_vec @ mats["mat_hp"]
    tot_lp_balls = k_vec @ mats["mat_lp"]
    tot_pava = k_vec @ mats["mat_pava"]
    tot_hp_pava = k_vec @ mats["mat_hp_pava"]
    tot_lp_pava = k_vec @ mats["mat_lp_pava"]
    
    # Matches with at least 1 ball bowled/faced
    # Note: k_vec is counts of match occurrences. If a match occurs k times, it contributes k matches to player's total.
    tot_matches = k_vec @ mats["mat_match_presence"]
    
    # Eligibility indicator
    is_eligible = (tot_balls >= min_balls) & (tot_hp_balls >= min_hp) & (tot_matches >= min_matches)
    
    # Pillar 1: Shrunk HP PAVA
    raw_hp_pava = np.where(tot_hp_balls >= 5, tot_hp_pava / np.maximum(tot_hp_balls, 1e-6), 0.0)
    w_shrink = tot_hp_balls / (tot_hp_balls + K_SHRINK)
    shrunk_hp_pava = w_shrink * raw_hp_pava
    
    # Pillar 2: Baseline Retention with shrinkage towards career mean
    career_mean = tot_pava / np.maximum(tot_balls, 1e-6)
    w_lp = tot_lp_balls / (tot_lp_balls + 10.0)
    lp_obs = np.where(tot_lp_balls > 0, tot_lp_pava / np.maximum(tot_lp_balls, 1e-6), career_mean)
    raw_lp_pava = np.where(tot_lp_balls >= 10, tot_lp_pava / np.maximum(tot_lp_balls, 1e-6), w_lp * lp_obs + (1.0 - w_lp) * career_mean)
    retention_delta = raw_hp_pava - raw_lp_pava
    
    # Pillar 3: Opportunity-Adjusted Consistency
    # Weighted variance of per-match rates: sum(k_m * (rate - mean)^2) / (sum(k_m) - 1)
    k_spells = k_vec[:, None] * mats["mat_valid_spell"]  # (n_matches, n_players)
    sum_k_spells = np.sum(k_spells, axis=0)               # (n_players,)
    
    # Weighted mean of rates
    weighted_sum_rates = np.sum(k_spells * mats["mat_rates"], axis=0)
    mean_rate = np.where(sum_k_spells >= 1, weighted_sum_rates / np.maximum(sum_k_spells, 1e-6), 0.0)
    
    # Weighted sum of squared deviations
    sq_diff = mats["mat_rates"] - mean_rate[None, :]
    weighted_sq_diff = np.sum(k_spells * (sq_diff ** 2), axis=0)
    sample_var = np.where(sum_k_spells >= 3, weighted_sq_diff / np.maximum(sum_k_spells - 1.0, 1e-6), 0.25)
    spell_sd = np.sqrt(np.maximum(sample_var, 0.0))
    spell_sd = np.where(sum_k_spells >= 3, spell_sd, 0.50)
    consistency_score = 100.0 / (1.0 + (spell_sd / 0.35))
    
    # Pillar 4: Context Adaptability
    tot_ipl_balls = k_vec @ mats["mat_ipl_balls"]
    tot_t20i_balls = k_vec @ mats["mat_t20i_balls"]
    tot_ipl_pava = k_vec @ mats["mat_ipl_pava"]
    tot_t20i_pava = k_vec @ mats["mat_t20i_pava"]
    
    has_both = (tot_ipl_balls >= 30) & (tot_t20i_balls >= 30)
    ipl_rate = np.where(tot_ipl_balls > 0, tot_ipl_pava / np.maximum(tot_ipl_balls, 1e-6), 0.0)
    t20i_rate = np.where(tot_t20i_balls > 0, tot_t20i_pava / np.maximum(tot_t20i_balls, 1e-6), 0.0)
    comp_diff = np.abs(ipl_rate - t20i_rate)
    adaptability_score = np.where(has_both, np.clip(100.0 - comp_diff * 40.0, 20.0, 100.0), 60.0)
    
    # Standardize across candidate pool using ddof=1 (matching pandas .std())
    pava_std = np.std(shrunk_hp_pava, ddof=1) if len(shrunk_hp_pava) > 1 else 1.0
    ret_std = np.std(retention_delta, ddof=1) if len(retention_delta) > 1 else 1.0
    pava_norm = (shrunk_hp_pava - np.mean(shrunk_hp_pava)) / (pava_std + 1e-6)
    ret_norm = (retention_delta - np.mean(retention_delta)) / (ret_std + 1e-6)
    
    raw_composite = (
        0.50 * pava_norm +
        0.20 * ret_norm +
        0.15 * (consistency_score / 50.0) +
        0.15 * (adaptability_score / 50.0)
    )
    
    scores = np.round(stats.norm.cdf(raw_composite) * 100.0, 2)
    return scores, is_eligible, {
        "shrunk_hp_pava": shrunk_hp_pava,
        "retention_delta": retention_delta,
        "consistency_score": consistency_score,
        "adaptability_score": adaptability_score,
        "tot_balls": tot_balls,
        "tot_hp_balls": tot_hp_balls,
        "tot_matches": tot_matches
    }


def run_match_clustered_bootstrap(
    deliveries_df: pd.DataFrame,
    n_iterations: int = 2000,
    seed: int = 42,
    is_batting: bool = True
) -> pd.DataFrame:
    """
    Run 2,000 match-clustered bootstrap resamples with exact ranking harmonization (P0-5).
    """
    logger.info(f"Building pre-aggregated matrices for {'Batting' if is_batting else 'Bowling'}...")
    mats = build_player_match_matrices(deliveries_df, is_batting=is_batting)
    n_matches = mats["n_matches"]
    n_players = mats["n_players"]
    player_ids = mats["player_ids"]
    name_map = mats["name_map"]
    
    # 1. Baseline Evaluation (k = 1 for all matches)
    k_base = np.ones(n_matches, dtype=np.float64)
    base_scores, base_eligible, _ = evaluate_scores_vectorized(mats, k_base)
    
    # Baseline ranks among eligible players
    base_ranks = np.full(n_players, 9999, dtype=np.int32)
    eligible_idx = np.where(base_eligible)[0]
    sub_scores = base_scores[eligible_idx]
    sub_ranks = np.argsort(np.argsort(-sub_scores)) + 1
    base_ranks[eligible_idx] = sub_ranks
    
    logger.info(f"Baseline eligible players: {len(eligible_idx)} / {n_players}")
    
    # 2. Resampling Loop
    np.random.seed(seed)
    score_dist = np.zeros((n_iterations, len(eligible_idx)), dtype=np.float32)
    rank_dist = np.zeros((n_iterations, len(eligible_idx)), dtype=np.int32)
    top10_counts = np.zeros(len(eligible_idx), dtype=np.int32)
    
    for b in range(n_iterations):
        # Sample match indices with replacement
        sampled = np.random.randint(0, n_matches, size=n_matches)
        k_vec = np.bincount(sampled, minlength=n_matches).astype(np.float64)
        
        scores, eligible, _ = evaluate_scores_vectorized(mats, k_vec)
        
        # Rank only eligible players in this resample
        resample_eligible_idx = np.where(eligible)[0]
        n_res_el = len(resample_eligible_idx)
        
        # Ranks for all players: default tail rank = n_res_el + 1
        current_ranks = np.full(n_players, n_res_el + 1, dtype=np.int32)
        if n_res_el > 0:
            res_scores = scores[resample_eligible_idx]
            res_ranks = np.argsort(np.argsort(-res_scores)) + 1
            current_ranks[resample_eligible_idx] = res_ranks
            
        score_dist[b] = scores[eligible_idx]
        rank_dist[b] = current_ranks[eligible_idx]
        top10_counts += (current_ranks[eligible_idx] <= 10).astype(np.int32)
        
    # 3. Compile output summary
    rows = []
    for i, idx in enumerate(eligible_idx):
        pid = player_ids[idx]
        p_scores = score_dist[:, i]
        p_ranks = rank_dist[:, i]
        
        rows.append({
            "player_id": pid,
            "player_name": name_map[pid],
            "baseline_rank": int(base_ranks[idx]),
            "baseline_score": round(float(base_scores[idx]), 2),
            "boot_mean_score": round(float(np.mean(p_scores)), 2),
            "boot_se_score": round(float(np.std(p_scores)), 2),
            "boot_score_ci_lower_95": round(float(np.percentile(p_scores, 2.5)), 2),
            "boot_score_ci_upper_95": round(float(np.percentile(p_scores, 97.5)), 2),
            "top10_inclusion_prob": round(float(top10_counts[i] / n_iterations), 4),
            "boot_mean_rank": round(float(np.mean(p_ranks)), 1),
            "boot_median_rank": int(np.median(p_ranks)),
            "boot_rank_ci_lower_95": int(np.percentile(p_ranks, 2.5)),
            "boot_rank_ci_upper_95": int(np.percentile(p_ranks, 97.5)),
        })
        
    out_df = pd.DataFrame(rows).sort_values("baseline_rank").reset_index(drop=True)
    return out_df
