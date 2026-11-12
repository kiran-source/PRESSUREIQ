"""Milestone 6 & 7 views: Page 7 (Rajasthan Royals Intelligence) and Page 8 (IPL 2027 Market Intelligence)."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.dashboard.analytics import (
    ALL_DISPLAY_MARKET_STATUSES,
    STRICT_MARKET_STATUSES,
    build_all_ipl_teams_overview,
    prepare_market_display,
    summarize_market_counts,
    summarize_rr_squad_intelligence,
)
from src.dashboard.charts import fig_market_team_matrix, fig_rr_role_depth
from src.dashboard.components import (
    render_callout,
    render_empty_state,
    render_kpi_grid,
    render_section_header,
    status_badge_html,
)
from src.dashboard.data_loader import DashboardDataBundle
from src.dashboard.design_tokens import IPL_FRANCHISES, PALETTE


def render_rr_intelligence(bundle: DashboardDataBundle) -> None:
    """Page 7: Rajasthan Royals tactical squad intelligence and SMS Jaipur strategy."""
    st.title("Rajasthan Royals Intelligence")
    intel = summarize_rr_squad_intelligence(bundle.eligibility_audit_df, bundle.rr_candidates_df)
    rr_core = intel["rr_core"]
    role_depth = intel["role_depth"]
    targets = intel["targets"]

    confirmed_rel_cnt = int(targets["market_verified_available"].sum()) if (not targets.empty and "market_verified_available" in targets.columns) else 0
    avg_core_score = float(rr_core["reliability_score"].mean()) if not rr_core.empty else 0.0

    rel_noun = "target is" if confirmed_rel_cnt == 1 else "targets are"
    render_callout(
        f"<b>Performance Fit vs Confirmed Auction Availability:</b> Statistical role fit (<code>rr_priority_score</code>) ranks cricket "
        f"utility at Sawai Mansingh Stadium (Jaipur). It does <b>NOT</b> grant open-auction availability: ahead of the <b>17 November 2026</b> "
        f"IPL retention deadline, <b>{confirmed_rel_cnt} external watchlist {rel_noun} confirmed released</b>.",
        accent=PALETTE["accent_violet"],
    )

    render_kpi_grid(
        [
            {"label": "RR 2026 Qualified Core", "value": f"{len(rr_core)} Profiles", "sub": "Model A qualified profiles verified on RR 2026 roster", "accent": PALETTE["accent_violet"], "icon": "shield"},
            {"label": "RR Core Mean Reliability", "value": f"{avg_core_score:.2f}" if avg_core_score > 0 else "N/A", "sub": "Led by Jofra Archer (#16 Bowler), Dhruv Jurel (#22), Riyan Parag (#28)", "accent": PALETTE["accent_blue"], "icon": "trophy"},
            {"label": "SMS Jaipur Strategic Needs", "value": "3 Priority Gaps", "sub": "#7 Seam Power Finisher | Middle-Overs Squeeze | Death Seam Depth", "accent": PALETTE["warning"], "icon": "activity"},
            {"label": "Confirmed Auction Releases", "value": f"{confirmed_rel_cnt} Targets", "sub": "Pre-Nov 17 ledger awaits official franchise filing before bidding", "accent": PALETTE["positive"], "icon": "briefcase"},
        ]
    )

    c1, c2 = st.columns([1.15, 0.95])
    with c1:
        render_section_header("RR 2026 Qualified Core Roster", "Verified current squad profiles (excluding departed former RR players)", icon="shield")
        if not rr_core.empty:
            cols = [c for c in ["player_name", "discipline", "role", "model_a_rank", "reliability_score", "hp_balls", "prc_archetype", "market_status_verified"] if c in rr_core.columns]
            st.dataframe(rr_core[cols], width="stretch", hide_index=True)
            st.caption("Departed historical RR alumni (e.g., Jos Buttler -> GT, Prasidh Krishna -> GT, Trent Boult -> MI, Sanju Samson -> CSK) remain correctly mapped to their verified 2026 squads.")
        else:
            render_empty_state("RR core audit unavailable", "Missing `player_eligibility_audit.csv`.")
    with c2:
        if not role_depth.empty:
            st.plotly_chart(fig_rr_role_depth(role_depth), width="stretch")

    # Batting vs Bowling Depth + Strengths & Weaknesses
    s1, s2 = st.columns(2)
    with s1:
        render_section_header("Squad Depth & Pressure Strengths", "Observed strengths across RR qualified batters and bowlers", icon="check")
        if not role_depth.empty:
            st.dataframe(role_depth, width="stretch", hide_index=True)
        render_callout(
            "<b>Key Strengths:</b> Strong middle-order composure (Dhruv Jurel #22, Riyan Parag #28), elite top-end pace leverage (Jofra Archer #16 Bowler), "
            "plus high-ceiling Tier C emerging prospects (Vaibhav Sooryavanshi, Vignesh Puthur).",
            accent=PALETTE["positive"],
        )
    with s2:
        render_section_header("Tactical Deficits & Emerging RR Options", "Venue-adjusted SMS Jaipur priorities (large boundaries & middle-overs grip)", icon="alert")
        render_callout(
            "<b>Target Deficits at SMS Jaipur:</b><br/>"
            "• <b>#7 Power Finisher Fit:</b> Contingency screen if rival finishers are released (e.g., Romario Shepherd RCB 2026 Pending Nov 17).<br/>"
            "• <b>Middle-Overs Finger Spin ('Jaipur Squeeze'):</b> Liam Dawson (#1 Bowler) &amp; Harpreet Brar (PBKS 2026 Pending Nov 17) benchmark flat-trajectory grip.<br/>"
            "• <b>Domestic Death Seam Depth:</b> Complement Sandeep Sharma with emerging pace watchlists (Prince Yadav #11 LSG 2026, Rasikh Salam #20).",
            accent=PALETTE["warning"],
        )

    render_section_header("Statistical Role-Fit Watchlist vs Verified Market Availability", "Filtered candidate ranking strictly separated from open-auction assumptions", icon="briefcase")
    if not targets.empty:
        t1, t2, t3 = st.columns(3)
        disc_f = t1.selectbox("Discipline", ["All", "Batting", "Bowling"], key="rr_cand_disc")
        stat_opts = sorted(targets["market_status"].dropna().unique().tolist())
        sel_stats = t2.multiselect("Filter Market Status", stat_opts, default=stat_opts, key="rr_cand_stat")
        only_rel = t3.checkbox("Only Confirmed Auction Releases", value=False, key="rr_only_rel")

        view_t = targets.copy()
        if disc_f != "All":
            view_t = view_t[view_t["discipline"] == disc_f]
        if sel_stats:
            view_t = view_t[view_t["market_status"].isin(sel_stats)]
        else:
            view_t = view_t.iloc[0:0].copy()
        if only_rel:
            view_t = view_t[view_t["market_verified_available"]]

        if view_t.empty:
            if only_rel:
                empty_title = "0 candidates currently satisfy Confirmed Released filter"
                empty_desc = (
                    "Expected pre-Nov 17 state: official IPL 2027 release lists have not been submitted yet. "
                    "Uncheck 'Only Confirmed Auction Releases' to view statistical role fit."
                )
            elif not sel_stats:
                empty_title = "No Market Status selected"
                empty_desc = "Select at least one Market Status value in the filter above to inspect watchlist candidates."
            else:
                empty_title = "No candidates match the active discipline and market-status filters"
                empty_desc = (
                    f"Active filters (Discipline: {disc_f}; Market Statuses selected: {len(sel_stats)}) returned 0 rows. "
                    "Broaden the Market Status selection or switch Discipline back to 'All'."
                )
            render_empty_state(empty_title, empty_desc)
        else:
            show_cols = [
                "rr_priority_rank", "player_name", "discipline", "latest_ipl_franchise", "model_a_rank",
                "reliability_score", "rr_priority_score", "eligibility_class", "market_status", "auction_availability", "market_source_url",
            ]
            st.dataframe(
                view_t[[c for c in show_cols if c in view_t.columns]].head(40),
                width="stretch",
                hide_index=True,
                column_config={"market_source_url": st.column_config.LinkColumn("Source URL")},
            )


def render_market_intelligence(bundle: DashboardDataBundle) -> None:
    """Page 8: Dynamic IPL 2027 Market Intelligence across all 10 teams + verified ledger."""
    st.title("IPL 2027 Market Intelligence")
    render_callout(
        "<b>Pre-Retention Market Safeguards (Snapshot Anchored 11 November 2026):</b><br/>"
        "• Official IPL 2027 retention submissions occur on <b>17 November 2026</b>; a 2026 contract does not confirm 2027 retention, and omission from an announcement never implies release.<br/>"
        "• Rumours are never promoted to confirmed transfers, and market activity <b>never modifies frozen Model A statistical scores</b>.",
        accent=PALETTE["warning"],
    )

    counts = summarize_market_counts(bundle.market_current)
    badges = "".join(
        f"{status_badge_html(st_name)} <span class='piq-mono' style='margin-right:10px;color:#F8FAFC;font-weight:700;'>{counts.get(st_name, 0)}</span>"
        for st_name in STRICT_MARKET_STATUSES
    )
    st.markdown(f"<div style='margin:6px 0 14px 0;line-height:2.1;'>{badges}</div>", unsafe_allow_html=True)

    tab_teams, tab_ledger, tab_changelog = st.tabs(
        [
            "All 10 IPL Franchises (Squads & 2027 Status)",
            "Source-Audited Ledger (17 Tracked Players)",
            "Chronological Market Audit Trail",
        ]
    )

    with tab_teams:
        teams_df = build_all_ipl_teams_overview(
            bundle.players_df,
            bundle.market_current,
            bundle.bat_df,
            bundle.bowl_df,
            bundle.rr_candidates_df,
        )
        if not teams_df.empty:
            st.plotly_chart(fig_market_team_matrix(teams_df), width="stretch")
            st.dataframe(teams_df, width="stretch", hide_index=True)

            render_section_header("Inspect Franchise Squad & Verified Transitions", "Select any IPL franchise to inspect dataset roster & 2027 ledger records", icon="briefcase")
            team_names = [t[1] for t in IPL_FRANCHISES]
            sel_team = st.selectbox("Select Franchise", team_names, index=7, key="mkt_team_pick")
            pl = bundle.players_df
            team_hist = (
                pl[(pl["team_name"] == sel_team) & (pl["comp_name"] == "IPL 2026")][["player_id", "player_name", "comp_name", "team_name"]]
                .drop_duplicates()
                .sort_values("player_name")
                if (not pl.empty and "comp_name" in pl.columns)
                else pd.DataFrame()
            )
            mkt = bundle.market_current
            team_mkt = mkt[(mkt["current_verified_franchise"] == sel_team) | (mkt["previous_franchise"] == sel_team)] if not mkt.empty else pd.DataFrame()

            tc1, tc2 = st.columns(2)
            with tc1:
                st.markdown(f"**{sel_team} — Audited 2027 Ledger Records**")
                if not team_mkt.empty:
                    st.dataframe(
                        team_mkt[["player_id", "player_name", "previous_franchise", "current_verified_franchise", "official_retention_status", "source_publication_date", "verification_timestamp", "confidence_classification", "source_url"]],
                        width="stretch",
                        hide_index=True,
                        column_config={"source_url": st.column_config.LinkColumn("Verified URL")},
                    )
                else:
                    render_empty_state(f"No tracked top-20 ledger overrides for {sel_team}", "2026 roster players remain Historical / Pending Nov 17 retention submissions.")
            with tc2:
                st.markdown(f"**{sel_team} — IPL 2026 Dataset Roster (`Historical / Pre-2027`)**")
                if not team_hist.empty:
                    st.dataframe(team_hist.rename(columns={"player_id": "ID", "player_name": "Player", "comp_name": "Season", "team_name": "Franchise"}), width="stretch", hide_index=True)
                else:
                    render_empty_state("No IPL 2026 rows found", "Check `players.parquet` dataset.")

    with tab_ledger:
        sel_statuses = st.multiselect("Filter by Strict Market Status", STRICT_MARKET_STATUSES, default=STRICT_MARKET_STATUSES, key="mkt_status_filter")
        disp_curr = prepare_market_display(bundle.market_current, selected_statuses=sel_statuses)
        if disp_curr.empty:
            render_empty_state("No tracked ledger entries match selected statuses", "Select additional statuses (e.g., Pending Verification or Confirmed Trade).")
        else:
            cols = [
                "player_id", "player_name", "previous_franchise", "current_verified_franchise",
                "official_retention_status", "official_release_status", "confirmed_trade_status",
                "transaction_mechanism", "rumour_status", "confidence_classification",
                "publisher", "source_publication_date", "verification_timestamp", "source_url",
            ]
            st.dataframe(
                disp_curr[[c for c in cols if c in disp_curr.columns]],
                width="stretch",
                hide_index=True,
                column_config={"source_url": st.column_config.LinkColumn("Verified Source URL")},
            )
            st.download_button(
                "Export Audited Market Ledger (CSV)",
                data=disp_curr.to_csv(index=False).encode("utf-8"),
                file_name="pressureiq_ipl2027_market_ledger.csv",
                mime="text/csv",
                key="dl_mkt_ledger",
            )

    with tab_changelog:
        if not bundle.market_changelog.empty:
            st.dataframe(
                bundle.market_changelog,
                width="stretch",
                hide_index=True,
                column_config={"source_url": st.column_config.LinkColumn("Source URL")},
            )
        else:
            render_empty_state("No market audit log entries found", "Check `ipl_2027_market_change_log.csv`.")

