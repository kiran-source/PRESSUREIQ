"""Milestone 5 views: Page 5 (Pressure Analytics) and Page 6 (Emerging Talent)."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.dashboard.analytics import (
    enrich_emerging_watchlist,
    prepare_leaderboard_table,
)
from src.dashboard.charts import (
    RR_BLUE,
    RR_PINK,
    fig_bpi_bopi_distribution,
    fig_emerging_opportunity_matrix,
    fig_expected_vs_observed_tiers,
    fig_sample_vs_score,
    fig_score_distribution,
    fig_shrinkage_curve,
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
    DashboardDataBundle,
    query_unestablished_profiles,
)
from src.dashboard.design_tokens import PALETTE


@st.cache_data(ttl=1800, show_spinner=False)
def _cached_unestablished(is_batting: bool) -> pd.DataFrame:
    return query_unestablished_profiles(is_batting=is_batting, pava_path=DELIVERIES_PAVA_PATH)


def render_pressure_analytics(bundle: DashboardDataBundle) -> None:
    """Page 5: BPI/BoPI distributions, PAVA physics, calibration, shrinkage & uncertainty."""
    st.title("Pressure Analytics")
    render_callout(
        "<b>Association vs. Causality Guardrail:</b> Visualized trends show <b>observed empirical associations</b> between pre-delivery state difficulty "
        "(BPI / BoPI) and marginal value added (PAVA) across 200,961 deliveries. Positive slopes summarize contextual co-variation and do not establish psychological causation.",
        accent=PALETTE["accent_terracotta"],
    )

    ps = bundle.pressure_summary or {}
    hist_df = ps.get("hist", pd.DataFrame())
    tiers_df = ps.get("tiers", pd.DataFrame())
    phase_out_df = ps.get("phase_outcomes", pd.DataFrame())

    total_b_hp = int(bundle.bat_df["hp_balls"].sum()) if not bundle.bat_df.empty else 0
    total_w_hp = int(bundle.bowl_df["hp_balls"].sum()) if not bundle.bowl_df.empty else 0

    render_kpi_grid(
        [
            {"label": "Operational HP Cutoff", "value": "P >= 50.0", "sub": "Partitions near empirical median delivery difficulty", "accent": PALETTE["accent_terracotta"], "icon": "activity"},
            {"label": "Qualified Cohort HP Balls", "value": f"{total_b_hp + total_w_hp:,}", "sub": f"Batters: {total_b_hp:,} | Bowlers: {total_w_hp:,} deliveries", "accent": PALETTE["accent_gold"], "icon": "database"},
            {"label": "EB Shrinkage Constant", "value": "K = 45.0 Balls", "sub": "Regularizes small samples to neutral replacement prior (0.0)", "accent": PALETTE["positive"], "icon": "book"},
            {"label": "Bootstrap Uncertainty", "value": "2,000 Resamples", "sub": "Match-clustered resampling preserving intra-match correlation", "accent": PALETTE["accent_burnt_orange"], "icon": "compare"},
        ]
    )

    c1, c2 = st.columns(2)
    with c1:
        if not hist_df.empty:
            st.plotly_chart(fig_bpi_bopi_distribution(hist_df), width="stretch")
            render_chart_caption("Continuous pressure distribution across 200,961 deliveries. Median delivery falls near 48.2, supporting the P >= 50.0 high-pressure boundary.")
        else:
            render_empty_state("BPI/BoPI histogram unavailable", "Parquet pressure summary could not be computed.")
    with c2:
        if not tiers_df.empty:
            st.plotly_chart(fig_expected_vs_observed_tiers(tiers_df), width="stretch")
            render_chart_caption("LightGBM baseline calibration across pressure tiers, showing progressive run suppression as match leverage escalates.")

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(fig_score_distribution(bundle.bat_df, "Batter Reliability Score Distribution (Qualified Cohort)", RR_BLUE), width="stretch")
        render_chart_caption("Distribution of 109 qualified batters. Median reliability score is 60.4; elite scores (>85) represent the upper decile.")
    with c4:
        st.plotly_chart(fig_score_distribution(bundle.bowl_df, "Bowler Reliability Score Distribution (Qualified Cohort)", RR_PINK), width="stretch")
        render_chart_caption("Distribution of 147 qualified bowlers. Median reliability score is 61.2; right-skewed tail reflects extreme death-overs run suppression.")

    c5, c6 = st.columns(2)
    with c5:
        st.plotly_chart(fig_shrinkage_curve(k_shrink=45.0), width="stretch")
        render_chart_caption("Empirical Bayes shrinkage progression: w = n / (n + 45). Small-sample outliers are regularized smoothly toward the neutral prior.")
    with c6:
        st.plotly_chart(fig_sample_vs_score(bundle.bowl_df, is_batting=False), width="stretch")
        render_chart_caption("Bowler sample exposure vs final reliability score. K=45 threshold marks 50% sample credibility.")

    if not tiers_df.empty:
        render_section_header("Observed vs LightGBM Expected Outcomes by Pressure Tier", "Calibrated baseline check across Low, Medium, High, and Extreme pressure", icon="activity")
        st.dataframe(
            tiers_df.drop(columns=[c for c in ["tier_order"] if c in tiers_df.columns]).rename(
                columns={
                    "pressure_tier": "BPI Tier",
                    "bat_balls": "Batter Balls",
                    "obs_bat_runs": "Obs Runs/Ball",
                    "exp_bat_runs": "Exp Runs/Ball",
                    "obs_boundary_pct": "Obs Boundary (%)",
                    "exp_boundary_pct": "Exp Boundary (%)",
                    "obs_dismissal_pct": "Obs Out (%)",
                    "exp_dismissal_pct": "Exp Out (%)",
                }
            ),
            width="stretch",
            hide_index=True,
        )

    if not phase_out_df.empty:
        render_section_header("League-Wide Phase Pressure & Baseline Summary", "Powerplay vs Middle vs Death scoring and difficulty averages", icon="database")
        st.dataframe(phase_out_df, width="stretch", hide_index=True)


def render_emerging_talent(bundle: DashboardDataBundle) -> None:
    """Page 6: Emerging Talent & Sample-Size-Aware Discovery."""
    st.title("Emerging Talent")
    render_callout(
        "<b>Proven Reliability vs Developmental Potential:</b> Players with fewer than <b>400 career balls</b>, <b>30 HP balls</b>, or <b>20 matches</b> "
        "fail Model A eligibility cutoffs and are isolated here. <b>Small-sample surges are never promoted into frozen Top-10 Model A rankings</b> "
        "or labeled guaranteed future stars.",
        accent=PALETTE["accent_terracotta"],
    )

    em_df = enrich_emerging_watchlist(bundle.emerging_df, bundle.market_current)
    if em_df.empty:
        render_empty_state("Emerging watchlist CSV unavailable", "Expected `data/processed/emerging_talent_watchlist.csv`.")
        return

    tier_a_n = int(em_df["category"].astype(str).str.startswith("Tier A").sum())
    tier_b_n = int(em_df["category"].astype(str).str.startswith("Tier B").sum())
    tier_c_n = int(em_df["category"].astype(str).str.startswith("Tier C").sum())

    render_kpi_grid(
        [
            {"label": "Watchlist Profiles", "value": f"{len(em_df)} Players", "sub": f"Tier A: {tier_a_n} | Tier B: {tier_b_n} | Tier C: {tier_c_n}", "accent": PALETTE["accent_terracotta"], "icon": "sparkles"},
            {"label": "Tier A Qualified Leader", "value": "Naman Dhir (#6)", "sub": "Score 93.30 | 589 balls, 184 HP (exceeds all cutoffs)", "accent": PALETTE["positive"], "icon": "trophy"},
            {"label": "Tier B Top Near-Miss", "value": "Prince Yadav (#11)", "sub": "Score 88.87 | 709 legal balls, 297 HP (0.29 pts off Top 10)", "accent": PALETTE["accent_gold"], "icon": "user"},
            {"label": "Tier C Exposure Guardrail", "value": "Vaibhav (7 HP) | Vignesh (72b)", "sub": "Excluded cleanly due to <30 HP or <400 legal ball thresholds", "accent": PALETTE["accent_burnt_orange"], "icon": "alert"},
        ]
    )

    st.plotly_chart(fig_emerging_opportunity_matrix(em_df), width="stretch")
    render_chart_caption("Watchlist distribution across career exposure (X-axis) and high-pressure opportunities (Y-axis). Dashed cutoffs (30 HP, 400 total balls) enforce Model A qualification boundaries.")

    tier_opts = sorted(em_df["category"].dropna().unique().tolist())
    sel_tiers = st.multiselect("Filter by Evaluation Tier", tier_opts, default=tier_opts, key="em_tier_filter")
    em_filt = em_df[em_df["category"].isin(sel_tiers)].copy() if sel_tiers else em_df.copy()

    render_section_header("Dedicated Emerging & Young Prospect Matrix", "Complete dataset exposure, Model A qualification status, and audited 2027 ledger state", icon="sparkles")
    st.dataframe(em_filt, width="stretch", hide_index=True)

    render_section_header("Inspect Watchlist Candidate Profile", "Audited stats separated strictly from market availability assumptions", icon="user")
    pick_name = st.selectbox("Select Watchlist Player", em_filt["player_name"].tolist(), key="em_pick")
    p_row = em_filt[em_filt["player_name"] == pick_name].iloc[0]
    render_callout(
        f"<b>{p_row['player_name']}</b> (Age {p_row['age']}, {p_row['nationality']}, Canonical ID <code>{p_row['player_id']}</code>)<br/>"
        f"<b>Tier:</b> {p_row['category']} | <b>Model A Status:</b> {p_row['pressure_reliability_score']}<br/>"
        f"<b>Role &amp; Squad Context:</b> {p_row['role']} | {p_row['franchise']} | <b>Market Audit:</b> {p_row['audited_market_status']}<br/>"
        f"<b>Tactical Assessment:</b> {p_row['tactical_assessment']}<br/>"
        f"<b>RR Actionable Note:</b> {p_row['recommendation_for_rr']}",
        accent=PALETTE["accent_terracotta"],
    )

    render_section_header("Dataset-Wide Below-Cutoff Prospects (Live DuckDB Screen)", "Players with >= 30 deliveries below official 400-ball / 30-HP / 20-match gates", icon="database")
    disc_tab1, disc_tab2 = st.tabs(["Below-Cutoff Batters", "Below-Cutoff Bowlers"])
    with disc_tab1:
        un_b = _cached_unestablished(is_batting=True)
        if not un_b.empty:
            st.dataframe(un_b.head(30), width="stretch", hide_index=True)
        else:
            render_empty_state("No batter prospect rows returned", "Check Parquet file access.")
    with disc_tab2:
        un_w = _cached_unestablished(is_batting=False)
        if not un_w.empty:
            st.dataframe(un_w.head(30), width="stretch", hide_index=True)
        else:
            render_empty_state("No bowler prospect rows returned", "Check Parquet file access.")

