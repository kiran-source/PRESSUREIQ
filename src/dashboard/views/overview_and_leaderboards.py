"""Milestone 3 views: Page 1 (Executive Overview) and Page 2 (Pressure Leaderboards)."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.dashboard.analytics import (
    _safe_float,
    compute_player_five_pillars,
    extract_unique_teams,
    filter_leaderboard,
    prepare_leaderboard_table,
)
from src.dashboard.charts import (
    ARCHETYPE_COLORS,
    RR_BLUE,
    RR_PINK,
    fig_batter_vs_bowler_comparison,
    fig_five_pillar_radar,
    fig_rank_uncertainty_intervals,
    fig_sample_vs_score,
    fig_top10_ci_bar,
)
from src.dashboard.components import (
    render_callout,
    render_empty_state,
    render_hero_banner,
    render_kpi_grid,
    render_section_header,
)
from src.dashboard.data_loader import (
    DELIVERIES_PAVA_PATH,
    MATCHES_PATH,
    DashboardDataBundle,
    query_season_format_stats,
)
from src.dashboard.design_tokens import PALETTE, PRODUCT_NAME, PRODUCT_TAGLINE, SNAPSHOT_ANCHOR_DATE


@st.cache_data(ttl=1800, show_spinner=False)
def _cached_slice_stats(is_batting: bool, season: int | None, comp_category: str | None) -> pd.DataFrame:
    return query_season_format_stats(
        is_batting=is_batting,
        season=season,
        comp_category=comp_category,
        pava_path=DELIVERIES_PAVA_PATH,
        matches_path=MATCHES_PATH,
    )


def render_overview(bundle: DashboardDataBundle) -> None:
    """Page 1: Executive Overview landing view."""
    render_hero_banner(
        title=f"{PRODUCT_NAME} — Cricket Pressure Intelligence",
        tagline=PRODUCT_TAGLINE,
        description=(
            "Franchise-grade evaluation engine engineered for Rajasthan Royals SupeRR Selector Season 2. "
            "Computes context-aware Expected Outcomes and Pressure-Adjusted Value Added (PAVA) across 200,999 historical deliveries "
            "to isolate genuine high-leverage composure from low-stakes volume accumulation."
        ),
        pills=["Confirmed", "Pending Verification"],
    )

    played_matches = 867
    if not bundle.matches_df.empty and "match_id" in bundle.matches_df.columns:
        total_catalog = len(bundle.matches_df)
    else:
        total_catalog = 883

    top_bat = bundle.bat_df.iloc[0] if not bundle.bat_df.empty else None
    top_bowl = bundle.bowl_df.iloc[0] if not bundle.bowl_df.empty else None
    top_bat_name = str(top_bat["player_name"]) if top_bat is not None else "N/A"
    top_bowl_name = str(top_bowl["player_name"]) if top_bowl is not None else "N/A"

    render_kpi_grid(
        [
            {
                "label": "Model A #1 Batter",
                "value": top_bat_name,
                "sub": (
                    f"Score {top_bat['reliability_score']:.2f} | CI [{top_bat['ci_lower_95']:.1f}, {top_bat['ci_upper_95']:.1f}] | {int(top_bat['hp_balls'])} HP balls"
                    if top_bat is not None
                    else "Frozen ranking unavailable"
                ),
                "accent": PALETTE["accent_blue"],
                "icon": "trophy",
            },
            {
                "label": "Model A #1 Bowler",
                "value": top_bowl_name,
                "sub": (
                    f"Score {top_bowl['reliability_score']:.2f} | CI [{top_bowl['ci_lower_95']:.1f}, {top_bowl['ci_upper_95']:.1f}] | {int(top_bowl['hp_balls'])} HP balls"
                    if top_bowl is not None
                    else "Frozen ranking unavailable"
                ),
                "accent": PALETTE["accent_violet"],
                "icon": "trophy",
            },
            {
                "label": "Evaluated Qualified Cohorts",
                "value": f"{len(bundle.bat_df)} Bat | {len(bundle.bowl_df)} Bowl",
                "sub": "Screened from 888 batters & 647 bowlers (>=400 balls, >=30 HP, >=20 matches)",
                "accent": PALETTE["positive"],
                "icon": "user",
            },
            {
                "label": "Dataset & Bootstrap Scope",
                "value": f"200,999 Balls | {played_matches} Matches",
                "sub": f"200,961 regular + 38 Super Over balls ({total_catalog} cataloged, 16 abandoned) | N=2,000 bootstraps",
                "accent": PALETTE["warning"],
                "icon": "database",
            },
        ]
    )

    render_callout(
        f"<b>Governance &amp; Scale Disclosure:</b> Composite <b>Reliability Score (0–100) = Phi(Z_composite) * 100</b> is a standardized "
        f"norm-referenced index across 5 weighted pillars — it is <b>NOT</b> a probability of match success. Statistical Model A rankings "
        f"remain frozen and strictly separate from the IPL 2027 market ledger (anchored to audited <b>{SNAPSHOT_ANCHOR_DATE}</b> snapshot ahead of "
        f"17 Nov official retention filings).",
        accent=PALETTE["accent_violet"],
    )

    bat_top = prepare_leaderboard_table(bundle.bat_df, is_batting=True).head(10)
    bowl_top = prepare_leaderboard_table(bundle.bowl_df, is_batting=False).head(10)

    c1, c2 = st.columns(2)
    with c1:
        render_section_header("Official Model A Top 10 Batters", "Frozen ranking order paired with 2,000-match bootstrap stability", icon="trophy")
        if not bat_top.empty:
            cols = ["rank", "player_name", "role", "reliability_score", "hp_balls", "kish_match_ess", "top10_inclusion_prob_pct", "score_ci_95"]
            avail = [c for c in cols if c in bat_top.columns]
            st.dataframe(
                bat_top[avail].rename(
                    columns={
                        "rank": "Rank",
                        "player_name": "Batter",
                        "role": "Role",
                        "reliability_score": "Score",
                        "hp_balls": "HP Balls",
                        "kish_match_ess": "Kish ESS",
                        "top10_inclusion_prob_pct": "Top-10 Prob (%)",
                        "score_ci_95": "95% CI",
                    }
                ),
                width="stretch",
                hide_index=True,
            )
    with c2:
        render_section_header("Official Model A Top 10 Bowlers", "Run suppression and death-overs wicket value added above expectation", icon="trophy")
        if not bowl_top.empty:
            cols = ["rank", "player_name", "pace_or_spin", "reliability_score", "hp_balls", "kish_match_ess", "top10_inclusion_prob_pct", "score_ci_95"]
            avail = [c for c in cols if c in bowl_top.columns]
            st.dataframe(
                bowl_top[avail].rename(
                    columns={
                        "rank": "Rank",
                        "player_name": "Bowler",
                        "pace_or_spin": "Type",
                        "reliability_score": "Score",
                        "hp_balls": "HP Balls",
                        "kish_match_ess": "Kish ESS",
                        "top10_inclusion_prob_pct": "Top-10 Prob (%)",
                        "score_ci_95": "95% CI",
                    }
                ),
                width="stretch",
                hide_index=True,
            )

    ch1, ch2 = st.columns(2)
    with ch1:
        st.plotly_chart(fig_top10_ci_bar(bundle.bat_df, "Top 10 Batters — Score & 95% Bootstrap CI", RR_BLUE), width="stretch")
    with ch2:
        st.plotly_chart(fig_top10_ci_bar(bundle.bowl_df, "Top 10 Bowlers — Score & 95% Bootstrap CI", RR_PINK), width="stretch")

    render_section_header("Key Analytical Findings & Research Limitations", "Core empirical discoveries and methodological guardrails", icon="book")
    f1, f2, f3 = st.columns(3)
    with f1:
        render_callout(
            "<b>1. Raw Rate Metrics Mislead:</b> Raw career strike rate shares only <b>3/10</b> overlap (Jaccard 0.176) with Model A pressure leaders, "
            "over-rewarding powerplay stat-padding and low-leverage run accumulation.",
            accent=PALETTE["accent_blue"],
        )
    with f2:
        render_callout(
            "<b>2. Small-Sample Bootstrap Dispersion:</b> Qualifiers with 35–83 HP balls (e.g., Rohit, Gaikwad, Salt, Dawson, Ishant) display wide 95% CIs "
            "because match resampling can drop exposure below the 30-HP eligibility gate.",
            accent=PALETTE["warning"],
        )
    with f3:
        render_callout(
            "<b>3. Strict Baseline & Market Separation:</b> Freeze integrity preserves pre-P0-3 fixed-120-ball calculations (`0.0` diff reproduction). Market availability "
            "remains isolated and awaits official 17 Nov 2026 retention lists.",
            accent=PALETTE["positive"],
        )

    st.plotly_chart(fig_batter_vs_bowler_comparison(bundle.bat_df, bundle.bowl_df), width="stretch")


def _render_single_discipline_leaderboard(bundle: DashboardDataBundle, is_batting: bool) -> None:
    disc_name = "Batters" if is_batting else "Bowlers"
    raw_df = bundle.bat_df if is_batting else bundle.bowl_df
    accent = RR_BLUE if is_batting else RR_PINK
    role_col = "role" if is_batting else "bowling_type"

    if raw_df.empty or "rank" not in raw_df.columns:
        render_empty_state(f"Official {disc_name} rankings unavailable", f"Verify `data/processed/final_{'batter' if is_batting else 'bowler'}_rankings.csv` is present.")
        return

    table_df = prepare_leaderboard_table(raw_df, is_batting=is_batting)

    f1, f2, f3, f4, f5 = st.columns([1.25, 1.05, 0.95, 1.1, 1.05])
    roles_avail = sorted(table_df[role_col].dropna().unique().tolist()) if role_col in table_df.columns else []
    sel_roles = f1.multiselect("Role / Bowling Style", roles_avail, default=roles_avail, key=f"lb_role_{disc_name}")

    season_opts = ["All (2022–2026 Official Baseline)", "2022", "2023", "2024", "2025", "2026"]
    sel_season = f2.selectbox("Season Slice (Empirical)", season_opts, key=f"lb_season_{disc_name}")

    format_opts = ["All Formats", "IPL", "T20I", "Other_T20"]
    sel_format = f3.selectbox("Format Slice", format_opts, key=f"lb_format_{disc_name}")

    all_teams = extract_unique_teams(table_df)
    sel_team = f4.selectbox("Dataset Team", ["All Teams"] + all_teams, key=f"lb_team_{disc_name}")

    raw_max_hp = int(pd.to_numeric(table_df["hp_balls"], errors="coerce").max() or 30)
    slider_max = max(40, min(400, raw_max_hp))
    min_hp = f5.slider("Min HP Balls (P >= 50)", min_value=30, max_value=slider_max, value=30, key=f"lb_hp_{disc_name}")

    s1, s2, s3 = st.columns([1.6, 1.1, 1.1])
    search_q = s1.text_input("Search Player Name", placeholder=f"Type {disc_name.lower()[:-1]} name...", key=f"lb_search_{disc_name}")
    sort_opts = {
        "Official Model A Rank (Default)": ("rank", True),
        "Reliability Score (High -> Low)": ("reliability_score", False),
        "Top-10 Inclusion Prob (%)": ("top10_inclusion_prob_pct", False),
        "High-Pressure Balls (Volume)": ("hp_balls", False),
        "Kish Effective Sample Size (ESS)": ("kish_match_ess", False),
        "Shrunk HP PAVA / Ball": ("shrunk_hp_pava_per_ball", False),
    }
    sel_sort = s2.selectbox("Sort Order (Rank Column Never Rewritten)", list(sort_opts.keys()), key=f"lb_sort_{disc_name}")
    scope_mode = s3.radio("Population View", ["Featured Top 10", f"Full Qualified Cohort ({len(table_df)})"], horizontal=True, key=f"lb_scope_{disc_name}")

    filtered = filter_leaderboard(
        table_df,
        roles=sel_roles,
        min_hp_balls=min_hp,
        search_query=search_q,
        team_filter=None if sel_team == "All Teams" else sel_team,
    )

    if sel_season != season_opts[0] or sel_format != "All Formats":
        yr = None if sel_season == season_opts[0] else int(sel_season)
        fmt = None if sel_format == "All Formats" else sel_format
        slice_df = _cached_slice_stats(is_batting=is_batting, season=yr, comp_category=fmt)
        if not slice_df.empty:
            filtered = filtered.merge(slice_df, on="player_id", how="inner")
            filtered = filtered[filtered["slice_balls"] > 0].copy()

    sort_col, sort_asc = sort_opts[sel_sort]
    if sort_col in filtered.columns:
        filtered = filtered.sort_values(sort_col, ascending=sort_asc, na_position="last")

    display_df = filtered.head(10).copy() if scope_mode == "Featured Top 10" and sel_sort == "Official Model A Rank (Default)" else filtered.copy()

    if display_df.empty:
        render_empty_state(
            f"No qualified {disc_name.lower()} match the active filters",
            "Relax the Role/Style selection, lower Min HP Balls, or switch Dataset Team / Season filters back to All.",
        )
        return

    render_callout(
        f"Showing <b>{len(display_df)}</b> of <b>{len(filtered)}</b> filtered {disc_name.lower()} (total qualified cohort: <b>{len(table_df)}</b>). "
        "<b>Sample Distinction:</b> <code>HP Balls</code> counts raw deliveries faced/bowled at P >= 50.0, whereas "
        "<code>EB Effective HP</code> = <code>n / (n + 45) * n</code> and <code>Kish Match ESS</code> = <code>(sum n_m)^2 / sum(n_m^2)</code> "
        "quantifies independent match-cluster concentration.",
        accent=accent,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_top10_ci_bar(display_df, f"Filtered Top {min(10, len(display_df))} {disc_name} — Score & 95% CI", accent), width="stretch")
    with c2:
        st.plotly_chart(fig_rank_uncertainty_intervals(display_df, top_n=min(12, len(display_df)), title=f"Rank Uncertainty (Model A vs 2,000-Bootstrap)"), width="stretch")

    render_section_header(f"Verified {disc_name} Telemetry Table", "Read-only view of frozen Model A metrics + bootstrap uncertainty", icon="trophy")
    base_cols = [
        "rank", "player_name", "dataset_ipl_team", role_col, "reliability_score", "score_ci_95",
        "top10_inclusion_prob_pct", "boot_median_rank", "rank_ci_95", "matches", "hp_balls",
        "eb_effective_hp_balls", "kish_match_ess", "shrunk_hp_pava_per_ball", "retention_delta", "prc_archetype",
    ]
    if "slice_balls" in display_df.columns:
        base_cols.extend(["slice_matches", "slice_balls", "slice_hp_balls", "slice_rate_stat", "slice_hp_raw_pava"])
    cols_show = [c for c in base_cols if c in display_df.columns]
    clean_tbl = display_df[cols_show].rename(
        columns={
            "rank": "Model A Rank",
            "player_name": "Player Name",
            "dataset_ipl_team": "Dataset Team",
            "role": "Role",
            "bowling_type": "Bowling Style",
            "reliability_score": "Reliability Score",
            "score_ci_95": "95% Score CI",
            "top10_inclusion_prob_pct": "Top-10 Prob (%)",
            "boot_median_rank": "Median Boot Rank",
            "rank_ci_95": "95% Rank Interval",
            "matches": "Matches",
            "hp_balls": "HP Balls (P>=50)",
            "eb_effective_hp_balls": "EB Effective HP",
            "kish_match_ess": "Kish Match ESS",
            "shrunk_hp_pava_per_ball": "Shrunk PAVA/Ball",
            "retention_delta": "Retention Delta",
            "prc_archetype": "PRC Class",
            "slice_matches": "Slice Matches",
            "slice_balls": "Slice Balls",
            "slice_hp_balls": "Slice HP Balls",
            "slice_rate_stat": "Slice SR" if is_batting else "Slice Econ",
            "slice_hp_raw_pava": "Slice HP PAVA",
        }
    )
    st.dataframe(clean_tbl, width="stretch", hide_index=True)

    # Export filtered view cleanly
    csv_bytes = clean_tbl.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"Export Filtered {disc_name} View (CSV)",
        data=csv_bytes,
        file_name=f"pressureiq_filtered_{disc_name.lower()}_view.csv",
        mime="text/csv",
        key=f"dl_{disc_name}",
    )

    # Position-based comparison & detailed player inspection
    col_pos, col_insp = st.columns([1.0, 1.15])
    with col_pos:
        render_section_header("Position / Role Benchmark", "Cohort mean score and median HP balls by role", icon="compare")
        pos_group_col = "role" if is_batting else "pace_or_spin"
        if pos_group_col in filtered.columns:
            pos_summary = (
                filtered.groupby(pos_group_col, as_index=False)
                .agg(
                    Players=("player_name", "count"),
                    Mean_Score=("reliability_score", "mean"),
                    Top_Score=("reliability_score", "max"),
                    Median_HP_Balls=("hp_balls", "median"),
                )
            )
            pos_summary["Mean_Score"] = pos_summary["Mean_Score"].round(2)
            st.dataframe(pos_summary, width="stretch", hide_index=True)

    with col_insp:
        render_section_header("Quick Player Inspection", "Select any player from filtered results to inspect 5-pillar profile", icon="user")
        sel_name = st.selectbox("Inspect Player", display_df["player_name"].tolist(), key=f"lb_insp_{disc_name}")
        p_row = display_df[display_df["player_name"] == sel_name].iloc[0]
        peer_subset = table_df[table_df[role_col] == p_row[role_col]] if role_col in table_df.columns else table_df
        peer_means: dict[str, float] = {}
        for _, pr in peer_subset.iterrows():
            for k, v in compute_player_five_pillars(pr).items():
                peer_means[k] = peer_means.get(k, 0.0) + v
        if len(peer_subset) > 0:
            peer_means = {k: v / len(peer_subset) for k, v in peer_means.items()}
        st.plotly_chart(fig_five_pillar_radar(p_row, peer_means, sel_name, str(p_row.get(role_col, disc_name))), width="stretch")

    st.plotly_chart(fig_sample_vs_score(filtered, is_batting=is_batting), width="stretch")


def render_leaderboards(bundle: DashboardDataBundle) -> None:
    """Page 2: Pressure Leaderboards with Batters & Bowlers tabs."""
    st.title("Pressure Leaderboards")
    render_callout(
        "<b>Frozen Model A Baselines:</b> Rankings are loaded read-only from immutable competition CSVs. "
        "Filtering, slicing by season/format, or changing sort order inspects the cohort without ever rewriting Model A scores or official ranks.",
        accent=PALETTE["accent_blue"],
    )
    tab_bat, tab_bowl = st.tabs(["Batters Leaderboard (109 Qualified)", "Bowlers Leaderboard (147 Qualified)"])
    with tab_bat:
        _render_single_discipline_leaderboard(bundle, is_batting=True)
    with tab_bowl:
        _render_single_discipline_leaderboard(bundle, is_batting=False)

