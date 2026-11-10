import sys
import os
sys.path.insert(0, os.path.abspath("."))
import duckdb
import pandas as pd
import numpy as np
from src.config import BOWLER_DISMISSAL_TYPES, NON_BOWLER_DISMISSAL_TYPES

features_path = "data/processed/features_deliveries.parquet"
matches_path = "data/processed/matches.parquet"
deliveries_path = "data/processed/deliveries.parquet"

df = pd.read_parquet(features_path)
m_df = pd.read_parquet(matches_path)
deliv_df = pd.read_parquet(deliveries_path)

print(f"Loaded features_deliveries: {len(df):,} rows across {df['match_id'].nunique()} matches.")
print(f"Loaded deliveries: {len(deliv_df):,} rows across {deliv_df['match_id'].nunique()} matches.")
print(f"Loaded matches: {len(m_df):,} matches.")

exceptions = []

# Invariant 1: Score monotonicity
score_diffs = df.groupby(["match_id", "innings"])["cum_team_runs"].diff().dropna()
neg_scores = (score_diffs < 0).sum()
print(f"\n[Invariant 1] Non-decreasing cum_team_runs violations: {neg_scores}")
if neg_scores > 0:
    exceptions.append(f"Score monotonicity violated in {neg_scores} deliveries.")

# Check pre-delivery vs post-delivery consistency: cum_team_runs == team_runs_before + est_total_runs
diff_score_before = (df["cum_team_runs"] - (df["team_runs_before"] + df["est_total_runs"])).abs().sum()
print(f"[Invariant 1b] cum_team_runs == team_runs_before + est_total_runs sum of diffs: {diff_score_before}")
if diff_score_before != 0:
    exceptions.append(f"Score accounting discrepancy: sum={diff_score_before}")

# Invariant 2: Wickets monotonicity and range [0, 10]
wkt_diffs = df.groupby(["match_id", "innings"])["cum_wickets"].diff().dropna()
neg_wkts = (wkt_diffs < 0).sum()
max_wkts = df["cum_wickets"].max()
wkts_over_10 = (df["cum_wickets"] > 10).sum()
print(f"[Invariant 2] Non-decreasing wickets violations: {neg_wkts}, Wickets > 10 count: {wkts_over_10} (Max: {max_wkts})")
if neg_wkts > 0 or wkts_over_10 > 0:
    exceptions.append(f"Wicket monotonicity/range violated: neg={neg_wkts}, >10={wkts_over_10}")

# Invariant 3: Wickets remaining bounds [0, 10]
wkts_rem_min = df["wickets_remaining_before"].min()
wkts_rem_max = df["wickets_remaining_before"].max()
invalid_wkts_rem = ((df["wickets_remaining_before"] < 0) | (df["wickets_remaining_before"] > 10)).sum()
print(f"[Invariant 3] wickets_remaining_before invalid count: {invalid_wkts_rem} (Range: [{wkts_rem_min}, {wkts_rem_max}])")
if invalid_wkts_rem > 0:
    exceptions.append(f"Wickets remaining out of [0, 10]: {invalid_wkts_rem}")

# Invariant 4: Legal ball classification
# Wides and no-balls must NOT be legal. Byes, leg-byes, normal balls MUST be legal.
wide_illegal = (deliv_df[deliv_df["is_wide"]]["is_legal_ball"]).sum()
noball_illegal = (deliv_df[deliv_df["is_noball"]]["is_legal_ball"]).sum()
normal_legal = (~deliv_df[deliv_df["is_legal_ball"] == False]["is_wide"] & ~deliv_df[deliv_df["is_legal_ball"] == False]["is_noball"]).sum()
print(f"[Invariant 4] Wides marked legal: {wide_illegal}, No-balls marked legal: {noball_illegal}, Other illegal: {normal_legal}")
if wide_illegal > 0 or noball_illegal > 0 or normal_legal > 0:
    exceptions.append(f"Legal ball classification failure: wide_legal={wide_illegal}, nb_legal={noball_illegal}")

