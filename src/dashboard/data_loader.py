"""Fault-tolerant, Streamlit-independent data access and DuckDB query layer for PRESSUREIQ."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
PROCESSED_DATA_DIR = ROOT / "data" / "processed"
SNAPSHOTS_DIR = PROCESSED_DATA_DIR / "snapshots"
DOCS_DIR = ROOT / "docs"

BATTER_RANKINGS_PATH = PROCESSED_DATA_DIR / "final_batter_rankings.csv"
BOWLER_RANKINGS_PATH = PROCESSED_DATA_DIR / "final_bowler_rankings.csv"
BOOT_BAT_PATH = PROCESSED_DATA_DIR / "bootstrap_2000_batters.parquet"
BOOT_BOWL_PATH = PROCESSED_DATA_DIR / "bootstrap_2000_bowlers.parquet"
DELIVERIES_PAVA_PATH = PROCESSED_DATA_DIR / "deliveries_with_pava.parquet"
INN_PAVA_PATH = PROCESSED_DATA_DIR / "batter_innings_pava.parquet"
SPELL_PAVA_PATH = PROCESSED_DATA_DIR / "bowler_spell_pava.parquet"
MATCHES_PATH = PROCESSED_DATA_DIR / "matches.parquet"
PLAYERS_PATH = PROCESSED_DATA_DIR / "players.parquet"
TEAMS_PATH = PROCESSED_DATA_DIR / "teams.parquet"
RR_CANDIDATES_PATH = PROCESSED_DATA_DIR / "rr_2027_candidate_rankings.csv"
RR_BATTER_TOP10_PATH = PROCESSED_DATA_DIR / "rr_2027_batter_top10.csv"
RR_BOWLER_TOP10_PATH = PROCESSED_DATA_DIR / "rr_2027_bowler_top10.csv"
ELIGIBILITY_AUDIT_PATH = PROCESSED_DATA_DIR / "player_eligibility_audit.csv"
EMERGING_TALENT_PATH = PROCESSED_DATA_DIR / "emerging_talent_watchlist.csv"
MARKET_SNAPSHOT_NOV11_PATH = SNAPSHOTS_DIR / "ipl_2027_market_snapshot_2026-11-11.csv"
MARKET_CURRENT_PATH = PROCESSED_DATA_DIR / "ipl_2027_player_market_template.csv"
MARKET_CHANGELOG_PATH = PROCESSED_DATA_DIR / "ipl_2027_market_change_log.csv"
BENCHMARK_PATH = DOCS_DIR / "MODEL_BENCHMARK_REPORT.json"
VALIDATION_PATH = DOCS_DIR / "VALIDATION_REPORT.json"
PROVENANCE_PATH = DOCS_DIR / "PROVENANCE.json"
PHASE2_MANIFEST_PATH = PROCESSED_DATA_DIR / "phase2_verification_manifest.json"

FROZEN_BATTER_SHA256 = "887f0c104047eb7b5c7d662b83600bacaf6263fa7162fc343b27800760b99b87"
FROZEN_BOWLER_SHA256 = "344d63c55cecc7bce9de3cd06d82b6ac8217fcd448bb3f2e93d55da314f1e7bb"


def _read_csv_safe(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except (OSError, ValueError, pd.errors.EmptyDataError, pd.errors.ParserError):
        return pd.DataFrame()


def _read_parquet_safe(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_parquet(path)
    except (OSError, ValueError):
        return pd.DataFrame()


def _read_json_safe(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            return data if isinstance(data, dict) else {}
    except (OSError, ValueError, json.JSONDecodeError):
        return {}


def _clean_market_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing non-status metadata cleanly while keeping status nulls distinct."""
    if df.empty:
        return df
    out = df.copy()
    for col in out.columns:
        if col == "official_retention_status":
            out[col] = out[col].fillna("Pending Verification").astype(str)
        elif out[col].dtype == object:
            out[col] = out[col].fillna("")
    return out


