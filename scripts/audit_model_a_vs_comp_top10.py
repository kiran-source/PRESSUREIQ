"""Comprehensive comparison between frozen Model A rankings and final competition top 10 CSVs."""

import numpy as np
import pandas as pd
from pathlib import Path

def audit_comparison():
    fb_a = pd.read_csv("data/processed/final_batter_rankings.csv")
    fb_c = pd.read_csv("data/processed/final_competition_batter_top10.csv")
    fw_a = pd.read_csv("data/processed/final_bowler_rankings.csv")
    fw_c = pd.read_csv("data/processed/final_competition_bowler_top10.csv")

    report = []
    report.append("# EXACT COMPARISON REPORT: MODEL A vs FINAL COMPETITION TOP 10\n")

    for disc, df_a, df_c in [("BATTERS", fb_a, fb_c), ("BOWLERS", fw_a, fw_c)]:
        top10_a = df_a.head(10).copy()
        report.append(f"## {disc} VERIFICATION")
        report.append(f"- Model A total evaluated rows: {len(df_a)} (Top 10 slice extracted for competition)")
        report.append(f"- Final Competition rows: {len(df_c)}")
        report.append(f"- Model A column count: {len(df_a.columns)}")
        report.append(f"- Final Competition column count: {len(df_c.columns)}")
        
        extra_in_comp = [c for c in df_c.columns if c not in df_a.columns]
        extra_in_a = [c for c in df_a.columns if c not in df_c.columns]
        report.append(f"- Columns unique to Competition deliverable: {extra_in_comp}")
        report.append(f"- Columns unique to Model A full table: {extra_in_a}")
        
        report.append("\n### Rank-by-Rank Value Parity:")
        all_match = True
        for i in range(10):
            ra = top10_a.iloc[i]
            rc = df_c.iloc[i]
            id_match = int(ra["player_id"]) == int(rc["player_id"])
            name_match = str(ra["player_name"]).strip() == str(rc["player_name"]).strip()
            score_match = bool(np.isclose(float(ra["reliability_score"]), float(rc["reliability_score"]), atol=1e-5))
            rank_match = int(ra["rank"]) == int(rc["rank"])
            
            row_ok = id_match and name_match and score_match and rank_match
            if not row_ok:
                all_match = False
            
            report.append(
                f"- Rank {i+1}: {ra['player_name']} (ID {ra['player_id']}) | "
                f"Model A Score: {ra['reliability_score']:.4f} | "
                f"Comp Score: {rc['reliability_score']:.4f} | "
                f"Match: {'PASS' if row_ok else 'FAIL'}"
            )
        
        report.append(f"\nAll 10 {disc} ranks, IDs, names, and scores match: **{'PASS' if all_match else 'FAIL'}**\n")
        
        # Check all common columns
        common_cols = [c for c in top10_a.columns if c in df_c.columns]
        common_diffs = []
        for c in common_cols:
            sa = top10_a[c].values
            sc = df_c[c].values
            if np.issubdtype(sa.dtype, np.number):
                if not np.allclose(sa, sc, equal_nan=True):
                    common_diffs.append(c)
            else:
                if not (sa == sc).all():
                    common_diffs.append(c)
        report.append(f"- Common columns evaluated: {len(common_cols)}")
        report.append(f"- Differing common columns: {common_diffs if common_diffs else 'None (100% Identical)'}")
        
        # Null values
        null_a = dict(top10_a.isnull().sum()[top10_a.isnull().sum() > 0])
        null_c = dict(df_c.isnull().sum()[df_c.isnull().sum() > 0])
        report.append(f"- Top 10 Model A null values: {null_a if null_a else 'None'}")
        report.append(f"- Final Competition null values: {null_c if null_c else 'None'}\n")

    output_text = "\n".join(report)
    print(output_text)

    # Also save to audit directory
    out_path = Path("audit/final_v64/EXACT_MODEL_A_VS_COMPETITION_TOP10_AUDIT.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output_text, encoding="utf-8")
    print(f"\nSaved report to {out_path}")

if __name__ == "__main__":
    audit_comparison()