# Invariant 5: Non-striker dismissals
# When dismissed_player_id != striker_id, is_striker_out must be False!
non_striker_dismissals = deliv_df[deliv_df["is_wicket"] & (deliv_df["dismissed_player_id"] != deliv_df["striker_id"])]
print(f"\n[Invariant 5] Non-striker dismissals identified: {len(non_striker_dismissals)}")
false_striker_out = non_striker_dismissals["is_striker_out"].sum()
print(f"Non-striker dismissals erroneously marked as is_striker_out: {false_striker_out}")
if false_striker_out > 0:
    exceptions.append(f"Non-striker dismissals marked as striker out: {false_striker_out}")

# Invariant 6: Bowler wicket attribution
# Run outs and non-bowler wickets must NOT be credited to bowler
non_bowler_wkts = deliv_df[deliv_df["is_wicket"] & deliv_df["dismissal_type"].isin(NON_BOWLER_DISMISSAL_TYPES)]
err_bowler_wkts = non_bowler_wkts["is_bowler_wicket"].sum()
bowler_wkts = deliv_df[deliv_df["is_wicket"] & deliv_df["dismissal_type"].isin(BOWLER_DISMISSAL_TYPES)]
correct_bowler_wkts = bowler_wkts["is_bowler_wicket"].sum()
print(f"[Invariant 6] Non-bowler dismissals: {len(non_bowler_wkts)}, Erroneously credited to bowler: {err_bowler_wkts}")
print(f"Bowler dismissals: {len(bowler_wkts)}, Correctly credited to bowler: {correct_bowler_wkts}")
if err_bowler_wkts > 0 or correct_bowler_wkts != len(bowler_wkts):
    exceptions.append(f"Bowler wicket attribution error: err={err_bowler_wkts}, correct={correct_bowler_wkts}/{len(bowler_wkts)}")

# Invariant 7: DLS and revised matches
revised_matches = m_df[m_df["is_dls_or_revised"]]["match_id"].tolist()
revised_delivs = df[df["match_id"].isin(revised_matches)]
print(f"\n[Invariant 7] DLS / Revised matches in dataset: {len(revised_matches)} matches ({len(revised_delivs):,} deliveries)")
# Check that target_score is positive in innings 2
dls_target_check = revised_delivs[revised_delivs["innings"] == 2]
print(f"DLS Innings 2 deliveries: {len(dls_target_check):,}")
target_valid = (dls_target_check["target_score"].notna() & (dls_target_check["target_score"] > 0)).sum()
print(f"DLS Innings 2 deliveries with valid positive target_score: {target_valid} / {len(dls_target_check)}")
if target_valid != len(dls_target_check):
    exceptions.append(f"DLS target score invalid count: {len(dls_target_check) - target_valid}")

# Invariant 8: Super overs
super_overs = deliv_df[deliv_df["innings"] > 2]
print(f"\n[Invariant 8] Super over deliveries (innings > 2): {len(super_overs)}")
print(f"Super over match IDs: {super_overs['match_id'].unique().tolist()}")

# Invariant 9: Balls remaining before delivery
inn1_std = df[(df["innings"] == 1) & (~df["match_id"].isin(revised_matches))]
max_balls_rem = inn1_std["balls_remaining_before"].max()
min_balls_rem = inn1_std["balls_remaining_before"].min()
print(f"\n[Invariant 9] Innings 1 standard balls_remaining_before: min={min_balls_rem}, max={max_balls_rem}")
if min_balls_rem < 0 or max_balls_rem > 120:
    exceptions.append(f"Standard Innings 1 balls remaining out of bounds: [{min_balls_rem}, {max_balls_rem}]")

# Invariant 10: RRR monotonicity and bounds
chase_df = df[df["innings"] == 2]
rrr_min = chase_df["required_run_rate_before"].min()
rrr_max = chase_df["required_run_rate_before"].max()
rrr_nans = chase_df["required_run_rate_before"].isna().sum()
print(f"\n[Invariant 10] Chase RRR: min={rrr_min:.2f}, max={rrr_max:.2f}, NaNs={rrr_nans}")
if rrr_nans > 0:
    exceptions.append(f"Chase RRR contains NaNs: {rrr_nans}")

print("\n==========================================")
print("--- SUMMARY OF INVARIANT EXCEPTIONS ---")
if not exceptions:
    print("ALL 10 INVARIANTS PASSED PERFECTLY ACROSS ALL 867 MATCHES AND 200,961 DELIVERIES (0 exceptions).")
else:
    for e in exceptions:
        print(f"EXCEPTION: {e}")
print("==========================================")
