"""Configuration and paths for PRESSUREIQ."""

import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "SupeRR Selector Season 2 _ Problem Statement _ Data Pack" / "SupeRR Selector Season 2 _ Data Pack"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
DOCS_DIR = PROJECT_ROOT / "docs"

# Ensure directories exist
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# Parquet File Paths
MATCHES_PARQUET = PROCESSED_DATA_DIR / "matches.parquet"
DELIVERIES_PARQUET = PROCESSED_DATA_DIR / "deliveries.parquet"
PLAYERS_PARQUET = PROCESSED_DATA_DIR / "players.parquet"
COMPETITIONS_PARQUET = PROCESSED_DATA_DIR / "competitions.parquet"
TEAMS_PARQUET = PROCESSED_DATA_DIR / "teams.parquet"
PLAYING_XI_PARQUET = PROCESSED_DATA_DIR / "playing_eleven.parquet"

# Domain Constants
LEGAL_BALL_PER_OVER = 6
MAX_T20_OVERS = 20
MAX_T20_LEGAL_BALLS = 120
TOTAL_WICKETS = 10

# Extras Type Codes mapped in raw data
# extras1_runs codes: 1=Overstep (NB), 2=wide, 3=legbyes, 4=byes, 5=other, 6=None, 7=Penalty
EXTRAS_CODE_MAP = {
    1: "noball",
    2: "wide",
    3: "legbye",
    4: "bye",
    5: "other_noball",
    6: "none",
    7: "penalty"
}

# Dismissals accredited to bowler
BOWLER_DISMISSAL_TYPES = {
    "Bowled",
    "Caught",
    "LBW",
    "Stump",
    "Hit Wicket"
}

# Non-bowler dismissals
NON_BOWLER_DISMISSAL_TYPES = {
    "RunOut",
    "Retire Out",
    "Obstructing the field",
    "Obstracting the field"
}
