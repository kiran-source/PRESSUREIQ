"""Milestone 8 views: Page 9 (Methodology & Validation) and Page 10 (Data Sources & Provenance)."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.dashboard.analytics import build_ablation_rows, build_benchmark_rows
from src.dashboard.charts import fig_shrinkage_curve
from src.dashboard.components import (
    render_callout,
    render_chart_caption,
    render_empty_state,
    render_kpi_grid,
    render_section_header,
    status_badge_html,
)
from src.dashboard.data_loader import (
    FROZEN_ARCHIVE_ZIP_SHA256,
    FROZEN_BATTER_SHA256,
    FROZEN_BOWLER_SHA256,
    FROZEN_MARKET_SNAPSHOT_SHA256,
    DashboardDataBundle,
)
from src.dashboard.design_tokens import PALETTE, PRODUCT_VERSION, RETENTION_DEADLINE_DATE, SNAPSHOT_ANCHOR_DATE


def render_methodology(bundle: DashboardDataBundle) -> None:
    """Page 9: Methodology, Formulas, Validation Metrics & Legacy vs P0-3 Reconciliation."""
    st.title("Methodology & Validation")

    render_kpi_grid(
        [
            {"label": "Frozen BPI Formula", "value": "0.42·R + 0.30·W + 0.18·C + 0.10·L", "sub": "0.00 max diff across 200,961 frozen deliveries", "accent": PALETTE["accent_terracotta"], "icon": "book"},
            {"label": "Frozen BoPI Formula", "value": "0.38·D + 0.26·W + 0.24·C + 0.12·L", "sub": "0.00 max diff across 200,961 frozen deliveries", "accent": PALETTE["accent_gold"], "icon": "book"},
            {"label": "Empirical Bayes Shrinkage", "value": "K = 45.0 Balls", "sub": "PAVA_shrunk = [n/(n+45)]*raw_hp + [45/(n+45)]*0.0", "accent": PALETTE["positive"], "icon": "activity"},
            {"label": "Composite Score Scale", "value": "Phi(Z) * 100", "sub": "5-pillar norm-referenced CDF score (NOT win probability)", "accent": PALETTE["accent_burnt_orange"], "icon": "compare"},
        ]
    )

    render_section_header("1. Continuous Pressure Equations & Phase Wicket Values", "Exact equations verified against `src/models/pressure_index.py` & `deliveries_with_pava.parquet`", icon="book")
    c1, c2 = st.columns(2)
    with c1:
        st.latex(r"\text{BPI}_t = \operatorname{clip}\left(0.42\,C_{\text{eff\_rate}} + 0.30\,C_{\text{res}} + 0.18\,C_{\text{climax}} + 0.10\,(B_{\text{ko}} + B_{\text{lev}}),\,0,\,100\right)")
        render_callout(
            "<b>BPI Components:</b><br/>"
            "• <b>Effective Rate Demand:</b> Inn2 <code>sigmoid((clip(RRR,2,24)-8.5)/2.2)*100</code>; Inn1 <code>sigmoid(-runs_above_par/14)*100</code>, scaled by <code>0.5 + 0.5*r</code>.<br/>"
            "• <b>Resource Scarcity:</b> <code>(clip(wickets_lost/9, 0, 1)^1.2) * 100</code> | <b>Climax:</b> <code>(r^1.3)*100</code>.<br/>"
            "• <b>Leverage Bonus:</b> <code>B_ko = 12.0</code> (knockout); <code>B_lev = 15.0</code> (tight chase finale).",
            accent=PALETTE["accent_terracotta"],
        )
    with c2:
        st.latex(r"\text{BoPI}_t = \operatorname{clip}\left(0.38\,C_{\text{defend}} + 0.26\,C_{\text{res\_opp}} + 0.24\,C_{\text{climax}} + 0.12\,(B_{\text{ko}} + B_{\text{tight}}),\,0,\,100\right)")
        render_callout(
            "<b>BoPI &amp; Unamplified Raw PAVA:</b><br/>"
            "• <b>Target Defense:</b> Inn2 <code>sigmoid((10.5-clip(RRR,2,24))/2.2)*100</code>; Inn1 <code>sigmoid(runs_above_par/14)*100</code>.<br/>"
            "• <b>PAVA (Bat):</b> <code>(R_act - E[R]) + V_W(phase)*(P(out) - W_act) + 0.50*(I_bnd - P(bnd))</code>.<br/>"
            "• <b>Phase Wicket Weights V_W:</b> Powerplay <code>5.20</code>, Middle <code>4.50</code>, Death <code>3.60</code> runs.",
            accent=PALETTE["accent_gold"],
        )

    render_section_header("2. Frozen Legacy 120-Ball Model A vs. Dynamic `max_innings_balls` Refinement", "Strict architectural separation protecting immutable rankings", icon="shield")
    reconcile_df = pd.DataFrame(
        [
            {
                "Implementation Variant": "Frozen Model A Baseline (Active Rankings)",
                "Completion Ratio Denominator": "Fixed T20 denominator (120.0 balls; r = (120 - balls_remaining)/120)",
                "Standard 20-Over Deliveries (199,320)": "Exact match (0.00 diff)",
                "Shortened Match Deliveries (1,641 / 23 matches)": "Pre-P0-3 fixed 120.0 denominator preserved",
                "Ranking Outputs Affected": "final_batter_rankings.csv (109), final_bowler_rankings.csv (147) — Frozen & Reproduced (0.00 diff)",
            },
            {
                "Implementation Variant": "P0-3 Dynamic Innings-Length Code (src/models/pressure_index.py)",
                "Completion Ratio Denominator": "Dynamic max_innings_balls (30–120 legal balls allocated)",
                "Standard 20-Over Deliveries (199,320)": "Exact match (0.00 diff)",
                "Shortened Match Deliveries (1,641 / 23 matches)": "Adjusted completion ratio & chase threshold dynamically",
                "Ranking Outputs Affected": "Isolated to research sensitivity; never silently overwrites frozen Model A CSVs",
            },
        ]
    )
    st.dataframe(reconcile_df, width="stretch", hide_index=True)

    render_section_header("3. Chronological ML Calibration & Empirical Bayes Uncertainty", "Out-of-sample LightGBM holdout benchmarks (Train <=2024, Val 2025, Test 2026)", icon="activity")
    c_bm, c_ab = st.columns(2)
    with c_bm:
        bm_df = build_benchmark_rows(bundle.benchmark)
        if not bm_df.empty:
            st.markdown("**Chronological LightGBM Benchmark (`MODEL_BENCHMARK_REPORT.json`)**")
            st.dataframe(bm_df, width="stretch", hide_index=True)
        else:
            render_empty_state("Benchmark JSON unavailable", "Check `docs/MODEL_BENCHMARK_REPORT.json`.")
    with c_ab:
        abl_df = build_ablation_rows(bundle.validation)
        if not abl_df.empty:
            st.markdown("**Five-Pillar Component Ablation (`VALIDATION_REPORT.json`)**")
            st.dataframe(abl_df, width="stretch", hide_index=True)
        else:
            render_empty_state("Validation ablation JSON unavailable", "Check `docs/VALIDATION_REPORT.json`.")

    st.plotly_chart(fig_shrinkage_curve(k_shrink=45.0), width="stretch")
    render_chart_caption("Empirical Bayes shrinkage progression curve (K=45.0 pseudo-deliveries). At n = 45 HP balls, the estimator assigns equal 50% weight to player empirical data and the neutral prior.")

    render_section_header("4. Methodological Exclusions, Small-Sample Sensitivity & Limitations", "Complete research transparency", icon="alert")
    render_callout(
        "• <b>Dataset Exclusions:</b> 16 abandoned zero-ball matches (out of 883 cataloged) excluded; 38 Super Over deliveries excluded from regular-overs Model A training/rankings; `bowl_speed` nulls/zeros (`38.7%`) filtered to `[50, 165]` km/h and excluded from LightGBM inputs.<br/>"
        "• <b>Small-Sample Bootstrap Variance:</b> Qualifiers with 35–83 HP balls or 22–29 matches exhibit wider 95% CIs and higher mean ranks when match resampling omits leverage appearances below the 30-HP threshold.<br/>"
        "• <b>PRC Descriptive Slope Boundary:</b> OLS PRC slopes (`Clutch Climber`, `Ice Cold Anchor`, `Pressure Fragile`) classify statistical delivery trajectories across leverage bands — not psychological traits.<br/>"
        "• <b>Score Scale Clarification:</b> Composite `0–100` Reliability Score (`Phi(Z_composite)*100`) is a norm-referenced percentile score, NOT a probability of match success.",
        accent=PALETTE["accent_terracotta"],
    )


def render_provenance(bundle: DashboardDataBundle) -> None:
    """Page 10: Data Sources, Checksums, Missingness & Market Changelog."""
    st.title("Data Sources & Provenance")

    integrity = bundle.integrity_status
    bat_ok = integrity.get("batter_frozen_match", False)
    bowl_ok = integrity.get("bowler_frozen_match", False)
    zip_ok = integrity.get("archive_zip_match")

    render_kpi_grid(
        [
            {"label": "Dashboard Version", "value": PRODUCT_VERSION, "sub": "Read-only presentation shell over frozen Model A artifacts", "accent": PALETTE["accent_terracotta"], "icon": "shield"},
            {"label": "Frozen Batters SHA-256", "value": "VERIFIED" if bat_ok else "MISMATCH", "sub": str(integrity.get("batter_csv_sha256", ""))[:22] + "…", "accent": PALETTE["positive"] if bat_ok else PALETTE["danger"], "icon": "check" if bat_ok else "alert"},
            {"label": "Frozen Bowlers SHA-256", "value": "VERIFIED" if bowl_ok else "MISMATCH", "sub": str(integrity.get("bowler_csv_sha256", ""))[:22] + "…", "accent": PALETTE["positive"] if bowl_ok else PALETTE["danger"], "icon": "check" if bowl_ok else "alert"},
            {"label": "Market Snapshot Anchor", "value": SNAPSHOT_ANCHOR_DATE, "sub": f"Next official BCCI filing: {RETENTION_DEADLINE_DATE}", "accent": PALETTE["accent_gold"], "icon": "database"},
        ]
    )

    snap_expected = FROZEN_MARKET_SNAPSHOT_SHA256
    snap_observed = str(integrity.get("market_snapshot_sha256", "MISSING"))
    if snap_observed == "MISSING" or not snap_observed:
        snap_status = "MISSING"
    elif snap_observed == snap_expected:
        snap_status = "EXACT MATCH"
    else:
        snap_status = "MISMATCH"

    render_section_header("Cryptographic Checksum & Artifact Lineage Registry", "Verified at runtime against immutable SHA-256 expectations", icon="shield")
    prov_rows = pd.DataFrame(
        [
            {"Artifact": "Frozen Official Batters CSV (`final_batter_rankings.csv`)", "Expected SHA-256": FROZEN_BATTER_SHA256, "Observed SHA-256": integrity.get("batter_csv_sha256", "MISSING"), "Status": "EXACT MATCH" if bat_ok else "MISMATCH"},
            {"Artifact": "Frozen Official Bowlers CSV (`final_bowler_rankings.csv`)", "Expected SHA-256": FROZEN_BOWLER_SHA256, "Observed SHA-256": integrity.get("bowler_csv_sha256", "MISSING"), "Status": "EXACT MATCH" if bowl_ok else "MISMATCH"},
            {"Artifact": "Original Submission Archive (`PRESSUREIQ_Final_Submission.zip`)", "Expected SHA-256": FROZEN_ARCHIVE_ZIP_SHA256, "Observed SHA-256": integrity.get("archive_zip_sha256", "NOT_PRESENT"), "Status": "EXACT MATCH" if zip_ok else ("NOT PRESENT" if zip_ok is None else "MISMATCH")},
            {"Artifact": "Pinned Market Snapshot (`ipl_2027_market_snapshot_2026-11-11.csv`)", "Expected SHA-256": snap_expected, "Observed SHA-256": snap_observed, "Status": snap_status},
        ]
    )
    st.dataframe(prov_rows, width="stretch", hide_index=True)

    render_section_header("Dataset Inventory & Transformation History", "Chronological data flow from official competition data pack", icon="database")
    inv_df = pd.DataFrame(
        [
            {"Dataset Layer": "Official Competition Data Pack (6 Raw CSVs)", "Coverage": "883 scheduled matches | 200,999 deliveries | IPL (2022–2026) + 470 T20Is + 30 Dev T20s", "Source": "Rajasthan Royals SupeRR Selector Season 2 Data Pack", "Mutability": "Strictly Read-Only (Never Deployed)"},
            {"Dataset Layer": "Cleaned & Reconstructed Deliveries (`deliveries.parquet`)", "Coverage": "200,999 deliveries | 867 played matches (16 zero-ball rain abandonments excluded)", "Source": "src/data/cleaner.py & state_reconstruction.py", "Mutability": "Derived Parquet"},
            {"Dataset Layer": "Model A Expectations & PAVA (`deliveries_with_pava.parquet`)", "Coverage": "200,961 regular-over balls (38 Super Over balls separated) | LightGBM OOF", "Source": "LightGBM Chronological Walk-Forward + Legacy 120-ball BPI/BoPI", "Mutability": "Model A Foundation"},
            {"Dataset Layer": "Frozen Rankings (`final_batter_rankings.csv` / `final_bowler_rankings.csv`)", "Coverage": "109 Qualified Batters | 147 Qualified Bowlers | N=2,000 Match Bootstrap", "Source": "src/analysis/reliability_engine.py & bootstrap_engine.py", "Mutability": "Frozen Competition Baseline"},
            {"Dataset Layer": "Audited IPL 2027 Market Ledger (`ipl_2027_player_market_template.csv`)", "Coverage": "17 tracked elite players | 256 RR candidate profiles", "Source": "Verified Publisher URLs (HTTP 200 checked 2026-11-12)", "Mutability": "Isolated Market Layer"},
        ]
    )
    st.dataframe(inv_df, width="stretch", hide_index=True)

    if bundle.missingness_df is not None and not bundle.missingness_df.empty:
        render_section_header("Observed Telemetry Missingness & Exclusions Audit", "Exact DuckDB row counts across 200,961 regular deliveries", icon="alert")
        st.dataframe(bundle.missingness_df, width="stretch", hide_index=True)

    if not bundle.market_current.empty and {"source_url", "publisher", "source_publication_date", "verification_timestamp"}.issubset(bundle.market_current.columns):
        render_section_header("Verified External Market Sources", "Deduplicated publisher references checked via HTTP 200 on 2026-11-12", icon="briefcase")
        src_tbl = (
            bundle.market_current[["publisher", "source_title", "source_publication_date", "verification_timestamp", "confidence_classification", "source_url"]]
            .drop_duplicates(subset=["source_url"])
            .sort_values("source_publication_date", ascending=False)
        )
        st.dataframe(
            src_tbl,
            width="stretch",
            hide_index=True,
            column_config={"source_url": st.column_config.LinkColumn("Source URL")},
        )

    render_section_header("Market Update & Audit History (`ipl_2027_market_change_log.csv`)", "Append-only provenance trail including Jos Buttler timestamp correction", icon="book")
    if not bundle.market_changelog.empty:
        st.dataframe(
            bundle.market_changelog,
            width="stretch",
            hide_index=True,
            column_config={"source_url": st.column_config.LinkColumn("Source URL")},
        )
    else:
        render_empty_state("No market change log rows available", "Check `data/processed/ipl_2027_market_change_log.csv`.")

