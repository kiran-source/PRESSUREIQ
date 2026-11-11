import pandas as pd
import numpy as np

deliv = pd.read_parquet('data/processed/deliveries_with_pava.parquet')
bat_boot = pd.read_parquet('data/processed/bootstrap_2000_batters.parquet')
bowl_boot = pd.read_parquet('data/processed/bootstrap_2000_bowlers.parquet')
bat_rank = pd.read_csv('data/processed/final_batter_rankings.csv')
bowl_rank = pd.read_csv('data/processed/final_bowler_rankings.csv')

print("=" * 120)
print("BATTER BOOTSTRAP METRICS (2,000 RESAMPLES)")
print("=" * 120)
for idx, row in bat_boot.head(10).iterrows():
    pname = row['player_name']
    sub = deliv[deliv['striker_name'] == pname]
    hp_sub = sub[sub['bpi'] >= 50.0]
    total_m = sub['match_id'].nunique()
    hp_m = hp_sub['match_id'].nunique()
    tot_b = len(sub[sub['is_batter_ball']])
    hp_b = len(hp_sub[hp_sub['is_batter_ball']])
    
    # Kish ESS
    # w_i = (1.0 + hp_sub['bpi'] / 50.0).values
    w_i = (1.0 + hp_sub['bpi'] / 50.0).values
    kish_ess = (np.sum(w_i)**2) / np.sum(w_i**2) if len(w_i) > 0 else 0.0
    
    print(f"Rank {row['baseline_rank']:<2} | {pname:<18} | Score: {row['baseline_score']:<5.2f} | Mean: {row['boot_mean_score']:<5.2f} (SD: {row['boot_se_score']:<5.2f}) | CI: [{row['boot_score_ci_lower_95']:<5.2f}, {row['boot_score_ci_upper_95']:<5.2f}] | Top10: {row['top10_inclusion_prob']:<6.4f} | MedRank: {row['boot_median_rank']:<3.0f} | RankCI: [{row['boot_rank_ci_lower_95']:<2.0f}, {row['boot_rank_ci_upper_95']:<3.0f}] | Matches: {total_m:<3} | HP_Matches: {hp_m:<2} | HP_Balls: {hp_b:<3} | KishESS: {kish_ess:<5.1f}")

print("\n" + "=" * 120)
print("BOWLER BOOTSTRAP METRICS (2,000 RESAMPLES)")
print("=" * 120)
for idx, row in bowl_boot.head(10).iterrows():
    pname = row['player_name']
    sub = deliv[deliv['bowler_name'] == pname]
    hp_sub = sub[sub['bopi'] >= 50.0]
    total_m = sub['match_id'].nunique()
    hp_m = hp_sub['match_id'].nunique()
    tot_b = len(sub[sub['is_legal_ball']])
    hp_b = len(hp_sub[hp_sub['is_legal_ball']])
    
    w_i = (1.0 + hp_sub['bopi'] / 50.0).values
    kish_ess = (np.sum(w_i)**2) / np.sum(w_i**2) if len(w_i) > 0 else 0.0
    
    print(f"Rank {row['baseline_rank']:<2} | {pname:<18} | Score: {row['baseline_score']:<5.2f} | Mean: {row['boot_mean_score']:<5.2f} (SD: {row['boot_se_score']:<5.2f}) | CI: [{row['boot_score_ci_lower_95']:<5.2f}, {row['boot_score_ci_upper_95']:<5.2f}] | Top10: {row['top10_inclusion_prob']:<6.4f} | MedRank: {row['boot_median_rank']:<3.0f} | RankCI: [{row['boot_rank_ci_lower_95']:<2.0f}, {row['boot_rank_ci_upper_95']:<3.0f}] | Matches: {total_m:<3} | HP_Matches: {hp_m:<2} | HP_Balls: {hp_b:<3} | KishESS: {kish_ess:<5.1f}")

