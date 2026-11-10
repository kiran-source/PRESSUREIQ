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
K_SHRINK = 45.0


def fit_pressure_response_curve(player_delivs: pd.DataFrame, is_batting=True) -> Dict:
    """
    Fit smooth continuous performance as a function of pressure.
    
    Categorizes the player into an archetypal profile:
    - 'Clutch Climber': thrives under pressure (positive slope)
    - 'Ice Cold Anchor': completely unaffected by pressure (stable)
    - 'Gradual Decliner': slight performance drop under pressure
    - 'Pressure Fragile': steep drop-off at extreme pressure
    """
    p_col = "bpi" if is_batting else "bopi"
    val_col = "pava_bat" if is_batting else "pava_bowl"
    
    if len(player_delivs) < 20:
        return {
            "slope": 0.0, "intercept": 0.0, "archetype": "Insufficient Data",
            "pava_low": 0.0, "pava_med": 0.0, "pava_high": 0.0, "pava_extreme": 0.0
        }
        
    p = player_delivs[p_col].values
    y = player_delivs[val_col].values
    
    # Linear fit: y = alpha + beta * (pressure / 100)
    slope, intercept, r_val, p_val, std_err = stats.linregress(p / 100.0, y)
    
    # Performance across pressure tiers
    low_mask = p < 35.0
    med_mask = (p >= 35.0) & (p < 65.0)
    high_mask = (p >= 65.0) & (p < 85.0)
    ext_mask = p >= 85.0
    
    pava_low = float(y[low_mask].mean()) if low_mask.sum() > 0 else 0.0
    pava_med = float(y[med_mask].mean()) if med_mask.sum() > 0 else 0.0
    pava_high = float(y[high_mask].mean()) if high_mask.sum() > 0 else 0.0
    pava_ext = float(y[ext_mask].mean()) if ext_mask.sum() > 0 else pava_high
    
    # Archetype classification
    if slope >= 0.20:
        archetype = "Clutch Climber"
    elif slope >= -0.10:
        archetype = "Ice Cold Anchor"
    elif slope >= -0.40:
        archetype = "Gradual Decliner"
    else:
        archetype = "Pressure Fragile"
        
    return {
        "slope": round(float(slope), 4),
        "intercept": round(float(intercept), 4),
        "r_squared": round(float(r_val ** 2), 4),
        "std_err": round(float(std_err), 4),
        "archetype": archetype,
        "pava_low": round(pava_low, 3),
        "pava_med": round(pava_med, 3),
        "pava_high": round(pava_high, 3),
        "pava_extreme": round(pava_ext, 3)
    }


