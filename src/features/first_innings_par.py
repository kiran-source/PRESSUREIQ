"""First innings par trajectory modeling for PRESSUREIQ.

In the 1st innings, teams do not have a chase target or required run rate.
This module estimates the context-aware par final score trajectory using
historical resource utilization curves (wickets in hand vs. balls remaining).
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple


def fit_par_resource_table(df_inn1: pd.DataFrame) -> pd.DataFrame:
    """
    Compute average runs scored in the remainder of innings 1
    conditioned on (comp_category, balls_remaining_bucket, wickets_remaining).
    """
    # Group into 6-ball over buckets (0-5, 6-11, ... 114-120)
    df = df_inn1.copy()
    df["over_bucket"] = (df["balls_remaining_before"] // 6) * 6
    
    # Calculate actual remaining runs scored in the innings after this ball
    # grp final score minus score before
    grp = df.groupby(["match_id", "innings"], sort=False)
    final_scores = grp["team_runs_before"].transform("last") + grp["est_total_runs"].transform("last")
    df["actual_remaining_runs"] = final_scores - df["team_runs_before"]
    
    # Resource lookup table
    res_table = df.groupby(
        ["comp_category", "over_bucket", "wickets_remaining_before"]
    )["actual_remaining_runs"].agg(["mean", "count"]).reset_index()
    res_table.rename(columns={"mean": "expected_remaining_runs"}, inplace=True)
    
    return res_table


class FirstInningsParModel:
    """Estimates par final score and score deviation for 1st innings deliveries."""
    
    def __init__(self):
        # Default global empirical lookup matrix (overs_remaining x wickets_remaining)
        # Calibrated on modern T20/IPL scoring baselines (~165-175 avg par)
        self.baseline_par = 168.0
        self.lookup_table: Dict[Tuple[str, int, int], float] = {}
        
    def fit(self, deliveries_df: pd.DataFrame):
        """Fit empirical par expectations on 1st innings deliveries."""
        inn1 = deliveries_df[
            (deliveries_df["innings"] == 1) & 
            (deliveries_df["balls_remaining_before"] <= 120)
        ].copy()
        
        if len(inn1) == 0:
            return
            
        grp = inn1.groupby(["match_id", "innings"], sort=False)
        final_scores = grp["team_runs_before"].transform("last") + grp["est_total_runs"].transform("last")
        inn1["actual_remaining_runs"] = np.maximum(0, final_scores - inn1["team_runs_before"])
        
        # Over bucket (in units of 6 balls)
        inn1["over_bucket"] = (inn1["balls_remaining_before"] // 6) * 6
        
        # Mean remaining runs
        agg = inn1.groupby(
            ["comp_category", "over_bucket", "wickets_remaining_before"]
        )["actual_remaining_runs"].mean()
        
        self.lookup_table = agg.to_dict()
        self.baseline_par = float(inn1.groupby("match_id")["est_total_runs"].sum().mean())
        
    def estimate_par_trajectory(self, row_comp: str, balls_rem: int, wkts_rem: int, score_before: int) -> Tuple[float, float]:
        """
        Estimate (par_final_score, runs_above_par_trajectory).
        
        par_final_score = current_score + expected_remaining_runs
        runs_above_par_trajectory = current_score - par_expected_at_this_ball
        """
        over_bucket = int((balls_rem // 6) * 6)
        wkts_rem = int(np.clip(wkts_rem, 0, 10))
        
        # Lookup expected remaining runs
        key = (row_comp, over_bucket, wkts_rem)
        if key in self.lookup_table:
            expected_remaining = self.lookup_table[key]
        else:
            # Calibrated resource decay anchored so that at 20 overs, 10 wickets = 1.0 (100% resources)
            overs_rem = balls_rem / 6.0
            norm_factor = 1.0 - np.exp(-0.12 * 20.0)
            ball_factor = (1.0 - np.exp(-0.12 * overs_rem)) / norm_factor
            wkt_factor = (wkts_rem / 10.0) ** 0.65
            resource_pct = np.clip(ball_factor * wkt_factor, 0.0, 1.0)
            expected_remaining = self.baseline_par * resource_pct
            
        par_final_score = score_before + expected_remaining
        
        # Pro-rated expected score at current ball assuming linear/convex path
        balls_bowled = 120 - balls_rem
        if balls_bowled <= 0:
            par_at_ball = 0.0
        else:
            # Fraction of par expected by this ball
            frac = balls_bowled / 120.0
            par_at_ball = par_final_score * frac
            
        runs_above_par = score_before - par_at_ball
        return float(par_final_score), float(runs_above_par)
