import pytest
import pandas as pd
import numpy as np
from src.models.pressure_index import compute_batting_pressure_index, compute_bowling_pressure_index


def test_bpi_monotonic_with_rrr():
    """BPI must strictly increase with Required Run Rate (RRR) in chase."""
    base_data = {
        "innings": [2, 2, 2],
        "required_run_rate_before": [6.0, 10.0, 15.0],
        "runs_above_par_trajectory": [0.0, 0.0, 0.0],
        "wickets_lost_before": [3, 3, 3],
        "wickets_remaining_before": [7, 7, 7],
        "balls_remaining_before": [60, 60, 60],
        "runs_required_before": [60, 100, 150],
        "is_knockout_stage": [False, False, False]
    }
    df = pd.DataFrame(base_data)
    res = compute_batting_pressure_index(df)
    bpi = res["bpi"].tolist()
    assert bpi[0] < bpi[1] < bpi[2], f"BPI should increase with RRR: {bpi}"


def test_bpi_monotonic_with_wickets_lost():
    """BPI must strictly increase with wickets lost (resource scarcity)."""
    base_data = {
        "innings": [2, 2, 2],
        "required_run_rate_before": [9.0, 9.0, 9.0],
        "runs_above_par_trajectory": [0.0, 0.0, 0.0],
        "wickets_lost_before": [1, 4, 8],
        "wickets_remaining_before": [9, 6, 2],
        "balls_remaining_before": [60, 60, 60],
        "runs_required_before": [90, 90, 90],
        "is_knockout_stage": [False, False, False]
    }
    df = pd.DataFrame(base_data)
    res = compute_batting_pressure_index(df)
    bpi = res["bpi"].tolist()
    assert bpi[0] < bpi[1] < bpi[2], f"BPI should increase with wickets lost: {bpi}"


def test_bpi_monotonic_with_balls_remaining():
    """Holding target rate constant, BPI must increase as balls remaining decrease (late innings urgency)."""
    base_data = {
        "innings": [2, 2, 2],
        "required_run_rate_before": [10.0, 10.0, 10.0],
        "runs_above_par_trajectory": [0.0, 0.0, 0.0],
        "wickets_lost_before": [4, 4, 4],
        "wickets_remaining_before": [6, 6, 6],
        "balls_remaining_before": [100, 50, 12],
        "runs_required_before": [100, 50, 20],
        "is_knockout_stage": [False, False, False]
    }
    df = pd.DataFrame(base_data)
    res = compute_batting_pressure_index(df)
    bpi = res["bpi"].tolist()
    assert bpi[0] < bpi[1] < bpi[2], f"BPI should increase as balls expire: {bpi}"


def test_bopi_monotonic_with_opposition_wickets_in_hand():
    """BoPI must increase when opposition has more wickets in hand (batters have freedom to attack)."""
    base_data = {
        "innings": [2, 2, 2],
        "required_run_rate_before": [8.5, 8.5, 8.5],
        "runs_above_par_trajectory": [0.0, 0.0, 0.0],
        "wickets_lost_before": [8, 4, 1],
        "wickets_remaining_before": [2, 6, 9],
        "balls_remaining_before": [60, 60, 60],
        "runs_required_before": [85, 85, 85],
        "is_knockout_stage": [False, False, False]
    }
    df = pd.DataFrame(base_data)
    res = compute_bowling_pressure_index(df)
    bopi = res["bopi"].tolist()
    assert bopi[0] < bopi[1] < bopi[2], f"BoPI should increase with wickets in hand: {bopi}"


def test_bopi_monotonic_with_chase_comfort():
    """BoPI must increase when opposition is cruising with lower RRR (bowler defense under high threat)."""
    base_data = {
        "innings": [2, 2, 2],
        "required_run_rate_before": [14.0, 9.0, 5.0],  # 14 is safe defense, 5 is danger
        "runs_above_par_trajectory": [0.0, 0.0, 0.0],
        "wickets_lost_before": [3, 3, 3],
        "wickets_remaining_before": [7, 7, 7],
        "balls_remaining_before": [36, 36, 36],
        "runs_required_before": [84, 54, 30],
        "is_knockout_stage": [False, False, False]
    }
    df = pd.DataFrame(base_data)
    res = compute_bowling_pressure_index(df)
    bopi = res["bopi"].tolist()
    assert bopi[0] < bopi[1] < bopi[2], f"BoPI should increase as target defense becomes harder (lower RRR): {bopi}"


def test_first_innings_par_pressure_symmetry():
    """In 1st innings: batting behind par raises BPI; bowling against a team ahead of par raises BoPI."""
    base_data = {
        "innings": [1, 1],
        "required_run_rate_before": [8.5, 8.5],
        "runs_above_par_trajectory": [-20.0, 20.0],  # Case 0: 20 behind par, Case 1: 20 ahead of par
        "wickets_lost_before": [3, 3],
        "wickets_remaining_before": [7, 7],
        "balls_remaining_before": [60, 60],
        "runs_required_before": [0, 0],
        "is_knockout_stage": [False, False]
    }
    df = pd.DataFrame(base_data)
    bpi = compute_batting_pressure_index(df)["bpi"].tolist()
    bopi = compute_bowling_pressure_index(df)["bopi"].tolist()
    
    # Batter is under more pressure when behind par (-20) than ahead (+20)
    assert bpi[0] > bpi[1], f"Batter under more pressure when behind par: {bpi}"
    # Bowler is under more pressure when batting team is ahead of par (+20) than behind (-20)
    assert bopi[1] > bopi[0], f"Bowler under more pressure when batting team ahead of par: {bopi}"
