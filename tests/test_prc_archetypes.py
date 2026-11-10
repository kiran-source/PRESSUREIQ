import pytest
import pandas as pd
import numpy as np
from src.analysis.reliability_engine import fit_pressure_response_curve


def test_prc_synthetic_increasing_clutch_climber():
    """Synthetic curve with performance increasing with pressure should be Clutch Climber."""
    # BPI from 10 to 90, PAVA increases from -0.5 to +0.8
    bpi = np.linspace(10, 90, 50)
    pava = -0.5 + 1.5 * (bpi / 100.0) + np.random.normal(0, 0.02, 50)
    df = pd.DataFrame({"bpi": bpi, "pava_bat": pava})
    
    res = fit_pressure_response_curve(df, is_batting=True)
    assert res["archetype"] == "Clutch Climber"
    assert res["slope"] > 0.20


def test_prc_synthetic_flat_ice_cold_anchor():
    """Synthetic curve with flat performance across pressure should be Ice Cold Anchor."""
    # BPI from 10 to 90, PAVA remains flat around 0.20
    bpi = np.linspace(10, 90, 50)
    pava = 0.20 + np.random.normal(0, 0.01, 50)
    df = pd.DataFrame({"bpi": bpi, "pava_bat": pava})
    
    res = fit_pressure_response_curve(df, is_batting=True)
    assert res["archetype"] == "Ice Cold Anchor"
    assert -0.10 <= res["slope"] < 0.20


def test_prc_synthetic_gradual_decliner():
    """Synthetic curve with slight decline should be Gradual Decliner."""
    # BPI from 10 to 90, PAVA decreases moderately (slope around -0.25)
    bpi = np.linspace(10, 90, 50)
    pava = 0.5 - 0.25 * (bpi / 100.0)
    df = pd.DataFrame({"bpi": bpi, "pava_bat": pava})
    
    res = fit_pressure_response_curve(df, is_batting=True)
    assert res["archetype"] == "Gradual Decliner"
    assert -0.40 <= res["slope"] < -0.10


def test_prc_synthetic_steep_drop_pressure_fragile():
    """Synthetic curve with steep decline should be Pressure Fragile."""
    # BPI from 10 to 90, PAVA drops sharply (slope < -0.40)
    bpi = np.linspace(10, 90, 50)
    pava = 0.8 - 0.9 * (bpi / 100.0)
    df = pd.DataFrame({"bpi": bpi, "pava_bat": pava})
    
    res = fit_pressure_response_curve(df, is_batting=True)
    assert res["archetype"] == "Pressure Fragile"
    assert res["slope"] < -0.40


def test_prc_synthetic_bowler_clutch_and_fragile():
    """Verify bowling curves independently using bopi and pava_bowl."""
    bopi = np.linspace(10, 90, 60)
    # Clutch bowler: pava_bowl improves with BoPI
    pava_clutch = -0.3 + 1.2 * (bopi / 100.0)
    df_clutch = pd.DataFrame({"bopi": bopi, "pava_bowl": pava_clutch})
    res_clutch = fit_pressure_response_curve(df_clutch, is_batting=False)
    assert res_clutch["archetype"] == "Clutch Climber"
    
    # Fragile bowler: pava_bowl degrades with BoPI
    pava_fragile = 0.5 - 0.8 * (bopi / 100.0)
    df_fragile = pd.DataFrame({"bopi": bopi, "pava_bowl": pava_fragile})
    res_fragile = fit_pressure_response_curve(df_fragile, is_batting=False)
    assert res_fragile["archetype"] == "Pressure Fragile"


def test_prc_insufficient_data():
    """Fewer than 20 deliveries must produce Insufficient Data."""
    bpi = np.linspace(10, 90, 15)
    pava = 0.5 + 0.5 * (bpi / 100.0)
    df = pd.DataFrame({"bpi": bpi, "pava_bat": pava})
    
    res = fit_pressure_response_curve(df, is_batting=True)
    assert res["archetype"] == "Insufficient Data"
