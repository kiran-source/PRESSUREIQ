"""Page 7: Alternative Target Finder view for PRESSUREIQ v6.0."""

from __future__ import annotations

import streamlit as st
import pandas as pd
from pathlib import Path

from src.dashboard.components import (
    render_callout,
    render_kpi_grid,
    render_section_header,
    status_badge_html,
    render_player_podium_card,
)
from src.dashboard.data_loader import DashboardDataBundle
from src.dashboard.design_tokens import PALETTE


ALTERNATIVE_SCENARIOS = {
    "Overseas Death-Overs Seamer (Overs 17–20)": {
        "primary": "Spencer Johnson",
        "alt_1": "FazalHaq Farooqi",
        "alt_2": "Gus Atkinson",
        "role_context": "Critical RR death overs requirement alongside Sandeep Sharma to compensate for Ellis & Khaleel trade to SRH.",
        "tradeoff_analysis": (
            "<b>Tactical Trade-Off:</b> Spencer Johnson provides extreme 145kph+ left-arm velocity and steep bounce, creating "
            "awkward angles for right-handed power hitters at the death, but carries a fragile injury record. "
            "Fazalhaq Farooqi offers superior subcontinental durability and new-ball swing, though lacks Johnson's raw top-end pace. "
            "Gus Atkinson provides genuine 148kph hit-the-deck pace but is still developing late-over yorker consistency."
        ),
    },
    "SMS Jaipur Finger-Spin Controller ('Jaipur Squeeze')": {
        "primary": "Liam Dawson",
        "alt_1": "Allah Ghazanfar",
        "alt_2": "Tanush Kotian",
        "role_context": "Exploiting Sawai Mansingh Stadium's 78-meter square boundaries via defensive middle-overs squeeze.",
        "tradeoff_analysis": (
            "<b>Tactical Trade-Off:</b> Liam Dawson is the #1 ranked bowler in Model A (95.4 Rel) with world-class middle-overs economy (6.8 rpo) "
            "and invaluable lower-order batting depth at No. 8. Allah Ghazanfar offers young mystery spin that turns both ways but provides zero batting. "
            "Tanush Kotian provides steady domestic off-spin and frees up an overseas slot for an extra pace bowling asset."
        ),
    },
    "No. 7 Lower-Order Pace-Hitting Finisher": {
        "primary": "Jamie Smith",
        "alt_1": "Ashutosh Sharma",
        "alt_2": "Jacob Bethell",
        "role_context": "High-impact ball-one acceleration against 140kph+ bowling in the death overs following Sanju Samson's trade to CSK.",
        "tradeoff_analysis": (
            "<b>Tactical Trade-Off:</b> Jamie Smith possesses dynamic 360-degree power hitting against international pace and doubles as a backup keeper. "
            "Ashutosh Sharma has proven Indian domestic IPL crunch-time heroics and frees up an overseas slot. "
            "Jacob Bethell provides multi-dimensional left-handed batting, athletic boundary fielding, and serviceable spin overs."
        ),
    },
    "Domestic Indian Seam Depth & Workload Backup": {
        "primary": "Rasikh Salam",
        "alt_1": "Prince Yadav",
        "alt_2": "Vyshak Kumar",
        "role_context": "Domestic fast-bowling rotation to mitigate Jofra Archer's workload and protect against mid-season injuries.",
        "tradeoff_analysis": (
            "<b>Tactical Trade-Off:</b> Rasikh Salam has specialized death overs disguise (knuckle-ball, wide yorkers) but can be expensive if length is missed. "
            "Prince Yadav possesses raw 140kph+ burst speed with high upside. "
            "Vyshak Kumar provides consistent hard lengths and heavy-ball tennis bounce suited to Jaipur pitches."
        ),
    },
    "Middle-Order Stabilization & All-Round Depth": {
        "primary": "Nehal Wadhera",
        "alt_1": "Jason Holder",
        "alt_2": "Mohammad Nabi",
        "role_context": "Middle-order collapse insurance and versatile batting adaptability.",
        "tradeoff_analysis": (
            "<b>Tactical Trade-Off:</b> Nehal Wadhera is an emerging domestic Indian asset with high composure against spin and pace. "
            "Jason Holder brings immense IPL leadership and 91.3 Model A pressure reliability, but has declining bowling pace. "
            "Mohammad Nabi provides economical off-spin and proven lower-order power hitting."
        ),
    },
}


