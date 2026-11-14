"""Rajasthan Royals Squad Fit & Alternative Target Recommender for PRESSUREIQ v6.0.

Evaluates candidate fit against Rajasthan Royals' specific squad gaps for IPL 2027
and generates role-based alternative target recommendations with trade-off rationale.

Key RR Squad Gaps for IPL 2027:
1. Overseas Death Overs Seamer (Overs 17-20 specialist alongside Sandeep Sharma & Jofra Archer)
2. SMS Jaipur Finger-Spin Controller / Spin Squeeze (Defensive economy for 78m boundary dimensions)
3. No. 7 Pace-Hitting Finisher (Lower-order acceleration against 140kph+ bowling)
4. Domestic Seam Depth (Backup Indian fast bowlers for rotation and workload mitigation)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class SquadFitEvaluation:
    player_id: int
    player_name: str
    addressed_gap: str
    tactical_role: str
    tactical_advantage: str
    primary_weakness: str
    squad_fit_score: float  # 0 to 100
    confidence_level: str
    best_alternative_name: str
    best_alternative_tradeoff: str


@dataclass(frozen=True)
class TargetAlternative:
    target_player_name: str
    target_role: str
    alternative_name: str
    alternative_discipline: str
    alternative_pressure_score: float
    tactical_tradeoff: str
    confidence: str


# Handcrafted, domain-verified squad fit evaluations for top realistic targets
TARGET_FIT_PROFILES: Dict[str, Dict[str, str]] = {
    "Liam Dawson": {
        "gap": "SMS Jaipur Finger-Spin Controller ('Jaipur Squeeze')",
        "role": "Defensive Left-Arm Orthodox Spinner & #8 Batter",
        "advantage": "World-class pressure metrics (95.4 Rel). Elite middle-overs economy (6.8 rpo) exploiting 78m Jaipur boundary dimensions.",
        "weakness": "Limited international exposure on flat Indian subcontinent batting decks; non-mystery bowling profile.",
        "fit_score": "96.0",
        "alt_name": "Allah Ghazanfar",
        "alt_tradeoff": "Ghazanfar offers mystery spin and higher turn, but Dawson provides significantly higher pressure reliability and batting depth."
    },
    "Spencer Johnson": {
        "gap": "Overseas Express Death Bowler",
        "role": "Left-Arm Express Fast Bowler (Overs 1-2 & 18-20)",
        "advantage": "145kph+ release speed, steep trajectory, left-arm angle creates nightmare angles for right-handed finishers at the death.",
        "weakness": "Fragile injury history requiring strict workload management; occasional control issues on slower pitches.",
        "fit_score": "95.0",
        "alt_name": "FazalHaq Farooqi",
        "alt_tradeoff": "Farooqi offers superior swing in the powerplay and subcontinental durability, but Johnson possesses 10kph greater raw top-end velocity."
    },
    "FazalHaq Farooqi": {
        "gap": "Overseas Death / Swing Pacer",
        "role": "Left-Arm Swing & Death Specialist",
        "advantage": "Elite subcontinental T20 pedigree, lethal new-ball inswing to right-handers and pinpoint yorkers at the death.",
        "weakness": "Vulnerable to straight boundary hitting when missing yorker length by even a few inches.",
        "fit_score": "93.0",
        "alt_name": "Spencer Johnson",
        "alt_tradeoff": "Johnson has higher top speed and bounce, but Farooqi is more durable and proven in Asian conditions."
    },
    "Allah Ghazanfar": {
        "gap": "SMS Jaipur Finger-Spin Controller",
        "role": "Mystery Off-Spinner",
        "advantage": "Extreme mystery variations (carrom ball, back-spinner) that suffocate boundary scoring in the middle overs.",
        "weakness": "Young sample size in high-pressure franchise knockouts; negligible batting contribution.",
        "fit_score": "91.0",
        "alt_name": "Tanush Kotian",
        "alt_tradeoff": "Kotian offers domestic Indian composure and batting capability, but Ghazanfar has genuine mystery wicket-taking potency."
    },
    "Jamie Smith": {
        "gap": "Dynamic WK-Batter & Pace Finisher",
        "role": "Middle/Lower-Order Power-Hitter & Backup Keeper",
        "advantage": "Extreme boundary hitting against 140kph+ pace; flexible across positions 4 through 7.",
        "weakness": "Limited experience against elite Indian mystery spinners on dry, turning surfaces.",
        "fit_score": "92.0",
        "alt_name": "Jacob Bethell",
        "alt_tradeoff": "Bethell provides bowling utility and left-handed batting, but Smith has higher pure striking power at the death."
    },
    "Jacob Bethell": {
        "gap": "No. 7 Lower-Order Finisher / Spin All-Rounder",
        "role": "Middle/Lower-Order Finisher & Slow Left-Arm Spinner",
        "advantage": "Modern 360-degree ramp/scoop player, exceptional fielding, gives RR crucial left-handed middle-order balance.",
        "weakness": "Developing game against high-pace back-of-a-length bouncers.",
        "fit_score": "91.0",
        "alt_name": "Ashutosh Sharma",
        "alt_tradeoff": "Ashutosh has proven domestic IPL crunch-time clutch heroics, but Bethell provides multi-dimensional all-round spin depth."
    },
    "Ashutosh Sharma": {
        "gap": "No. 7 Lower-Order Pace Finisher",
        "role": "Lower-Order Finisher (#7 / #8)",
        "advantage": "Indian domestic player freeing up an overseas slot; proven ability to hit sixes off 145kph bowling from ball one.",
        "weakness": "High dot-ball rate early in innings; specialized exclusively for the final 3-4 overs.",
        "fit_score": "94.0",
        "alt_name": "Nehal Wadhera",
        "alt_tradeoff": "Wadhera can anchor the innings from No. 4/5, whereas Ashutosh is purely an explosive death-over enforcer."
    },
    "Nehal Wadhera": {
        "gap": "Middle-Order Stabilization & Power",
        "role": "No. 5/6 Left-Handed Batter",
        "advantage": "Domestic Indian asset with supreme poise against both spin and pace; proven IPL pedigree.",
        "weakness": "Needs 5-8 balls to settle before accelerating; not a natural No. 7 ball-one hitter.",
        "fit_score": "89.0",
        "alt_name": "Ashutosh Sharma",
        "alt_tradeoff": "Ashutosh hits instantly from ball one, while Wadhera provides top-order collapse insurance."
    },
    "Tanush Kotian": {
        "gap": "Domestic Finger-Spin Depth",
        "role": "Right-Arm Off-Spinner & Useful Lower-Order Bat",
        "advantage": "Economical flatter trajectory tailor-made for Jaipur's long square boundaries; allows overseas slot elsewhere.",
        "weakness": "Lacks mystery variation to buy wickets on placid surfaces.",
        "fit_score": "88.0",
        "alt_name": "Allah Ghazanfar",
        "alt_tradeoff": "Ghazanfar has higher ceiling, but Kotian consumes zero overseas player quota."
    },
    "Rasikh Salam": {
        "gap": "Domestic Seam Depth & Death Backup",
        "role": "Indian Death Overs Seamer",
        "advantage": "Subtle changes of pace, deceptive knuckle-ball, and reliable wide yorker execution.",
        "weakness": "High economy volatility when yorker length is missed; vulnerable to left-handers.",
        "fit_score": "90.0",
        "alt_name": "Vyshak Kumar",
        "alt_tradeoff": "Vyshak provides heavy-ball hard lengths, but Rasikh has sharper specialized death yorker control."
    },
    "Vyshak Kumar": {
        "gap": "Domestic Seam Depth",
        "role": "Enforcer Fast Bowler",
        "advantage": "Hits the deck hard at 138kph; effective at extracting tennis-ball bounce on Jaipur pitches.",
        "weakness": "Predictable length bowling if batsman steps out; higher boundary concession percentage.",
        "fit_score": "87.0",
        "alt_name": "Rasikh Salam",
        "alt_tradeoff": "Rasikh is a death overs specialist, while Vyshak is better suited for middle-overs hit-the-deck bowling."
    },
    "Gus Atkinson": {
        "gap": "Overseas Express Fast Bowler",
        "role": "Express Strike Bowler (Overs 1-10)",
        "advantage": "True 148kph velocity, sharp bouncers, tests batsman footwork with genuine skiddy pace.",
        "weakness": "Developing death overs execution; can travel on true bounce tracks.",
        "fit_score": "89.0",
        "alt_name": "Spencer Johnson",
        "alt_tradeoff": "Johnson is left-armed with superior death yorkers, but Atkinson offers fiercer new-ball pace."
    },
    "Jason Holder": {
        "gap": "Experienced Seam All-Rounder",
        "role": "Lower-Order Finisher & Middle-Over Seamer",
        "advantage": "Massive height, reliable boundary catches, veteran leadership, and 91.3 Model A pressure reliability.",
        "weakness": "Diminished bowling pace (125kph); susceptible to quick boundary hitting at the death.",
        "fit_score": "86.0",
        "alt_name": "Jacob Bethell",
        "alt_tradeoff": "Holder brings proven veteran experience, but Bethell provides youthful mobility and 360-degree batting."
    },
    "Mohit Sharma": {
        "gap": "Domestic Death Overs Specialist",
        "role": "Death Overs Slower-Ball Craftsman",
        "advantage": "Mastery of back-of-the-hand slower balls, wide yorkers, and immense IPL playoff experience.",
        "weakness": "Lacks raw pace; vulnerable when batsmen sit deep in their crease anticipating slower balls.",
        "fit_score": "88.0",
        "alt_name": "Rasikh Salam",
        "alt_tradeoff": "Salam has longer career runway, but Mohit has unmatched situational composure."
    }
}


def evaluate_player_squad_fit(
    player_id: int,
    player_name: str,
    discipline: str,
    primary_role: str,
    is_targetable: bool
) -> SquadFitEvaluation:
    """Evaluate how candidate addresses Rajasthan Royals' specific squad gaps."""
    if player_name in TARGET_FIT_PROFILES:
        prof = TARGET_FIT_PROFILES[player_name]
        return SquadFitEvaluation(
            player_id=player_id,
            player_name=player_name,
            addressed_gap=prof["gap"],
            tactical_role=prof["role"],
            tactical_advantage=prof["advantage"],
            primary_weakness=prof["weakness"],
            squad_fit_score=float(prof["fit_score"]),
            confidence_level="High Domain & Tactical Evidence",
            best_alternative_name=prof["alt_name"],
            best_alternative_tradeoff=prof["alt_tradeoff"]
        )

    # General algorithmic squad fit
    role_lower = primary_role.lower()
    if discipline == "Bowler":
        if "death" in role_lower or "fast" in role_lower:
            gap = "Overseas / Domestic Death Pace Depth"
            adv = "High-pressure execution in overs 16-20 to support Sandeep Sharma and Jofra Archer."
            weak = "Risk of boundary concession under extreme power-hitting conditions."
            score = 82.0 if is_targetable else 60.0
            alt = "Spencer Johnson"
            tradeoff = "Spencer Johnson provides verified left-arm angle and 145kph velocity."
        elif "spin" in role_lower or "orthodox" in role_lower:
            gap = "Jaipur Finger-Spin Squeeze"
            adv = "Middle-overs boundary suppression on Jaipur's 78-meter square boundary dimensions."
            weak = "Limited wicket-taking punch on non-responsive batting surfaces."
            score = 80.0 if is_targetable else 55.0
            alt = "Liam Dawson"
            tradeoff = "Liam Dawson provides #1 Model A pressure reliability and lower-order batting depth."
        else:
            gap = "Bowling Squad Depth"
            adv = "Tactical flexibility and rotational depth across 14 league fixtures."
            weak = "Uncertain defined niche in primary starting XI."
            score = 75.0 if is_targetable else 50.0
            alt = "Rasikh Salam"
            tradeoff = "Rasikh Salam is a dedicated domestic death-overs specialist."
    else:
        if "finisher" in role_lower or "lower" in role_lower:
            gap = "No. 7 Lower-Order Pace-Hitting Finisher"
            adv = "High-impact boundary striking against 140kph+ bowling in the death overs."
            weak = "Vulnerability to high-class leg-spin in the middle overs."
            score = 85.0 if is_targetable else 65.0
            alt = "Ashutosh Sharma"
            tradeoff = "Ashutosh Sharma frees up an overseas spot while hitting at extreme death strike rates."
        elif "keeper" in role_lower or "wk" in role_lower:
            gap = "Wicketkeeper-Batter Depth"
            adv = "Protects against injury to Dhruv Jurel and adds middle-order flexibility."
            weak = "Batting position competition in top 6."
            score = 80.0 if is_targetable else 55.0
            alt = "Jamie Smith"
            tradeoff = "Jamie Smith has dynamic 360-degree power hitting against international pace."
        else:
            gap = "Batting Squad Depth"
            adv = "Top/middle-order stabilization during powerplay or middle overs."
            weak = "Redundant with existing core of Jaiswal, Parag, and Jurel."
            score = 72.0 if is_targetable else 50.0
            alt = "Nehal Wadhera"
            tradeoff = "Nehal Wadhera provides versatile middle-order poise."

    return SquadFitEvaluation(
        player_id=player_id,
        player_name=player_name,
        addressed_gap=gap,
        tactical_role=primary_role,
        tactical_advantage=adv,
        primary_weakness=weak,
        squad_fit_score=score,
        confidence_level="Moderate Algorithmic Model B Fit",
        best_alternative_name=alt,
        best_alternative_tradeoff=tradeoff
    )
