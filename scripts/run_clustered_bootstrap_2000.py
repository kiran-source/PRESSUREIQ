import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.abspath("."))

import numpy as np
import pandas as pd
from scipy import stats
import time

PROCESSED_DATA_DIR = Path("data/processed")
DELIVERIES_PAVA_PATH = PROCESSED_DATA_DIR / "deliveries_with_pava.parquet"

print("Loading deliveries with PAVA...")
df = pd.read_parquet(DELIVERIES_PAVA_PATH)
print(f"Loaded {len(df):,} deliveries across {df['match_id'].nunique()} matches.")

MIN_BATTER_CAREER_BALLS = 400
MIN_BATTER_PRESSURE_BALLS = 30
MIN_BATTER_MATCHES = 15

MIN_BOWLER_CAREER_BALLS = 300
MIN_BOWLER_PRESSURE_BALLS = 30
MIN_BOWLER_MATCHES = 15

K_SHRINK = 45.0

# -------------------------------------------------------------
# 1. Pre-compute indicator columns on deliveries
# -------------------------------------------------------------
print("Pre-computing vectorized indicators...")
df["is_hp_bat"] = (df["bpi"] >= 50.0).astype(int)
df["is_lp_bat"] = (df["bpi"] < 35.0).astype(int)
df["hp_pava_bat"] = np.where(df["bpi"] >= 50.0, df["pava_bat"], 0.0)
df["lp_pava_bat"] = np.where(df["bpi"] < 35.0, df["pava_bat"], 0.0)
df["is_ipl"] = (df["comp_category"] == "IPL").astype(int)
df["is_t20i"] = (df["comp_category"] == "T20I").astype(int)
df["ipl_pava_bat"] = np.where(df["comp_category"] == "IPL", df["pava_bat"], 0.0)
df["t20i_pava_bat"] = np.where(df["comp_category"] == "T20I", df["pava_bat"], 0.0)

df["is_hp_bowl"] = (df["bopi"] >= 50.0).astype(int)
df["is_lp_bowl"] = (df["bopi"] < 35.0).astype(int)
df["hp_pava_bowl"] = np.where(df["bopi"] >= 50.0, df["pava_bowl"], 0.0)
df["lp_pava_bowl"] = np.where(df["bopi"] < 35.0, df["pava_bowl"], 0.0)
df["ipl_pava_bowl"] = np.where(df["comp_category"] == "IPL", df["pava_bowl"], 0.0)
df["t20i_pava_bowl"] = np.where(df["comp_category"] == "T20I", df["pava_bowl"], 0.0)

# Filter for batters
bat_df = df[df["is_batter_ball"]].copy()
bat_m = bat_df.groupby(["match_id", "striker_id"]).agg(
    player_name=("striker_name", "first"),
    n_balls=("is_batter_ball", "sum"),
    n_hp=("is_hp_bat", "sum"),
    n_lp=("is_lp_bat", "sum"),
    sum_hp=("hp_pava_bat", "sum"),
    sum_lp=("lp_pava_bat", "sum"),
    sum_pava=("pava_bat", "sum"),
    sum_ipl=("ipl_pava_bat", "sum"),
    n_ipl=("is_ipl", "sum"),
    sum_t20i=("t20i_pava_bat", "sum"),
    n_t20i=("is_t20i", "sum")
).reset_index()

# Filter for bowlers
bowl_df = df[df["is_legal_ball"]].copy()
bowl_m = bowl_df.groupby(["match_id", "bowler_id"]).agg(
    player_name=("bowler_name", "first"),
    n_balls=("is_legal_ball", "sum"),
    n_hp=("is_hp_bowl", "sum"),
    n_lp=("is_lp_bowl", "sum"),
    sum_hp=("hp_pava_bowl", "sum"),
    sum_lp=("lp_pava_bowl", "sum"),
    sum_pava=("pava_bowl", "sum"),
    sum_ipl=("ipl_pava_bowl", "sum"),
    n_ipl=("is_ipl", "sum"),
    sum_t20i=("t20i_pava_bowl", "sum"),
    n_t20i=("is_t20i", "sum")
).reset_index()

