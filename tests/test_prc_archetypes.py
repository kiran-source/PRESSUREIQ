"""Tests for Pressure Response Curve (PRC) archetypes (P1-7 & Issue 3).

Tests the classifier on synthetic curves that:
1. Increase under pressure (Clutch Climber)
2. Decrease under pressure (Gradual Decliner)
3. Remain flat (Ice Cold Anchor)
4. Collapse at extreme pressure (Pressure Fragile)
5. Have sparse/insufficient data (Unclassified)
"""

import numpy as np
import pandas as pd
import pytest

from src.analysis.reliability_engine import fit_pressure_response_curve


def test_prc_clutch_climber():
    """Performance systematically increases as pressure rises."""
    np.random.seed(42)
    p = np.linspace(20, 95, 60)
    # y increases with pressure: slope approx +0.60
    y = 0.60 * (p / 100.0) + np.random.normal(0, 0.05, len(p))
    df = pd.DataFrame({"bpi": p, "raw_bat_value": y})
    prc = fit_pressure_response_curve(df, is_batting=True)
    assert prc["archetype"] == "Clutch Climber"
    assert prc["slope"] > 0.15


def test_prc_gradual_decliner():
    """Performance moderately declines as pressure rises."""
    np.random.seed(42)
    p = np.linspace(20, 95, 60)
    # y declines with pressure: slope approx -0.22
    y = -0.22 * (p / 100.0) + np.random.normal(0, 0.04, len(p))
    df = pd.DataFrame({"bpi": p, "raw_bat_value": y})
    prc = fit_pressure_response_curve(df, is_batting=True)
    assert prc["archetype"] == "Gradual Decliner"
    assert prc["slope"] < -0.10


def test_prc_ice_cold_anchor():
    """Performance is invariant to pressure."""
    np.random.seed(42)
    p = np.linspace(20, 95, 60)
    # flat performance
    y = 0.10 + np.random.normal(0, 0.04, len(p))
    df = pd.DataFrame({"bpi": p, "raw_bat_value": y})
    prc = fit_pressure_response_curve(df, is_batting=True)
    assert prc["archetype"] == "Ice Cold Anchor"
    assert abs(prc["slope"]) < 0.15


def test_prc_extreme_collapse_fragile():
    """Performs well up to high pressure, but collapses at extreme pressure (>85)."""
    rows = []
    # 20 low balls at +0.15
    for _ in range(20):
        rows.append({"bpi": 25.0, "raw_bat_value": 0.15})
    # 20 medium balls at +0.20
    for _ in range(20):
        rows.append({"bpi": 50.0, "raw_bat_value": 0.20})
    # 15 high balls at +0.35 (strong)
    for _ in range(15):
        rows.append({"bpi": 75.0, "raw_bat_value": 0.35})
    # 10 extreme balls at -0.30 (severe collapse)
    for _ in range(10):
        rows.append({"bpi": 92.0, "raw_bat_value": -0.30})
        
    df = pd.DataFrame(rows)
    prc = fit_pressure_response_curve(df, is_batting=True)
    assert prc["archetype"] == "Pressure Fragile"


def test_prc_insufficient_evidence():
    """Fewer than 30 deliveries or < 10 HP deliveries returns Unclassified."""
    df = pd.DataFrame({
        "bpi": [20.0, 30.0, 40.0],
        "raw_bat_value": [0.1, 0.2, 0.3]
    })
    prc = fit_pressure_response_curve(df, is_batting=True)
    assert prc["archetype"] == "Unclassified (Insufficient Evidence)"
    assert prc["slope"] == 0.0
