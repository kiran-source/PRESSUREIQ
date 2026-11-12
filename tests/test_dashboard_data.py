"""Unit tests for modular dashboard data loading, analytics, charts, and market safeguards."""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from src.dashboard.data_loader import (
    FROZEN_BATTER_SHA256,
    FROZEN_BOWLER_SHA256,
    _read_csv_safe,
    _read_json_safe,
    _read_parquet_safe,
    load_dashboard_bundle_uncached,
    query_player_deliveries,
    query_season_format_stats,
    query_unestablished_profiles,
)
from src.dashboard.analytics import (
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
    sanitize_availability_label,
    summarize_market_counts,
    summarize_rr_squad_intelligence,
)
from src.dashboard.charts import (
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


def test_dashboard_bundle_loads_and_preserves_frozen_hashes():
    bundle = load_dashboard_bundle_uncached()
    assert len(bundle.bat_df) == 109
    assert len(bundle.bowl_df) == 147
    assert bundle.integrity_status["batter_csv_sha256"] == FROZEN_BATTER_SHA256
    assert bundle.integrity_status["bowler_csv_sha256"] == FROZEN_BOWLER_SHA256
    assert bundle.integrity_status["batter_frozen_match"] is True
    assert bundle.integrity_status["bowler_frozen_match"] is True
    assert "boot_median_rank" in bundle.bat_df.columns
    assert "kish_match_ess" in bundle.bat_df.columns


def test_effective_sample_distinguished_from_raw_opportunities():
    bundle = load_dashboard_bundle_uncached()
    bat_tbl = prepare_leaderboard_table(bundle.bat_df, is_batting=True)
    bowl_tbl = prepare_leaderboard_table(bundle.bowl_df, is_batting=False)

    assert bat_tbl.iloc[0]["player_name"] == "Ruturaj Gaikwad"
    assert bat_tbl.iloc[0]["rank"] == 1
    assert bowl_tbl.iloc[0]["player_name"] == "Liam Dawson"
    assert bowl_tbl.iloc[0]["rank"] == 1

    assert (bat_tbl["eb_effective_hp_balls"] < bat_tbl["hp_balls"]).all()
    assert (bowl_tbl["eb_effective_hp_balls"] < bowl_tbl["hp_balls"]).all()
    assert bat_tbl["kish_match_ess"].notna().all()


def test_filters_preserve_official_rank_without_mutation():
    bundle = load_dashboard_bundle_uncached()
    bat_tbl = prepare_leaderboard_table(bundle.bat_df, is_batting=True)
    filtered = filter_leaderboard(bat_tbl, roles=["Middle_Order"], min_hp_balls=100, search_query="Suryakumar")
    assert len(filtered) == 1
    assert filtered.iloc[0]["player_name"] == "Suryakumar Yadav"
    assert filtered.iloc[0]["rank"] == 4
    assert len(extract_unique_teams(bat_tbl)) > 0


def test_duckdb_season_slice_and_unestablished_queries():
    s2025 = query_season_format_stats(is_batting=True, season=2025, comp_category="IPL")
    assert not s2025.empty
    assert {"player_id", "slice_matches", "slice_balls", "slice_hp_balls"}.issubset(s2025.columns)

    unest = query_unestablished_profiles(is_batting=True)
    assert not unest.empty
    assert ((unest["balls"] < 400) | (unest["hp_balls"] < 30) | (unest["matches"] < 20)).all()


def test_market_safeguards_and_nov5_trade_counterparties():
    # Case-insensitive & NaN checks
    for bad_txt in ("Confirmed Available", "confirmed available", "officially released", "Released for Auction", None, float("nan")):
        for bad_stat in ("Pending Verification", "Rumour", "Policy/Eligibility Review", "Confirmed Trade"):
            out = sanitize_availability_label(bad_stat, bad_txt)
            assert "confirmed available" not in out.lower()
            assert "officially released" not in out.lower()

    bundle = load_dashboard_bundle_uncached()
    counts = summarize_market_counts(bundle.market_snapshot_nov11)
    assert counts["Confirmed Trade"] == 1
    assert counts["Pending Verification"] == 15
    assert counts["Policy/Eligibility Review"] == 1
    assert counts["Confirmed Released"] == 0

    disp = prepare_market_display(bundle.market_snapshot_nov11)
    assert not disp.empty
    assert (disp["official_release_status"] != "Confirmed Available").all()

    rr_info = summarize_rr_squad_intelligence(bundle.eligibility_audit_df, bundle.rr_candidates_df)
    assert not rr_info["rr_core"].empty
    assert "Jos Buttler" not in rr_info["rr_core"]["player_name"].values
    assert not rr_info["targets"]["market_verified_available"].any()

    # Check Liam Livingstone (CSK) & Khaleel Ahmed (SRH) Nov 5 trade counterparties are Class C Confirmed Trade
    cand = bundle.rr_candidates_df
    liv = cand[cand["player_name"] == "Liam Livingstone"]
    kha = cand[cand["player_name"] == "Khaleel Ahmed"]
    assert not liv.empty and (liv["eligibility_class"] == "C").all() and (liv["latest_ipl_franchise"] == "Chennai Super Kings").all()
    assert not kha.empty and (kha["eligibility_class"] == "C").all() and (kha["latest_ipl_franchise"] == "Sunrisers Hyderabad").all()


def test_missing_file_and_edge_case_resilience(tmp_path):
    assert _read_csv_safe(tmp_path / "missing.csv").empty
    assert _read_parquet_safe(tmp_path / "missing.parquet").empty
    assert _read_json_safe(tmp_path / "missing.json") == {}

    corrupt = tmp_path / "bad.json"
    corrupt.write_text("{not-json", encoding="utf-8")
    assert _read_json_safe(corrupt) == {}

    # Empty DataFrame chart safety (never raise KeyError: 'rank')
    empty_df = pd.DataFrame()
    assert len(fig_top10_ci_bar(empty_df, "Empty").data) == 0
    assert len(fig_rank_uncertainty_intervals(empty_df, top_n=10).data) == 0
    assert len(fig_score_distribution(empty_df, "Empty").data) == 0
    assert len(fig_sample_vs_score(empty_df).data) == 0

    # Missing player_id and NaN pillar robustness
    sel, means, r_rank, r_cnt = compute_peer_comparison(empty_df, 999999, "role")
    assert sel.empty and means == {} and r_rank == 0 and r_cnt == 0

    nan_row = pd.Series({"shrunk_hp_pava_per_ball": np.nan, "retention_delta": np.nan, "consistency_score": np.nan})
    pillars = compute_player_five_pillars(nan_row)
    assert all(isinstance(v, float) and np.isfinite(v) for v in pillars.values())


def test_charts_and_player_intelligence_render_cleanly():
    bundle = load_dashboard_bundle_uncached()
    bat_tbl = prepare_leaderboard_table(bundle.bat_df, is_batting=True)
    sel, peer_means, role_rank, role_count = compute_peer_comparison(bat_tbl, 6059, "role")
    assert sel["player_name"] == "Ruturaj Gaikwad"
    assert role_rank >= 1 and role_count >= 1
    assert len(compute_player_five_pillars(sel)) == 5

    delivs = query_player_deliveries(6059, is_batting=True)
    phase_df = compute_player_phase_summary(delivs, is_batting=True)
    assert not phase_df.empty

    # Verify Ruturaj Gaikwad's PRC chart has zero '+nan' labels on empty extreme/high tiers
    prc_fig = fig_pressure_response_curve(delivs, "Ruturaj Gaikwad", is_batting=True)
    for txt in prc_fig.data[0].text:
        assert "nan" not in str(txt).lower()

    assert not build_benchmark_rows(bundle.benchmark).empty
    assert not build_ablation_rows(bundle.validation).empty
    assert "audited_market_status" in enrich_emerging_watchlist(bundle.emerging_df, bundle.market_snapshot_nov11).columns

    rr_info = summarize_rr_squad_intelligence(bundle.eligibility_audit_df, bundle.rr_candidates_df)
    figs = [
        fig_top10_ci_bar(bat_tbl, "Top 10"),
        fig_score_distribution(bat_tbl, "Dist"),
        fig_sample_vs_score(bat_tbl, is_batting=True),
        fig_rank_uncertainty_intervals(bat_tbl, top_n=10),
        prc_fig,
        fig_phase_performance(phase_df, "Ruturaj Gaikwad", is_batting=True),
        fig_five_pillar_radar(sel, peer_means, "Ruturaj Gaikwad", "Top_Order"),
        fig_batter_vs_bowler_comparison(bundle.bat_df, bundle.bowl_df),
        fig_rr_role_depth(rr_info["role_depth"]),
    ]
    for f in figs:
        assert len(f.data) > 0


def test_bowler_economy_includes_illegal_delivery_runs():
    """Verify Pathirana (8661) phase and slice economy includes wide/no-ball runs (MCC parity)."""
    delivs = query_player_deliveries(8661, is_batting=False)
    phase_df = compute_player_phase_summary(delivs, is_batting=False)
    assert not phase_df.empty
    total_legal_balls = int(phase_df["Legal Balls"].sum())
    total_runs_conceded = int(phase_df["Runs Conceded"].sum())
    assert total_legal_balls == 1132
    assert total_runs_conceded == 1630
    assert round(total_runs_conceded * 6.0 / total_legal_balls, 2) == 8.64

    slice_df = query_season_format_stats(is_batting=False)
    pat_row = slice_df[slice_df["player_id"] == 8661].iloc[0]
    assert int(pat_row["slice_balls"]) == 1132
    assert float(pat_row["slice_rate_stat"]) == 8.64


def test_rr_core_visible_when_candidates_empty():
    """Verify summarize_rr_squad_intelligence keeps rr_core & role_depth when candidates_df is empty."""
    bundle = load_dashboard_bundle_uncached()
    out = summarize_rr_squad_intelligence(bundle.eligibility_audit_df, pd.DataFrame())
    assert not out["rr_core"].empty
    assert not out["role_depth"].empty
    assert out["targets"].empty


def test_v3_teams_comparison_pressure_analytics_and_charts():
    """Verify v3 10-team overview, multi-player comparison, DuckDB pressure summary & new charts."""
    from src.dashboard.analytics import build_all_ipl_teams_overview, build_multi_player_comparison
    from src.dashboard.charts import (
        fig_bpi_bopi_distribution,
        fig_emerging_opportunity_matrix,
        fig_expected_vs_observed_tiers,
        fig_market_team_matrix,
        fig_multi_player_ci_bars,
        fig_multi_player_prc_overlay,
        fig_multi_player_radar,
        fig_player_expected_vs_observed,
        fig_shrinkage_curve,
    )

    bundle = load_dashboard_bundle_uncached()
    teams_df = build_all_ipl_teams_overview(
        bundle.players_df,
        bundle.market_current,
        bundle.bat_df,
        bundle.bowl_df,
        bundle.rr_candidates_df,
    )
    assert len(teams_df) == 10
    srh_row = teams_df[teams_df["Code"] == "SRH"].iloc[0]
    assert srh_row["Confirmed Trades In"] == 1

    cmp_bat = build_multi_player_comparison(bundle.bat_df.head(3), is_batting=True)
    cmp_bowl = build_multi_player_comparison(bundle.bowl_df.head(2), is_batting=False)
    assert len(cmp_bat) == 3 and "Career SR" in cmp_bat.columns
    assert len(cmp_bowl) == 2 and "Career Economy" in cmp_bowl.columns

    ps = bundle.pressure_summary or {}
    assert not ps["hist"].empty
    assert not ps["tiers"].empty
    assert bundle.missingness_df is not None and not bundle.missingness_df.empty

    p1 = query_player_deliveries(int(bundle.bat_df.iloc[0]["player_id"]), is_batting=True)
    p2 = query_player_deliveries(int(bundle.bat_df.iloc[3]["player_id"]), is_batting=True)
    new_figs = [
        fig_player_expected_vs_observed(p1, str(bundle.bat_df.iloc[0]["player_name"]), is_batting=True),
        fig_multi_player_radar(bundle.bat_df.head(3)),
        fig_multi_player_ci_bars(bundle.bat_df.head(3)),
        fig_multi_player_prc_overlay({str(bundle.bat_df.iloc[0]["player_name"]): p1, str(bundle.bat_df.iloc[3]["player_name"]): p2}, is_batting=True),
        fig_bpi_bopi_distribution(ps["hist"]),
        fig_expected_vs_observed_tiers(ps["tiers"]),
        fig_shrinkage_curve(45.0),
        fig_emerging_opportunity_matrix(bundle.emerging_df),
        fig_market_team_matrix(teams_df),
    ]
    for f in new_figs:
        assert len(f.data) > 0