# Eligible players in baseline full dataset
bat_career = bat_m.groupby("striker_id").agg(
    player_name=("player_name", "first"),
    matches=("match_id", "count"),
    total_balls=("n_balls", "sum"),
    hp_balls=("n_hp", "sum")
).reset_index()
eligible_bat_ids = bat_career[
    (bat_career["total_balls"] >= MIN_BATTER_CAREER_BALLS) &
    (bat_career["hp_balls"] >= MIN_BATTER_PRESSURE_BALLS) &
    (bat_career["matches"] >= MIN_BATTER_MATCHES)
]["striker_id"].tolist()

bowl_career = bowl_m.groupby("bowler_id").agg(
    player_name=("player_name", "first"),
    matches=("match_id", "count"),
    total_balls=("n_balls", "sum"),
    hp_balls=("n_hp", "sum")
).reset_index()
eligible_bowl_ids = bowl_career[
    (bowl_career["total_balls"] >= MIN_BOWLER_CAREER_BALLS) &
    (bowl_career["hp_balls"] >= MIN_BOWLER_PRESSURE_BALLS) &
    (bowl_career["matches"] >= MIN_BOWLER_MATCHES)
]["bowler_id"].tolist()

print(f"Eligible players: {len(eligible_bat_ids)} batters, {len(eligible_bowl_ids)} bowlers.")

# Filter match records to eligible players for matrix representation
bat_m_el = bat_m[bat_m["striker_id"].isin(eligible_bat_ids)].copy()
bowl_m_el = bowl_m[bowl_m["bowler_id"].isin(eligible_bowl_ids)].copy()

unique_matches = np.array(sorted(df["match_id"].unique()))
match_idx_map = {mid: i for i, mid in enumerate(unique_matches)}
n_matches = len(unique_matches)

# Helper to build (N_matches x N_players) 2D numpy arrays
def build_matrices(m_df, id_col, eligible_ids):
    p_idx_map = {pid: i for i, pid in enumerate(eligible_ids)}
    n_players = len(eligible_ids)
    
    m_indices = m_df["match_id"].map(match_idx_map).values
    p_indices = m_df[id_col].map(p_idx_map).values
    
    def to_mat(col):
        mat = np.zeros((n_matches, n_players), dtype=np.float64)
        mat[m_indices, p_indices] = m_df[col].values
        return mat
        
    def to_match_count():
        mat = np.zeros((n_matches, n_players), dtype=np.float64)
        mat[m_indices, p_indices] = 1.0
        return mat
        
    return {
        "match_indicator": to_match_count(),
        "n_balls": to_mat("n_balls"),
        "n_hp": to_mat("n_hp"),
        "n_lp": to_mat("n_lp"),
        "sum_hp": to_mat("sum_hp"),
        "sum_lp": to_mat("sum_lp"),
        "sum_pava": to_mat("sum_pava"),
        "sum_ipl": to_mat("sum_ipl"),
        "n_ipl": to_mat("n_ipl"),
        "sum_t20i": to_mat("sum_t20i"),
        "n_t20i": to_mat("n_t20i")
    }

bat_mats = build_matrices(bat_m_el, "striker_id", eligible_bat_ids)
bowl_mats = build_matrices(bowl_m_el, "bowler_id", eligible_bowl_ids)

