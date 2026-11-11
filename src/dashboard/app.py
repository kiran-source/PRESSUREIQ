"""PRESSUREIQ — Cricket Pressure Intelligence (Jury-Ready Streamlit Dashboard)."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.dashboard.analytics import (
    STRICT_MARKET_STATUSES,
    _safe_float,
    build_ablation_rows,
    build_benchmark_rows,
    compute_peer_comparison,
    compute_player_five_pillars,
    compute_player_phase_summary,
    enrich_emerging_watchlist,
    extract_unique_teams,
    filter_leaderboard,
    prepare_leaderboard_table,
    prepare_market_display,
    summarize_market_counts,
    summarize_rr_squad_intelligence,
)
from src.dashboard.charts import (
    RR_BLUE,
    RR_PINK,
    fig_batter_vs_bowler_comparison,
    fig_five_pillar_radar,
    fig_phase_performance,
    fig_pressure_response_curve,
    fig_rank_uncertainty_intervals,
    fig_rr_role_depth,
    fig_sample_vs_score,
    fig_score_distribution,
    fig_top10_ci_bar,
)
from src.dashboard.data_loader import (
    DELIVERIES_PAVA_PATH,
    INN_PAVA_PATH,
    MATCHES_PATH,
    SPELL_PAVA_PATH,
    DashboardDataBundle,
    load_dashboard_bundle_uncached,
    query_player_deliveries,
    query_player_match_contributions,
    query_season_format_stats,
    query_unestablished_profiles,
)

st.set_page_config(
    page_title="PRESSUREIQ — Cricket Pressure Intelligence",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .main .block-container { padding-top: 1.4rem; padding-bottom: 2rem; max-width: 1420px; }
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #004BA0;
        border-radius: 8px;
        padding: 14px 16px;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    }
    .kpi-label { font-size: 0.78rem; color: #475569; text-transform: uppercase; letter-spacing: 0.04em; font-weight: 600; }
    .kpi-value { font-size: 1.55rem; color: #0F172A; font-weight: 700; margin-top: 2px; }
    .kpi-sub { font-size: 0.78rem; color: #64748B; margin-top: 2px; }
    .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 999px;
        font-size: 0.74rem;
        font-weight: 600;
        margin-right: 4px;
    }
    .badge-trade { background: #DBEAFE; color: #1E40AF; border: 1px solid #93C5FD; }
    .badge-pending { background: #FEF3C7; color: #92400E; border: 1px solid #FCD34D; }
    .badge-policy { background: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5; }
    .badge-retained { background: #D1FAE5; color: #065F46; border: 1px solid #6EE7B7; }
    .badge-released { background: #E0E7FF; color: #3730A3; border: 1px solid #A5B4FC; }
    .badge-rumour { background: #F1F5F9; color: #334155; border: 1px solid #CBD5E1; }
    .banner-frozen {
        background: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-left: 4px solid #EA1B88;
        padding: 10px 14px;
        border-radius: 6px;
        font-size: 0.88rem;
        color: #1E293B;
        margin-bottom: 1rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

PAGES = [
    "1. Executive Overview",
    "2. Top 10 Pressure-Resilient Batters",
    "3. Top 10 Pressure-Resilient Bowlers",
    "4. Player Intelligence",
    "5. Pressure Analytics",
    "6. Emerging Talent",
    "7. Rajasthan Royals Squad Intelligence",
    "8. Auction & Market Intelligence",
    "9. Methodology & Validation",
    "10. Data Sources & Audit Trail",
]


@st.cache_data(ttl=3600, show_spinner=False)
def _cached_bundle() -> DashboardDataBundle:
    return load_dashboard_bundle_uncached()


@st.cache_data(ttl=1800, show_spinner=False)
def _cached_slice_stats(is_batting: bool, season: int | None, comp_category: str | None) -> pd.DataFrame:
    return query_season_format_stats(
        is_batting=is_batting,
        season=season,
        comp_category=comp_category,
        pava_path=DELIVERIES_PAVA_PATH,
        matches_path=MATCHES_PATH,
    )


@st.cache_data(ttl=1800, show_spinner=False)
def _cached_unestablished(is_batting: bool) -> pd.DataFrame:
    return query_unestablished_profiles(is_batting=is_batting, pava_path=DELIVERIES_PAVA_PATH)


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


def _fmt_int(val, fallback: str = "N/A") -> str:
    if val is None or pd.isna(val):
        return fallback
    return str(int(round(float(val))))


def _render_kpi_card(col, label: str, value: str, sub: str) -> None:
    col.markdown(
        f'<div class="kpi-card"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>',
        unsafe_allow_html=True,
    )


def _render_leaderboard_view(bundle: DashboardDataBundle, is_batting: bool) -> None:
    disc_name = "Batters" if is_batting else "Bowlers"
    raw_df = bundle.bat_df if is_batting else bundle.bowl_df
    accent = RR_BLUE if is_batting else RR_PINK
    role_col = "role" if is_batting else "bowling_type"

    st.title(f"{'2. Top 10 Pressure-Resilient Batters' if is_batting else '3. Top 10 Pressure-Resilient Bowlers'}")
    st.markdown(
        f'<div class="banner-frozen"><b>Official Model A Baseline (Frozen):</b> Evaluated across <b>{len(raw_df)}</b> qualified {disc_name.lower()} '
        f'(>=400 balls, >=30 high-pressure balls at P >= 50.0, >=20 matches; 2022–2026). '
        f'<b>Metric Note:</b> Composite Reliability Score (0–100) is a norm-referenced standardized percentile index, NOT a probability of match success.</div>',
        unsafe_allow_html=True,
    )

    if raw_df.empty or "rank" not in raw_df.columns:
        st.error(f"Official {disc_name.lower()} ranking CSV is unavailable or missing expected schema.")
        return

    table_df = prepare_leaderboard_table(raw_df, is_batting=is_batting)

    f1, f2, f3, f4, f5 = st.columns([1.2, 1.1, 1.1, 1.1, 1.2])
    roles_avail = sorted(table_df[role_col].dropna().unique().tolist()) if role_col in table_df.columns else []
    sel_roles = f1.multiselect("Role / Type Filter", roles_avail, default=roles_avail, key=f"role_{disc_name}")

    season_opts = ["All (2022–2026 Official Baseline)", "2022", "2023", "2024", "2025", "2026"]
    sel_season = f2.selectbox("Season Slice (Empirical)", season_opts, key=f"season_{disc_name}")

    format_opts = ["All Formats", "IPL", "T20I", "Other_T20"]
    sel_format = f3.selectbox("Format Slice", format_opts, key=f"format_{disc_name}")

    all_teams = extract_unique_teams(table_df)
    sel_team = f4.selectbox("Mapped Team", ["All Teams"] + all_teams, key=f"team_{disc_name}")

    raw_max_hp = int(pd.to_numeric(table_df["hp_balls"], errors="coerce").max() or 30)
    slider_max = max(40, min(400, raw_max_hp))
    min_hp = f5.slider("Min HP Opportunities (P>=50)", min_value=30, max_value=slider_max, value=30, step=10, key=f"hp_{disc_name}")

    search_q = st.text_input("Search Player Name", placeholder="Filter by player name...", key=f"q_{disc_name}")

    filtered = filter_leaderboard(
        table_df,
        roles=sel_roles,
        role_col=role_col,
        team_filter=sel_team,
        min_hp_balls=min_hp,
        search_query=search_q,
    )

    is_sliced = sel_season != "All (2022–2026 Official Baseline)" or sel_format != "All Formats"
    if is_sliced:
        yr_arg = int(sel_season) if sel_season != "All (2022–2026 Official Baseline)" else None
        fmt_arg = None if sel_format == "All Formats" else sel_format
        slice_df = _cached_slice_stats(is_batting=is_batting, season=yr_arg, comp_category=fmt_arg)
        if slice_df.empty:
            st.warning(
                f"No empirical delivery data matched slice **{sel_season} | {sel_format}** (or delivery parquet is unavailable). "
                "Adjust Season or Format filters above."
            )
            return
        filtered = filtered.merge(slice_df, on="player_id", how="inner")
        filtered = filtered[filtered["slice_balls"] > 0]
        st.info(
            f"Showing **{len(filtered)}** Model A qualified {disc_name.lower()} active in slice "
            f"**{sel_season} | {sel_format}**. Official Model A Career Rank (`rank`) and Reliability Score remain frozen; slice columns display unshrunk empirical slice counts and Raw HP PAVA."
        )

    if filtered.empty:
        st.warning("No qualified players match the selected filter combination. Relax a filter above to restore results.")
        return

    c_chart1, c_chart2 = st.columns(2)
    with c_chart1:
        st.plotly_chart(
            fig_top10_ci_bar(filtered, f"Filtered Top 10 {disc_name} — Score & 95% Bootstrap CI", accent),
            width="stretch",
        )
    with c_chart2:
        st.plotly_chart(
            fig_rank_uncertainty_intervals(
                filtered,
                top_n=min(12, len(filtered)),
                title=f"Top {min(12, len(filtered))} Rank Uncertainty (Model A vs 2,000-Bootstrap)",
            ),
            width="stretch",
        )

    st.subheader(f"Detailed Leaderboard Table ({len(filtered)} {'Player' if len(filtered) == 1 else 'Players'})")
    st.caption(
        "Sample-Size Distinction: `HP Opportunities` = raw deliveries faced/bowled at BPI/BoPI >= 50.0. "
        "`Kish Match ESS` = effective independent match clusters; `EB Effective HP Balls` = n_hp * (n_hp / (n_hp + 45))."
    )

    base_cols = [
        "rank",
        "player_name",
        role_col,
        "reliability_score",
        "primary_rate_label",
        "matches",
        "total_sample_balls",
        "hp_balls",
        "kish_match_ess",
        "eb_effective_hp_balls",
        "score_ci_95",
        "top10_prob_pct",
        "boot_median_rank_int",
        "rank_ci_95",
        "prc_archetype",
    ]
    if is_sliced:
        base_cols.extend(["slice_matches", "slice_balls", "slice_hp_balls", "slice_rate_stat", "slice_hp_raw_pava"])

    cols_present = [c for c in base_cols if c in filtered.columns]
    rename_map = {
        "rank": "Official Rank",
        "player_name": "Player",
        role_col: "Role" if is_batting else "Bowling Style",
        "reliability_score": "Pressure Score",
        "primary_rate_label": "Career SR" if is_batting else "Career Econ",
        "matches": "Matches",
        "total_sample_balls": "Total Balls" if is_batting else "Legal Balls",
        "hp_balls": "HP Opportunities",
        "kish_match_ess": "Kish Match ESS",
        "eb_effective_hp_balls": "EB Effective HP Balls",
        "score_ci_95": "95% Score CI",
        "top10_prob_pct": "Top-10 Prob (%)",
        "boot_median_rank_int": "Median Boot Rank",
        "rank_ci_95": "95% Rank Interval",
        "prc_archetype": "PRC Archetype",
        "slice_matches": "Slice Matches",
        "slice_balls": "Slice Balls",
        "slice_hp_balls": "Slice HP Balls",
        "slice_rate_stat": "Slice SR" if is_batting else "Slice Econ",
        "slice_hp_raw_pava": "Slice HP Raw PAVA",
    }
    st.dataframe(filtered[cols_present].rename(columns=rename_map), width="stretch", hide_index=True)


def render_executive_overview(bundle: DashboardDataBundle) -> None:
    st.title("PRESSUREIQ — Cricket Pressure Intelligence")
    prov_raw = bundle.provenance.get("row_count_reconciliation", {})
    prov_q = bundle.provenance.get("quality_checks", {})
    raw_balls = prov_raw.get("raw_ball_by_ball_deliveries", 200999)
    reg_balls = prov_raw.get("features_and_pava_deliveries", 200961)
    so_balls = prov_raw.get("delta_deliveries", 38)
    played_m = prov_q.get("matches_with_ball_data", 867)

    st.markdown(
        f'<div class="banner-frozen"><b>Official Model A Competition Baseline (Frozen):</b> {raw_balls:,} raw deliveries '
        f'({reg_balls:,} regular overs + {so_balls} Super Over balls) across {played_m} played matches (2022–2026) | '
        f'<b>Market Snapshot Anchor:</b> 11 November 2026 (Ahead of 17 Nov IPL 2027 Retention Deadline)</div>',
        unsafe_allow_html=True,
    )

    if bundle.bat_df.empty or bundle.bowl_df.empty:
        st.warning("Official ranking datasets (`final_batter_rankings.csv` / `final_bowler_rankings.csv`) are unavailable.")
        return

    bat_df = bundle.bat_df.sort_values("rank")
    bowl_df = bundle.bowl_df.sort_values("rank")

    top_bat = bat_df.iloc[0]
    top_bowl = bowl_df.iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    _render_kpi_card(
        c1,
        "Model A #1 Batter",
        f"{top_bat['player_name']}",
        f"Score: {_safe_float(top_bat['reliability_score']):.2f} | CI [{_safe_float(top_bat['ci_lower_95']):.1f}, {_safe_float(top_bat['ci_upper_95']):.1f}] | {_fmt_int(top_bat['hp_balls'])} HP balls",
    )
    _render_kpi_card(
        c2,
        "Model A #1 Bowler",
        f"{top_bowl['player_name']}",
        f"Score: {_safe_float(top_bowl['reliability_score']):.2f} | CI [{_safe_float(top_bowl['ci_lower_95']):.1f}, {_safe_float(top_bowl['ci_upper_95']):.1f}] | {_fmt_int(top_bowl['hp_balls'])} HP balls",
    )
    _render_kpi_card(
        c3,
        "Evaluated Cohorts (Model A)",
        f"{len(bat_df)} Batters | {len(bowl_df)} Bowlers",
        f"Filtered from {prov_q.get('unique_batters', 888)} batters & {prov_q.get('unique_bowlers', 647)} bowlers (>=400 balls, >=30 HP, >=20 matches)",
    )
    _render_kpi_card(
        c4,
        "Data & Bootstrap Coverage",
        f"{reg_balls:,} Balls | {played_m} Matches",
        "2022–2026 (IPL + T20I + Other T20) | N=2,000 Match-Clustered Bootstraps",
    )

    st.markdown("---")
    left_p, right_p = st.columns(2)
    with left_p:
        st.subheader("Official Model A Top 10 Batters")
        bat_view = prepare_leaderboard_table(bat_df, True).head(10)
        st.dataframe(
            bat_view[["rank", "player_name", "role", "reliability_score", "hp_balls", "top10_prob_pct", "score_ci_95"]].rename(
                columns={
                    "rank": "Rank",
                    "player_name": "Batter",
                    "role": "Role",
                    "reliability_score": "Score",
                    "hp_balls": "HP Balls",
                    "top10_prob_pct": "Top-10 Prob (%)",
                    "score_ci_95": "95% CI",
                }
            ),
            width="stretch",
            hide_index=True,
        )
    with right_p:
        st.subheader("Official Model A Top 10 Bowlers")
        bowl_view = prepare_leaderboard_table(bowl_df, False).head(10)
        st.dataframe(
            bowl_view[["rank", "player_name", "pace_or_spin", "reliability_score", "hp_balls", "top10_prob_pct", "score_ci_95"]].rename(
                columns={
                    "rank": "Rank",
                    "player_name": "Bowler",
                    "pace_or_spin": "Type",
                    "reliability_score": "Score",
                    "hp_balls": "HP Balls",
                    "top10_prob_pct": "Top-10 Prob (%)",
                    "score_ci_95": "95% CI",
                }
            ),
            width="stretch",
            hide_index=True,
        )

    st.warning(
        "**Bootstrap Uncertainty & Sample-Size Disclosure:** High-pressure cricket encounters suffer heavy match-to-match variance. "
        "Notice top-10 inclusion probabilities under 2,000 match-clustered resamples: #1 batter Ruturaj Gaikwad (45 HP balls) carries a **60.9%** top-10 inclusion probability "
        "and rank CI `[#1, #107]`; #1 bowler Liam Dawson (83 HP balls) carries **41.9%** and rank CI `[#1, #152]`. "
        "Players with smaller HP samples have wider intervals and are regularized toward league average via Empirical Bayes shrinkage (`K = 45`)."
    )

    m1, m2 = st.columns([3, 2])
    with m1:
        st.subheader("Ranking Methodology Summary (Model A)")
        st.markdown(
            """
            1. **Continuous Pressure Indices (BPI / BoPI, 0–100):** Quantify delivery-level chase urgency, resource scarcity, innings climax, and match leverage prior to each ball.
            2. **Chronological Expected Outcomes (LightGBM):** Out-of-fold / walk-forward models predict expected runs, boundary probability, and dismissal probability for every state vector.
            3. **Pressure-Adjusted Value Added (PAVA):** Computes runs and phase-weighted wicket surplus above expectation, preserving both unamplified raw PAVA (`raw_bat_value`, `raw_bowl_value`) and leverage-weighted PAVA.
            4. **Five-Pillar Empirical Bayes Reliability:** Synthesizes shrunk high-pressure PAVA (`P >= 50.0`), baseline retention delta, match-level consistency, context adaptability, and evidence weight into a standardized 0–100 composite score (not a probability of success).
            """
        )
    with m2:
        st.subheader("Verification & Market Snapshot Status")
        bat_ok = "VERIFIED BYTE-IDENTICAL" if bundle.integrity_status.get("batter_frozen_match") else "HASH MISMATCH"
        bowl_ok = "VERIFIED BYTE-IDENTICAL" if bundle.integrity_status.get("bowler_frozen_match") else "HASH MISMATCH"
        mkt_counts = summarize_market_counts(bundle.market_snapshot_nov11)
        st.info(
            f"- **Batter CSV Parity:** `{bat_ok}`\n"
            f"- **Bowler CSV Parity:** `{bowl_ok}`\n"
            f"- **Market Snapshot Date:** `2026-11-11` (`{mkt_counts['Confirmed Trade']}` Confirmed Trade, `{mkt_counts['Pending Verification']}` Pending Verification, `{mkt_counts['Policy/Eligibility Review']}` Policy Review, `{mkt_counts['Confirmed Released']}` Confirmed Releases)\n"
            "- **Separation Mandate:** Statistical Model A rankings never depend on IPL contract rumours or availability."
        )


def render_player_intelligence(bundle: DashboardDataBundle) -> None:
    st.title("4. Player Intelligence")
    st.markdown(
        "Deep-dive delivery profile for any qualified Model A player. "
        "**Note:** The 0–100 composite Reliability Score is a norm-referenced percentile score, **never** a probability of success."
    )

    c_sel1, c_sel2 = st.columns([1, 2])
    disc = c_sel1.radio("Discipline", ["Batters", "Bowlers"], horizontal=True, key="pi_disc")
    is_bat = disc == "Batters"
    pool = prepare_leaderboard_table(bundle.bat_df if is_bat else bundle.bowl_df, is_batting=is_bat)
    role_col = "role" if is_bat else "bowling_type"

    if pool.empty:
        st.error("Player pool data missing.")
        return

    player_name = c_sel2.selectbox("Select Player Profile", pool["player_name"].tolist(), key="pi_player")
    pid = int(pool[pool["player_name"] == player_name]["player_id"].iloc[0])

    row, peer_means, role_rank, role_count = compute_peer_comparison(pool, pid, role_col)
    if row.empty:
        st.warning("Selected player record could not be loaded.")
        return

    delivs = _cached_player_delivs(pid, is_bat)
    matches_contrib = _cached_player_matches(pid, is_bat)
    phase_df = compute_player_phase_summary(delivs, is_batting=is_bat)

    ess_val = row.get("kish_match_ess")
    ess_txt = f"{_safe_float(ess_val):.1f}" if pd.notna(ess_val) else "N/A"

    k1, k2, k3, k4, k5 = st.columns(5)
    _render_kpi_card(k1, "Official Model A Rank", f"#{_fmt_int(row.get('rank'))} / {len(pool)}", f"#{role_rank} of {role_count} in {row[role_col]}")
    _render_kpi_card(k2, "Composite Score", f"{_safe_float(row.get('reliability_score')):.2f}", f"95% CI {row.get('score_ci_95', 'N/A')}")
    _render_kpi_card(k3, "HP Opportunities", f"{_fmt_int(row.get('hp_balls'))} balls", f"Kish Match ESS: {ess_txt} | EB Wt: {_safe_float(row.get('eb_shrinkage_weight')):.3f}")
    _render_kpi_card(k4, "Bootstrap Rank", f"Med #{_fmt_int(row.get('boot_median_rank_int'))}", f"Rank CI {row.get('rank_ci_95', 'N/A')} | Top-10: {_safe_float(row.get('top10_prob_pct')):.1f}%")
    _render_kpi_card(k5, "PRC Archetype", f"{row.get('prc_archetype', 'N/A')}", f"Linear Slope: {_safe_float(row.get('prc_slope')):+.4f}")

    st.markdown("---")
    g1, g2 = st.columns(2)
    with g1:
        st.plotly_chart(fig_pressure_response_curve(delivs, player_name, is_batting=is_bat), width="stretch")
    with g2:
        st.plotly_chart(fig_five_pillar_radar(row, peer_means, player_name, str(row[role_col])), width="stretch")

    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.subheader("Phase-Wise Analysis")
        if not phase_df.empty:
            st.dataframe(phase_df, width="stretch", hide_index=True)
            st.plotly_chart(fig_phase_performance(phase_df, player_name, is_batting=is_bat), width="stretch")
        else:
            st.info("No delivery-level phase breakdown available.")

    with p_col2:
        st.subheader("Peer Comparison & Evidence Rationale")
        pillars = compute_player_five_pillars(row)
        comp_rows = [{"Pillar": k, player_name: pillars[k], f"{row[role_col]} Peer Mean": peer_means.get(k, 0.0)} for k in pillars]
        st.dataframe(pd.DataFrame(comp_rows), width="stretch", hide_index=True)

        st.markdown(
            f"""
            **Selection Rationale & Limitations:**
            - **Shrunk HP PAVA/ball:** `{_safe_float(row.get('shrunk_hp_pava_per_ball')):+.4f}` runs/ball (Raw unshrunk: `{_safe_float(row.get('raw_hp_pava_per_ball')):+.4f}`).
            - **Retention Delta (High vs Low Pressure):** `{_safe_float(row.get('retention_delta')):+.3f}` runs/ball.
            - **Evidence & Uncertainty:** Based on `{_fmt_int(row.get('matches'))}` matches (`{_fmt_int(row.get('total_sample_balls'))}` total balls, `{_fmt_int(row.get('hp_balls'))}` high-pressure balls, EB effective `{_safe_float(row.get('eb_effective_hp_balls')):.1f}` balls). Wide bootstrap rank interval `{row.get('rank_ci_95', 'N/A')}` indicates rank sensitivity across resampled matches.
            - **Mapped Dataset Teams:** {row.get('teams_list') or 'N/A'}
            """
        )

    st.subheader("Match-Level PAVA Contributions (Most Recent 15 Matches)")
    if not matches_contrib.empty:
        show_cols = [c for c in ["match_date", "home_team", "away_team", "stage", "comp_category", "balls_faced", "legal_balls", "runs", "runs_conceded", "wickets", "high_pressure_balls", "raw_value", "total_pava", "pava_per_ball"] if c in matches_contrib.columns]
        st.dataframe(matches_contrib[show_cols].head(15), width="stretch", hide_index=True)
    else:
        st.info("Match-level contribution log unavailable.")


def render_pressure_analytics(bundle: DashboardDataBundle) -> None:
    st.title("5. Pressure Analytics")
    st.markdown("Cohort-level interactive exploration of score distributions, sample-size shrinkage, phase pressure, and bootstrap instability.")

    t1, t2 = st.tabs([f"Batters Cohort ({len(bundle.bat_df)})", f"Bowlers Cohort ({len(bundle.bowl_df)})"])
    with t1:
        if bundle.bat_df.empty:
            st.warning("Batter dataset unavailable.")
        else:
            c1, c2 = st.columns(2)
            c1.plotly_chart(fig_score_distribution(bundle.bat_df, "Batter Reliability Score Distribution by PRC Archetype"), width="stretch")
            c2.plotly_chart(fig_sample_vs_score(bundle.bat_df, is_batting=True), width="stretch")
            st.plotly_chart(fig_rank_uncertainty_intervals(bundle.bat_df, top_n=15, title="Top 15 Batters — Frozen Rank vs 2,000-Bootstrap Median & 95% Interval"), width="stretch")

    with t2:
        if bundle.bowl_df.empty:
            st.warning("Bowler dataset unavailable.")
        else:
            c1, c2 = st.columns(2)
            c1.plotly_chart(fig_score_distribution(bundle.bowl_df, "Bowler Reliability Score Distribution by PRC Archetype"), width="stretch")
            c2.plotly_chart(fig_sample_vs_score(bundle.bowl_df, is_batting=False), width="stretch")
            st.plotly_chart(fig_rank_uncertainty_intervals(bundle.bowl_df, top_n=15, title="Top 15 Bowlers — Frozen Rank vs 2,000-Bootstrap Median & 95% Interval"), width="stretch")

    st.markdown("---")
    b1, b2 = st.columns(2)
    with b1:
        if not bundle.bat_df.empty and not bundle.bowl_df.empty:
            st.plotly_chart(fig_batter_vs_bowler_comparison(bundle.bat_df, bundle.bowl_df), width="stretch")
        else:
            st.info("Cohort comparison unavailable until both ranking tables are present.")
    with b2:
        st.subheader("League-Wide Phase Pressure & Raw PAVA Summary")
        if not bundle.phase_cohort_df.empty:
            st.dataframe(bundle.phase_cohort_df, width="stretch", hide_index=True)
        else:
            st.info("League phase summary unavailable.")
        st.info("Death overs record the highest BoPI/BPI tension, explaining why Empirical Bayes shrinkage heavily penalizes low-volume specialists.")


def render_emerging_talent(bundle: DashboardDataBundle) -> None:
    st.title("6. Emerging Talent Discovery")
    st.warning(
        "**Separation Guardrail:** Developmental potential and small-sample upside are kept **strictly separate** from proven Model A pressure reliability. "
        "Players below 400 total balls or 30 high-pressure balls fail Model A qualification and carry wide estimation uncertainty."
    )

    tab_wl, tab_emp = st.tabs(["Curated Young & Breakout Watchlist", "Empirical Below-Threshold Discovery (DuckDB)"])

    with tab_wl:
        em_df = enrich_emerging_watchlist(bundle.emerging_df, bundle.market_snapshot_nov11)
        if em_df.empty:
            st.info("Watchlist CSV not present.")
        else:
            tiers = sorted(em_df["category"].dropna().unique().tolist())
            sel_tiers = st.multiselect("Evidence Quality Tier", tiers, default=tiers, key="em_tiers")
            sub = em_df[em_df["category"].isin(sel_tiers)]
            st.dataframe(
                sub[
                    [
                        "player_name",
                        "age",
                        "nationality",
                        "category",
                        "role",
                        "franchise",
                        "total_balls_dataset",
                        "hp_balls_dataset",
                        "pressure_reliability_score",
                        "audited_market_status",
                    ]
                ].rename(
                    columns={
                        "player_name": "Player",
                        "age": "Age",
                        "nationality": "Nationality",
                        "category": "Evidence Tier",
                        "role": "Role",
                        "franchise": "Dataset / 2026 Franchise",
                        "total_balls_dataset": "Total Balls",
                        "hp_balls_dataset": "HP Balls",
                        "pressure_reliability_score": "Model A Score / Status",
                        "audited_market_status": "Audited Market Status (11 Nov)",
                    }
                ),
                width="stretch",
                hide_index=True,
            )

            if not sub.empty:
                sel_em = st.selectbox("Inspect Watchlist Profile", sub["player_name"].tolist(), key="em_pick")
                r = sub[sub["player_name"] == sel_em].iloc[0]
                st.markdown(f"**{r['player_name']}** ({r['role']}) — **Tactical Assessment:** {r['tactical_assessment']}")
                st.caption(f"Phase / Recruitment Note (Market Status = {r['audited_market_status']}): Contract availability remains unconfirmed until official Nov 17 BCCI submissions.")

    with tab_emp:
        st.markdown("Players excluded from Model A solely due to sample thresholds (`>= 30` balls, but `< 400` career balls or `< 30` HP balls or `< 20` matches):")
        d_type = st.radio("Discipline", ["Batters", "Bowlers"], horizontal=True, key="em_disc")
        unest_df = _cached_unestablished(is_batting=(d_type == "Batters"))
        if not unest_df.empty:
            st.dataframe(unest_df, width="stretch", hide_index=True)
        else:
            st.info("No below-threshold profiles returned.")


def render_rr_squad_intelligence(bundle: DashboardDataBundle) -> None:
    st.title("7. Rajasthan Royals Squad Intelligence")
    st.markdown(
        '<div class="banner-frozen"><b>Analytical Fit vs Verified Market Availability:</b> Statistical Role Fit (`rr_priority_score`) evaluates cricket value at Sawai Mansingh Stadium (Jaipur). '
        'It is strictly separated from contractual availability: as of <b>11 November 2026</b>, <b>0</b> external targets are confirmed released for open auction.</div>',
        unsafe_allow_html=True,
    )

    rr_summary = summarize_rr_squad_intelligence(bundle.eligibility_audit_df, bundle.rr_candidates_df)
    rr_core = rr_summary["rr_core"]
    role_depth = rr_summary["role_depth"]
    targets = rr_summary["targets"]

    c1, c2 = st.columns([1.15, 1])
    with c1:
        st.subheader("RR 2026 Qualified Core (Model A Baseline)")
        if not rr_core.empty:
            st.dataframe(
                rr_core[
                    [
                        "player_name",
                        "discipline",
                        "role",
                        "model_a_rank",
                        "reliability_score",
                        "hp_balls",
                        "prc_archetype",
                        "market_status_verified",
                    ]
                ].rename(
                    columns={
                        "player_name": "Player",
                        "discipline": "Discipline",
                        "role": "Role",
                        "model_a_rank": "Model A Rank",
                        "reliability_score": "Pressure Score",
                        "hp_balls": "HP Balls",
                        "prc_archetype": "PRC Archetype",
                        "market_status_verified": "2027 Market Status",
                    }
                ),
                width="stretch",
                hide_index=True,
            )
        else:
            st.info("RR squad audit CSV unavailable.")
        st.caption(
            "Note: Jos Buttler (GT), Prasidh Krishna (GT), Trent Boult (MI), and Sanju Samson (CSK trade prior to 2026) are verified with other IPL 2026 franchises and NOT listed as RR core."
        )
    with c2:
        st.plotly_chart(fig_rr_role_depth(role_depth), width="stretch")

    s1, s2 = st.columns(2)
    with s1:
        st.subheader("Pressure Strengths & Weaknesses")
        st.markdown(
            """
            - **Strengths:** Jofra Archer (#16 Model A Bowler, `84.11`), Dhruv Jurel (#22 Batter, `86.81`, Ice Cold Anchor), Riyan Parag (#28 Batter, `85.22`), Ravindra Jadeja & Sam Curran all-round depth, and emerging youngsters Vaibhav Sooryavanshi & Vignesh Puthur.
            - **Weaknesses / Deficits:** Need reliable **death-overs yorker partner** alongside Sandeep Sharma/Jofra Archer (`Overs 17–20`), **high-tempo #7 seam-bowling finisher**, and **economical finger-spin squeeze** tailored to Jaipur's 74–76m square/straight boundaries.
            """
        )
    with s2:
        st.subheader("Candidate Recruitment Fit vs Actual Availability")
        disc_rr = st.radio("Target Pool", ["Batter", "Bowler"], horizontal=True, key="rr_disc_t")
        if not targets.empty:
            t_sub = targets[targets["discipline"] == disc_rr].head(20)
            st.dataframe(
                t_sub[
                    [
                        "player_name",
                        "latest_ipl_franchise",
                        "eligibility_class",
                        "model_a_rank",
                        "reliability_score",
                        "rr_priority_score",
                        "market_status",
                        "auction_availability",
                        "rr_role_need",
                    ]
                ].rename(
                    columns={
                        "player_name": "Candidate",
                        "latest_ipl_franchise": "Verified 2026 Team",
                        "eligibility_class": "Class",
                        "model_a_rank": "Model A Rank",
                        "reliability_score": "Model A Score",
                        "rr_priority_score": "Statistical Fit Score",
                        "market_status": "Market Status",
                        "auction_availability": "Verified Availability Disclosure",
                        "rr_role_need": "SMS Tactical Fit",
                    }
                ),
                width="stretch",
                hide_index=True,
            )


def _badge_html(status: str) -> str:
    cls_map = {
        "Confirmed Trade": "badge-trade",
        "Confirmed Retained": "badge-retained",
        "Confirmed Released": "badge-released",
        "Pending Verification": "badge-pending",
        "Rumour": "badge-rumour",
        "Policy/Eligibility Review": "badge-policy",
    }
    return f'<span class="badge {cls_map.get(status, "badge-rumour")}">{status}</span>'


def render_market_intelligence(bundle: DashboardDataBundle) -> None:
    st.title("8. Auction & Market Intelligence")
    st.warning(
        "**Pre-Retention Chronology Guardrails (Audit Date: 11 November 2026):**\n"
        "- Official IPL 2027 retention submissions are due **17 November 2026** (`6 days away`). A 2026 squad record is **NOT proof of 2027 retention**, and missing from a list is **NOT released**.\n"
        "- **Pending Verification** records are unverified and are strictly isolated from open-auction availability lists.\n"
        "- **Nathan Ellis (`Confirmed Trade`):** CSK -> SRH (5 Nov 2026) — unavailable for RR auction targeting.\n"
        "- **Haris Rauf (`Policy/Eligibility Review`):** Classified under longstanding post-2008 geopolitical/BCCI policy context (no fabricated individual ban).\n"
        "- Rumours and contract changes **never** alter Model A statistical scores."
    )

    tab_snap, tab_log = st.tabs(["11 November 2026 Competition Snapshot (Pinned)", "Post-Audit Change Log & Retractions"])

    with tab_snap:
        snap = bundle.market_snapshot_nov11.copy()
        counts = summarize_market_counts(snap)
        badge_line = " ".join([f"{_badge_html(s)} <b>{counts[s]}</b>&nbsp;&nbsp;" for s in STRICT_MARKET_STATUSES])
        st.markdown(badge_line, unsafe_allow_html=True)
        st.markdown("")

        sel_statuses = st.multiselect(
            "Filter by Strict Market Status",
            STRICT_MARKET_STATUSES,
            default=STRICT_MARKET_STATUSES,
            key="mkt_status_f",
        )
        sub = prepare_market_display(snap, selected_statuses=sel_statuses)
        if sub.empty:
            st.info("No market records match the selected statuses.")
        else:
            cols_show = [
                "player_id",
                "player_name",
                "current_verified_franchise",
                "previous_franchise",
                "official_retention_status",
                "official_release_status",
                "transaction_mechanism",
                "publisher",
                "source_publication_date",
                "verification_timestamp",
                "evidence_excerpt",
                "confidence_classification",
                "source_url",
            ]
            cols_present = [c for c in cols_show if c in sub.columns]
            st.dataframe(
                sub[cols_present].rename(
                    columns={
                        "player_id": "ID",
                        "player_name": "Player",
                        "current_verified_franchise": "Current Franchise (2026/Trade)",
                        "previous_franchise": "Previous Franchise",
                        "official_retention_status": "Market Status",
                        "official_release_status": "Verified Release Status",
                        "transaction_mechanism": "Verified Mechanism",
                        "publisher": "Source Publisher",
                        "source_publication_date": "Pub Date",
                        "verification_timestamp": "Verified Timestamp",
                        "evidence_excerpt": "Evidence Excerpt",
                        "confidence_classification": "Confidence Level",
                        "source_url": "Source URL",
                    }
                ),
                width="stretch",
                hide_index=True,
            )

    with tab_log:
        st.markdown("Tracks all verified transitions and retractions of unsupported legacy claims while keeping the **11 November 2026 Snapshot** immutable.")
        if not bundle.market_changelog.empty:
            st.dataframe(bundle.market_changelog, width="stretch", hide_index=True)
        else:
            st.info("No change log records loaded.")


def render_methodology_validation(bundle: DashboardDataBundle) -> None:
    st.title("9. Methodology & Validation")
    st.markdown(
        "Plain-language scientific documentation synchronized against executable code (`src/`). "
        "Where an earlier specification document differed from executable code, **the discrepancy is explicitly disclosed below**."
    )

    m1, m2 = st.columns(2)
    with m1:
        st.subheader("Core Mathematical Architecture")
        st.markdown(
            """
            - **BPI & BoPI (0–100):** Four-component continuous pressure indices combining chase rate/defense urgency, wickets/resource scarcity, innings climax, and match leverage prior to delivery.
            - **Expected-Outcome Models:** LightGBM trained strictly chronologically (`Train <= 2024`, `Val 2025`, `Test 2026`) predicting expected runs, dismissal probability, and boundary probability.
            - **PAVA (Raw vs Leverage-Weighted):**
              - `raw_bat_value = (runs - exp_runs) + V_w * (prob_out - is_out) + 0.5 * (is_bnd - prob_bnd)`
              - `leverage_pava = raw_value * (1.0 + Pressure / 50.0)`
            - **Empirical Bayes Shrinkage (`K_shrink = 45.0`):** Pulls small-sample performers smoothly toward replacement mean (`w_EB = n_hp / (n_hp + 45)`).
            - **Match-Clustered Bootstrap (`N = 2,000`):** Resamples whole matches to quantify rank and score instability without assuming delivery independence.
            """
        )

    with m2:
        st.subheader("Explicit Spec-vs-Code Discrepancies & Limitations")
        st.warning(
            """
            1. **High-Pressure Threshold (`P >= 50.0` vs `[65, 85)`):** `reliability_engine.py` uses `bpi >= 50.0` / `bopi >= 50.0` (median split ensuring >=30 HP ball volume), whereas descriptive display tiers label `[65, 85)` as High and `>= 85` as Extreme.
            2. **PRC Slope (`scipy.stats.linregress` vs Exponential Text):** Executable `fit_pressure_response_curve()` fits linear OLS `y = alpha + beta * (P / 100)` rather than exponential decay.
            3. **Sample-Size Sensitivity:** Small-HP batters like Ruturaj Gaikwad (45 HP balls) carry Top-10 inclusion uncertainty (`60.9%`), disclosed via 95% bootstrap intervals.
            4. **Cohort Count Lineage:** Canonical Model A covers **109 batters / 147 bowlers** (combined IPL + T20Is); earlier IPL-only drafts reported 94/137, and an experimental total-deliveries benchmark evaluated 153 bowlers.
            """
        )

    st.markdown("---")
    c_bench, c_abl = st.columns(2)
    with c_bench:
        st.subheader("Chronological Out-of-Sample Model Benchmarks")
        bm_df = build_benchmark_rows(bundle.benchmark)
        if not bm_df.empty:
            st.dataframe(bm_df, width="stretch", hide_index=True)

    with c_abl:
        st.subheader("Component Ablation Study (`VALIDATION_REPORT.json`)")
        abl_df = build_ablation_rows(bundle.validation)
        if not abl_df.empty:
            st.dataframe(abl_df, width="stretch", hide_index=True)


def render_audit_trail(bundle: DashboardDataBundle) -> None:
    st.title("10. Data Sources & Audit Trail")
    st.markdown("Cryptographic provenance, raw-to-processed row reconciliation, and Phase 2 clean-room verification ledger.")

    prov = bundle.provenance
    rec = prov.get("row_count_reconciliation", {})
    st.info(
        f"**Row-Count Reconciliation:** Raw CSV `{rec.get('raw_ball_by_ball_deliveries', 200999):,}` deliveries -> "
        f"Processed regular overs `{rec.get('features_and_pava_deliveries', 200961):,}` + "
        f"`{rec.get('delta_deliveries', 38)}` Super Over deliveries (`{rec.get('audit_status', 'VERIFIED')}`)."
    )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Raw Competition CSV Hashes (`PROVENANCE.json`)")
        raw_files = prov.get("raw_files", {})
        if raw_files:
            r_df = pd.DataFrame(
                [{"Dataset": k, "Rows": v["rows"], "Cols": v["cols"], "SHA-256": v["sha256"]} for k, v in raw_files.items()]
            )
            st.dataframe(r_df, width="stretch", hide_index=True)

    with c2:
        st.subheader("Frozen Baseline & Verification Status")
        st.code(
            f"Final Submission ZIP : 76059a8f5f8b8de5126a5ed8b2a9378fb6664016989f3125df7ca4bbbe9696db\n"
            f"Master Baseline Git  : fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2\n"
            f"Batter Rankings CSV  : {bundle.integrity_status.get('batter_csv_sha256')}\n"
            f"Bowler Rankings CSV  : {bundle.integrity_status.get('bowler_csv_sha256')}\n"
            f"Frozen Integrity     : {bundle.integrity_status.get('batter_frozen_match') and bundle.integrity_status.get('bowler_frozen_match')}",
            language="text",
        )

    p2 = bundle.phase2_manifest
    if p2:
        st.subheader("Phase A Clean-Room Independent Verification Summary")
        checks = p2.get("checks", {})
        st.markdown("**Passed Checks:**\n" + "\n".join(f"- ✅ {x}" for x in checks.get("passed", [])))
        if checks.get("failed"):
            st.markdown("**Failed Checks Disclosed:**\n" + "\n".join(f"- ❌ {x}" for x in checks.get("failed", [])))
        if checks.get("blocked"):
            st.markdown("**Blocked Checks Disclosed:**\n" + "\n".join(f"- ⚠️ {x}" for x in checks.get("blocked", [])))


def main() -> None:
    bundle = _cached_bundle()

    with st.sidebar:
        st.markdown("## 🏏 PRESSUREIQ")
        st.caption("Rajasthan Royals SupeRR Selector S2")
        page = st.radio("Navigation", PAGES, label_visibility="collapsed")
        st.markdown("---")
        st.caption(
            "**Data Coverage:** 200,961 balls (2022–2026)\n\n"
            "**Snapshot Anchor:** 11 Nov 2026\n\n"
            "**Retention Deadline:** 17 Nov 2026\n\n"
            "**Confidentiality:** Zero raw CSV downloads"
        )

    if page == PAGES[0]:
        render_executive_overview(bundle)
    elif page == PAGES[1]:
        _render_leaderboard_view(bundle, is_batting=True)
    elif page == PAGES[2]:
        _render_leaderboard_view(bundle, is_batting=False)
    elif page == PAGES[3]:
        render_player_intelligence(bundle)
    elif page == PAGES[4]:
        render_pressure_analytics(bundle)
    elif page == PAGES[5]:
        render_emerging_talent(bundle)
    elif page == PAGES[6]:
        render_rr_squad_intelligence(bundle)
    elif page == PAGES[7]:
        render_market_intelligence(bundle)
    elif page == PAGES[8]:
        render_methodology_validation(bundle)
    elif page == PAGES[9]:
        render_audit_trail(bundle)


if __name__ == "__main__":
    main()
