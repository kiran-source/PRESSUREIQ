"""Player Consistency, Volatility, and Downside Risk Engine for PRESSUREIQ v6.0.

Computes match-to-match variation, downside failure rates, stability indices,
and 4-quadrant ceiling vs consistency archetypes for candidate evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ConsistencyProfile:
    player_id: int
    player_name: str
    discipline: str
    match_count: int
    mean_metric: float
    metric_std: float
    coeff_variation: float
    ceiling_metric: float  # 90th percentile match performance
    downside_failure_rate: float  # % matches below failure threshold
    dependability_score: float  # 100 - (failure_rate * 100)
    stability_score: float  # 100 * (1 / (1 + CV))
    sample_confidence: float  # Min(100, matches / 30 * 100)
    risk_quadrant: str  # 4-quadrant classification


def evaluate_batter_consistency(
    player_id: int,
    player_name: str,
    bat_innings: pd.DataFrame
) -> ConsistencyProfile:
    """Evaluate batter match-level volatility, downside failure, and ceiling."""
    sub = bat_innings[bat_innings["striker_id"] == player_id]
    n_matches = len(sub)
    if n_matches < 3:
        return ConsistencyProfile(
            player_id=player_id,
            player_name=player_name,
            discipline="Batter",
            match_count=n_matches,
            mean_metric=float(sub["runs"].mean()) if n_matches > 0 else 0.0,
            metric_std=0.0,
            coeff_variation=1.0,
            ceiling_metric=float(sub["runs"].max()) if n_matches > 0 else 0.0,
            downside_failure_rate=0.50,
            dependability_score=50.0,
            stability_score=40.0,
            sample_confidence=round(min(100.0, (n_matches / 25.0) * 100.0), 1),
            risk_quadrant="Low Evidence, High Uncertainty"
        )

    runs = sub["runs"].values
    mean_runs = float(np.mean(runs))
    std_runs = float(np.std(runs, ddof=1)) if n_matches > 1 else 0.0
    cv = (std_runs / max(mean_runs, 1.0))

    # Downside failure: scored < 15 runs in an innings
    failures = (runs < 15).sum()
    failure_rate = float(failures / n_matches)
    ceiling_runs = float(np.percentile(runs, 85))

    dependability = round(max(0.0, min(100.0, (1.0 - failure_rate) * 100.0)), 1)
    stability = round(max(0.0, min(100.0, 100.0 / (1.0 + cv))), 1)
    confidence = round(min(100.0, (n_matches / 35.0) * 100.0), 1)

    # 4-Quadrant Classification
    if n_matches < 15:
        quadrant = "Low Evidence, High Uncertainty"
    elif ceiling_runs >= 45.0 and cv <= 0.85:
        quadrant = "High Ceiling, Consistent"
    elif ceiling_runs >= 45.0 and cv > 0.85:
        quadrant = "High Ceiling, High Volatility"
    elif ceiling_runs < 45.0 and dependability >= 50.0:
        quadrant = "Moderate Ceiling, Highly Reliable"
    else:
        quadrant = "High Ceiling, High Volatility"

    return ConsistencyProfile(
        player_id=player_id,
        player_name=player_name,
        discipline="Batter",
        match_count=n_matches,
        mean_metric=round(mean_runs, 1),
        metric_std=round(std_runs, 1),
        coeff_variation=round(cv, 2),
        ceiling_metric=round(ceiling_runs, 1),
        downside_failure_rate=round(failure_rate, 2),
        dependability_score=dependability,
        stability_score=stability,
        sample_confidence=confidence,
        risk_quadrant=quadrant
    )


def evaluate_bowler_consistency(
    player_id: int,
    player_name: str,
    bowl_spells: pd.DataFrame
) -> ConsistencyProfile:
    """Evaluate bowler match-level volatility, economy stability, and wickets ceiling."""
    sub = bowl_spells[bowl_spells["bowler_id"] == player_id]
    n_spells = len(sub)
    if n_spells < 3:
        return ConsistencyProfile(
            player_id=player_id,
            player_name=player_name,
            discipline="Bowler",
            match_count=n_spells,
            mean_metric=8.5,
            metric_std=0.0,
            coeff_variation=1.0,
            ceiling_metric=1.0,
            downside_failure_rate=0.50,
            dependability_score=50.0,
            stability_score=40.0,
            sample_confidence=round(min(100.0, (n_spells / 25.0) * 100.0), 1),
            risk_quadrant="Low Evidence, High Uncertainty"
        )

    # Compute spell economy
    econs = np.where(sub["legal_balls"] > 0, (sub["runs_conceded"] / sub["legal_balls"]) * 6.0, 9.0)
    mean_econ = float(np.mean(econs))
    std_econ = float(np.std(econs, ddof=1)) if n_spells > 1 else 0.0
    cv = (std_econ / max(mean_econ, 1.0))

    # Downside failure: conceded economy > 10.5 without taking a wicket
    wkts = sub["wickets"].values
    failures = ((econs > 10.5) & (wkts == 0)).sum()
    failure_rate = float(failures / n_spells)
    ceiling_wkts = float(np.percentile(wkts, 85))

    dependability = round(max(0.0, min(100.0, (1.0 - failure_rate) * 100.0)), 1)
    stability = round(max(0.0, min(100.0, 100.0 / (1.0 + cv))), 1)
    confidence = round(min(100.0, (n_spells / 35.0) * 100.0), 1)

    # 4-Quadrant Classification
    if n_spells < 15:
        quadrant = "Low Evidence, High Uncertainty"
    elif ceiling_wkts >= 2.0 and mean_econ <= 8.2:
        quadrant = "High Ceiling, Consistent"
    elif ceiling_wkts >= 2.0 and mean_econ > 8.2:
        quadrant = "High Ceiling, High Volatility"
    elif ceiling_wkts < 2.0 and dependability >= 70.0:
        quadrant = "Moderate Ceiling, Highly Reliable"
    else:
        quadrant = "High Ceiling, High Volatility"

    return ConsistencyProfile(
        player_id=player_id,
        player_name=player_name,
        discipline="Bowler",
        match_count=n_spells,
        mean_metric=round(mean_econ, 2),
        metric_std=round(std_econ, 2),
        coeff_variation=round(cv, 2),
        ceiling_metric=round(ceiling_wkts, 1),
        downside_failure_rate=round(failure_rate, 2),
        dependability_score=dependability,
        stability_score=stability,
        sample_confidence=confidence,
        risk_quadrant=quadrant
    )