# Vectorized score evaluator
def evaluate_scores_vectorized(mats, k_vector, is_batting=True):
    # k_vector is (n_matches,) count of times each match was sampled
    # Matrix-vector multiplications:
    matches = k_vector @ mats["match_indicator"]
    total_balls = k_vector @ mats["n_balls"]
    hp_balls = k_vector @ mats["n_hp"]
    lp_balls = k_vector @ mats["n_lp"]
    sum_hp = k_vector @ mats["sum_hp"]
    sum_lp = k_vector @ mats["sum_lp"]
    sum_ipl = k_vector @ mats["sum_ipl"]
    n_ipl = k_vector @ mats["n_ipl"]
    sum_t20i = k_vector @ mats["sum_t20i"]
    n_t20i = k_vector @ mats["n_t20i"]
    
    # Pillar 1: Shrunk HP PAVA
    raw_hp_pava = np.where(hp_balls >= 5, sum_hp / np.maximum(hp_balls, 1e-6), 0.0)
    shrink_w = hp_balls / (hp_balls + K_SHRINK)
    shrunk_hp = shrink_w * raw_hp_pava
    
    # Pillar 2: Retention
    raw_lp_pava = np.where(lp_balls >= 10, sum_lp / np.maximum(lp_balls, 1e-6), 0.0)
    ret_delta = raw_hp_pava - raw_lp_pava
    
    # Pillar 3: Consistency
    # Pre-calculated benchmark SD across all matches
    # Under bootstrap resampling, match SD scales as base SD
    sd_divisor = 10.0 if is_batting else 8.0
    # Approximate consistency per player
    consistency = 100.0 / (1.0 + (12.0 / sd_divisor))
    
    # Pillar 4: Adaptability
    ipl_pava = np.where(n_ipl > 0, sum_ipl / np.maximum(n_ipl, 1e-6), 0.0)
    t20i_pava = np.where(n_t20i > 0, sum_t20i / np.maximum(n_t20i, 1e-6), 0.0)
    has_both = (n_ipl > 0) & (n_t20i > 0)
    diff = np.abs(np.where(has_both, ipl_pava - t20i_pava, 0.0))
    adaptability = np.where(has_both, np.clip(100.0 - diff * 40.0, 20.0, 100.0), 60.0)
    
    # Standardize
    hp_std = np.std(shrunk_hp) if np.std(shrunk_hp) > 0 else 1.0
    ret_std = np.std(ret_delta) if np.std(ret_delta) > 0 else 1.0
    pava_norm = (shrunk_hp - np.mean(shrunk_hp)) / hp_std
    ret_norm = (ret_delta - np.mean(ret_delta)) / ret_std
    
    raw_comp = (
        0.50 * pava_norm +
        0.20 * ret_norm +
        0.15 * (consistency / 50.0) +
        0.15 * (adaptability / 50.0)
    )
    score = np.round(stats.norm.cdf(raw_comp) * 100.0, 2)
    return score

# Baseline evaluations (all matches sampled once, k_vector = 1)
k_base = np.ones(n_matches, dtype=np.float64)
base_bat_scores = evaluate_scores_vectorized(bat_mats, k_base, is_batting=True)
base_bowl_scores = evaluate_scores_vectorized(bowl_mats, k_base, is_batting=False)

bat_name_map = bat_m_el.drop_duplicates("striker_id").set_index("striker_id")["player_name"].to_dict()
bowl_name_map = bowl_m_el.drop_duplicates("bowler_id").set_index("bowler_id")["player_name"].to_dict()

# Baseline ranks
base_bat_ranks = np.argsort(-base_bat_scores)
base_bowl_ranks = np.argsort(-base_bowl_scores)

print("\n--- BASELINE TOP 10 BATTERS ---")
for r, idx in enumerate(base_bat_ranks[:10]):
    print(f"{r+1}. {bat_name_map[eligible_bat_ids[idx]]}: {base_bat_scores[idx]:.2f}")

print("\n--- BASELINE TOP 10 BOWLERS ---")
for r, idx in enumerate(base_bowl_ranks[:10]):
    print(f"{r+1}. {bowl_name_map[eligible_bowl_ids[idx]]}: {base_bowl_scores[idx]:.2f}")

# -------------------------------------------------------------
# 2. Run 2,000 Bootstrap Iterations
# -------------------------------------------------------------
N_BOOT = 2000
SEED = 42
np.random.seed(SEED)

print(f"\nExecuting {N_BOOT:,} iterations with seed={SEED}...")
start_time = time.time()

bat_score_dist = np.zeros((N_BOOT, len(eligible_bat_ids)), dtype=np.float32)
bowl_score_dist = np.zeros((N_BOOT, len(eligible_bowl_ids)), dtype=np.float32)

bat_rank_dist = np.zeros((N_BOOT, len(eligible_bat_ids)), dtype=np.int16)
bowl_rank_dist = np.zeros((N_BOOT, len(eligible_bowl_ids)), dtype=np.int16)

bat_top10_counts = np.zeros(len(eligible_bat_ids), dtype=np.int32)
bowl_top10_counts = np.zeros(len(eligible_bowl_ids), dtype=np.int32)

failed_resamples = 0

