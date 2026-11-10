"""End-to-end data processing and Parquet generation pipeline for PRESSUREIQ."""

import os
import sys
import logging
import json
from pathlib import Path
import duckdb
import pandas as pd

from src.config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    DOCS_DIR,
    COMPETITIONS_PARQUET,
    TEAMS_PARQUET,
    PLAYERS_PARQUET,
    PLAYING_XI_PARQUET,
    MATCHES_PARQUET,
    DELIVERIES_PARQUET
)
from src.data.cleaner import (
    clean_competitions,
    clean_teams,
    clean_player_mapping,
    clean_playing_eleven,
    clean_matches,
    clean_deliveries
)
from src.data.state_reconstruction import reconstruct_match_states

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("PRESSUREIQ.Pipeline")


def run_pipeline() -> dict:
    """Execute the data processing pipeline from raw CSVs to Parquet."""
    logger.info("Starting PRESSUREIQ Data Engineering Pipeline...")
    provenance = {"raw_files": {}, "processed_files": {}, "quality_checks": {}}
    
    # 1. Load Competitions
    comp_path = RAW_DATA_DIR / "competitions.csv"
    logger.info(f"Loading {comp_path}...")
    comp_raw = pd.read_csv(comp_path)
    provenance["raw_files"]["competitions"] = {"rows": len(comp_raw), "cols": len(comp_raw.columns)}
    comp_clean = clean_competitions(comp_raw)
    comp_clean.to_parquet(COMPETITIONS_PARQUET, index=False)
    provenance["processed_files"]["competitions"] = {"path": str(COMPETITIONS_PARQUET), "rows": len(comp_clean)}
    
    # 2. Load Teams
    teams_path = RAW_DATA_DIR / "teams.csv"
    logger.info(f"Loading {teams_path}...")
    teams_raw = pd.read_csv(teams_path)
    provenance["raw_files"]["teams"] = {"rows": len(teams_raw), "cols": len(teams_raw.columns)}
    teams_clean = clean_teams(teams_raw)
    teams_clean.to_parquet(TEAMS_PARQUET, index=False)
    provenance["processed_files"]["teams"] = {"path": str(TEAMS_PARQUET), "rows": len(teams_clean)}
    
    # 3. Load Player Mapping
    map_path = RAW_DATA_DIR / "competition_team_player_mapping.csv"
    logger.info(f"Loading {map_path}...")
    map_raw = pd.read_csv(map_path)
    provenance["raw_files"]["player_mapping"] = {"rows": len(map_raw), "cols": len(map_raw.columns)}
    players_clean = clean_player_mapping(map_raw)
    players_clean.to_parquet(PLAYERS_PARQUET, index=False)
    provenance["processed_files"]["players"] = {"path": str(PLAYERS_PARQUET), "rows": len(players_clean)}
    
    # 4. Load Playing XI
    pe_path = RAW_DATA_DIR / "playing_eleven.csv"
    logger.info(f"Loading {pe_path}...")
    pe_raw = pd.read_csv(pe_path)
    provenance["raw_files"]["playing_eleven"] = {"rows": len(pe_raw), "cols": len(pe_raw.columns)}
    pe_clean = clean_playing_eleven(pe_raw)
    pe_clean.to_parquet(PLAYING_XI_PARQUET, index=False)
    provenance["processed_files"]["playing_eleven"] = {"path": str(PLAYING_XI_PARQUET), "rows": len(pe_clean)}
    
    # 5. Load Matches
    matches_path = RAW_DATA_DIR / "matches.csv"
    logger.info(f"Loading {matches_path}...")
    matches_raw = pd.read_csv(matches_path)
    provenance["raw_files"]["matches"] = {"rows": len(matches_raw), "cols": len(matches_raw.columns)}
    matches_clean = clean_matches(matches_raw, comp_df=comp_clean)
    matches_clean.to_parquet(MATCHES_PARQUET, index=False)
    provenance["processed_files"]["matches"] = {"path": str(MATCHES_PARQUET), "rows": len(matches_clean)}
    
    # 6. Load Ball by Ball
    bbb_path = RAW_DATA_DIR / "ball_by_ball.csv"
    logger.info(f"Loading {bbb_path} (large file, ~41MB)...")
    bbb_raw = pd.read_csv(bbb_path, low_memory=False)
    provenance["raw_files"]["ball_by_ball"] = {"rows": len(bbb_raw), "cols": len(bbb_raw.columns)}
    
    # Clean deliveries
    logger.info("Cleaning deliveries and computing legal balls...")
    deliveries_clean = clean_deliveries(bbb_raw)
    
    # Merge competition category and match date from matches
    logger.info("Merging match metadata...")
    match_meta = matches_clean[["match_id", "comp_category", "match_date", "venue_country", "venue_id"]].copy()
    deliveries_clean = deliveries_clean.merge(match_meta, on="match_id", how="left")
    
    # Reconstruct match states
    logger.info("Reconstructing delivery-level match states and chase dynamics...")
    deliveries_with_state = reconstruct_match_states(deliveries_clean, matches_clean)
    
    logger.info(f"Writing {DELIVERIES_PARQUET}...")
    deliveries_with_state.to_parquet(DELIVERIES_PARQUET, index=False)
    provenance["processed_files"]["deliveries"] = {
        "path": str(DELIVERIES_PARQUET),
        "rows": len(deliveries_with_state),
        "columns": len(deliveries_with_state.columns)
    }
    
    # 7. Quality Checks & DuckDB Validation
    logger.info("Performing DuckDB validation...")
    con = duckdb.connect()
    con.execute(f"CREATE VIEW deliveries AS SELECT * FROM read_parquet('{DELIVERIES_PARQUET.as_posix()}')")
    con.execute(f"CREATE VIEW matches AS SELECT * FROM read_parquet('{MATCHES_PARQUET.as_posix()}')")
    
    total_matches_with_balls = con.execute("SELECT COUNT(DISTINCT match_id) FROM deliveries").fetchone()[0]
    total_deliveries = con.execute("SELECT COUNT(*) FROM deliveries").fetchone()[0]
    total_legal_balls = con.execute("SELECT COUNT(*) FROM deliveries WHERE is_legal_ball = true").fetchone()[0]
    total_wickets = con.execute("SELECT COUNT(*) FROM deliveries WHERE is_wicket = true").fetchone()[0]
    total_batters = con.execute("SELECT COUNT(DISTINCT striker_id) FROM deliveries").fetchone()[0]
    total_bowlers = con.execute("SELECT COUNT(DISTINCT bowler_id) FROM deliveries").fetchone()[0]
    
    provenance["quality_checks"] = {
        "matches_with_ball_data": total_matches_with_balls,
        "total_deliveries": total_deliveries,
        "total_legal_balls": total_legal_balls,
        "total_wickets": total_wickets,
        "unique_batters": total_batters,
        "unique_bowlers": total_bowlers,
        "legal_ball_pct": round(total_legal_balls / total_deliveries * 100, 2)
    }
    
    logger.info(f"Pipeline completed successfully. Summary: {provenance['quality_checks']}")
    
    # Write Provenance and Quality log
    log_file = DOCS_DIR / "PROVENANCE.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(provenance, f, indent=2)
    logger.info(f"Provenance saved to {log_file}")
    
    return provenance


if __name__ == "__main__":
    run_pipeline()
