"""First innings par trajectory modeling for PRESSUREIQ.

In the 1st innings, teams do not have a chase target or required run rate.
This module estimates the context-aware par final score trajectory using
strictly chronological historical resource utilization curves (wickets in hand vs. balls remaining).

STRICT TEMPORAL CAUSALITY GUARANTEE:
A delivery in match M on date D NEVER uses the final score of match M or any
future matches (> M). Completed matches are ingested into the historical lookup
accumulator strictly AFTER match M has received its predictions.
"""

from typing import Dict, Tuple, Optional
import numpy as np
import pandas as pd

DEFAULT_BASELINE_PAR = 168.0
DEFAULT_K_PRIOR = 15.0


def calculate_analytical_par_prior(
    balls_rem: float,
    wkts_rem: float,
    baseline_par: float = DEFAULT_BASELINE_PAR,
    max_balls: float = 120.0
) -> float:
    """
    Duckworth-Lewis inspired analytical resource prior for T20 cricket.
    
    Resource decay function: Z(u, w) = Z_0 * [ (1 - exp(-b * u/6)) / (1 - exp(-b * 20)) ] * (w / 10)^alpha
    where u is balls remaining, w is wickets remaining.
    """
    if balls_rem <= 0 or wkts_rem <= 0:
        return 0.0
        
    overs_rem = balls_rem / 6.0
    norm_factor = 1.0 - np.exp(-0.12 * 20.0)
    ball_factor = (1.0 - np.exp(-0.12 * overs_rem)) / norm_factor
    wkt_factor = (wkts_rem / 10.0) ** 0.65
    resource_pct = np.clip(ball_factor * wkt_factor, 0.0, 1.0)
    
    # Scale appropriately for shortened matches
    match_length_scale = max_balls / 120.0
    return float(baseline_par * resource_pct * match_length_scale)


