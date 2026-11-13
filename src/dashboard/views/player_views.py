"""Milestone 4 views: Page 3 (Player Intelligence) and Page 4 (Player Comparison)."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.dashboard.analytics import (
    _safe_float,
    build_multi_player_comparison,
    compute_player_five_pillars,
    compute_player_phase_summary,
    prepare_leaderboard_table,
)
from src.dashboard.charts import (
    RR_BLUE,
    RR_PINK,
    _apply_base_layout,
    build_player_color_map,
    fig_five_pillar_radar,
    fig_multi_player_ci_bars,
    fig_multi_player_prc_overlay,
    fig_multi_player_radar,
    fig_phase_performance,
    fig_player_expected_vs_observed,
    fig_pressure_response_curve,
)
from src.dashboard.components import (
    render_callout,
    render_chart_caption,
    render_empty_state,
    render_kpi_grid,
    render_section_header,
)
from src.dashboard.data_loader import (
    DELIVERIES_PAVA_PATH,
    INN_PAVA_PATH,
    MATCHES_PATH,
    SPELL_PAVA_PATH,
    DashboardDataBundle,
    query_player_deliveries,
    query_player_match_contributions,
)
from src.dashboard.design_tokens import PALETTE


@st.cache_data(ttl=1800, show_spinner=False)
def _cached_player_delivs(player_id: int, is_batting: bool) -> pd.DataFrame:
    return query_player_deliveries(player_id=player_id, is_batting=is_batting, pava_path=DELIVERIES_PAVA_PATH)


@st.cache_data(ttl=1800, show_spinner=False)
def _cached_player_matches(player_id: int, is_batting: bool) -> pd.DataFrame:
    return query_player_match_contributions(
        player_id=player_id,
        is_batting=is_batting,
        inn_path=INN_PAVA_PATH,
        spell_path=SPELL_PAVA_PATH,
        matches_path=MATCHES_PATH,
    )


def _compute_peer_means(df: pd.DataFrame, role_col: str, role_val: str) -> dict[str, float]:
    peer_df = df[df[role_col] == role_val] if role_col in df.columns else df
    if peer_df.empty:
        peer_df = df
    means: dict[str, float] = {}
    for _, row in peer_df.iterrows():
        for k, v in compute_player_five_pillars(row).items():
            means[k] = means.get(k, 0.0) + v
    if len(peer_df) > 0:
        means = {k: v / len(peer_df) for k, v in means.items()}
    return means


def render_player_intelligence(bundle: DashboardDataBundle) -> None:
    """Page 3: Comprehensive single-player intelligence & match evidence view."""
    st.title("Player Intelligence")

    preselect_disc = st.session_state.get("jump_disc", "Batting")
    c_disc, c_player = st.columns([0.9, 2.1])
    disc = c_disc.radio(
        "Discipline",
        ["Batting", "Bowling"],
        index=0 if preselect_disc == "Batting" else 1,
        horizontal=True,
        key="pi_disc",
    )
    is_batting = disc == "Batting"
    base_df = prepare_leaderboard_table(bundle.bat_df if is_batting else bundle.bowl_df, is_batting=is_batting)

    if base_df.empty:
        render_empty_state(f"No {disc.lower()} cohort loaded", "Check frozen Model A ranking CSV availability.")
        return

    names = base_df["player_name"].tolist()
    default_idx = 0
    jump_player = st.session_state.get("jump_player_name")
    if jump_player and jump_player in names:
        default_idx = names.index(jump_player)

    sel_player = c_player.selectbox(
        f"Inspect Qualified {disc[:-3]}er",
        names,
        index=default_idx,
        key=f"pi_sel_{disc}",
    )
    row = base_df[base_df["player_name"] == sel_player].iloc[0]
    pid = int(row["player_id"])
    role_col = "role" if is_batting else "bowling_type"
    role_val = str(row.get(role_col, disc))

    # Look up audited market status if tracked
    mkt_status = "Pending Verification (Pre-Nov 17)"
    mkt_team = str(row.get("dataset_ipl_team", "International / Non-IPL"))
    if not bundle.market_current.empty and pid in bundle.market_current["player_id"].values:
        m_row = bundle.market_current[bundle.market_current["player_id"] == pid].iloc[0]
        raw_status = m_row.get("official_retention_status")
        if pd.notna(raw_status) and str(raw_status).strip() != "":
            mkt_status = str(raw_status).strip()
        raw_curr_team = m_row.get("current_verified_franchise")
        if pd.notna(raw_curr_team) and str(raw_curr_team).strip() != "":
            mkt_team = str(raw_curr_team).strip()

    render_kpi_grid(
        [
            {
                "label": f"Frozen Model A Rank ({disc})",
                "value": f"#{int(row['rank'])} of {len(base_df)}",
                "sub": f"Player ID {pid} | {role_val} | Cohort Team: {mkt_team}",
                "accent": PALETTE["accent_terracotta"],
                "icon": "trophy",
            },
            {
                "label": "Reliability Score & 95% CI",
                "value": f"{row['reliability_score']:.2f}",
                "sub": f"95% Boot CI: {row.get('score_ci_95', 'N/A')} | Top-10 Prob: {_safe_float(row.get('top10_inclusion_prob'))*100:.2f}%",
                "accent": PALETTE["accent_gold"],
                "icon": "activity",
            },
            {
                "label": "High-Pressure Sample & Kish ESS",
                "value": f"{int(row['hp_balls'])} HP | {_safe_float(row.get('kish_match_ess')):.1f} ESS",
                "sub": f"{int(row['matches'])} matches | EB Weight w={_safe_float(row.get('eb_shrinkage_weight')):.3f} (K=45)",
                "accent": PALETTE["positive"],
                "icon": "database",
            },
            {
                "label": "Shrunk HP PAVA & PRC Class",
                "value": f"{_safe_float(row.get('shrunk_hp_pava_per_ball')):+.3f} / ball",
                "sub": f"PRC: {row.get('prc_archetype', 'N/A')} (slope {_safe_float(row.get('prc_slope')):+.3f}) | Market: {mkt_status}",
                "accent": PALETTE["accent_burnt_orange"],
                "icon": "user",
            },
        ]
    )

    # Career metrics strip
    if is_batting:
        perf_txt = (
            f"<b>Career Dataset Aggregates:</b> Matches: <b>{int(row['matches'])}</b> | Valid Balls: <b>{int(row['total_balls'])}</b> | "
            f"Runs: <b>{int(row['total_runs'])}</b> | Career SR: <b>{row['career_sr']:.1f}</b> | "
            f"Raw HP PAVA: <b>{row['raw_hp_pava_per_ball']:+.3f}</b> | Retention Delta: <b>{row['retention_delta']:+.3f}</b>"
        )
    else:
        perf_txt = (
            f"<b>Career Dataset Aggregates:</b> Matches: <b>{int(row['matches'])}</b> | Legal / Total Deliveries: <b>{int(row['legal_balls'])} / {int(row.get('total_deliveries', row['legal_balls']))}</b> | "
            f"Wickets: <b>{int(row['total_wickets'])}</b> | Career Econ: <b>{row['career_economy']:.2f}</b> | "
            f"Raw HP PAVA: <b>{row['raw_hp_pava_per_ball']:+.3f}</b> | Retention Delta: <b>{row['retention_delta']:+.3f}</b>"
        )
    render_callout(perf_txt, accent=PALETTE["accent_terracotta"])

    player_delivs = _cached_player_delivs(pid, is_batting=is_batting)
    player_matches = _cached_player_matches(pid, is_batting=is_batting)
    phase_df = compute_player_phase_summary(player_delivs, is_batting=is_batting)

    peer_means = _compute_peer_means(base_df, role_col, role_val)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_five_pillar_radar(row, peer_means, sel_player, role_val), width="stretch")
        render_chart_caption(f"Five-pillar composure profile for {sel_player} benchmarked against {role_val} positional peers across 2022–2026.")
    with c2:
        if not player_delivs.empty:
            st.plotly_chart(fig_pressure_response_curve(player_delivs, sel_player, is_batting=is_batting), width="stretch")
            render_chart_caption("Mean delivery PAVA across leverage tiers. Positive surplus in High [65–85) and Extreme (>=85) bands indicates clutch amplification.")
        else:
            render_empty_state("Delivery-level trace unavailable", "Parquet telemetry not loaded for this environment.")

    c3, c4 = st.columns(2)
    with c3:
        if not phase_df.empty:
            st.plotly_chart(fig_phase_performance(phase_df, sel_player, is_batting=is_batting), width="stretch")
            render_chart_caption("Empirical PAVA/ball partitioned across Powerplay (overs 1–6), Middle (7–15), and Death (16–20) phases.")
        else:
            render_empty_state("Phase breakdown unavailable", "No phase deliveries found.")
    with c4:
        if not player_delivs.empty:
            st.plotly_chart(fig_player_expected_vs_observed(player_delivs, sel_player, is_batting=is_batting), width="stretch")
            render_chart_caption("LightGBM state-conditioned expected scoring benchmark compared directly against actual player outcome rates.")

    # Pressure Index Distribution for the selected player
    if not player_delivs.empty:
        ball_col = "is_batter_ball" if is_batting else "is_legal_ball"
        p_col = "bpi" if is_batting else "bopi"
        sub_p = player_delivs[player_delivs[ball_col] == 1].dropna(subset=[p_col]).copy()
        if not sub_p.empty:
            fig_pdist = px.histogram(
                sub_p,
                x=p_col,
                nbins=20,
                color_discrete_sequence=[RR_BLUE if is_batting else RR_PINK],
                labels={p_col: f"{'BPI' if is_batting else 'BoPI'} Exposure Distribution [0–100]"},
            )
            fig_pdist = _apply_base_layout(fig_pdist, f"{'BPI' if is_batting else 'BoPI'} Delivery Exposure Histogram — {sel_player}", height=340)
            fig_pdist.add_vline(x=50.0, line_dash="dash", line_color=PALETTE["warning"], annotation_text="Operational HP Threshold (50.0)")
            st.plotly_chart(fig_pdist, width="stretch")
            render_chart_caption(f"Continuous delivery-level leverage distribution for {sel_player}. Dotted marker at 50.0 defines the high-pressure opportunity boundary.")

    if not phase_df.empty:
        render_section_header("Phase-Wise Summary & Sample Strengths / Limitations", "Exact empirical counts across Powerplay, Middle, and Death overs", icon="activity")
        st.dataframe(phase_df, width="stretch", hide_index=True)

    # Strengths & limitations panel
    ci_width = _safe_float(row.get("ci_upper_95")) - _safe_float(row.get("ci_lower_95"))
    hp_n = int(row["hp_balls"])
    lim_notes = []
    if hp_n < 70:
        lim_notes.append(f"Moderate high-pressure exposure ({hp_n} HP balls) increases bootstrap CI width ({ci_width:.1f} pts) due to match-cluster sensitivity.")
    if int(row["matches"]) < 30:
        lim_notes.append(f"Low match count ({int(row['matches'])} matches) yields wider bootstrap rank interval {row.get('rank_ci_95', '')}.")
    if not lim_notes:
        lim_notes.append(f"Deep multi-match volume ({int(row['matches'])} matches, {hp_n} HP balls, Kish ESS {_safe_float(row.get('kish_match_ess')):.1f}) supports narrow bootstrap uncertainty.")
    lim_notes.append("PRC label describes the empirical OLS slope of delivery PAVA against pressure index — NOT a psychological trait.")

    render_callout(
        f"<b>Analytical Strengths &amp; Limitations — {sel_player}:</b><br/>"
        f"• <b>Strength:</b> Shrunk HP PAVA of <b>{_safe_float(row.get('shrunk_hp_pava_per_ball')):+.3f}</b> runs/ball and retention delta "
        f"<b>{_safe_float(row.get('retention_delta')):+.3f}</b> vs low-pressure baseline.<br/>"
        + "<br/>".join(f"• <b>Limitation / Governance Note:</b> {note}" for note in lim_notes),
        accent=PALETTE["accent_terracotta"],
    )

    render_section_header("Match-Level PAVA Contributions", "Sorted chronologically from most recent match (DuckDB predicate query)", icon="database")
    if not player_matches.empty:
        st.dataframe(player_matches.head(60), width="stretch", hide_index=True)
    else:
        render_empty_state("No match-level table entries", "Innings/spell PAVA parquet files were not present for this player.")


def render_player_comparison(bundle: DashboardDataBundle) -> None:
    """Page 4: Comparable multi-player head-to-head telemetry comparator."""
    st.title("Player Comparison")
    render_callout(
        "<b>Methodological Integrity Rule:</b> Comparisons are strictly constrained within the <b>same discipline</b> (Batters vs Batters OR Bowlers vs Bowlers) "
        "using matched scales, so incompatible batting vs bowling rates are never artificially forced onto one axis.",
        accent=PALETTE["accent_terracotta"],
    )

    c_d, c_sel = st.columns([0.85, 2.15])
    disc = c_d.radio("Compare Within Discipline", ["Batters", "Bowlers"], horizontal=True, key="cmp_disc")
    is_batting = disc == "Batters"
    df = prepare_leaderboard_table(bundle.bat_df if is_batting else bundle.bowl_df, is_batting=is_batting)

    if df.empty or len(df) < 2:
        render_empty_state("Insufficient cohort records", "At least 2 qualified players are required for comparison.")
        return

    all_names = df["player_name"].tolist()
    default_picks = all_names[:3] if len(all_names) >= 3 else all_names[:2]
    if is_batting and "Ruturaj Gaikwad" in all_names and "Suryakumar Yadav" in all_names and "Jos Buttler" in all_names:
        default_picks = ["Ruturaj Gaikwad", "Suryakumar Yadav", "Jos Buttler"]
    elif (not is_batting) and "Liam Dawson" in all_names and "Haris Rauf" in all_names and "Nathan Ellis" in all_names:
        default_picks = ["Liam Dawson", "Haris Rauf", "Nathan Ellis"]

    selected_names = c_sel.multiselect(
        f"Select 2 to 4 {disc} to Compare",
        all_names,
        default=default_picks,
        max_selections=4,
        key=f"cmp_picks_{disc}",
    )

    if len(selected_names) < 2:
        render_empty_state("Select at least 2 players", "Choose between 2 and 4 players from the selector above to render side-by-side charts.")
        return

    sel_df = df[df["player_name"].isin(selected_names)].copy()
    sel_df["_order"] = sel_df["player_name"].apply(lambda n: selected_names.index(n))
    sel_df = sel_df.sort_values("_order").drop(columns=["_order"])

    render_section_header("Side-by-Side Comparable Telemetry Matrix", "Exact frozen metrics, uncertainty intervals, Kish ESS, and OLS PRC slope", icon="compare")
    comp_tbl = build_multi_player_comparison(sel_df, is_batting=is_batting)
    st.dataframe(comp_tbl, width="stretch", hide_index=True)

    color_map = build_player_color_map(sel_df["player_name"].tolist())

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_multi_player_radar(sel_df, color_map=color_map), width="stretch")
        render_chart_caption("Comparative five-pillar radar illustrating relative balance across execution surplus, retention stability, consistency, and adaptability.")
    with c2:
        st.plotly_chart(fig_multi_player_ci_bars(sel_df, color_map=color_map), width="stretch")
        render_chart_caption("Reliability Scores with 95% bootstrap confidence intervals. Overlapping error intervals indicate indistinguishable statistical difference.")

    # Fetch delivery telemetry for overlaid PRC + phase comparisons
    deliv_map = {}
    phase_rows = []
    for _, r in sel_df.iterrows():
        pname = str(r["player_name"])
        pid = int(r["player_id"])
        p_delivs = _cached_player_delivs(pid, is_batting=is_batting)
        deliv_map[pname] = p_delivs
        ph_df = compute_player_phase_summary(p_delivs, is_batting=is_batting)
        if not ph_df.empty:
            ph_df.insert(0, "Player", pname)
            phase_rows.append(ph_df)

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(fig_multi_player_prc_overlay(deliv_map, is_batting=is_batting, color_map=color_map), width="stretch")
        render_chart_caption("Trajectory slopes across rising leverage bands. Rising profiles isolate candidates who elevate performance when stakes escalate.")
    with c4:
        if phase_rows:
            comb_phase = pd.concat(phase_rows, ignore_index=True)
            fig_ph = px.bar(
                comb_phase,
                x="Phase",
                y="Raw PAVA / Ball",
                color="Player",
                color_discrete_map=color_map,
                barmode="group",
                text="Balls",
                labels={"Raw PAVA / Ball": "Mean Raw PAVA (Runs/Ball)"},
            )
            fig_ph = _apply_base_layout(fig_ph, "Phase-Wise Mean Raw PAVA Comparison (Labels = Balls)", height=390)
            fig_ph.add_hline(y=0.0, line_dash="dot", line_color="rgba(148,163,184,0.4)")
            st.plotly_chart(fig_ph, width="stretch")
            render_chart_caption("Phase-wise value added across Powerplay, Middle, and Death overs (bar numbers indicate total balls faced/bowled).")

    render_section_header("Statistical Strengths, Sample Trade-offs & Limitations", "Interpreting score margins alongside sample volume", icon="book")
    for _, r in sel_df.iterrows():
        ci_w = _safe_float(r.get("ci_upper_95")) - _safe_float(r.get("ci_lower_95"))
        render_callout(
            f"<b>{r['player_name']} (#{int(r['rank'])})</b> — Score <b>{r['reliability_score']:.2f}</b> | "
            f"95% CI width: <b>{ci_w:.1f} pts</b> | Top-10 Prob: <b>{_safe_float(r.get('top10_inclusion_prob'))*100:.1f}%</b> | "
            f"Exposure: <b>{int(r['hp_balls'])} HP balls</b> (Kish ESS <b>{_safe_float(r.get('kish_match_ess')):.1f}</b> across {int(r['matches'])} matches) | "
            f"Shrunk PAVA <b>{_safe_float(r.get('shrunk_hp_pava_per_ball')):+.3f}</b>, PRC class <i>{r.get('prc_archetype')}</i>.",
            accent=PALETTE["accent_terracotta"] if ci_w <= 35 else PALETTE["accent_gold"],
        )