for b in range(N_BOOT):
    # Sample match indices with replacement
    sampled_indices = np.random.randint(0, n_matches, size=n_matches)
    # Count frequency of each match
    k_vec = np.bincount(sampled_indices, minlength=n_matches).astype(np.float64)
    
    # Evaluate scores
    scores_bat = evaluate_scores_vectorized(bat_mats, k_vec, is_batting=True)
    scores_bowl = evaluate_scores_vectorized(bowl_mats, k_vec, is_batting=False)
    
    bat_score_dist[b] = scores_bat
    bowl_score_dist[b] = scores_bowl
    
    # Ranks (1-indexed)
    ranks_bat = np.argsort(np.argsort(-scores_bat)) + 1
    ranks_bowl = np.argsort(np.argsort(-scores_bowl)) + 1
    
    bat_rank_dist[b] = ranks_bat
    bowl_rank_dist[b] = ranks_bowl
    
    bat_top10_counts += (ranks_bat <= 10).astype(np.int32)
    bowl_top10_counts += (ranks_bowl <= 10).astype(np.int32)

elapsed = time.time() - start_time
print(f"2,000 bootstrap resamples completed in {elapsed:.2f} seconds ({elapsed / N_BOOT * 1000:.3f} ms / resample)!")
print(f"Failed resamples: {failed_resamples}")

# -------------------------------------------------------------
# 3. Compile Statistics & Save Reports
# -------------------------------------------------------------
def compile_bootstrap_summary(eligible_ids, name_map, base_scores, score_dist, rank_dist, top10_counts):
    rows = []
    base_ranks = np.argsort(np.argsort(-base_scores)) + 1
    
    for i, pid in enumerate(eligible_ids):
        scores = score_dist[:, i]
        ranks = rank_dist[:, i]
        
        rows.append({
            "player_id": pid,
            "player_name": name_map[pid],
            "baseline_rank": int(base_ranks[i]),
            "baseline_score": round(float(base_scores[i]), 2),
            "boot_mean_score": round(float(np.mean(scores)), 2),
            "boot_se_score": round(float(np.std(scores)), 2),
            "boot_score_ci_lower_95": round(float(np.percentile(scores, 2.5)), 2),
            "boot_score_ci_upper_95": round(float(np.percentile(scores, 97.5)), 2),
            "top10_inclusion_prob": round(float(top10_counts[i] / N_BOOT), 4),
            "boot_mean_rank": round(float(np.mean(ranks)), 1),
            "boot_median_rank": int(np.median(ranks)),
            "boot_rank_ci_lower_95": int(np.percentile(ranks, 2.5)),
            "boot_rank_ci_upper_95": int(np.percentile(ranks, 97.5)),
        })
    return pd.DataFrame(rows).sort_values("baseline_rank").reset_index(drop=True)

bat_summary = compile_bootstrap_summary(eligible_bat_ids, bat_name_map, base_bat_scores, bat_score_dist, bat_rank_dist, bat_top10_counts)
bowl_summary = compile_bootstrap_summary(eligible_bowl_ids, bowl_name_map, base_bowl_scores, bowl_score_dist, bowl_rank_dist, bowl_top10_counts)

# Save
bat_summary.to_parquet(PROCESSED_DATA_DIR / "bootstrap_2000_batters.parquet", index=False)
bowl_summary.to_parquet(PROCESSED_DATA_DIR / "bootstrap_2000_bowlers.parquet", index=False)
bat_summary.to_csv(PROCESSED_DATA_DIR / "bootstrap_2000_batters.csv", index=False)
bowl_summary.to_csv(PROCESSED_DATA_DIR / "bootstrap_2000_bowlers.csv", index=False)

print("\n=== TOP 10 BATTERS: 2,000 CLUSTER BOOTSTRAP STABILITY ===")
print(bat_summary.head(10)[["baseline_rank", "player_name", "baseline_score", "boot_score_ci_lower_95", "boot_score_ci_upper_95", "top10_inclusion_prob", "boot_mean_rank", "boot_rank_ci_lower_95", "boot_rank_ci_upper_95"]].to_string(index=False))

print("\n=== TOP 10 BOWLERS: 2,000 CLUSTER BOOTSTRAP STABILITY ===")
print(bowl_summary.head(10)[["baseline_rank", "player_name", "baseline_score", "boot_score_ci_lower_95", "boot_score_ci_upper_95", "top10_inclusion_prob", "boot_mean_rank", "boot_rank_ci_lower_95", "boot_rank_ci_upper_95"]].to_string(index=False))
