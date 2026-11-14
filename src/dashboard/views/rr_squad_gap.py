"""Page 5: Squad Gap Analysis view for PRESSUREIQ v6.0."""

from __future__ import annotations

import streamlit as st
import pandas as pd
from pathlib import Path

from src.dashboard.components import (
    render_callout,
    render_kpi_grid,
    render_section_header,
    status_badge_html,
    render_chart_caption,
)
from src.dashboard.charts import fig_rr_role_depth
from src.dashboard.data_loader import DashboardDataBundle
from src.dashboard.design_tokens import PALETTE


def render_squad_gap_analysis(bundle: DashboardDataBundle) -> None:
    """Render the official Rajasthan Royals Squad Gap Analysis for IPL 2027."""
    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom: 1.2rem; border-bottom: 1px solid {PALETTE['border_subtle']}; padding-bottom: 0.8rem;">
            <div>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase; color: {PALETTE['accent_terracotta']}; font-weight: 600;">
                    STRATEGIC FRANCHISE SCOUTING &bull; SQUAD ARCHITECTURE
                </span>
                <h1 style="font-family: 'Playfair Display', Georgia, serif; font-size: 2.2rem; font-weight: 600; color: {PALETTE['text_primary']}; margin: 0.2rem 0 0 0;">
                    Rajasthan Royals Squad Gap Analysis
                </h1>
                <p style="font-family: 'Inter', sans-serif; font-size: 0.92rem; color: {PALETTE['text_secondary']}; margin: 0.2rem 0 0 0;">
                    Detailed tactical roster audit, SMS Jaipur venue alignment, and priority recruitment targets for IPL 2027.
                </p>
            </div>
            <div style="text-align: right;">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; background: {PALETTE['bg_surface_subtle']}; padding: 0.35rem 0.65rem; border-radius: 4px; border: 1px solid {PALETTE['border_card']}; color: {PALETTE['text_secondary']};">
                    VENUE PROFILE: Sawai Mansingh Stadium (78m Square Boundaries)
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Overview Callout
    render_callout(
        "<b>SMS Jaipur Strategic Imperative:</b> Sawai Mansingh Stadium features the longest square boundary dimensions (78m) "
        "in the IPL. Tactical success relies on restrictive finger-spin control ('Jaipur Squeeze') to limit boundary percentages "
        "and disciplined pace execution with cutters into the pitch. At the same time, away fixtures demand extreme power hitting "
        "at No. 7 and high-velocity death bowling.",
        accent=PALETTE["accent_terracotta"],
    )

    # Roster KPI Summary
    render_kpi_grid([
        {
            "label": "Verified RR Core Squad",
            "value": "11 Players",
            "sub": "Jaiswal, Parag, Jurel, Archer, Sandeep, Hetmyer, Jadeja, Curran",
            "accent": PALETTE["accent_terracotta"],
            "icon": "shield",
        },
        {
            "label": "Overseas Player Slots",
            "value": "3 Active (5 Open)",
            "sub": "Archer, Hetmyer, Curran currently rostered",
            "accent": PALETTE["accent_gold"],
            "icon": "globe",
        },
        {
            "label": "Critical Tactical Gaps",
            "value": "4 Deficits",
            "sub": "Death Seamer &bull; Spin Squeeze &bull; No. 7 Finisher &bull; Seam Depth",
            "accent": PALETTE["danger"],
            "icon": "alert-triangle",
        },
        {
            "label": "Targetable Auction Pool",
            "value": "28 Evaluated",
            "sub": "Pre-qualified open-auction candidates under Model B",
            "accent": PALETTE["positive"],
            "icon": "target",
        },
    ])

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Current Roster & Role Depth
    c1, c2 = st.columns([1.1, 0.9])
    with c1:
        render_section_header("Current Verified RR Squad Core", "Retained core & confirmed arrivals ahead of auction", icon="users")
        core_data = [
            {"Player": "Yashasvi Jaiswal", "Role": "Indian Opener", "Discipline": "Batting", "Status": "Retained Core", "Key Strength": "Powerplay boundary acceleration"},
            {"Player": "Riyan Parag", "Role": "Middle-Order All-Rounder", "Discipline": "Batting", "Status": "Retained Core", "Key Strength": "Spin hitting & crisis stabilization"},
            {"Player": "Dhruv Jurel", "Role": "Wicketkeeper-Finisher", "Discipline": "Batting", "Status": "Retained Core", "Key Strength": "Composure under pressure (#22 Model A)"},
            {"Player": "Shimron Hetmyer", "Role": "Overseas Power Finisher", "Discipline": "Batting", "Status": "Retained Core", "Key Strength": "Death overs boundary percentage"},
            {"Player": "Ravindra Jadeja", "Role": "Spin All-Rounder", "Discipline": "All-Rounder", "Status": "Traded In (CSK)", "Key Strength": "World-class fielding & left-arm spin"},
            {"Player": "Sam Curran", "Role": "Seam All-Rounder", "Discipline": "All-Rounder", "Status": "Traded In (PBKS)", "Key Strength": "Death overs variations & batting depth"},
            {"Player": "Jofra Archer", "Role": "Lead Fast Bowler", "Discipline": "Bowling", "Status": "Retained Core", "Key Strength": "Express 150kph pace & bounce (#16 Bowler)"},
            {"Player": "Sandeep Sharma", "Role": "Domestic Death Specialist", "Discipline": "Bowling", "Status": "Retained Core", "Key Strength": "Wide yorkers & knuckle-ball execution"},
            {"Player": "Tushar Deshpande", "Role": "Indian Seamer", "Discipline": "Bowling", "Status": "Retained Core", "Key Strength": "New-ball swing & hit-the-deck pace"},
            {"Player": "Vaibhav Sooryavanshi", "Role": "Emerging Opener", "Discipline": "Batting", "Status": "Retained Core", "Key Strength": "High-ceiling prospect"},
            {"Player": "Donovan Ferreira", "Role": "Overseas Finisher", "Discipline": "Batting", "Status": "Retained Core", "Key Strength": "Explosive lower-order power"},
        ]
        st.dataframe(pd.DataFrame(core_data), width="stretch", hide_index=True)

    with c2:
        render_section_header("Role Depth & Deficit Visualization", "Distribution across tactical responsibility tiers", icon="bar-chart-2")
        role_df = pd.DataFrame([
            {"Role": "Top-Order Batting", "Current Depth": 2, "Status": "Solid"},
            {"Role": "Middle-Order Core", "Current Depth": 3, "Status": "Adequate"},
            {"Role": "#7 Power Finisher", "Current Depth": 1, "Status": "Critical Deficit"},
            {"Role": "Finger-Spin Control", "Current Depth": 1, "Status": "Deficit (Jaipur)"},
            {"Role": "Lead Express Pace", "Current Depth": 1, "Status": "Workload Risk"},
            {"Role": "Death Overs Seam", "Current Depth": 1, "Status": "Critical Deficit"},
            {"Role": "Domestic Seam Depth", "Current Depth": 1, "Status": "Deficit"},
        ])
        st.dataframe(role_df, width="stretch", hide_index=True)
        render_chart_caption("Role depth assessment highlights two critical vulnerabilities: reliance on a single specialist at the death (Sandeep Sharma) and missing lower-order finishing depth.")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 4 Deep Dives into Critical Gaps
    render_section_header("Deep-Dive: The 4 Priority Recruitment Targets", "Detailed tactical rationale and recommended targets", icon="target")

    d1, d2 = st.columns(2)
    with d1:
        st.markdown(
            f"""
            <div style="background:{PALETTE['bg_surface']}; border:1px solid {PALETTE['border_card']}; border-radius:6px; padding:1.2rem; margin-bottom:1rem;">
                <span style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:{PALETTE['accent_terracotta']}; font-weight:600; text-transform:uppercase;">DEFICIT 1</span>
                <h3 style="font-family:'Playfair Display',serif; font-size:1.3rem; margin:0.3rem 0; color:{PALETTE['text_primary']};">Overseas Death-Overs Seamer (Overs 17–20)</h3>
                <p style="font-size:0.85rem; color:{PALETTE['text_secondary']}; line-height:1.5;">
                    <b>Why RR Needs This:</b> With Nathan Ellis traded to SRH and Arshdeep Singh traded to MI, RR has zero overseas pace specialists 
                    for the final 4 overs. Sandeep Sharma requires a high-pace partner with a sharp yorker to prevent opposition late-order surges.
                </p>
                <div style="background:{PALETTE['bg_surface_subtle']}; padding:0.6rem 0.8rem; border-radius:4px; font-size:0.8rem;">
                    <b>Primary Target:</b> Spencer Johnson (145kph left-arm express, death yorkers)<br/>
                    <b>Best Alternative:</b> Fazalhaq Farooqi (Subcontinental swing and death execution)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="background:{PALETTE['bg_surface']}; border:1px solid {PALETTE['border_card']}; border-radius:6px; padding:1.2rem;">
                <span style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:{PALETTE['accent_terracotta']}; font-weight:600; text-transform:uppercase;">DEFICIT 2</span>
                <h3 style="font-family:'Playfair Display',serif; font-size:1.3rem; margin:0.3rem 0; color:{PALETTE['text_primary']};">SMS Jaipur Finger-Spin Controller ('Jaipur Squeeze')</h3>
                <p style="font-size:0.85rem; color:{PALETTE['text_secondary']}; line-height:1.5;">
                    <b>Why RR Needs This:</b> Jaipur's 78-meter square boundaries reward defensive finger spinners who bowl flat trajectories (6.5–7.2 rpo) 
                    and force batsmen to hit to the longest parts of the ground. Jadeja requires a restrictive partner.
                </p>
                <div style="background:{PALETTE['bg_surface_subtle']}; padding:0.6rem 0.8rem; border-radius:4px; font-size:0.8rem;">
                    <b>Primary Target:</b> Liam Dawson (#1 Model A Bowler, 95.4 Rel, 6.8 rpo middle overs)<br/>
                    <b>Best Alternative:</b> Allah Ghazanfar (Mystery off-spin variation) / Tanush Kotian (Domestic)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with d2:
        st.markdown(
            f"""
            <div style="background:{PALETTE['bg_surface']}; border:1px solid {PALETTE['border_card']}; border-radius:6px; padding:1.2rem; margin-bottom:1rem;">
                <span style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:{PALETTE['accent_terracotta']}; font-weight:600; text-transform:uppercase;">DEFICIT 3</span>
                <h3 style="font-family:'Playfair Display',serif; font-size:1.3rem; margin:0.3rem 0; color:{PALETTE['text_primary']};">No. 7 Lower-Order Pace-Hitting Finisher</h3>
                <p style="font-size:0.85rem; color:{PALETTE['text_secondary']}; line-height:1.5;">
                    <b>Why RR Needs This:</b> With Sanju Samson departing to CSK and middle-order roles shifting, RR requires an explosive 
                    power striker who can enter in overs 16–18 and hit 140kph+ bowling for sixes from ball one.
                </p>
                <div style="background:{PALETTE['bg_surface_subtle']}; padding:0.6rem 0.8rem; border-radius:4px; font-size:0.8rem;">
                    <b>Primary Target:</b> Jamie Smith (360-degree power hitter against high pace)<br/>
                    <b>Best Alternative:</b> Ashutosh Sharma (Domestic Indian crunch-time finisher) / Jacob Bethell
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="background:{PALETTE['bg_surface']}; border:1px solid {PALETTE['border_card']}; border-radius:6px; padding:1.2rem;">
                <span style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:{PALETTE['accent_terracotta']}; font-weight:600; text-transform:uppercase;">DEFICIT 4</span>
                <h3 style="font-family:'Playfair Display',serif; font-size:1.3rem; margin:0.3rem 0; color:{PALETTE['text_primary']};">Domestic Indian Seam Depth</h3>
                <p style="font-size:0.85rem; color:{PALETTE['text_secondary']}; line-height:1.5;">
                    <b>Why RR Needs This:</b> Jofra Archer's long-term injury history requires planned rotation during back-to-back fixtures. 
                    RR needs reliable domestic Indian fast bowlers who can execute hard lengths and maintain discipline.
                </p>
                <div style="background:{PALETTE['bg_surface_subtle']}; padding:0.6rem 0.8rem; border-radius:4px; font-size:0.8rem;">
                    <b>Primary Target:</b> Rasikh Salam (Deceptive knuckle-ball & death overs)<br/>
                    <b>Best Alternative:</b> Prince Yadav (140kph burst speed) / Vyshak Kumar (Heavy ball hard lengths)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
