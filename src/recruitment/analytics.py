"""Role-Specific Performance, Matchup, and Phase Intelligence Engine for PRESSUREIQ v6.0.

Computes granular situational metrics:
- 6 Batting Roles & 8 Bowling Roles
- Phase-wise splits (Powerplay overs 1-6, Middle overs 7-15, Death overs 16-20)
- Matchups (Batters vs Pace & Spin; Bowlers vs RHB & LHB)
- High-Pressure sub-cohort metrics (BPI >= 65, BOPI >= 65)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class BatterAdvancedMetrics:
    player_id: int
    player_name: str
    primary_role: str
    batting_style: str  # LHB or RHB
    total_runs: int
    total_balls: int
    career_sr: float
    career_avg: float
    dot_pct: float
    boundary_pct: float
    six_pct: float
    pp_sr: float
    middle_sr: float
    death_sr: float
    chase_sr: float
    first_inn_sr: float
    vs_pace_sr: float
    vs_pace_avg: float
    vs_spin_sr: float
    vs_spin_avg: float
    hp_sr: float
    hp_boundary_pct: float
    hp_dot_pct: float
    role_suitability_score: float  # 0 to 100


@dataclass(frozen=True)
class BowlerAdvancedMetrics:
    player_id: int
    player_name: str
    primary_role: str
    bowling_style: str  # Pace, Spin, Left-arm, etc.
    legal_balls: int
    total_wickets: int
    career_economy: float
    career_sr: float
    career_avg: float
    dot_pct: float
    boundary_conceded_pct: float
    pp_economy: float
    pp_wickets: int
    middle_economy: float
    middle_wickets: int
    death_economy: float
    death_wickets: int
    defending_economy: float
    chasing_economy: float
    vs_rhb_economy: float
    vs_lhb_economy: float
    hp_economy: float
    hp_dot_pct: float
    role_suitability_score: float  # 0 to 100


def calculate_batter_metrics(
    player_id: int,
    player_name: str,
    deliv: pd.DataFrame,
    role_hint: str = "Middle-Order"
) -> BatterAdvancedMetrics:
    """Extract role, phase, and matchup analytics for a single batter."""
    sub = deliv[deliv["striker_id"] == player_id]
    n_balls = len(sub)
    if n_balls == 0:
        return BatterAdvancedMetrics(
            player_id=player_id, player_name=player_name, primary_role=role_hint,
            batting_style="RHB", total_runs=0, total_balls=0, career_sr=100.0,
            career_avg=20.0, dot_pct=40.0, boundary_pct=12.0, six_pct=3.0,
            pp_sr=110.0, middle_sr=115.0, death_sr=135.0, chase_sr=115.0,
            first_inn_sr=115.0, vs_pace_sr=120.0, vs_pace_avg=22.0,
            vs_spin_sr=115.0, vs_spin_avg=24.0, hp_sr=110.0,
            hp_boundary_pct=10.0, hp_dot_pct=45.0, role_suitability_score=70.0
        )

    bat_style = str(sub["batting_type"].iloc[0]) if sub["batting_type"].notna().any() else "RHB"
    runs = int(sub["batter_runs"].sum())
    dismissals = int((sub["dismissed_player_id"] == player_id).sum())
    avg = round(runs / max(dismissals, 1), 1)
    sr = round((runs / n_balls) * 100.0, 1)

    dots = (sub["batter_runs"] == 0).sum()
    bnds = (sub["is_four"] | sub["is_six"]).sum()
    sixes = sub["is_six"].sum()

    dot_pct = round((dots / n_balls) * 100.0, 1)
    bnd_pct = round((bnds / n_balls) * 100.0, 1)
    six_pct = round((sixes / n_balls) * 100.0, 1)

    # Phase splits
    pp = sub[sub["phase"] == "Powerplay"]
    mid = sub[sub["phase"] == "Middle"]
    dth = sub[sub["phase"] == "Death"]

    pp_sr = round((pp["batter_runs"].sum() / max(len(pp), 1)) * 100.0, 1) if len(pp) > 0 else sr
    mid_sr = round((mid["batter_runs"].sum() / max(len(mid), 1)) * 100.0, 1) if len(mid) > 0 else sr
    dth_sr = round((dth["batter_runs"].sum() / max(len(dth), 1)) * 100.0, 1) if len(dth) > 0 else sr

    # Innings chase vs 1st inn
    chase = sub[sub["innings"] == 2]
    first = sub[sub["innings"] == 1]
    chase_sr = round((chase["batter_runs"].sum() / max(len(chase), 1)) * 100.0, 1) if len(chase) > 0 else sr
    first_sr = round((first["batter_runs"].sum() / max(len(first), 1)) * 100.0, 1) if len(first) > 0 else sr

    # Pace vs Spin
    pace = sub[sub["pace_or_spin"] == "Pace"]
    spin = sub[sub["pace_or_spin"] == "Spin"]
    pace_sr = round((pace["batter_runs"].sum() / max(len(pace), 1)) * 100.0, 1) if len(pace) > 0 else sr
    pace_dis = int((pace["dismissed_player_id"] == player_id).sum())
    pace_avg = round(pace["batter_runs"].sum() / max(pace_dis, 1), 1) if len(pace) > 0 else avg

    spin_sr = round((spin["batter_runs"].sum() / max(len(spin), 1)) * 100.0, 1) if len(spin) > 0 else sr
    spin_dis = int((spin["dismissed_player_id"] == player_id).sum())
    spin_avg = round(spin["batter_runs"].sum() / max(spin_dis, 1), 1) if len(spin) > 0 else avg

    # High Pressure (BPI >= 65)
    hp = sub[sub["bpi"] >= 65.0] if "bpi" in sub.columns else sub.iloc[:0]
    hp_sr = round((hp["batter_runs"].sum() / max(len(hp), 1)) * 100.0, 1) if len(hp) > 0 else sr
    hp_bnd = round(((hp["is_four"] | hp["is_six"]).sum() / max(len(hp), 1)) * 100.0, 1) if len(hp) > 0 else bnd_pct
    hp_dot = round(((hp["batter_runs"] == 0).sum() / max(len(hp), 1)) * 100.0, 1) if len(hp) > 0 else dot_pct

    # Determine primary role
    if len(pp) / n_balls >= 0.50:
        role = "Opener"
        role_suit = min(100.0, (pp_sr / 140.0) * 50.0 + min(50.0, (100.0 - dot_pct)))
    elif len(dth) / n_balls >= 0.35:
        role = "Finisher"
        role_suit = min(100.0, (dth_sr / 170.0) * 60.0 + min(40.0, bnd_pct * 1.5))
    elif "keeper" in role_hint.lower() or "wk" in role_hint.lower():
        role = "Wicketkeeper-Batter"
        role_suit = min(100.0, (sr / 140.0) * 50.0 + (avg / 35.0) * 50.0)
    elif "all-rounder" in role_hint.lower():
        role = "Batting All-Rounder"
        role_suit = min(100.0, (sr / 135.0) * 50.0 + (dth_sr / 160.0) * 50.0)
    elif len(mid) / n_balls >= 0.50:
        role = "Middle-Order Batter"
        role_suit = min(100.0, (mid_sr / 135.0) * 50.0 + (spin_sr / 135.0) * 50.0)
    else:
        role = "Top-Order Anchor"
        role_suit = min(100.0, (avg / 40.0) * 50.0 + (sr / 135.0) * 50.0)

    return BatterAdvancedMetrics(
        player_id=player_id, player_name=player_name, primary_role=role,
        batting_style=bat_style, total_runs=runs, total_balls=n_balls,
        career_sr=sr, career_avg=avg, dot_pct=dot_pct, boundary_pct=bnd_pct,
        six_pct=six_pct, pp_sr=pp_sr, middle_sr=mid_sr, death_sr=dth_sr,
        chase_sr=chase_sr, first_inn_sr=first_sr, vs_pace_sr=pace_sr,
        vs_pace_avg=pace_avg, vs_spin_sr=spin_sr, vs_spin_avg=spin_avg,
        hp_sr=hp_sr, hp_boundary_pct=hp_bnd, hp_dot_pct=hp_dot,
        role_suitability_score=round(role_suit, 1)
    )


def calculate_bowler_metrics(
    player_id: int,
    player_name: str,
    deliv: pd.DataFrame,
    role_hint: str = "Fast Bowler"
) -> BowlerAdvancedMetrics:
    """Extract role, phase, and matchup analytics for a single bowler."""
    sub = deliv[deliv["bowler_id"] == player_id]
    n_balls = len(sub)
    if n_balls == 0:
        return BowlerAdvancedMetrics(
            player_id=player_id, player_name=player_name, primary_role=role_hint,
            bowling_style="Fast Bowler", legal_balls=0, total_wickets=0, career_economy=8.5,
            career_sr=20.0, career_avg=28.0, dot_pct=35.0, boundary_conceded_pct=15.0,
            pp_economy=8.0, pp_wickets=0, middle_economy=8.2, middle_wickets=0,
            death_economy=10.0, death_wickets=0, defending_economy=8.5, chasing_economy=8.5,
            vs_rhb_economy=8.5, vs_lhb_economy=8.5, hp_economy=9.2, hp_dot_pct=35.0,
            role_suitability_score=70.0
        )

    bowl_style = str(sub["bowling_type"].iloc[0]) if sub["bowling_type"].notna().any() else role_hint
    legal = int(sub["is_legal_ball"].sum()) if "is_legal_ball" in sub.columns else n_balls
    runs_conc = int(sub["bowler_runs_conceded"].sum())
    wkts = int(sub["is_bowler_wicket"].sum())

    econ = round((runs_conc / max(legal, 1)) * 6.0, 2)
    sr = round(legal / max(wkts, 1), 1)
    avg = round(runs_conc / max(wkts, 1), 1)

    dots = (sub["bowler_runs_conceded"] == 0).sum()
    bnds = (sub["is_four"] | sub["is_six"]).sum()
    dot_pct = round((dots / n_balls) * 100.0, 1)
    bnd_conc_pct = round((bnds / n_balls) * 100.0, 1)

    # Phases
    pp = sub[sub["phase"] == "Powerplay"]
    mid = sub[sub["phase"] == "Middle"]
    dth = sub[sub["phase"] == "Death"]

    pp_econ = round((pp["bowler_runs_conceded"].sum() / max(len(pp), 1)) * 6.0, 2) if len(pp) > 0 else econ
    pp_wkts = int(pp["is_bowler_wicket"].sum())
    mid_econ = round((mid["bowler_runs_conceded"].sum() / max(len(mid), 1)) * 6.0, 2) if len(mid) > 0 else econ
    mid_wkts = int(mid["is_bowler_wicket"].sum())
    dth_econ = round((dth["bowler_runs_conceded"].sum() / max(len(dth), 1)) * 6.0, 2) if len(dth) > 0 else econ
    dth_wkts = int(dth["is_bowler_wicket"].sum())

    # Defending vs Chasing
    defend = sub[sub["innings"] == 2]  # Bowler bowling in 2nd inn = defending total
    chase = sub[sub["innings"] == 1]   # Bowler bowling in 1st inn = bowling first
    def_econ = round((defend["bowler_runs_conceded"].sum() / max(len(defend), 1)) * 6.0, 2) if len(defend) > 0 else econ
    chase_econ = round((chase["bowler_runs_conceded"].sum() / max(len(chase), 1)) * 6.0, 2) if len(chase) > 0 else econ

    # Matchups: vs RHB vs LHB
    rhb = sub[sub["batting_type"] == "RHB"]
    lhb = sub[sub["batting_type"] == "LHB"]
    rhb_econ = round((rhb["bowler_runs_conceded"].sum() / max(len(rhb), 1)) * 6.0, 2) if len(rhb) > 0 else econ
    lhb_econ = round((lhb["bowler_runs_conceded"].sum() / max(len(lhb), 1)) * 6.0, 2) if len(lhb) > 0 else econ

    # High pressure (BOPI >= 65)
    hp = sub[sub["bopi"] >= 65.0] if "bopi" in sub.columns else sub.iloc[:0]
    hp_econ = round((hp["bowler_runs_conceded"].sum() / max(len(hp), 1)) * 6.0, 2) if len(hp) > 0 else econ
    hp_dot = round(((hp["bowler_runs_conceded"] == 0).sum() / max(len(hp), 1)) * 100.0, 1) if len(hp) > 0 else dot_pct

    # Classify role
    is_spin = ("spin" in bowl_style.lower() or "orthodox" in bowl_style.lower() or "break" in bowl_style.lower())
    if len(dth) / n_balls >= 0.30:
        role = "Death-Over Specialist"
        role_suit = min(100.0, max(0.0, (12.5 - dth_econ) * 12.0 + min(50.0, (wkts / max(len(dth) / 6.0, 1.0)) * 60.0)))
    elif is_spin and ("orthodox" in bowl_style.lower() or "left-arm" in bowl_style.lower()):
        role = "Left-Arm Orthodox Spinner"
        role_suit = min(100.0, max(0.0, (10.0 - mid_econ) * 20.0 + (dot_pct / 40.0) * 45.0))
    elif is_spin and "leg" in bowl_style.lower():
        role = "Leg-Spinner"
        role_suit = min(100.0, max(0.0, (10.0 - econ) * 16.0 + min(50.0, (wkts / 15.0) * 50.0)))
    elif is_spin:
        role = "Middle-Over Spinner"
        role_suit = min(100.0, max(0.0, (9.8 - mid_econ) * 20.0 + (dot_pct / 40.0) * 45.0))
    elif len(pp) / n_balls >= 0.40:
        role = "Powerplay Wicket-Taker"
        role_suit = min(100.0, max(0.0, (9.8 - pp_econ) * 16.0 + min(50.0, (pp_wkts / 8.0) * 50.0)))
    else:
        role = "Fast Bowler"
        role_suit = min(100.0, max(0.0, (10.5 - econ) * 16.0 + (dot_pct / 40.0) * 45.0))

    return BowlerAdvancedMetrics(
        player_id=player_id, player_name=player_name, primary_role=role,
        bowling_style=bowl_style, legal_balls=legal, total_wickets=wkts,
        career_economy=econ, career_sr=sr, career_avg=avg, dot_pct=dot_pct,
        boundary_conceded_pct=bnd_conc_pct, pp_economy=pp_econ, pp_wickets=pp_wkts,
        middle_economy=mid_econ, middle_wickets=mid_wkts, death_economy=dth_econ,
        death_wickets=dth_wkts, defending_economy=def_econ, chasing_economy=chase_econ,
        vs_rhb_economy=rhb_econ, vs_lhb_economy=lhb_econ, hp_economy=hp_econ,
        hp_dot_pct=hp_dot, role_suitability_score=round(role_suit, 1)
    )
