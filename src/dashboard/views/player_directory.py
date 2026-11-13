"""Milestone 5 view: Searchable visual catalog for all 227 qualified athletes (v5.0 Section 8)."""

from __future__ import annotations

import html
from typing import Any, Dict, List
import pandas as pd
import streamlit as st

from src.dashboard.components import (
    jump_to_player,
    render_callout,
    render_empty_state,
    render_kpi_grid,
    render_section_header,
)
from src.dashboard.data_loader import DashboardDataBundle
from src.dashboard.design_tokens import PALETTE
from src.dashboard.player_images import get_player_image_b64


def _build_unified_directory(bundle: DashboardDataBundle) -> pd.DataFrame:
    records: List[Dict[str, Any]] = []

    # Process batters
    if not bundle.bat_df.empty:
        for _, r in bundle.bat_df.iterrows():
            records.append({
                "player_id": int(r["player_id"]),
                "player_name": str(r["player_name"]),
                "discipline": "Batting",
                "rank": int(r["rank"]),
                "role": str(r.get("role", "Batter")),
                "team": str(r.get("dataset_ipl_team", "International")),
                "reliability_score": float(r["reliability_score"]),
                "score_ci_95": str(r.get("score_ci_95", "N/A")),
                "hp_balls": int(r["hp_balls"]),
                "shrunk_pava": float(r.get("shrunk_hp_pava_per_ball", 0.0)),
                "top10_prob": float(r.get("top10_inclusion_prob", 0.0)),
            })

    # Process bowlers
    if not bundle.bowl_df.empty:
        for _, r in bundle.bowl_df.iterrows():
            records.append({
                "player_id": int(r["player_id"]),
                "player_name": str(r["player_name"]),
                "discipline": "Bowling",
                "rank": int(r["rank"]),
                "role": str(r.get("bowling_type", "Bowler")),
                "team": str(r.get("dataset_ipl_team", "International")),
                "reliability_score": float(r["reliability_score"]),
                "score_ci_95": str(r.get("score_ci_95", "N/A")),
                "hp_balls": int(r["hp_balls"]),
                "shrunk_pava": float(r.get("shrunk_hp_pava_per_ball", 0.0)),
                "top10_prob": float(r.get("top10_inclusion_prob", 0.0)),
            })

    return pd.DataFrame(records)