def compute_file_sha256(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    h = hashlib.sha256()
    with open(path, "rb") as fp:
        for chunk in iter(lambda: fp.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _merge_bootstrap_details(rankings_df: pd.DataFrame, boot_df: pd.DataFrame) -> pd.DataFrame:
    if rankings_df.empty:
        return rankings_df
    df = rankings_df.copy()
    if not boot_df.empty and "boot_median_rank" in boot_df.columns and "boot_median_rank" not in df.columns:
        extra_cols = ["player_id", "boot_median_rank"]
        if "boot_se_score" in boot_df.columns:
            extra_cols.append("boot_se_score")
        df = df.merge(boot_df[extra_cols].drop_duplicates(subset=["player_id"]), on="player_id", how="left")
    if "boot_median_rank" not in df.columns:
        df["boot_median_rank"] = df.get("boot_mean_rank", pd.Series(dtype=float))
    return df


def _attach_player_teams(rankings_df: pd.DataFrame, players_df: pd.DataFrame) -> pd.DataFrame:
    """Attach mapped teams string and latest IPL team cleanly from players.parquet."""
    if rankings_df.empty:
        return rankings_df
    df = rankings_df.copy()
    if players_df.empty:
        df["teams_list"] = ""
        return df

    ipl_franchises = (
        "Rajasthan Royals", "Chennai Super Kings", "Mumbai Indians", "Kolkata Knight Riders",
        "Royal Challengers Bengaluru", "Delhi Capitals", "Punjab Kings", "Sunrisers Hyderabad",
        "Gujarat Titans", "Lucknow Super Giants",
    )
    grouped = (
        players_df.groupby("player_id")["team_name"]
        .apply(lambda s: list(dict.fromkeys([str(v) for v in s if pd.notna(v)])))
        .to_dict()
    )

    def _fmt_teams(pid: int) -> str:
        return ", ".join(grouped.get(pid, []))

    def _latest_ipl(pid: int) -> str:
        t = grouped.get(pid, [])
        ipl = [x for x in t if any(f in x for f in ipl_franchises)]
        return ipl[-1] if ipl else "International / Non-IPL"

    df["teams_list"] = df["player_id"].map(_fmt_teams)
    if "dataset_ipl_team" not in df.columns:
        df["dataset_ipl_team"] = df["player_id"].map(_latest_ipl)
    return df


def query_match_cluster_ess(pava_path: Path = DELIVERIES_PAVA_PATH, is_batting: bool = True) -> pd.DataFrame:
    """Compute per-player Kish Effective Sample Size across match clusters via parameterized DuckDB."""
    if not pava_path.exists():
        return pd.DataFrame(columns=["player_id", "kish_match_ess", "hp_matches_played"])

    id_col = "striker_id" if is_batting else "bowler_id"
    p_col = "bpi" if is_batting else "bopi"
    ball_filter = "is_batter_ball = 1" if is_batting else "is_legal_ball = 1"
    p_str = str(pava_path.resolve())

    sql = f"""
    WITH per_match AS (
        SELECT
            {id_col} AS player_id,
            match_id,
            COUNT(*) AS hp_balls_in_match
        FROM read_parquet(?)
        WHERE {ball_filter} AND {p_col} >= 50.0
        GROUP BY {id_col}, match_id
    )
    SELECT
        player_id,
        COUNT(*) AS hp_matches_played,
        ROUND(POWER(SUM(hp_balls_in_match), 2) / NULLIF(SUM(POWER(hp_balls_in_match, 2)), 0), 2) AS kish_match_ess
    FROM per_match
    GROUP BY player_id
    """
    con = duckdb.connect()
    try:
        return con.execute(sql, [p_str]).df()
    finally:
        con.close()


def query_season_format_stats(
    is_batting: bool = True,
    season: Optional[int] = None,
    comp_category: Optional[str] = None,
    pava_path: Path = DELIVERIES_PAVA_PATH,
    matches_path: Path = MATCHES_PATH,
) -> pd.DataFrame:
    """Query exact empirical delivery-level stats filtered by season and/or format via DuckDB."""
    if not pava_path.exists() or not matches_path.exists():
        return pd.DataFrame()

    p_str = str(pava_path.resolve())
    m_str = str(matches_path.resolve())
    id_col = "striker_id" if is_batting else "bowler_id"
    p_col = "bpi" if is_batting else "bopi"
    raw_col = "raw_bat_value" if is_batting else "raw_bowl_value"
    ball_filter = "d.is_batter_ball = 1" if is_batting else "d.is_legal_ball = 1"

    clauses = [ball_filter]
    params: List[Any] = [p_str, m_str]
    if season is not None:
        clauses.append("EXTRACT(YEAR FROM TRY_CAST(m.match_date AS TIMESTAMP)) = ?")
        params.append(int(season))
    if comp_category and comp_category != "All Formats":
        clauses.append("d.comp_category = ?")
        params.append(str(comp_category))

    where_sql = " AND ".join(clauses)
    metric_sql = (
        "ROUND(SUM(d.batter_runs) * 100.0 / NULLIF(COUNT(*), 0), 1) AS slice_rate_stat"
        if is_batting
        else "ROUND(SUM(d.bowler_runs_conceded) * 6.0 / NULLIF(COUNT(*), 0), 2) AS slice_rate_stat"
    )

    sql = f"""
    SELECT
        d.{id_col} AS player_id,
        COUNT(DISTINCT d.match_id) AS slice_matches,
        COUNT(*) AS slice_balls,
        SUM(CASE WHEN d.{p_col} >= 50.0 THEN 1 ELSE 0 END) AS slice_hp_balls,
        {metric_sql},
        ROUND(AVG(CASE WHEN d.{p_col} >= 50.0 THEN d.{raw_col} ELSE NULL END), 4) AS slice_hp_raw_pava
    FROM read_parquet(?) d
    JOIN read_parquet(?) m ON d.match_id = m.match_id
    WHERE {where_sql}
    GROUP BY d.{id_col}
    """
    con = duckdb.connect()
    try:
        return con.execute(sql, params).df()
    finally:
        con.close()


def query_player_deliveries(
    player_id: int,
    is_batting: bool = True,
    pava_path: Path = DELIVERIES_PAVA_PATH,
) -> pd.DataFrame:
    """Load delivery-level PAVA records for a single player using DuckDB predicate pushdown."""
    if not pava_path.exists():
        return pd.DataFrame()

    p_str = str(pava_path.resolve())
    id_col = "striker_id" if is_batting else "bowler_id"
    cols = (
        "match_id, innings, match_date, comp_category, phase, runs, batter_runs, "
        "is_batter_ball, is_legal_ball, is_boundary, is_wicket, is_bowler_wicket, "
        "bowler_runs_conceded, bpi, bopi, raw_bat_value, raw_bowl_value, pava_bat, pava_bowl"
    )
    sql = f"SELECT {cols} FROM read_parquet(?) WHERE {id_col} = ?"
    con = duckdb.connect()
    try:
        return con.execute(sql, [p_str, int(player_id)]).df()
    finally:
        con.close()


def query_player_match_contributions(
    player_id: int,
    is_batting: bool = True,
    inn_path: Path = INN_PAVA_PATH,
    spell_path: Path = SPELL_PAVA_PATH,
    matches_path: Path = MATCHES_PATH,
) -> pd.DataFrame:
    """Load per-match innings or spell PAVA summaries enriched with match date and teams."""
    target_path = inn_path if is_batting else spell_path
    if not target_path.exists():
        return pd.DataFrame()
    t_str = str(target_path.resolve())
    id_col = "striker_id" if is_batting else "bowler_id"
    con = duckdb.connect()
    try:
        if matches_path.exists():
            m_str = str(matches_path.resolve())
            sql = f"""
            SELECT p.*, m.match_date, m.home_team, m.away_team, m.stage
            FROM read_parquet(?) p
            LEFT JOIN read_parquet(?) m ON p.match_id = m.match_id
            WHERE p.{id_col} = ?
            ORDER BY m.match_date DESC
            """
            return con.execute(sql, [t_str, m_str, int(player_id)]).df()
        sql = f"SELECT * FROM read_parquet(?) WHERE {id_col} = ?"
        return con.execute(sql, [t_str, int(player_id)]).df()
    finally:
        con.close()


def query_unestablished_profiles(
    is_batting: bool = True,
    pava_path: Path = DELIVERIES_PAVA_PATH,
) -> pd.DataFrame:
    """Query empirical delivery profiles for players below official Model A thresholds."""
    if not pava_path.exists():
        return pd.DataFrame()
    p_str = str(pava_path.resolve())
    id_col = "striker_id" if is_batting else "bowler_id"
    name_col = "striker_name" if is_batting else "bowler_name"
    p_col = "bpi" if is_batting else "bopi"
    raw_col = "raw_bat_value" if is_batting else "raw_bowl_value"
    ball_filter = "is_batter_ball = 1" if is_batting else "is_legal_ball = 1"

    sql = f"""
    SELECT
        {id_col} AS player_id,
        ANY_VALUE({name_col}) AS player_name,
        COUNT(DISTINCT match_id) AS matches,
        COUNT(*) AS balls,
        SUM(CASE WHEN {p_col} >= 50.0 THEN 1 ELSE 0 END) AS hp_balls,
        ROUND(AVG(CASE WHEN {p_col} >= 50.0 THEN {raw_col} ELSE NULL END), 4) AS hp_raw_pava,
        ROUND(AVG(CASE WHEN phase = 'Powerplay' THEN {raw_col} ELSE NULL END), 4) AS pp_raw_pava,
        ROUND(AVG(CASE WHEN phase = 'Middle' THEN {raw_col} ELSE NULL END), 4) AS mid_raw_pava,
        ROUND(AVG(CASE WHEN phase = 'Death' THEN {raw_col} ELSE NULL END), 4) AS death_raw_pava
    FROM read_parquet(?)
    WHERE {ball_filter}
    GROUP BY {id_col}
    HAVING COUNT(*) >= 30 AND (COUNT(*) < 400 OR SUM(CASE WHEN {p_col} >= 50.0 THEN 1 ELSE 0 END) < 30 OR COUNT(DISTINCT match_id) < 20)
    ORDER BY hp_balls DESC, balls DESC
    LIMIT 60
    """
    con = duckdb.connect()
    try:
        return con.execute(sql, [p_str]).df()
    finally:
        con.close()


def query_cohort_phase_summary(pava_path: Path = DELIVERIES_PAVA_PATH) -> pd.DataFrame:
    """Aggregate league-wide phase pressure and PAVA statistics via parameterized DuckDB."""
    if not pava_path.exists():
        return pd.DataFrame()
    p_str = str(pava_path.resolve())
    sql = """
    SELECT
        phase,
        COUNT(*) AS deliveries,
        ROUND(AVG(bpi), 2) AS mean_bpi,
        ROUND(AVG(bopi), 2) AS mean_bopi,
        ROUND(AVG(raw_bat_value), 4) AS mean_raw_bat_pava,
        ROUND(AVG(raw_bowl_value), 4) AS mean_raw_bowl_pava
    FROM read_parquet(?)
    GROUP BY phase
    """
    con = duckdb.connect()
    try:
        return con.execute(sql, [p_str]).df()
    finally:
        con.close()


@dataclass
class DashboardDataBundle:
    bat_df: pd.DataFrame
    bowl_df: pd.DataFrame
    matches_df: pd.DataFrame
    players_df: pd.DataFrame
    emerging_df: pd.DataFrame
    market_snapshot_nov11: pd.DataFrame
    market_current: pd.DataFrame
    market_changelog: pd.DataFrame
    rr_candidates_df: pd.DataFrame
    eligibility_audit_df: pd.DataFrame
    phase_cohort_df: pd.DataFrame
    benchmark: Dict[str, Any]
    validation: Dict[str, Any]
    provenance: Dict[str, Any]
    phase2_manifest: Dict[str, Any]
    integrity_status: Dict[str, Any]


def load_dashboard_bundle_uncached() -> DashboardDataBundle:
    """Pure, uncached loader usable in both Streamlit and headless unit tests."""
    bat_raw = _read_csv_safe(BATTER_RANKINGS_PATH)
    bowl_raw = _read_csv_safe(BOWLER_RANKINGS_PATH)
    boot_bat = _read_parquet_safe(BOOT_BAT_PATH)
    boot_bowl = _read_parquet_safe(BOOT_BOWL_PATH)
    players_df = _read_parquet_safe(PLAYERS_PATH)
    matches_df = _read_parquet_safe(MATCHES_PATH)

    bat_df = _merge_bootstrap_details(bat_raw, boot_bat)
    bowl_df = _merge_bootstrap_details(bowl_raw, boot_bowl)
    bat_df = _attach_player_teams(bat_df, players_df)
    bowl_df = _attach_player_teams(bowl_df, players_df)

    bat_ess = query_match_cluster_ess(DELIVERIES_PAVA_PATH, is_batting=True)
    bowl_ess = query_match_cluster_ess(DELIVERIES_PAVA_PATH, is_batting=False)
    if not bat_df.empty and not bat_ess.empty:
        bat_df = bat_df.merge(bat_ess, on="player_id", how="left")
    if not bowl_df.empty and not bowl_ess.empty:
        bowl_df = bowl_df.merge(bowl_ess, on="player_id", how="left")

    bat_sha = compute_file_sha256(BATTER_RANKINGS_PATH)
    bowl_sha = compute_file_sha256(BOWLER_RANKINGS_PATH)

    market_snap = _clean_market_frame(_read_csv_safe(MARKET_SNAPSHOT_NOV11_PATH))
    market_curr = _clean_market_frame(_read_csv_safe(MARKET_CURRENT_PATH))
    if market_snap.empty and not market_curr.empty:
        market_snap = market_curr.copy()

    return DashboardDataBundle(
        bat_df=bat_df,
        bowl_df=bowl_df,
        matches_df=matches_df,
        players_df=players_df,
        emerging_df=_read_csv_safe(EMERGING_TALENT_PATH),
        market_snapshot_nov11=market_snap,
        market_current=market_curr,
        market_changelog=_read_csv_safe(MARKET_CHANGELOG_PATH),
        rr_candidates_df=_read_csv_safe(RR_CANDIDATES_PATH),
        eligibility_audit_df=_read_csv_safe(ELIGIBILITY_AUDIT_PATH),
        phase_cohort_df=query_cohort_phase_summary(DELIVERIES_PAVA_PATH),
        benchmark=_read_json_safe(BENCHMARK_PATH),
        validation=_read_json_safe(VALIDATION_PATH),
        provenance=_read_json_safe(PROVENANCE_PATH),
        phase2_manifest=_read_json_safe(PHASE2_MANIFEST_PATH),
        integrity_status={
            "batter_csv_sha256": bat_sha,
            "bowler_csv_sha256": bowl_sha,
            "batter_frozen_match": bat_sha == FROZEN_BATTER_SHA256,
            "bowler_frozen_match": bowl_sha == FROZEN_BOWLER_SHA256,
        },
    )
