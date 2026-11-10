"""Player Reliability Scoring, Pressure Response Curves (PRC), and Decomposition Engine.

Implements the five-pillar reliability decomposition, Empirical Bayes shrinkage,
Pressure Response Curve (PRC) archetyping, and counterfactual comparisons.
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from scipy import stats

logger = logging.getLogger("PRESSUREIQ.ReliabilityEngine")

# Minimum exposure thresholds for eligibility in final rankings
MIN_BATTER_CAREER_BALLS = 400
MIN_BATTER_PRESSURE_BALLS = 30
MIN_BATTER_MATCHES = 20

MIN_BOWLER_CAREER_BALLS = 400
MIN_BOWLER_PRESSURE_BALLS = 30
MIN_BOWLER_MATCHES = 20

# Empirical Bayes Shrinkage parameter (pseudo-deliveries)
# Calibrated from variance ratio: sigma_within^2 (~1.8) / sigma_between^2 (~0.04) ≈ 45
K_SHRINK = 45.0


def fit_pressure_response_curve(player_delivs: pd.DataFrame, is_batting: bool = True) -> Dict:
    """
    Fit linear pressure-response trend and classify into archetypes (P1-7).
    
    Evaluates rate of performance above expectation (raw_bat_value or raw_bowl_value)
    as a function of normalized pressure (p / 100.0).
    
    Archetypes:
    - 'Clutch Climber': statistically positive slope under pressure (beta >= 0.15, p <= 0.15)
    - 'Ice Cold Anchor': invariant across pressure conditions (abs(beta) < 0.15 or flat)
    - 'Gradual Decliner': moderate negative slope under pressure (-0.30 <= beta < -0.10)
    - 'Pressure Fragile': steep drop-off (beta < -0.30) or extreme-tier collapse
    - 'Unclassified (Insufficient Evidence)': < 30 total balls or < 10 high-pressure balls
    """
    p_col = "bpi" if is_batting else "bopi"
    val_col = "raw_bat_value" if is_batting else "raw_bowl_value"
    
    # Fallback to computing raw value if not present
    if val_col not in player_delivs.columns:
        if is_batting:
            val_col = "pava_bat"
            y = (player_delivs[val_col] / (1.0 + player_delivs[p_col].fillna(35.0) / 50.0)).values
        else:
            val_col = "pava_bowl"
            y = (player_delivs[val_col] / (1.0 + player_delivs[p_col].fillna(45.0) / 50.0)).values
    else:
        y = player_delivs[val_col].values
        
    p = player_delivs[p_col].fillna(35.0 if is_batting else 45.0).values
    n_delivs = len(player_delivs)
    n_hp = (p >= 50.0).sum()
    
    if n_delivs < 30 or n_hp < 10:
        return {
            "slope": 0.0,
            "intercept": 0.0,
            "r_squared": 0.0,
            "std_err": 0.0,
            "p_value": 1.0,
            "archetype": "Unclassified (Insufficient Evidence)",
            "pava_low": 0.0,
            "pava_med": 0.0,
            "pava_high": 0.0,
            "pava_extreme": 0.0
        }
        
    # Linear fit: y = alpha + beta * (pressure / 100)
    slope, intercept, r_val, p_val, std_err = stats.linregress(p / 100.0, y)
    
    # Performance across pressure tiers
    low_mask = p < 35.0
    med_mask = (p >= 35.0) & (p < 65.0)
    high_mask = (p >= 65.0) & (p < 85.0)
    ext_mask = p >= 85.0
    
    val_low = float(y[low_mask].mean()) if low_mask.sum() >= 5 else 0.0
    val_med = float(y[med_mask].mean()) if med_mask.sum() >= 5 else 0.0
    val_high = float(y[high_mask].mean()) if high_mask.sum() >= 5 else 0.0
    val_ext = float(y[ext_mask].mean()) if ext_mask.sum() >= 5 else None
    
    # Archetype determination
    if val_ext is not None and val_high >= 0.10 and val_ext <= (val_high - 0.25):
        # Extreme pressure collapse (choke at climax)
        archetype = "Pressure Fragile"
    elif slope >= 0.15 and p_val <= 0.15:
        archetype = "Clutch Climber"
    elif slope <= -0.30 and p_val <= 0.15:
        archetype = "Pressure Fragile"
    elif slope <= -0.10 and p_val <= 0.15:
        archetype = "Gradual Decliner"
    else:
        archetype = "Ice Cold Anchor"
        
    return {
        "slope": round(float(slope), 4),
        "intercept": round(float(intercept), 4),
        "r_squared": round(float(r_val ** 2), 4),
        "std_err": round(float(std_err), 4),
        "p_value": round(float(p_val), 4),
        "archetype": archetype,
        "pava_low": round(val_low, 3),
        "pava_med": round(val_med, 3),
        "pava_high": round(val_high, 3),
        "pava_extreme": round(val_ext if val_ext is not None else val_high, 3)
    }


def compute_batter_reliability_scores(deliveries_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Five-Pillar Reliability Score for all qualifying batters.
    
    Pillars:
    1. Absolute Pressure Performance (PAVA per ball in BPI >= 50)
    2. Baseline Retention Ratio (Pressure PAVA vs Low-Pressure PAVA with shrinkage)
    3. Match-to-Match Consistency (opportunity-adjusted per-ball PAVA variance)
    4. Adaptability (IPL vs T20I, Chase vs 1st Innings)
    5. Evidence Strength (Empirical Bayes exposure weighting, K=45)
    """
    logger.info("Computing Batter Reliability Scores...")
    bat_deliv = deliveries_df[deliveries_df["is_batter_ball"]].copy()
    
    results = []
    for pid, group in bat_deliv.groupby("striker_id"):
        pname = group["striker_name"].iloc[0]
        n_balls = len(group)
        n_matches = group["match_id"].nunique()
        
        # High pressure deliveries (BPI >= 50)
        hp_group = group[group["bpi"] >= 50.0]
        n_hp_balls = len(hp_group)
        
        # Low pressure deliveries (BPI < 35)
        lp_group = group[group["bpi"] < 35.0]
        n_lp_balls = len(lp_group)
        
        if n_balls < 50:
            continue
            
        # 1. Absolute Pressure Performance
        raw_hp_pava = hp_group["pava_bat"].mean() if n_hp_balls >= 5 else 0.0
        
        # 2. Baseline Retention (P1-6: shrink towards career baseline mean when low pressure exposure is sparse)
        career_rate = group["pava_bat"].mean()
        if n_lp_balls >= 10:
            raw_lp_pava = lp_group["pava_bat"].mean()
        else:
            w_lp = n_lp_balls / (n_lp_balls + 10.0)
            lp_sub_rate = lp_group["pava_bat"].mean() if n_lp_balls > 0 else career_rate
            raw_lp_pava = w_lp * lp_sub_rate + (1.0 - w_lp) * career_rate
        retention_delta = raw_hp_pava - raw_lp_pava
        
        # 3. Match-to-Match Consistency (P1-6: Opportunity-adjusted per-ball rate variance across innings)
        inn_stats = group.groupby("match_id").agg(
            inn_pava=("pava_bat", "sum"),
            inn_balls=("is_batter_ball", "sum")
        )
        valid_inns = inn_stats[inn_stats["inn_balls"] >= 5]
        if len(valid_inns) >= 3:
            inn_rates = valid_inns["inn_pava"] / valid_inns["inn_balls"]
            inn_sd = float(inn_rates.std())
        else:
            inn_sd = 0.50
        consistency_score = 100.0 / (1.0 + (inn_sd / 0.35))
        
        # 4. Context Adaptability
        ipl_group = group[group["comp_category"] == "IPL"]
        t20i_group = group[group["comp_category"] == "T20I"]
        if len(ipl_group) >= 30 and len(t20i_group) >= 30:
            ipl_pava = ipl_group["pava_bat"].mean()
            t20i_pava = t20i_group["pava_bat"].mean()
            comp_diff = abs(ipl_pava - t20i_pava)
            adaptability_score = np.clip(100.0 - (comp_diff * 40.0), 20.0, 100.0)
        else:
            adaptability_score = 60.0
            
        # 5. Evidence Strength / Empirical Bayes Shrinkage
        shrinkage_weight = n_hp_balls / (n_hp_balls + K_SHRINK)
        shrunk_hp_pava = shrinkage_weight * raw_hp_pava + (1.0 - shrinkage_weight) * 0.0
        
        # Fit Pressure Response Curve (PRC)
        prc = fit_pressure_response_curve(group, is_batting=True)
        
        # Batting role
        roles = group["batting_role"].value_counts()
        primary_role = roles.index[0] if len(roles) > 0 else "Middle_Order"
        
        results.append({
            "player_id": pid,
            "player_name": pname,
            "role": primary_role,
            "matches": n_matches,
            "total_balls": n_balls,
            "hp_balls": n_hp_balls,
            "total_runs": group["batter_runs"].sum(),
            "career_sr": round((group["batter_runs"].sum() / n_balls) * 100.0, 1),
            "raw_hp_pava_per_ball": round(raw_hp_pava, 3),
            "shrunk_hp_pava_per_ball": round(shrunk_hp_pava, 3),
            "retention_delta": round(retention_delta, 3),
            "consistency_score": round(consistency_score, 1),
            "adaptability_score": round(adaptability_score, 1),
            "evidence_weight": round(shrinkage_weight, 3),
            "prc_archetype": prc["archetype"],
            "prc_slope": prc["slope"],
            "is_eligible": (
                n_balls >= MIN_BATTER_CAREER_BALLS and
                n_hp_balls >= MIN_BATTER_PRESSURE_BALLS and
                n_matches >= MIN_BATTER_MATCHES
            )
        })
        
    df_res = pd.DataFrame(results)
    
    # Composite Reliability Score (0 to 100)
    pava_norm = (df_res["shrunk_hp_pava_per_ball"] - df_res["shrunk_hp_pava_per_ball"].mean()) / (df_res["shrunk_hp_pava_per_ball"].std() + 1e-6)
    ret_norm = (df_res["retention_delta"] - df_res["retention_delta"].mean()) / (df_res["retention_delta"].std() + 1e-6)
    
    raw_composite = (
        0.50 * pava_norm +
        0.20 * ret_norm +
        0.15 * (df_res["consistency_score"] / 50.0) +
        0.15 * (df_res["adaptability_score"] / 50.0)
    )
    
    df_res["reliability_score"] = np.round(stats.norm.cdf(raw_composite) * 100.0, 2)
    df_res.sort_values(by="reliability_score", ascending=False, inplace=True)
    return df_res


