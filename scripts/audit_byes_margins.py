import duckdb
import pandas as pd
import re
import numpy as np

raw_bbb = "SupeRR Selector Season 2 _ Problem Statement _ Data Pack/SupeRR Selector Season 2 _ Data Pack/ball_by_ball.csv"
raw_matches = "SupeRR Selector Season 2 _ Problem Statement _ Data Pack/SupeRR Selector Season 2 _ Data Pack/matches.csv"

con = duckdb.connect()

# Extract run margin from matches.csv
matches_df = con.execute(f"""
    SELECT match_id, comp_id, result
    FROM read_csv_auto('{raw_matches}')
    WHERE lower(result) LIKE '%won by%run%'
""").fetchdf()

def extract_margin(res):
    m = re.search(r'won by\s+(\d+)\s+run', res, re.IGNORECASE)
    return int(m.group(1)) if m else None

matches_df["official_margin"] = matches_df["result"].apply(extract_margin)
matches_df = matches_df.dropna(subset=["official_margin"])
print(f"Parsed official run margins for {len(matches_df)} matches.")

# Reconstruct innings 1 and innings 2 totals under Treatment 1 (byes/legbyes = 1 run) and Treatment 0 (byes/legbyes = 0 runs)
bbb_df = con.execute(f"""
    SELECT match_id, innings, runs, extras_type, extras1_runs, extras_2_runs
    FROM read_csv_auto('{raw_bbb}')
    WHERE innings IN (1, 2)
""").fetchdf()

# Merge
df = bbb_df.merge(matches_df[["match_id", "official_margin"]], on="match_id", how="inner")

extras_lower = df["extras_type"].fillna("none").str.lower()
is_wide = extras_lower == "wide"
is_noball = extras_lower.isin(["overstep", "other"])
is_legbye = extras_lower == "legbyes"
is_bye = extras_lower == "byes"
is_penalty = extras_lower == "penalty"

# Treatment 1: max(1, extras_2) -> 1 run for byes/legbyes
runs_t1 = np.where(
    is_wide, 1 + df["extras_2_runs"],
    np.where(
        is_noball, 1 + df["runs"] + df["extras_2_runs"],
        np.where(
            is_legbye | is_bye, np.maximum(1, df["extras_2_runs"]),
            np.where(is_penalty, 5, df["runs"])
        )
    )
)

# Treatment 0: 0 runs for byes/legbyes unless recorded in runs or extras_2
runs_t0 = np.where(
    is_wide, 1 + df["extras_2_runs"],
    np.where(
        is_noball, 1 + df["runs"] + df["extras_2_runs"],
        np.where(
            is_legbye | is_bye, df["runs"] + df["extras_2_runs"],
            np.where(is_penalty, 5, df["runs"])
        )
    )
)

df["runs_t1"] = runs_t1
df["runs_t0"] = runs_t0

# Innings totals
inn_totals = df.groupby(["match_id", "innings"]).agg({
    "runs_t1": "sum",
    "runs_t0": "sum",
    "official_margin": "first"
}).unstack(level=1)

inn1_t1 = inn_totals["runs_t1"][1]
inn2_t1 = inn_totals["runs_t1"][2]
margin_t1 = inn1_t1 - inn2_t1

inn1_t0 = inn_totals["runs_t0"][1]
inn2_t0 = inn_totals["runs_t0"][2]
margin_t0 = inn1_t0 - inn2_t0

official = inn_totals["official_margin"][1]

diff_t1 = margin_t1 - official
diff_t0 = margin_t0 - official

valid_mask = diff_t1.notna() & diff_t0.notna()

diff_t1 = diff_t1[valid_mask]
diff_t0 = diff_t0[valid_mask]

print("\n--- TREATMENT 1: Byes/Legbyes = 1 run (Current Heuristic max(1, extras_2)) ---")
print(f"Exact match count: {(diff_t1 == 0).sum()} / {len(diff_t1)} ({(diff_t1 == 0).mean()*100:.1f}%)")
print(f"Within +/- 1 run: {(diff_t1.abs() <= 1).sum()} / {len(diff_t1)} ({(diff_t1.abs() <= 1).mean()*100:.1f}%)")
print(f"Mean error: {diff_t1.mean():.3f}, Median error: {diff_t1.median():.3f}, Std: {diff_t1.std():.3f}")
print(f"MAE: {diff_t1.abs().mean():.3f}")

print("\n--- TREATMENT 0: Byes/Legbyes = 0 runs (Raw Recorded Only) ---")
print(f"Exact match count: {(diff_t0 == 0).sum()} / {len(diff_t0)} ({(diff_t0 == 0).mean()*100:.1f}%)")
print(f"Within +/- 1 run: {(diff_t0.abs() <= 1).sum()} / {len(diff_t0)} ({(diff_t0.abs() <= 1).mean()*100:.1f}%)")
print(f"Mean error: {diff_t0.mean():.3f}, Median error: {diff_t0.median():.3f}, Std: {diff_t0.std():.3f}")
print(f"MAE: {diff_t0.abs().mean():.3f}")

print("\nDistribution of (margin_reconstructed - official_margin) in Treatment 1:")
print(diff_t1.value_counts().sort_index().head(15))
