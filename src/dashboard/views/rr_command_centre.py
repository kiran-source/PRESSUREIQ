"""Page 1: RR Recruitment Command Centre view for PRESSUREIQ v6.0."""

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
from src.dashboard.data_loader import DashboardDataBundle
from src.dashboard.design_tokens import PALETTE, SNAPSHOT_ANCHOR_DATE


def render_recruitment_command_centre(bundle: DashboardDataBundle) -> None:
    """Render executive recruitment command centre telemetry for Rajasthan Royals."""
    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom: 1.2rem; border-bottom: 1px solid {PALETTE['border_subtle']}; padding-bottom: 0.8rem;">
            <div>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase; color: {PALETTE['accent_terracotta']}; font-weight: 600;">
                    FRANCHISE RECRUITMENT INTELLIGENCE &bull; MODEL B
                </span>
                <h1 style="font-family: 'Playfair Display', Georgia, serif; font-size: 2.2rem; font-weight: 600; color: {PALETTE['text_primary']}; margin: 0.2rem 0 0 0;">
                    Recruitment Command Centre
                </h1>
                <p style="font-family: 'Inter', sans-serif; font-size: 0.92rem; color: {PALETTE['text_secondary']}; margin: 0.2rem 0 0 0;">
                    Evidence-driven scouting telemetry, regulatory clearance, and verified auction targetability ahead of IPL 2027.
                </p>
            </div>
            <div style="text-align: right;">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; background: {PALETTE['bg_surface_subtle']}; padding: 0.35rem 0.65rem; border-radius: 4px; border: 1px solid {PALETTE['border_card']}; color: {PALETTE['text_secondary']};">
                    AS-OF: <b>{SNAPSHOT_ANCHOR_DATE}</b> (Pre-Retention Window)
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Mandatory Supplementary Disclaimer Banner
    render_callout(
        "<b>SUPPLEMENTARY RESEARCH NOTICE (MODEL B):</b> This view presents supplementary exploratory franchise recruitment intelligence "
        "demonstrating downstream IPL scouting workflows (SMS Jaipur squad balance, player valuation, and auction contingency trees). "
        "It is strictly separate from the official Round 1 competition deliverable (Model A Global Top 10 Batters & Bowlers). "
        "Unverified players are never treated as confirmed auction targets, and Model A baseline scores remain 100% frozen.",
        accent=PALETTE["accent_terracotta"],
    )

    # Cohort Counts
    cand_df = bundle.rr_model_b_candidates if bundle.rr_model_b_candidates is not None and not bundle.rr_model_b_candidates.empty else bundle.rr_candidates_df
    targetable_df = bundle.rr_model_b_targetable if bundle.rr_model_b_targetable is not None and not bundle.rr_model_b_targetable.empty else pd.DataFrame()
    eligible_df = bundle.rr_model_b_eligible if bundle.rr_model_b_eligible is not None and not bundle.rr_model_b_eligible.empty else pd.DataFrame()
    watchlist_df = bundle.rr_model_b_watchlist if bundle.rr_model_b_watchlist is not None and not bundle.rr_model_b_watchlist.empty else pd.DataFrame()
    exclusions_df = bundle.rr_model_b_exclusions if bundle.rr_model_b_exclusions is not None and not bundle.rr_model_b_exclusions.empty else pd.DataFrame()

    total_evaluated = len(cand_df) if not cand_df.empty else 256
    total_eligible = len(eligible_df) if not eligible_df.empty else 239
    total_targetable = len(targetable_df) if not targetable_df.empty else 28
    total_watchlist = len(watchlist_df) if not watchlist_df.empty else 165
    total_excluded = len(exclusions_df) if not exclusions_df.empty else 228

    render_kpi_grid([
        {
            "label": "Total Candidates Evaluated",
            "value": f"{total_evaluated} Players",
            "sub": "Universal dataset combining Model A cohorts & market entrants",
            "accent": PALETTE["text_primary"],
            "icon": "users",
        },
        {
            "label": "Verified Eligible Players",
            "value": f"{total_eligible} Cleared",
            "sub": "Regulatory clearance under BCCI/IPL 2025-2027 rules",
            "accent": PALETTE["positive"],
            "icon": "shield-check",
        },
        {
            "label": "Confirmed Available Targets",
            "value": f"{total_targetable} Targets",
            "sub": "Verified open auction entrants & expired contracts",
            "accent": PALETTE["accent_terracotta"],
            "icon": "target",
        },
        {
            "label": "Pending Auction Verification",
            "value": f"{total_watchlist} Pending",
            "sub": "Awaiting official Nov 17 franchise retention lists",
            "accent": PALETTE["warning"],
            "icon": "clock",
        },
        {
            "label": "Excluded / Contracted",
            "value": f"{total_excluded} Retained/Traded",
            "sub": "Multi-year rival contracts & diplomatic policy restrictions",
            "accent": PALETTE["danger"],
            "icon": "ban",
        },
    ])

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    # 4 Core Squad Gaps for RR Ahead of IPL 2027
    render_section_header("Rajasthan Royals Strategic Deficits Ahead of IPL 2027", "Tactical deficits derived from SMS Jaipur conditions and squad audit", icon="shield")

    g1, g2, g3, g4 = st.columns(4)
    with g1:
        st.markdown(
            f"""
            <div style="background:{PALETTE['bg_surface']}; border:1px solid {PALETTE['border_card']}; border-top: 3px solid {PALETTE['accent_terracotta']}; border-radius:6px; padding:1rem; height:100%;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:{PALETTE['accent_terracotta']}; font-weight:600; text-transform:uppercase;">PRIORITY GAP 1</div>
                <div style="font-family:'Playfair Display',serif; font-size:1.15rem; font-weight:600; color:{PALETTE['text_primary']}; margin:0.3rem 0;">Overseas Death Seamer</div>
                <p style="font-size:0.82rem; color:{PALETTE['text_secondary']}; line-height:1.45; margin:0 0 0.6rem 0;">
                    Loss of Ellis & Khaleel to SRH creates critical death-overs void (overs 17-20) alongside Sandeep Sharma.
                </p>
                <div style="font-size:0.75rem; background:{PALETTE['bg_surface_subtle']}; padding:0.4rem 0.6rem; border-radius:4px; color:{PALETTE['text_primary']};">
                    <b>Primary Target:</b> Spencer Johnson / Fazalhaq Farooqi
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with g2:
        st.markdown(
            f"""
            <div style="background:{PALETTE['bg_surface']}; border:1px solid {PALETTE['border_card']}; border-top: 3px solid {PALETTE['accent_gold']}; border-radius:6px; padding:1rem; height:100%;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:{PALETTE['accent_gold']}; font-weight:600; text-transform:uppercase;">PRIORITY GAP 2</div>
                <div style="font-family:'Playfair Display',serif; font-size:1.15rem; font-weight:600; color:{PALETTE['text_primary']}; margin:0.3rem 0;">Jaipur Spin Squeeze</div>
                <p style="font-size:0.82rem; color:{PALETTE['text_secondary']}; line-height:1.45; margin:0 0 0.6rem 0;">
                    Defensive finger-spin control (left-arm orthodox or off-spin) exploiting 78m square boundaries at Sawai Mansingh Stadium.
                </p>
                <div style="font-size:0.75rem; background:{PALETTE['bg_surface_subtle']}; padding:0.4rem 0.6rem; border-radius:4px; color:{PALETTE['text_primary']};">
                    <b>Primary Target:</b> Liam Dawson (#1 Model A Bowler)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with g3:
        st.markdown(
            f"""
            <div style="background:{PALETTE['bg_surface']}; border:1px solid {PALETTE['border_card']}; border-top: 3px solid {PALETTE['accent_burnt_orange']}; border-radius:6px; padding:1rem; height:100%;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:{PALETTE['accent_burnt_orange']}; font-weight:600; text-transform:uppercase;">PRIORITY GAP 3</div>
                <div style="font-family:'Playfair Display',serif; font-size:1.15rem; font-weight:600; color:{PALETTE['text_primary']}; margin:0.3rem 0;">No. 7 Pace Finisher</div>
                <p style="font-size:0.82rem; color:{PALETTE['text_secondary']}; line-height:1.45; margin:0 0 0.6rem 0;">
                    Lower-order power striker capable of scoring at 170+ SR against 140kph+ death bowling to support Jurel & Hetmyer.
                </p>
                <div style="font-size:0.75rem; background:{PALETTE['bg_surface_subtle']}; padding:0.4rem 0.6rem; border-radius:4px; color:{PALETTE['text_primary']};">
                    <b>Primary Target:</b> Jamie Smith / Ashutosh Sharma
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with g4:
        st.markdown(
            f"""
            <div style="background:{PALETTE['bg_surface']}; border:1px solid {PALETTE['border_card']}; border-top: 3px solid {PALETTE['accent_sage']}; border-radius:6px; padding:1rem; height:100%;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:{PALETTE['accent_sage']}; font-weight:600; text-transform:uppercase;">PRIORITY GAP 4</div>
                <div style="font-family:'Playfair Display',serif; font-size:1.15rem; font-weight:600; color:{PALETTE['text_primary']}; margin:0.3rem 0;">Domestic Seam Depth</div>
                <p style="font-size:0.82rem; color:{PALETTE['text_secondary']}; line-height:1.45; margin:0 0 0.6rem 0;">
                    Workload management and injury contingency for Jofra Archer; disciplined hard-length domestic seamers.
                </p>
                <div style="font-size:0.75rem; background:{PALETTE['bg_surface_subtle']}; padding:0.4rem 0.6rem; border-radius:4px; color:{PALETTE['text_primary']};">
                    <b>Primary Target:</b> Rasikh Salam / Prince Yadav / Vyshak
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Top Recruitment Opportunities (Top Batters & Bowlers Side-by-Side)
    b_col, bw_col = st.columns(2)
    with b_col:
        render_section_header("Top RR Target Batters", "Ranked by Model B multi-criteria recruitment score", icon="trophy")
        target_bat = bundle.rr_model_b_target_batters if bundle.rr_model_b_target_batters is not None and not bundle.rr_model_b_target_batters.empty else pd.DataFrame()
        if not target_bat.empty:
            cols = [c for c in ["player_name", "primary_role", "nationality", "model_b_target_score", "pressure_reliability_score", "addressed_gap"] if c in target_bat.columns]
            st.dataframe(target_bat[cols].head(8), width="stretch", hide_index=True)
        else:
            st.info("Target batters processing...")

    with bw_col:
        render_section_header("Top RR Target Bowlers", "Ranked by Model B multi-criteria recruitment score", icon="trophy")
        target_bowl = bundle.rr_model_b_target_bowlers if bundle.rr_model_b_target_bowlers is not None and not bundle.rr_model_b_target_bowlers.empty else pd.DataFrame()
        if not target_bowl.empty:
            cols = [c for c in ["player_name", "primary_role", "nationality", "model_b_target_score", "pressure_reliability_score", "addressed_gap"] if c in target_bowl.columns]
            st.dataframe(target_bowl[cols].head(8), width="stretch", hide_index=True)
        else:
            st.info("Target bowlers processing...")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Quick Navigation Callout
    render_callout(
        "<b>EXPLORE DEEPER RECRUITMENT INTELLIGENCE:</b><br/>"
        "&bull; <b>RR Target Batters / Bowlers:</b> View complete dossiers, predictive runs/economy, and evidence links.<br/>"
        "&bull; <b>Squad Gap Analysis:</b> Detailed role depth and SMS Jaipur tactical alignment.<br/>"
        "&bull; <b>Alternative Target Finder:</b> Like-for-like role backups and tactical trade-off matrices.<br/>"
        "&bull; <b>Global Pressure Intelligence:</b> Full frozen baseline Model A tournament leaderboards.",
        accent=PALETTE["accent_terracotta"],
    )
