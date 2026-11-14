"""Model B Recruitment Scoring Engine for PRESSUREIQ v6.0.

Implements the official 6-component multi-criteria recruitment formula:
1. Pressure Reliability: 25% (Preserved Model A reliability / PAVA / PRC)
2. Overall T20 Performance: 20% (Career SR, Avg, Economy, Boundary %, Dot %)
3. Predictive Performance: 15% (Model B LightGBM/Ridge validated expectation under pressure)
4. Role Suitability: 15% (Phase execution, situational role benchmark alignment)
5. RR Squad Fit: 15% (SMS Jaipur conditions, 4 core RR deficits addressed)
6. Consistency & Adaptability: 10% (Match-level stability, downside risk mitigation, sample confidence)

Total = 100.0%.

Hard Gating Filters:
- Eligibility: Must be 'Eligible' (BCCI/IPL regulatory clearance).
- Targetability: Must be 'Confirmed Available', 'Confirmed Released', or verified open auction candidate.
- Contracted stars, traded players to rival clubs, and policy-restricted candidates are routed to Watchlist / Exclusions.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class RecruitmentEvaluation:
    player_id: int
    player_name: str
    discipline: str  # "Batter" or "Bowler"
    nationality: str
    is_overseas: bool
    latest_ipl_franchise: str
    primary_role: str
    eligibility_status: str
    auction_availability: str
    is_targetable: bool

    # Model B Component Scores (0 to 100)
    pressure_reliability_score: float  # 25%
    overall_performance_score: float   # 20%
    predictive_score: float            # 15%
    role_suitability_score: float      # 15%
    rr_squad_fit_score: float          # 15%
    consistency_score: float           # 10%

    # Final Model B Recruitment Target Score (0 to 100)
    model_b_target_score: float
    model_b_rank: int

    # Model A Reference (Immutable Baseline)
    model_a_rank: int
    model_a_reliability: float

    # Strategic Metadata
    addressed_gap: str
    tactical_advantage: str
    primary_weakness: str
    best_alternative_name: str
    best_alternative_tradeoff: str
    confidence_level: str
    risk_quadrant: str
    recruitment_rationale: str
    source_url: str


def compute_model_b_score(
    pressure_rel: float,
    t20_perf: float,
    pred_perf: float,
    role_suit: float,
    squad_fit: float,
    consistency: float,
    is_targetable: bool,
    is_eligible: bool,
    sample_weight: float = 1.0
) -> float:
    """Compute the weighted 6-component recruitment score with hard eligibility & targetability gates."""
    if not is_eligible:
        return 0.0

    # Base weighted sum
    raw_score = (
        (pressure_rel * 0.25) +
        (t20_perf * 0.20) +
        (pred_perf * 0.15) +
        (role_suit * 0.15) +
        (squad_fit * 0.15) +
        (consistency * 0.10)
    )

    adj_score = raw_score

    # If player is NOT auction-targetable (e.g. contracted or traded to a rival franchise),
    # heavily discount their RR priority score so they do not enter confirmed auction target lists
    if not is_targetable:
        adj_score = min(adj_score * 0.70, 75.0)

    return round(float(adj_score), 2)
