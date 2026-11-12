"""PRESSUREIQ v3 — Premium Interactive Cricket Intelligence Platform."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.dashboard.components import (
    render_callout,
    render_footer,
    render_sidebar_brand,
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
    initial_sidebar_state="expanded",
)


@st.cache_data(ttl=3600, show_spinner=False)
def _cached_bundle() -> DashboardDataBundle:
    return load_dashboard_bundle_uncached()


def _init_session_state() -> None:
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

    # Sidebar shell: Branding, Global Player Jump, 10 Routes, Freshness & Provenance
    with st.sidebar:
        render_sidebar_brand()

        # Global Search / Quick Jump across all 256 qualified profiles
        bat_names = [f"{n} (Bat)" for n in bundle.bat_df["player_name"].tolist()] if not bundle.bat_df.empty else []
        bowl_names = [f"{n} (Bowl)" for n in bundle.bowl_df["player_name"].tolist()] if not bundle.bowl_df.empty else []
        jump_opts = ["Select player to inspect…"] + bat_names + bowl_names
        quick_pick = st.selectbox("Quick Player Lookup", jump_opts, index=0, key="global_quick_pick")
        if quick_pick != "Select player to inspect…":
            if quick_pick.endswith(" (Bat)"):
                st.session_state["jump_disc"] = "Batting"
                st.session_state["jump_player_name"] = quick_pick[:-6]
            else:
                st.session_state["jump_disc"] = "Bowling"
                st.session_state["jump_player_name"] = quick_pick[:-7]
            if st.button("Open Player Profile", width="stretch", key="global_jump_btn"):
                st.session_state["active_page"] = "Player Intelligence"
                st.rerun()

        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
        current_idx = NAV_LABELS.index(st.session_state["active_page"]) if st.session_state["active_page"] in NAV_LABELS else 0
        chosen_page = st.radio(
            "Navigation",
            NAV_LABELS,
            index=current_idx,
            key="nav_radio",
        )
        if chosen_page != st.session_state["active_page"]:
            st.session_state["active_page"] = chosen_page

        st.divider()
        meta = NAV_META.get(chosen_page, {})
        st.caption(f"View: {meta.get('subtitle', '')}")
        st.markdown(
            f"<div style='font-size:0.78rem;color:#94A3B8;line-height:1.55;'>"
            f"<b>Version:</b> {PRODUCT_NAME} {PRODUCT_VERSION}<br/>"
            f"<b>Data Coverage:</b> 200,999 raw balls (867 matches)<br/>"
            f"<b>Snapshot Date:</b> {SNAPSHOT_ANCHOR_DATE}<br/>"
            f"<b>Retention Filing:</b> {RETENTION_DEADLINE_DATE}<br/>"
            f"<b>Security:</b> Read-only frozen Model A CSVs"
            f"</div>",
            unsafe_allow_html=True,
        )

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
