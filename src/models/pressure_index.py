"""Pressure Index calculation module for PRESSUREIQ.

Computes separate, calibrated 0-100 Batting Pressure Index (BPI)
and Bowling Pressure Index (BoPI) based purely on contextual difficulty.
"""

import numpy as np
import pandas as pd
from typing import Tuple


def sigmoid(x: np.ndarray) -> np.ndarray:
    """Stable sigmoid activation."""
    return 1.0 / (1.0 + np.exp(-np.clip(x, -15.0, 15.0)))


def compute_batting_pressure_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Batting Pressure Index (BPI) on a continuous 0-100 scale.
    
    Components:
    1. Rate Demand: RRR in chase, or deficit from par trajectory in 1st innings.
    2. Resource Scarcity: Wickets lost (fewer resources left).
    3. Climax / Urgency: Fewer balls remaining to achieve target / set total.
    4. Match Leverage: Closeness of finish and knockout multiplier.
    """
    res = pd.DataFrame(index=df.index)
    
    # --- 1. Scoring Demand Component (0 - 100) ---
    # Innings 2: Driven by Required Run Rate (baseline 8.5)
    rrr = df["required_run_rate_before"].fillna(8.5).values
    # In death overs with small targets, clip RRR to reasonable bounds
    rrr_clean = np.clip(rrr, 2.0, 24.0)
    rate_demand_inn2 = sigmoid((rrr_clean - 8.5) / 2.2) * 100.0
    
    # Innings 1: Driven by deficit from par trajectory
    runs_above_par = df["runs_above_par_trajectory"].fillna(0.0).values
    rate_demand_inn1 = sigmoid((-runs_above_par) / 14.0) * 100.0
    
    inn_mask = (df["innings"] == 1).values
    rate_comp = np.where(inn_mask, rate_demand_inn1, rate_demand_inn2)
    
    # --- 2. Resource Scarcity Component (0 - 100) ---
    wkts_lost = df["wickets_lost_before"].fillna(0).values
    resource_comp = (np.clip(wkts_lost / 9.0, 0.0, 1.0) ** 1.2) * 100.0
    
    # --- 3. Climax / Temporal Urgency Component (0 - 100) ---
    # In shortened matches, scheduled available balls is max_innings_balls (e.g., 30, 48, 84, 90, 120)
    if "max_innings_balls" in df.columns:
        max_balls = np.maximum(df["max_innings_balls"].fillna(120.0).values.astype(float), 1.0)
    else:
        b_rem_val = df["balls_remaining_before"].fillna(120.0).values.astype(float)
        b_bef_val = df["legal_balls_before"].fillna(0.0).values.astype(float) if "legal_balls_before" in df.columns else 0.0
        max_balls = np.maximum(120.0, b_rem_val + b_bef_val)
        
    if "legal_balls_before" in df.columns:
        balls_bowled = df["legal_balls_before"].fillna(0.0).values.astype(float)
    else:
        b_rem_arr = df["balls_remaining_before"].fillna(120.0).values.astype(float)
        balls_bowled = np.clip(max_balls - b_rem_arr, 0.0, max_balls)
        
    # Temporal completion ratio: strictly 0.0 at the first delivery of any match, 1.0 at the final scheduled ball
    completion_ratio = np.clip(balls_bowled / max_balls, 0.0, 1.0)
    climax_comp = (completion_ratio ** 1.3) * 100.0
    
    # Interaction: high rate demand at the climax is exponentially harder
    climax_factor = 0.5 + 0.5 * completion_ratio
    effective_rate = rate_comp * climax_factor
    
    # --- 4. Leverage & Match Stage (0 - 100) ---
    is_knockout = df["is_knockout_stage"].fillna(False).values
    knockout_bonus = np.where(is_knockout, 12.0, 0.0)
    
    # Close chase leverage (scaled for match length: final 25% of match and tight runs required)
    balls_rem = np.where(df["balls_remaining_before"].notna(), df["balls_remaining_before"].values, max_balls)
    runs_req = df["runs_required_before"].fillna(100.0).values
    chase_threshold = np.maximum(12.0, max_balls * 0.25)
    close_chase = (~inn_mask) & (balls_rem <= chase_threshold) & (runs_req <= 50) & (runs_req > 0)
    leverage_bonus = np.where(close_chase, 15.0, 0.0)
    
    # --- Composite BPI (Calibrated 0-100) ---
    raw_bpi = (
        0.42 * effective_rate +
        0.30 * resource_comp +
        0.18 * climax_comp +
        0.10 * (knockout_bonus + leverage_bonus)
    )
    
    # Calibrate to exact 0-100 range
    bpi_score = np.clip(raw_bpi, 0.0, 100.0)
    
    res["bpi"] = np.round(bpi_score, 2)
    res["bpi_rate_comp"] = np.round(rate_comp, 2)
    res["bpi_resource_comp"] = np.round(resource_comp, 2)
    res["bpi_climax_comp"] = np.round(climax_comp, 2)
    res["bpi_tier"] = pd.cut(
        res["bpi"],
        bins=[-0.1, 35.0, 65.0, 85.0, 100.0],
        labels=["Low", "Medium", "High", "Extreme"]
    )
    return res


def compute_bowling_pressure_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Bowling Pressure Index (BoPI) on a continuous 0-100 scale.
    
    Components:
    1. Target Defense Pressure: High when opposition is easily on track (low RRR),
       forcing bowler into boundary-prevention and wicket-taking mode.
    2. Batting Resources In Hand: High when opposition has many wickets in hand.
    3. Death / Climax Exposure: Extreme accuracy demanded in overs 16-20.
    4. Match Leverage & Knockout stakes.
    """
    res = pd.DataFrame(index=df.index)
    
    # --- 1. Target Defense Difficulty (0 - 100) ---
    # In 2nd innings: If RRR is low (e.g. 5.5 RPO), bowling team has little margin for error
    # Conversely, if RRR is 14 RPO, bowler has cushion.
    # So defense difficulty is high when RRR is low or when match is in balance (RRR ~ 7-10)
    rrr = df["required_run_rate_before"].fillna(8.5).values
    rrr_clean = np.clip(rrr, 2.0, 24.0)
    # Bowler pressure peaks when RRR is low (chasing team in control) or game is neck-and-neck
    defend_demand_inn2 = sigmoid((10.5 - rrr_clean) / 2.2) * 100.0
    
    # In 1st innings: If batting team is ahead of par, bowler is under high pressure
    runs_above_par = df["runs_above_par_trajectory"].fillna(0.0).values
    defend_demand_inn1 = sigmoid(runs_above_par / 14.0) * 100.0
    
    inn_mask = (df["innings"] == 1).values
    defend_comp = np.where(inn_mask, defend_demand_inn1, defend_demand_inn2)
    
    # --- 2. Batting Resources In Hand (0 - 100) ---
    # Bowler faces more pressure when batting team has many wickets remaining (e.g., 8-10 wickets)
    wkts_rem = df["wickets_remaining_before"].fillna(10).values
    resource_comp = (np.clip(wkts_rem / 10.0, 0.0, 1.0) ** 1.1) * 100.0
    
    # --- 3. Death & Climax Pressure (0 - 100) ---
    if "max_innings_balls" in df.columns:
        max_balls = np.maximum(df["max_innings_balls"].fillna(120.0).values.astype(float), 1.0)
    else:
        b_rem_val = df["balls_remaining_before"].fillna(120.0).values.astype(float)
        b_bef_val = df["legal_balls_before"].fillna(0.0).values.astype(float) if "legal_balls_before" in df.columns else 0.0
        max_balls = np.maximum(120.0, b_rem_val + b_bef_val)
        
    if "legal_balls_before" in df.columns:
        balls_bowled = df["legal_balls_before"].fillna(0.0).values.astype(float)
    else:
        b_rem_arr = df["balls_remaining_before"].fillna(120.0).values.astype(float)
        balls_bowled = np.clip(max_balls - b_rem_arr, 0.0, max_balls)
        
    completion_ratio = np.clip(balls_bowled / max_balls, 0.0, 1.0)
    climax_comp = (completion_ratio ** 1.4) * 100.0
    
    # --- 4. Match Leverage & Stage (0 - 100) ---
    is_knockout = df["is_knockout_stage"].fillna(False).values
    knockout_bonus = np.where(is_knockout, 12.0, 0.0)
    
    # Tight finish: final 15% of overs and chasing team needs <= 30 runs
    balls_rem = np.where(df["balls_remaining_before"].notna(), df["balls_remaining_before"].values, max_balls)
    runs_req = df["runs_required_before"].fillna(100.0).values
    bowl_threshold = np.maximum(6.0, max_balls * 0.15)
    close_finish = (~inn_mask) & (balls_rem <= bowl_threshold) & (runs_req <= 30) & (runs_req > 0)
    leverage_bonus = np.where(close_finish, 18.0, 0.0)
    
    # --- Composite BoPI (Calibrated 0-100) ---
    raw_bopi = (
        0.38 * defend_comp +
        0.26 * resource_comp +
        0.24 * climax_comp +
        0.12 * (knockout_bonus + leverage_bonus)
    )
    
    bopi_score = np.clip(raw_bopi, 0.0, 100.0)
    
    res["bopi"] = np.round(bopi_score, 2)
    res["bopi_defend_comp"] = np.round(defend_comp, 2)
    res["bopi_resource_comp"] = np.round(resource_comp, 2)
    res["bopi_climax_comp"] = np.round(climax_comp, 2)
    res["bopi_tier"] = pd.cut(
        res["bopi"],
        bins=[-0.1, 35.0, 65.0, 85.0, 100.0],
        labels=["Low", "Medium", "High", "Extreme"]
    )
    return res

