"""PRESSUREIQ v3 — Premium Interactive Cricket Intelligence Platform."""

from __future__ import annotations

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
from src.dashboard.views.player_views import render_player_comparison, render_player_intelligence
from src.dashboard.views.rr_and_market import render_market_intelligence, render_rr_intelligence

st.set_page_config(
    page_title="PRESSUREIQ — Cricket Pressure Intelligence",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="auto",
)


@st.cache_data(ttl=3600, show_spinner=False)
def _cached_bundle() -> DashboardDataBundle:
    return load_dashboard_bundle_uncached()


def _init_session_state() -> None:
    qp = st.query_params.get("page")
    if qp and qp in NAV_LABELS:
        st.session_state["active_page"] = qp
    elif "active_page" not in st.session_state:
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

    # Redesigned Luxury Editorial Sidebar (User Requirements v4.1)
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
        "Overview": render_overview,
        "Pressure Leaderboards": render_leaderboards,
        "Player Intelligence": render_player_intelligence,
        "Player Comparison": render_player_comparison,
        "Pressure Analytics": render_pressure_analytics,
        "Emerging Talent": render_emerging_talent,
        "Rajasthan Royals Intelligence": render_rr_intelligence,
        "IPL 2027 Market Intelligence": render_market_intelligence,
        "Methodology & Validation": render_methodology,
        "Data Sources & Provenance": render_provenance,
    }
    routes[active_page](bundle)

    render_footer(
        batter_sha=str(bundle.integrity_status.get("batter_csv_sha256", "")),
        bowler_sha=str(bundle.integrity_status.get("bowler_csv_sha256", "")),
    )


if __name__ == "__main__":
    main()
