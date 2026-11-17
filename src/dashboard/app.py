"""PRESSUREIQ v3 — Premium Interactive Cricket Intelligence Platform."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure repository root is on sys.path so 'src' can always be imported regardless of working directory
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import pandas as pd
import streamlit as st

from src.dashboard.components import (
    render_callout,
    render_footer,
    render_sidebar_brand,
    render_sidebar_lookup,
    render_sidebar_navigation,
    render_sidebar_status,
    render_top_bar,
)
from src.dashboard.data_loader import DashboardDataBundle, load_dashboard_bundle_uncached
from src.dashboard.design_tokens import (
    NAV_LABELS,
    NAV_META,
    PALETTE,
    PRODUCT_NAME,
    PRODUCT_VERSION,
    RETENTION_DEADLINE_DATE,
    SNAPSHOT_ANCHOR_DATE,
)
from src.dashboard.styles import inject_global_styles
from src.dashboard.views.analytics_and_emerging import render_emerging_talent, render_pressure_analytics
from src.dashboard.views.methodology_and_provenance import render_methodology, render_provenance
from src.dashboard.views.overview_and_leaderboards import render_leaderboards, render_overview
from src.dashboard.views.player_directory import render_player_directory
from src.dashboard.views.player_views import render_player_comparison, render_player_intelligence
from src.dashboard.views.rr_and_market import render_market_intelligence, render_rr_intelligence
from src.dashboard.views.rr_command_centre import render_recruitment_command_centre
from src.dashboard.views.rr_target_batters import render_rr_target_batters
from src.dashboard.views.rr_target_bowlers import render_rr_target_bowlers
from src.dashboard.views.rr_squad_gap import render_squad_gap_analysis
from src.dashboard.views.rr_alternatives import render_alternative_target_finder
from src.dashboard.views.rr_watchlist import render_eligibility_and_watchlist

st.set_page_config(
    page_title="PRESSUREIQ — Rajasthan Royals Recruitment Intelligence",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="auto",
)


@st.cache_data(ttl=3600, show_spinner=False)
def _cached_bundle() -> DashboardDataBundle:
    return load_dashboard_bundle_uncached()


PAGE_ALIASES = {
    "Overview": "Official Competition Leaderboards",
    "Pressure Leaderboards": "Official Competition Leaderboards",
    "Global Pressure Intelligence": "Official Competition Leaderboards",
    "Competition Leaderboards": "Official Competition Leaderboards",
    "Player Intelligence": "Player Intelligence Profiles",
    "Player Comparison": "Player Comparison Lab",
    "Rajasthan Royals Intelligence": "Squad Gap Analysis",
    "IPL 2027 Market Intelligence": "Eligibility & Auction Watchlist",
    "Methodology & Validation": "Methodology & Model Validation",
}


def _init_session_state() -> None:
    qp = st.query_params.get("page")
    if qp:
        resolved = PAGE_ALIASES.get(qp, qp)
        if resolved in NAV_LABELS:
            st.session_state["active_page"] = resolved
        elif qp in NAV_LABELS:
            st.session_state["active_page"] = qp
    if "active_page" not in st.session_state:
        st.session_state["active_page"] = NAV_LABELS[0]

    if "jump_player_name" not in st.session_state:
        st.session_state["jump_player_name"] = None
    if "jump_disc" not in st.session_state:
        st.session_state["jump_disc"] = "Batting"


def main() -> None:
    _init_session_state()
    inject_global_styles()

    bundle = _cached_bundle()
    frozen_ok = bool(
        bundle.integrity_status.get("batter_frozen_match", False)
        and bundle.integrity_status.get("bowler_frozen_match", False)
    )

    # Redesigned Luxury Editorial Sidebar (User Requirements v4.1 & v6.0)
    with st.sidebar:
        render_sidebar_brand()
        render_sidebar_lookup(bundle)
        render_sidebar_navigation(active_page=st.session_state["active_page"])
        render_sidebar_status(frozen_ok=frozen_ok)

    active_page = st.session_state["active_page"]
    render_top_bar(page_label=active_page, frozen_ok=frozen_ok, snapshot_date=SNAPSHOT_ANCHOR_DATE)

    if not frozen_ok:
        render_callout(
            f"<b>Integrity Warning:</b> Runtime SHA-256 check detected a mismatch against frozen Model A rankings. "
            f"Batters: <code>{bundle.integrity_status.get('batter_csv_sha256')}</code> | "
            f"Bowlers: <code>{bundle.integrity_status.get('bowler_csv_sha256')}</code>.",
            accent=PALETTE["danger"],
        )

    routes = {
        # Round 1 Primary Deliverables (Model A)
        "Official Competition Leaderboards": render_leaderboards,
        "Global Pressure Intelligence": render_leaderboards,
        "Pressure Leaderboards": render_leaderboards,
        "Overview": render_overview,

        # Additional Scouting & Analytics
        "Pressure Analytics & Physics": render_pressure_analytics,
        "Pressure Analytics": render_pressure_analytics,
        "Player Intelligence Profiles": render_player_intelligence,
        "Player Intelligence": render_player_intelligence,
        "Player Comparison Lab": render_player_comparison,
        "Player Comparison": render_player_comparison,
        "Player Directory": render_player_directory,
        "Methodology & Model Validation": render_methodology,
        "Methodology & Validation": render_methodology,
        "Data Sources & Provenance": render_provenance,
        "Emerging Talent": render_emerging_talent,

        # Supplementary RR Recruitment Intelligence (Model B)
        "Recruitment Command Centre": render_recruitment_command_centre,
        "RR Target Batters": render_rr_target_batters,
        "RR Target Bowlers": render_rr_target_bowlers,
        "Squad Gap Analysis": render_squad_gap_analysis,
        "Rajasthan Royals Intelligence": render_squad_gap_analysis,
        "Alternative Target Finder": render_alternative_target_finder,
        "Eligibility & Auction Watchlist": render_eligibility_and_watchlist,
        "IPL 2027 Market Intelligence": render_eligibility_and_watchlist,
    }
    renderer = routes.get(active_page, render_leaderboards)
    renderer(bundle)

    render_footer(
        batter_sha=str(bundle.integrity_status.get("batter_csv_sha256", "")),
        bowler_sha=str(bundle.integrity_status.get("bowler_csv_sha256", "")),
    )


if __name__ == "__main__":
    main()