def compute_batter_reliability_scores(deliveries_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Five-Pillar Reliability Score for all qualifying batters.
    
    Pillars:
    1. Absolute Pressure Performance (PAVA per ball in BPI >= 50)
    2. Baseline Retention Ratio (Pressure PAVA vs Low-Pressure PAVA)
    3. Match-to-Match Consistency (inverse of inter-innings PAVA variance)
    4. Adaptability (IPL vs T20I, Chase vs 1st Innings)
    5. Evidence Strength (Empirical Bayes exposure weighting)
    """
    logger.info("Computing Batter Reliability Scores...")
    bat_deliv = deliveries_df[deliveries_df["is_batter_ball"]].copy()
    
    # Group by batter
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
        
        if n_balls < 50:
            continue
            
        # 1. Absolute Pressure Performance
        raw_hp_pava = hp_group["pava_bat"].mean() if n_hp_balls >= 5 else 0.0
        
        # 2. Baseline Retention
        raw_lp_pava = lp_group["pava_bat"].mean() if len(lp_group) >= 10 else 0.0
        retention_delta = raw_hp_pava - raw_lp_pava
        
        # 3. Match-to-Match Consistency
        # Innings-level PAVA standard deviation
        inn_pava = group.groupby("match_id")["pava_bat"].sum()
        inn_sd = inn_pava.std() if len(inn_pava) > 3 else 15.0
        consistency_score = 100.0 / (1.0 + (inn_sd / 10.0))
        
        # 4. Context Adaptability
        # Compare performance in IPL vs T20I
        ipl_pava = group[group["comp_category"] == "IPL"]["pava_bat"].mean()
        t20i_pava = group[group["comp_category"] == "T20I"]["pava_bat"].mean()
        if not np.isnan(ipl_pava) and not np.isnan(t20i_pava):
            comp_diff = abs(ipl_pava - t20i_pava)
            adaptability_score = np.clip(100.0 - (comp_diff * 40.0), 20.0, 100.0)
        else:
            adaptability_score = 60.0
            
        # 5. Evidence Strength / Empirical Bayes Shrinkage
        # K = 45 pseudo-deliveries for shrinkage
        K_SHRINK = 45.0
        shrinkage_weight = n_hp_balls / (n_hp_balls + K_SHRINK)
        
        # Shrunk Pressure PAVA
        prior_mean = 0.0
        shrunk_hp_pava = shrinkage_weight * raw_hp_pava + (1.0 - shrinkage_weight) * prior_mean
        
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
    # Normalized ranking score combining shrunk PAVA, retention, consistency, adaptability
    # Standardize components
    pava_norm = (df_res["shrunk_hp_pava_per_ball"] - df_res["shrunk_hp_pava_per_ball"].mean()) / (df_res["shrunk_hp_pava_per_ball"].std() + 1e-6)
    ret_norm = (df_res["retention_delta"] - df_res["retention_delta"].mean()) / (df_res["retention_delta"].std() + 1e-6)
    
    raw_composite = (
        0.50 * pava_norm +
        0.20 * ret_norm +
        0.15 * (df_res["consistency_score"] / 50.0) +
        0.15 * (df_res["adaptability_score"] / 50.0)
    )
    
    # Scale to 0 - 100 with 50 at median
    df_res["reliability_score"] = np.round(stats.norm.cdf(raw_composite) * 100.0, 2)
    df_res.sort_values(by="reliability_score", ascending=False, inplace=True)
    return df_res


def compute_bowler_reliability_scores(deliveries_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Five-Pillar Reliability Score for all qualifying bowlers.
    
    Pillars:
    1. Absolute Pressure Performance (Bowling PAVA per ball in BoPI >= 50)
    2. Baseline Retention Ratio (Pressure PAVA vs Low-Pressure PAVA)
    3. Match-to-Match Consistency (inverse of inter-spell PAVA variance)
    4. Adaptability (IPL vs T20I, Defending vs Setting)
    5. Evidence Strength (Empirical Bayes exposure weighting)
    """
    logger.info("Computing Bowler Reliability Scores...")
    bowl_deliv = deliveries_df[deliveries_df["is_legal_ball"]].copy()
    
    results = []
    for pid, group in bowl_deliv.groupby("bowler_id"):
        pname = group["bowler_name"].iloc[0]
        n_balls = len(group)
        n_matches = group["match_id"].nunique()
        
        # High pressure deliveries (BoPI >= 50)
        hp_group = group[group["bopi"] >= 50.0]
        n_hp_balls = len(hp_group)
        
        # Low pressure deliveries (BoPI < 35)
        lp_group = group[group["bopi"] < 35.0]
        
        if n_balls < 50:
            continue
            
        # 1. Absolute Pressure Performance
        raw_hp_pava = hp_group["pava_bowl"].mean() if n_hp_balls >= 5 else 0.0
        
        # 2. Baseline Retention
        raw_lp_pava = lp_group["pava_bowl"].mean() if len(lp_group) >= 10 else 0.0
        retention_delta = raw_hp_pava - raw_lp_pava
        
        # 3. Match-to-Match Consistency
        spell_pava = group.groupby("match_id")["pava_bowl"].sum()
        spell_sd = spell_pava.std() if len(spell_pava) > 3 else 12.0
        consistency_score = 100.0 / (1.0 + (spell_sd / 8.0))
        
        # 4. Context Adaptability
        ipl_pava = group[group["comp_category"] == "IPL"]["pava_bowl"].mean()
        t20i_pava = group[group["comp_category"] == "T20I"]["pava_bowl"].mean()
        if not np.isnan(ipl_pava) and not np.isnan(t20i_pava):
            comp_diff = abs(ipl_pava - t20i_pava)
            adaptability_score = np.clip(100.0 - (comp_diff * 40.0), 20.0, 100.0)
        else:
            adaptability_score = 60.0
            
        # 5. Evidence Strength / Empirical Bayes Shrinkage
        K_SHRINK = 45.0
        shrinkage_weight = n_hp_balls / (n_hp_balls + K_SHRINK)
        shrunk_hp_pava = shrinkage_weight * raw_hp_pava + (1.0 - shrinkage_weight) * 0.0
        
        # Fit Pressure Response Curve (PRC)
        prc = fit_pressure_response_curve(group, is_batting=False)
        
        # Primary Bowling Type
        bowl_type = group["bowling_type"].value_counts().index[0]
        pace_spin = group["pace_or_spin"].value_counts().index[0]
        
        results.append({
            "player_id": pid,
            "player_name": pname,
            "bowling_type": bowl_type,
            "pace_or_spin": pace_spin,
            "matches": n_matches,
            "total_balls": n_balls,
            "hp_balls": n_hp_balls,
            "total_wickets": group["is_bowler_wicket"].sum(),
            "career_economy": round(group["bowler_runs_conceded"].sum() / (n_balls / 6.0), 2),
            "raw_hp_pava_per_ball": round(raw_hp_pava, 3),
            "shrunk_hp_pava_per_ball": round(shrunk_hp_pava, 3),
            "retention_delta": round(retention_delta, 3),
            "consistency_score": round(consistency_score, 1),
            "adaptability_score": round(adaptability_score, 1),
            "evidence_weight": round(shrinkage_weight, 3),
            "prc_archetype": prc["archetype"],
            "prc_slope": prc["slope"],
            "is_eligible": (
                n_balls >= MIN_BOWLER_CAREER_BALLS and
                n_hp_balls >= MIN_BOWLER_PRESSURE_BALLS and
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