def compute_bowler_reliability_scores(deliveries_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Five-Pillar Reliability Score for all qualifying bowlers (P0-4 & P1-6).
    
    P0-4 Strict Accounting:
    Includes all deliveries bowled (wides, no-balls) for total runs conceded and PAVA,
    while using legal balls for overs and legal-ball exposure denominators.
    """
    logger.info("Computing Bowler Reliability Scores...")
    # P0-4: Do NOT filter on is_legal_ball; bowler_id.notna() captures all deliveries bowled
    bowl_deliv = deliveries_df[deliveries_df["bowler_id"].notna()].copy()
    
    results = []
    for pid, group in bowl_deliv.groupby("bowler_id"):
        pname = group["bowler_name"].iloc[0]
        legal_balls = int(group["is_legal_ball"].sum())
        total_deliveries = len(group)
        n_matches = group["match_id"].nunique()
        
        # High pressure deliveries (BoPI >= 50)
        hp_group = group[group["bopi"] >= 50.0]
        n_hp_legal_balls = int(hp_group["is_legal_ball"].sum())
        n_hp_balls = len(hp_group)
        
        # Low pressure deliveries (BoPI < 35)
        lp_group = group[group["bopi"] < 35.0]
        n_lp_legal_balls = int(lp_group["is_legal_ball"].sum())
        
        if legal_balls < 50:
            continue
            
        # 1. Absolute Pressure Performance (total HP PAVA / legal HP balls)
        hp_pava_sum = hp_group["pava_bowl"].sum()
        raw_hp_pava = (hp_pava_sum / max(n_hp_legal_balls, 1)) if n_hp_legal_balls >= 5 else 0.0
        
        # 2. Baseline Retention (shrink towards career baseline mean when low pressure exposure is sparse)
        career_rate = group["pava_bowl"].sum() / max(legal_balls, 1)
        if n_lp_legal_balls >= 10:
            raw_lp_pava = lp_group["pava_bowl"].sum() / max(n_lp_legal_balls, 1)
        else:
            w_lp = n_lp_legal_balls / (n_lp_legal_balls + 10.0)
            lp_sub_rate = (lp_group["pava_bowl"].sum() / max(n_lp_legal_balls, 1)) if n_lp_legal_balls > 0 else career_rate
            raw_lp_pava = w_lp * lp_sub_rate + (1.0 - w_lp) * career_rate
        retention_delta = raw_hp_pava - raw_lp_pava
        
        # 3. Match-to-Match Consistency (P1-6: Opportunity-adjusted per-ball rate variance across spells)
        spell_stats = group.groupby("match_id").agg(
            spell_pava=("pava_bowl", "sum"),
            spell_legal=("is_legal_ball", "sum")
        )
        valid_spells = spell_stats[spell_stats["spell_legal"] >= 6]
        if len(valid_spells) >= 3:
            spell_rates = valid_spells["spell_pava"] / valid_spells["spell_legal"]
            spell_sd = float(spell_rates.std())
        else:
            spell_sd = 0.50
        consistency_score = 100.0 / (1.0 + (spell_sd / 0.35))
        
        # 4. Context Adaptability
        ipl_group = group[group["comp_category"] == "IPL"]
        t20i_group = group[group["comp_category"] == "T20I"]
        ipl_legal = ipl_group["is_legal_ball"].sum()
        t20i_legal = t20i_group["is_legal_ball"].sum()
        if ipl_legal >= 30 and t20i_legal >= 30:
            ipl_pava = ipl_group["pava_bowl"].sum() / ipl_legal
            t20i_pava = t20i_group["pava_bowl"].sum() / t20i_legal
            comp_diff = abs(ipl_pava - t20i_pava)
            adaptability_score = np.clip(100.0 - (comp_diff * 40.0), 20.0, 100.0)
        else:
            adaptability_score = 60.0
            
        # 5. Evidence Strength / Empirical Bayes Shrinkage
        shrinkage_weight = n_hp_legal_balls / (n_hp_legal_balls + K_SHRINK)
        shrunk_hp_pava = shrinkage_weight * raw_hp_pava + (1.0 - shrinkage_weight) * 0.0
        
        # Fit Pressure Response Curve (PRC)
        prc = fit_pressure_response_curve(group, is_batting=False)
        
        # Primary Bowling Type
        bowl_type = group["bowling_type"].value_counts().index[0]
        pace_spin = group["pace_or_spin"].value_counts().index[0]
        runs_conceded = float(group["bowler_runs_conceded"].sum())
        career_economy = round(runs_conceded / (max(legal_balls, 1) / 6.0), 2)
        
        results.append({
            "player_id": pid,
            "player_name": pname,
            "bowling_type": bowl_type,
            "pace_or_spin": pace_spin,
            "matches": n_matches,
            "legal_balls": legal_balls,
            "total_balls": legal_balls,  # Backwards compatibility
            "total_deliveries": total_deliveries,
            "hp_balls": n_hp_legal_balls,
            "total_wickets": int(group["is_bowler_wicket"].sum()),
            "career_economy": career_economy,
            "raw_hp_pava_per_ball": round(raw_hp_pava, 3),
            "shrunk_hp_pava_per_ball": round(shrunk_hp_pava, 3),
            "retention_delta": round(retention_delta, 3),
            "consistency_score": round(consistency_score, 1),
            "adaptability_score": round(adaptability_score, 1),
            "evidence_weight": round(shrinkage_weight, 3),
            "prc_archetype": prc["archetype"],
            "prc_slope": prc["slope"],
            "is_eligible": (
                legal_balls >= MIN_BOWLER_CAREER_BALLS and
                n_hp_legal_balls >= MIN_BOWLER_PRESSURE_BALLS and
                n_matches >= MIN_BOWLER_MATCHES
            )
        })
        
    df_res = pd.DataFrame(results)
    
    # Standardize components
    pava_norm = (df_res["shrunk_hp_pava_per_ball"] - df_res["shrunk_hp_pava_per_ball"].mean()) / (df_res["shrunk_hp_pava_per_ball"].std() + 1e-6)
    ret_norm = (df_res["retention_delta"] - df_res["retention_delta"].mean()) / (df_res["retention_delta"].std() + 1e-6)
    
    raw_composite = (
        0.50 * pava_norm +
        0.20 * ret_norm +
        0.15 * (df_res["consistency_score"] / 50.0) +
        0.15 * (df_res["adaptability_score"] / 50.0)
    )
    
    df_res["reliability_score"] = np.round(stats.norm.cdf(raw_composite) * 100.0, 2)
    df_res.sort_values(by="reliability_score", ascending=False, inplace=True)
    return df_res