class FirstInningsParModel:
    """Estimates par final score and score deviation for 1st innings deliveries."""
    
    def __init__(self, baseline_par: float = DEFAULT_BASELINE_PAR, k_prior: float = DEFAULT_K_PRIOR):
        self.baseline_par = baseline_par
        self.k_prior = k_prior
        self.lookup_sum: Dict[Tuple[str, int, int], float] = {}
        self.lookup_cnt: Dict[Tuple[str, int, int], int] = {}
        self.lookup_table: Dict[Tuple[str, int, int], float] = {}
        
    def fit(self, deliveries_df: pd.DataFrame):
        """Fit empirical par lookup table (legacy batch interface)."""
        inn1 = deliveries_df[
            (deliveries_df["innings"] == 1) & 
            (deliveries_df["balls_remaining_before"] <= 120)
        ].copy()
        if len(inn1) == 0:
            return
            
        grp = inn1.groupby(["match_id", "innings"], sort=False)
        final_scores = grp["team_runs_before"].transform("last") + grp["est_total_runs"].transform("last")
        inn1["actual_remaining_runs"] = np.maximum(0, final_scores - inn1["team_runs_before"])
        inn1["over_bucket"] = (inn1["balls_remaining_before"] // 6) * 6
        agg = inn1.groupby(
            ["comp_category", "over_bucket", "wickets_remaining_before"]
        )["actual_remaining_runs"].mean()
        self.lookup_table = agg.to_dict()
        
    def estimate_par_trajectory(
        self,
        row_comp: str,
        balls_rem: int,
        wkts_rem: int,
        score_before: int
    ) -> Tuple[float, float]:
        """Estimate par final score and runs above par using lookup table or analytical prior."""
        over_bucket = int((balls_rem // 6) * 6)
        wkts_clean = int(np.clip(wkts_rem, 0, 10))
        key = (row_comp, over_bucket, wkts_clean)
        
        if key in self.lookup_table:
            expected_remaining = self.lookup_table[key]
        else:
            expected_remaining = calculate_analytical_par_prior(
                float(balls_rem), float(wkts_clean), self.baseline_par, 120.0
            )
            
        par_final = score_before + expected_remaining
        balls_bowled = 120 - balls_rem
        frac = balls_bowled / 120.0 if balls_bowled > 0 else 0.0
        par_at = par_final * frac
        return float(par_final), float(score_before - par_at)
        
    def estimate_single_delivery(
        self,
        comp_category: str,
        balls_rem: int,
        wkts_rem: int,
        score_before: int,
        legal_balls_before: int,
        max_balls: int = 120
    ) -> Tuple[float, float]:
        """Estimate par final score and runs above par trajectory for a single state."""
        over_bucket = int((balls_rem // 6) * 6)
        wkts_clean = int(np.clip(wkts_rem, 0, 10))
        max_b = float(np.maximum(1, max_balls))
        
        prior_val = calculate_analytical_par_prior(
            float(balls_rem), float(wkts_clean), self.baseline_par, max_b
        )
        
        key = (comp_category, over_bucket, wkts_clean)
        cnt = self.lookup_cnt.get(key, 0)
        if cnt > 0:
            exp_remaining = (self.lookup_sum[key] + self.k_prior * prior_val) / (cnt + self.k_prior)
        else:
            exp_remaining = prior_val
            
        par_final = score_before + exp_remaining
        
        # Pro-rated expected score at current legal delivery
        frac_elapsed = float(np.clip(legal_balls_before / max_b, 0.0, 1.0))
        par_at_ball = par_final * frac_elapsed
        runs_above_par = score_before - par_at_ball
        return float(par_final), float(runs_above_par)


def compute_chronological_first_innings_par(
    deliveries_df: pd.DataFrame,
    baseline_par: float = DEFAULT_BASELINE_PAR,
    k_prior: float = DEFAULT_K_PRIOR
) -> pd.DataFrame:
    """
    Compute strictly chronological, match-isolated 1st innings par trajectories.
    
    Guarantees:
    1. Zero same-match leakage: Completed outcome of match M is NEVER used for match M.
    2. Zero future-match leakage: Future matches (> M) are NEVER used for match M.
    3. Shortened innings physics: Uses max_innings_balls for trajectory proportions.
    
    Returns DataFrame indexed identical to deliveries_df with:
    - 'par_final_score'
    - 'runs_above_par_trajectory'
    """
    df = deliveries_df.copy()
    
    # Initialize output columns
    df["par_final_score"] = np.nan
    df["runs_above_par_trajectory"] = np.nan
    
    inn1_mask = df["innings"] == 1
    if not inn1_mask.any():
        return df
        
    inn1 = df[inn1_mask].copy()
    
    # Ensure chronological sorting
    sort_cols = ["match_date", "match_id", "overid", "over_ball_num", "innings_ball_num"]
    existing_sort_cols = [c for c in sort_cols if c in inn1.columns]
    inn1 = inn1.sort_values(by=existing_sort_cols)
    
    # Helper columns
    inn1["over_bucket"] = (inn1["balls_remaining_before"] // 6) * 6
    inn1["wkts_clean"] = np.clip(inn1["wickets_remaining_before"], 0, 10).astype(int)
    max_balls_col = inn1["max_innings_balls"].astype(float) if "max_innings_balls" in inn1.columns else np.full(len(inn1), 120.0)
    inn1["max_balls_clean"] = max_balls_col
    
    hist_sum: Dict[Tuple[str, int, int], float] = {}
    hist_cnt: Dict[Tuple[str, int, int], int] = {}
    
    par_final_results = []
    runs_above_results = []
    indices_order = []
    
    # Process match-by-match in strict temporal order
    for mid, m_df in inn1.groupby("match_id", sort=False):
        comps = m_df["comp_category"].values
        o_buks = m_df["over_bucket"].values
        w_rems = m_df["wkts_clean"].values
        s_befs = m_df["team_runs_before"].values
        b_rems = m_df["balls_remaining_before"].values
        b_elaps = m_df["legal_balls_before"].values
        m_balls = m_df["max_balls_clean"].values
        
        # 1. Estimate par for deliveries in match M using ONLY prior historical matches
        m_par = []
        m_above = []
        for c, ob, w, sb, br, be, mb in zip(comps, o_buks, w_rems, s_befs, b_rems, b_elaps, m_balls):
            k = (c, ob, w)
            prior_val = calculate_analytical_par_prior(float(br), float(w), baseline_par, mb)
            cnt = hist_cnt.get(k, 0)
            if cnt > 0:
                exp_rem = (hist_sum[k] + k_prior * prior_val) / (cnt + k_prior)
            else:
                exp_rem = prior_val
                
            p_fin = sb + exp_rem
            frac = be / mb if mb > 0 else 0.0
            par_at = p_fin * frac
            m_par.append(float(p_fin))
            m_above.append(float(sb - par_at))
            
        par_final_results.extend(m_par)
        runs_above_results.extend(m_above)
        indices_order.extend(m_df.index.tolist())
        
        # 2. Add completed match M outcome to accumulator strictly AFTER scoring match M
        m_final_score = s_befs[-1] + m_df["est_total_runs"].iloc[-1]
        m_rem_actual = m_final_score - s_befs
        for c, ob, w, rem in zip(comps, o_buks, w_rems, m_rem_actual):
            k = (c, ob, w)
            hist_sum[k] = hist_sum.get(k, 0.0) + float(rem)
            hist_cnt[k] = hist_cnt.get(k, 0) + 1
            
    # Assign back using exact row indices
    df.loc[indices_order, "par_final_score"] = np.round(par_final_results, 2)
    df.loc[indices_order, "runs_above_par_trajectory"] = np.round(runs_above_results, 2)
    return df
