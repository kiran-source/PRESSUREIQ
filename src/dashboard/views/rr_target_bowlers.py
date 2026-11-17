"""Page 3: RR Target Bowlers view for PRESSUREIQ v6.0."""

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


def render_rr_target_bowlers(bundle: DashboardDataBundle) -> None:
    """Render the official Rajasthan Royals Target Bowlers board under Model B."""
    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom: 1.2rem; border-bottom: 1px solid {PALETTE['border_subtle']}; padding-bottom: 0.8rem;">
            <div>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase; color: {PALETTE['accent_terracotta']}; font-weight: 600;">
                    MODEL B &bull; AUCTION ACQUISITION BOARD
                </span>
                <h1 style="font-family: 'Playfair Display', Georgia, serif; font-size: 2.2rem; font-weight: 600; color: {PALETTE['text_primary']}; margin: 0.2rem 0 0 0;">
                    Rajasthan Royals Target Bowlers
                </h1>
                <p style="font-family: 'Inter', sans-serif; font-size: 0.92rem; color: {PALETTE['text_secondary']}; margin: 0.2rem 0 0 0;">
                    Verified eligible and realistically targetable bowlers addressing Rajasthan Royals squad gaps for IPL 2027.
                </p>
            </div>
            <div style="text-align: right;">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; background: {PALETTE['bg_surface_subtle']}; padding: 0.35rem 0.65rem; border-radius: 4px; border: 1px solid {PALETTE['border_card']}; color: {PALETTE['text_secondary']};">
                    WEIGHTS: Rel 25% &bull; T20 20% &bull; Pred 15% &bull; Role 15% &bull; RR Fit 15% &bull; Cons 10%
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Supplementary Disclaimer
    render_callout(
        "<b>SUPPLEMENTARY RESEARCH NOTICE (MODEL B):</b> Unlike global competition deliverables (Model A), this board presents supplementary "
        "franchise-specific recruitment analysis. It strictly excludes retained rival franchise bowlers (Jasprit Bumrah at MI, "
        "Matheesha Pathirana at KKR, Rashid Khan at GT) and confirmed traded bowlers (Nathan Ellis to SRH, Arshdeep Singh to MI, "
        "Kuldeep Yadav to LSG, T Natarajan to SRH). Only verified eligible, open auction targets appear here.",
        accent=PALETTE["accent_terracotta"],
    )

    df = bundle.rr_model_b_target_bowlers if bundle.rr_model_b_target_bowlers is not None and not bundle.rr_model_b_target_bowlers.empty else pd.DataFrame()
    if df.empty:
        st.warning("Model B Target Bowlers dataset is currently being compiled.")
        return

    # Filter Controls
    f1, f2, f3 = st.columns([1.2, 1.2, 1.6])
    roles = ["All"] + sorted(df["primary_role"].dropna().unique().tolist())
    selected_role = f1.selectbox("Filter by Primary Role", roles, key="target_bowl_role")
    
    nat_filter = f2.selectbox("Player Classification", ["All Players", "Indian Domestic Only", "Overseas Only"], key="target_bowl_nat")
    min_score = f3.slider("Minimum Model B Recruitment Score", min_value=50.0, max_value=95.0, value=65.0, step=1.0, key="target_bowl_score")

    filtered = df.copy()
    if selected_role != "All":
        filtered = filtered[filtered["primary_role"] == selected_role]
    if nat_filter == "Indian Domestic Only":
        filtered = filtered[~filtered["is_overseas"]]
    elif nat_filter == "Overseas Only":
        filtered = filtered[filtered["is_overseas"]]
    filtered = filtered[filtered["model_b_target_score"] >= min_score].reset_index(drop=True)

    # Top Podium / Spotlight Cards for Top 3
    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    render_section_header("Recruitment Target Spotlight", "Primary auction acquisition priorities evaluated for Rajasthan Royals", icon="star")

    top3 = filtered.head(3)
    p_cols = st.columns(3)
    for idx, (_, r) in enumerate(top3.iterrows()):
        with p_cols[idx]:
            render_player_podium_card(
                rank=idx + 1,
                name=r["player_name"],
                discipline="Bowler",
                role=f"{r['primary_role']} ({r['nationality']})",
                score=float(r["model_b_target_score"]),
                pava=float(r.get("pressure_reliability_score", 0.0)),
                balls=int(r.get("hp_balls", 0)),
                archetype=str(r.get("prc_archetype", "Ice Cold Anchor")),
                player_id=int(r.get("player_id", 0)),
            )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Detailed Editorial Target Board Table
    render_section_header(f"Candidate Board ({len(filtered)} Targets Qualified)", "Complete recruitment telemetry and evidence links", icon="table")

    display_cols = [
        "player_name", "nationality", "primary_role", "bowling_style", "model_b_target_score",
        "pressure_reliability_score", "overall_performance_score", "predictive_score",
        "rr_squad_fit_score", "addressed_gap", "auction_availability"
    ]
    renamed_cols = {
        "player_name": "Candidate",
        "nationality": "Origin",
        "primary_role": "Tactical Role",
        "bowling_style": "Discipline Style",
        "model_b_target_score": "Model B Score",
        "pressure_reliability_score": "Pressure Rel (A)",
        "overall_performance_score": "T20 Perf",
        "predictive_score": "Pred Score",
        "rr_squad_fit_score": "RR Fit",
        "addressed_gap": "Addressed RR Squad Need",
        "auction_availability": "Auction Status"
    }

    st.dataframe(
        filtered[display_cols].rename(columns=renamed_cols),
        width="stretch",
        hide_index=True
    )

    # Interactive Jump to Dossier
    st.markdown("<div style='height: 1.0rem;'></div>", unsafe_allow_html=True)
    c_sel, c_act = st.columns([2.5, 1.0])
    selected_p = c_sel.selectbox("Select Candidate to Inspect Intelligence Dossier:", filtered["player_name"].tolist(), key="sel_target_bowl")
    if c_act.button("Open Player Intelligence Dossier", key="jump_target_bowl", type="primary"):
        st.session_state["jump_player_name"] = selected_p
        st.session_state["jump_disc"] = "Bowling"
        st.session_state["active_page"] = "Player Intelligence"
        st.rerun()