def render_player_directory(bundle: DashboardDataBundle) -> None:
    """Render full visual player directory with search, filters, grid/table view modes."""
    st.title("Player Directory")
    render_callout(
        "<b>Visual Scouting Catalog:</b> Browse all <b>227 qualified athletes</b> (109 batters, 147 bowlers) "
        "screened under strict Model A qualification criteria (>=400 career balls, >=30 high-pressure deliveries, >=20 matches). "
        "Select any card to jump immediately to the full player intelligence dossier.",
        accent=PALETTE["accent_terracotta"],
    )

    df = _build_unified_directory(bundle)
    if df.empty:
        render_empty_state("No player directory data found", "Verify frozen ranking files are loaded.")
        return

    # Top search & quick filter controls
    c_s, c_d, c_v = st.columns([1.8, 1.2, 1.0])
    search_q = c_s.text_input("Instant Player Search", placeholder="Type athlete name...", key="dir_search")
    disc_filter = c_d.radio("Discipline Filter", ["All Athletes", "Batters Only", "Bowlers Only"], horizontal=True, key="dir_disc")
    view_mode = c_v.radio("Display Mode", ["Photo Grid", "Compact Table"], horizontal=True, key="dir_view_mode")

    # Second row filters: Role, Team, Sort
    f1, f2, f3 = st.columns([1.2, 1.2, 1.6])

    # Filter by discipline
    filtered = df.copy()
    if disc_filter == "Batters Only":
        filtered = filtered[filtered["discipline"] == "Batting"]
    elif disc_filter == "Bowlers Only":
        filtered = filtered[filtered["discipline"] == "Bowling"]

    # Role filter
    all_roles = sorted(filtered["role"].dropna().unique().tolist())
    sel_roles = f1.multiselect("Filter by Role / Bowling Style", all_roles, default=[], key="dir_roles", placeholder="All Roles")
    if sel_roles:
        filtered = filtered[filtered["role"].isin(sel_roles)]

    # Team filter
    all_teams = sorted(filtered["team"].dropna().unique().tolist())
    sel_team = f2.selectbox("Filter by Squad / Team", ["All Squads"] + all_teams, key="dir_team")
    if sel_team != "All Squads":
        filtered = filtered[filtered["team"] == sel_team]

    # Search filter
    if search_q.strip():
        q_lower = search_q.strip().lower()
        filtered = filtered[filtered["player_name"].str.lower().str.contains(q_lower, na=False)]

    # Sort options
    sort_opts = {
        "Reliability Score (High → Low)": ("reliability_score", False),
        "Model A Rank (Ascending)": ("rank", True),
        "High-Pressure Deliveries (Volume)": ("hp_balls", False),
        "Alphabetical (A–Z)": ("player_name", True),
        "Shrunk HP PAVA (Highest Surplus)": ("shrunk_pava", False),
    }
    sel_sort = f3.selectbox("Sort Order", list(sort_opts.keys()), key="dir_sort")
    sort_col, sort_asc = sort_opts[sel_sort]
    filtered = filtered.sort_values(sort_col, ascending=sort_asc)

    # Indicator
    total_athletes = len(set(df["player_name"]))
    matched_athletes = len(set(filtered["player_name"]))
    st.caption(f"Showing **{len(filtered)}** cohort dossiers across **{matched_athletes}** unique qualified athletes (total tournament pool: **{total_athletes}** athletes).")

    if filtered.empty:
        render_empty_state("No athletes match current filters", "Try clearing search text or resetting role and squad selections.")
        return

    if view_mode == "Photo Grid":
        rows_list = list(filtered.iterrows())
        for row_idx in range(0, len(rows_list), 4):
            chunk = rows_list[row_idx:row_idx + 4]
            cols = st.columns(4)
            for c_idx, (_, r) in enumerate(chunk):
                pname = str(r["player_name"])
                pid = int(r["player_id"])
                disc = str(r["discipline"])
                rank = int(r["rank"])
                role = str(r["role"])
                team = str(r["team"])
                score = float(r["reliability_score"])
                pava = float(r["shrunk_pava"])
                b64_img = get_player_image_b64(pname)

                medallion_color = "#C5A46D" if rank == 1 else ("#BD6548" if rank <= 3 else "#77675D")
                disc_badge = "BAT" if disc == "Batting" else "BOWL"

                card_html = (
                    f'<div class="piq-dir-card">'
                    f'<div class="piq-dir-rank" style="background:#282321;color:{medallion_color};border:1px solid {medallion_color};">#{rank} {disc_badge}</div>'
                    f'<img src="{b64_img}" alt="{html.escape(pname)}" class="piq-dir-portrait" loading="eager" />'
                    f'<div class="piq-dir-name">{html.escape(pname)}</div>'
                    f'<div class="piq-dir-meta">{html.escape(role)} · {html.escape(team)}</div>'
                    f'<div class="piq-dir-score-box">'
                    f'<span class="piq-dir-score-val">{score:.2f}</span>'
                    f'<span class="piq-dir-score-label">Score</span>'
                    f'</div>'
                    f'<div style="font-size:0.72rem;color:#77675D;margin-bottom:10px;">'
                    f'HP PAVA: <b style="font-family:var(--font-mono);color:#BD6548;">{pava:+.3f}</b> / ball'
                    f'</div>'
                    f'</div>'
                )
                with cols[c_idx]:
                    st.markdown(card_html, unsafe_allow_html=True)
                    if st.button(f"Inspect Profile →", key=f"dir_btn_{pid}_{disc}_{rank}_{row_idx}_{c_idx}", use_container_width=True):
                        jump_to_player(pname, disc)
    else:
        # Compact Table View
        table_cols = ["rank", "player_name", "discipline", "role", "team", "reliability_score", "score_ci_95", "hp_balls", "shrunk_pava"]
        tbl_show = filtered[table_cols].rename(
            columns={
                "rank": "Model A Rank",
                "player_name": "Athlete",
                "discipline": "Discipline",
                "role": "Role / Style",
                "team": "Squad",
                "reliability_score": "Score",
                "score_ci_95": "95% CI",
                "hp_balls": "HP Balls",
                "shrunk_pava": "Shrunk HP PAVA",
            }
        )
        st.dataframe(tbl_show, width="stretch", hide_index=True)
        sel_t_player = st.selectbox("Quick Jump to Athlete Profile", filtered["player_name"].unique().tolist(), key="dir_tbl_jump")
        p_sub = filtered[filtered["player_name"] == sel_t_player].iloc[0]
        if st.button(f"Open {sel_t_player} Dossier →", key="dir_tbl_jump_btn"):
            jump_to_player(sel_t_player, str(p_sub["discipline"]))