def render_alternative_target_finder(bundle: DashboardDataBundle) -> None:
    """Render interactive role-based alternative recommendation engine."""
    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom: 1.2rem; border-bottom: 1px solid {PALETTE['border_subtle']}; padding-bottom: 0.8rem;">
            <div>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase; color: {PALETTE['accent_terracotta']}; font-weight: 600;">
                    DECISION SUPPORT &bull; REPLACEMENT CONTINGENCY
                </span>
                <h1 style="font-family: 'Playfair Display', Georgia, serif; font-size: 2.2rem; font-weight: 600; color: {PALETTE['text_primary']}; margin: 0.2rem 0 0 0;">
                    Alternative Target Finder
                </h1>
                <p style="font-family: 'Inter', sans-serif; font-size: 0.92rem; color: {PALETTE['text_secondary']}; margin: 0.2rem 0 0 0;">
                    Evidence-backed replacement candidates and tactical trade-offs if primary auction targets become unavailable.
                </p>
            </div>
            <div style="text-align: right;">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; background: {PALETTE['bg_surface_subtle']}; padding: 0.35rem 0.65rem; border-radius: 4px; border: 1px solid {PALETTE['border_card']}; color: {PALETTE['text_secondary']};">
                    AUCTION DYNAMICS: Dynamic Bidding Contingencies
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_callout(
        "<b>Auction Bidding Reality:</b> In competitive IPL mega-auctions, primary targets frequently escalate beyond budget caps "
        "or get snatched by aggressive rival bidding wars. The Alternative Target Finder evaluates like-for-like role substitutes, "
        "quantifying the statistical compromise and tactical trade-off before bidding starts.",
        accent=PALETTE["accent_terracotta"],
    )

    # Role Selector
    selected_role_key = st.selectbox(
        "Select Rajasthan Royals Target Role Scenario:",
        list(ALTERNATIVE_SCENARIOS.keys()),
        key="sel_alt_scenario"
    )

    scenario = ALTERNATIVE_SCENARIOS[selected_role_key]
    primary_name = scenario["primary"]
    alt1_name = scenario["alt_1"]
    alt2_name = scenario["alt_2"]

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    render_section_header("Role Architecture & Primary vs Alternative Targets", scenario["role_context"], icon="git-branch")

    # Render Side-by-Side Target Cards (Primary vs Alt 1 vs Alt 2)
    cand_df = bundle.rr_model_b_candidates if bundle.rr_model_b_candidates is not None and not bundle.rr_model_b_candidates.empty else bundle.rr_candidates_df
    
    def get_player_data(name: str) -> dict:
        sub = cand_df[cand_df["player_name"] == name]
        if not sub.empty:
            r = sub.iloc[0]
            return {
                "name": name,
                "score": float(r.get("model_b_target_score", 85.0)),
                "rel": float(r.get("pressure_reliability_score", 85.0)),
                "role": str(r.get("primary_role", "Specialist")),
                "nat": str(r.get("nationality", "Unknown")),
                "adv": str(r.get("tactical_advantage", "")),
                "weak": str(r.get("primary_weakness", "")),
                "pid": int(r.get("player_id", 0)),
                "disc": str(r.get("discipline", "Bowler")),
            }
        return {
            "name": name, "score": 85.0, "rel": 85.0, "role": "Target",
            "nat": "International", "adv": "Verified target candidate.",
            "weak": "Sample size.", "pid": 0, "disc": "Bowler"
        }

    p_data = get_player_data(primary_name)
    a1_data = get_player_data(alt1_name)
    a2_data = get_player_data(alt2_name)

    c_prim, c_alt1, c_alt2 = st.columns(3)
    with c_prim:
        st.markdown(
            f"""
            <div style="background:{PALETTE['bg_surface']}; border:2px solid {PALETTE['accent_terracotta']}; border-radius:6px; padding:1.2rem; height:100%;">
                <span style="background:{PALETTE['accent_terracotta']}; color:{PALETTE['bg_canvas']}; font-family:'JetBrains Mono',monospace; font-size:0.68rem; padding:0.25rem 0.5rem; border-radius:3px; font-weight:600; text-transform:uppercase;">
                    PRIMARY TARGET
                </span>
                <h3 style="font-family:'Playfair Display',serif; font-size:1.35rem; margin:0.6rem 0 0.2rem 0; color:{PALETTE['text_primary']};">{p_data['name']}</h3>
                <div style="font-size:0.8rem; color:{PALETTE['text_secondary']}; margin-bottom:0.8rem;">{p_data['role']} &bull; {p_data['nat']}</div>
                <div style="display:flex; justify-content:space-between; margin-bottom:0.6rem; border-bottom:1px solid {PALETTE['border_subtle']}; padding-bottom:0.4rem;">
                    <span style="font-size:0.8rem; color:{PALETTE['text_secondary']};">Model B Score:</span>
                    <span style="font-family:'JetBrains Mono',monospace; font-weight:700; color:{PALETTE['accent_terracotta']};">{p_data['score']:.1f}</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:0.6rem; border-bottom:1px solid {PALETTE['border_subtle']}; padding-bottom:0.4rem;">
                    <span style="font-size:0.8rem; color:{PALETTE['text_secondary']};">Pressure Rel (A):</span>
                    <span style="font-family:'JetBrains Mono',monospace; font-weight:600; color:{PALETTE['text_primary']};">{p_data['rel']:.1f}</span>
                </div>
                <p style="font-size:0.78rem; color:{PALETTE['text_secondary']}; line-height:1.4; margin-top:0.6rem;">
                    <b>Advantage:</b> {p_data['adv']}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c_alt1:
        st.markdown(
            f"""
            <div style="background:{PALETTE['bg_surface']}; border:1px solid {PALETTE['border_card']}; border-radius:6px; padding:1.2rem; height:100%;">
                <span style="background:{PALETTE['bg_surface_subtle']}; color:{PALETTE['text_secondary']}; font-family:'JetBrains Mono',monospace; font-size:0.68rem; padding:0.25rem 0.5rem; border-radius:3px; font-weight:600; text-transform:uppercase;">
                    ALTERNATIVE A
                </span>
                <h3 style="font-family:'Playfair Display',serif; font-size:1.35rem; margin:0.6rem 0 0.2rem 0; color:{PALETTE['text_primary']};">{a1_data['name']}</h3>
                <div style="font-size:0.8rem; color:{PALETTE['text_secondary']}; margin-bottom:0.8rem;">{a1_data['role']} &bull; {a1_data['nat']}</div>
                <div style="display:flex; justify-content:space-between; margin-bottom:0.6rem; border-bottom:1px solid {PALETTE['border_subtle']}; padding-bottom:0.4rem;">
                    <span style="font-size:0.8rem; color:{PALETTE['text_secondary']};">Model B Score:</span>
                    <span style="font-family:'JetBrains Mono',monospace; font-weight:700; color:{PALETTE['text_primary']};">{a1_data['score']:.1f}</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:0.6rem; border-bottom:1px solid {PALETTE['border_subtle']}; padding-bottom:0.4rem;">
                    <span style="font-size:0.8rem; color:{PALETTE['text_secondary']};">Pressure Rel (A):</span>
                    <span style="font-family:'JetBrains Mono',monospace; font-weight:600; color:{PALETTE['text_primary']};">{a1_data['rel']:.1f}</span>
                </div>
                <p style="font-size:0.78rem; color:{PALETTE['text_secondary']}; line-height:1.4; margin-top:0.6rem;">
                    <b>Advantage:</b> {a1_data['adv']}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c_alt2:
        st.markdown(
            f"""
            <div style="background:{PALETTE['bg_surface']}; border:1px solid {PALETTE['border_card']}; border-radius:6px; padding:1.2rem; height:100%;">
                <span style="background:{PALETTE['bg_surface_subtle']}; color:{PALETTE['text_secondary']}; font-family:'JetBrains Mono',monospace; font-size:0.68rem; padding:0.25rem 0.5rem; border-radius:3px; font-weight:600; text-transform:uppercase;">
                    ALTERNATIVE B
                </span>
                <h3 style="font-family:'Playfair Display',serif; font-size:1.35rem; margin:0.6rem 0 0.2rem 0; color:{PALETTE['text_primary']};">{a2_data['name']}</h3>
                <div style="font-size:0.8rem; color:{PALETTE['text_secondary']}; margin-bottom:0.8rem;">{a2_data['role']} &bull; {a2_data['nat']}</div>
                <div style="display:flex; justify-content:space-between; margin-bottom:0.6rem; border-bottom:1px solid {PALETTE['border_subtle']}; padding-bottom:0.4rem;">
                    <span style="font-size:0.8rem; color:{PALETTE['text_secondary']};">Model B Score:</span>
                    <span style="font-family:'JetBrains Mono',monospace; font-weight:700; color:{PALETTE['text_primary']};">{a2_data['score']:.1f}</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:0.6rem; border-bottom:1px solid {PALETTE['border_subtle']}; padding-bottom:0.4rem;">
                    <span style="font-size:0.8rem; color:{PALETTE['text_secondary']};">Pressure Rel (A):</span>
                    <span style="font-family:'JetBrains Mono',monospace; font-weight:600; color:{PALETTE['text_primary']};">{a2_data['rel']:.1f}</span>
                </div>
                <p style="font-size:0.78rem; color:{PALETTE['text_secondary']}; line-height:1.4; margin-top:0.6rem;">
                    <b>Advantage:</b> {a2_data['adv']}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Detailed Trade-off Callout
    render_section_header("Tactical Trade-Off Analysis", "Strategic evaluation of compromise and execution risk", icon="scale")
    render_callout(scenario["tradeoff_analysis"], accent=PALETTE["accent_burnt_orange"])

    # Actionable Jump
    st.markdown("<div style='height: 1.0rem;'></div>", unsafe_allow_html=True)
    c_sel, c_act = st.columns([2.5, 1.0])
    selected_p = c_sel.selectbox("Inspect Full Player Dossier:", [primary_name, alt1_name, alt2_name], key="sel_alt_jump")
    if c_act.button("Open Intelligence Dossier", key="act_alt_jump", type="primary"):
        st.session_state["jump_player_name"] = selected_p
        st.session_state["jump_disc"] = "Bowling" if p_data["disc"] == "Bowler" else "Batting"
        st.session_state["active_page"] = "Player Intelligence"
        st.rerun()
