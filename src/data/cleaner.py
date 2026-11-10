"""Data cleaning and standardization module for PRESSUREIQ."""

import logging
import numpy as np
import pandas as pd
from typing import Dict, Tuple

from src.config import BOWLER_DISMISSAL_TYPES, NON_BOWLER_DISMISSAL_TYPES

logger = logging.getLogger(__name__)


def clean_competitions(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize competitions dataset."""
    df = df.copy()
    df["comp_id"] = df["comp_id"].astype(np.int64)
    df["comp_name"] = df["comp_name"].str.strip()
    df["match_format"] = df["match_format"].str.strip()
    df["season"] = df["season"].astype(str).str.strip()
    
    # Competition category: IPL, T20I, or Other_T20
    is_ipl = df["comp_name"].str.contains("IPL|Indian Premier League", case=False, na=False)
    df["comp_category"] = np.where(
        is_ipl,
        "IPL",
        np.where(df["match_format"] == "T20I", "T20I", "Other_T20")
    )
    return df


def clean_teams(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize teams dataset."""
    df = df.copy()
    df["comp_id"] = df["comp_id"].astype(np.int64)
    df["team_id"] = df["team_id"].astype(np.int64)
    df["team_name"] = df["team_name"].str.strip()
    return df.drop_duplicates()


def clean_player_mapping(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize competition-team-player mapping."""
    df = df.copy()
    df["comp_id"] = df["comp_id"].astype(np.int64)
    df["team_id"] = df["team_id"].astype(np.int64)
    df["player_id"] = df["player_id"].astype(np.int64)
    df["player_name"] = df["player_name"].str.strip()
    return df.drop_duplicates(subset=["comp_id", "team_id", "player_id"])


def clean_playing_eleven(df: pd.DataFrame) -> pd.DataFrame:
    """Clean playing XI data, converting boolean strings and standardizing IDs."""
    df = df.copy()
    df["match_id"] = df["match_id"].astype(np.int64)
    df["team_id"] = df["team_id"].astype(np.int64)
    df["player_id"] = df["player_id"].astype(np.int64)
    
    # Standardize string booleans
    def parse_bool(col: pd.Series) -> pd.Series:
        return col.astype(str).str.strip().str.lower().map({
            "true": True,
            "1": True,
            "false": False,
            "0": False,
            "nan": False,
            "none": False
        }).fillna(False).astype(bool)

    df["is_played"] = parse_bool(df["is_played"])
    df["is_captain"] = parse_bool(df["is_captain"])
    df["is_wk"] = parse_bool(df["is_wk"])
    df["is_impact"] = df["is_impact"].fillna(0).astype(int)
    df["is_impact_off"] = df["is_impact_off"].fillna(0).astype(int)
    
    return df


def clean_matches(df: pd.DataFrame, comp_df: pd.DataFrame = None) -> pd.DataFrame:
    """Clean matches data, parsing dates, stages, and outcome flags."""
    df = df.copy()
    df["match_id"] = df["match_id"].astype(np.int64)
    df["comp_id"] = df["comp_id"].astype(np.int64)
    df["match_date"] = pd.to_datetime(df["match_date"], errors="coerce")
    df["stage"] = df["stage"].fillna("Unknown").str.strip()
    df["venue_country"] = df["venue_country"].fillna("Unknown").str.strip()
    df["home_team"] = df["home_team"].str.strip()
    df["away_team"] = df["away_team"].str.strip()
    df["result"] = df["result"].fillna("No Result").str.strip()
    
    # Revised overs & targets
    df["is_dls_or_revised"] = (
        df["revised_target"].notna() | 
        df["first_inn_revised_overs"].notna() | 
        df["second_inn_revised_overs"].notna()
    )
    
    # Match outcome type
    res_lower = df["result"].str.lower()
    df["outcome_type"] = np.where(
        res_lower.str.contains("won by.*run", regex=True), "win_by_runs",
        np.where(res_lower.str.contains("won by.*wicket", regex=True), "win_by_wickets",
        np.where(res_lower.str.contains("tied"), "tie",
        np.where(res_lower.str.contains("abandoned"), "abandoned", "no_result")))
    )
    
    # Join competition category if supplied
    if comp_df is not None:
        cat_map = comp_df.set_index("comp_id")["comp_category"].to_dict()
        df["comp_category"] = df["comp_id"].map(cat_map).fillna("Unknown")
    
    return df


def clean_deliveries(df: pd.DataFrame) -> pd.DataFrame:
    """Clean delivery-level data with legal ball counting and run attribution."""
    df = df.copy()
    
    # Primary identifiers
    df["match_id"] = df["match_id"].astype(np.int64)
    df["innings"] = df["innings"].astype(np.int8)
    df["overid"] = df["overid"].astype(np.int8)
    df["over_ball_num"] = df["over_ball_num"].astype(np.int8)
    df["innings_ball_num"] = df["innings_ball_num"].astype(np.int16)
    
    df["striker_id"] = df["striker_id"].astype(np.int64)
    df["striker_name"] = df["striker_name"].str.strip()
    df["non_striker_id"] = df["non_striker_id"].astype(np.int64)
    df["non_striker_name"] = df["non_striker_name"].str.strip()
    df["bowler_id"] = df["bowler_id"].astype(np.int64)
    df["bowler_name"] = df["bowler_name"].str.strip()
    
    # Normalizing categorical text
    df["batting_type"] = df["batting_type"].fillna("Unknown").str.strip()
    df["bowling_type"] = df["bowling_type"].fillna("Unknown").str.strip()
    df["pace_or_spin"] = df["pace_or_spin"].fillna("Unknown").str.strip()
    
    # Fix typo in dismissal_type
    df["dismissal_type"] = df["dismissal_type"].replace({"Obstracting the field": "Obstructing the field"})
    
    # Extras classification
    extras = df["extras_type"].fillna("none").str.lower()
    df["is_wide"] = extras == "wide"
    df["is_noball"] = extras.isin(["overstep", "other"])
    df["is_legbye"] = extras == "legbyes"
    df["is_bye"] = extras == "byes"
    df["is_penalty"] = extras == "penalty"
    df["is_any_extras"] = extras != "none"
    
    # Cricket rule: A legal delivery is one that is neither wide nor no-ball
    df["is_legal_ball"] = ~(df["is_wide"] | df["is_noball"])
    
    # Batter runs: directly from 'runs' column (off the bat)
    df["batter_runs"] = df["runs"].astype(np.int8)
    
    # Boundaries
    df["is_four"] = df["is_four"].fillna(False).astype(bool)
    df["is_six"] = df["is_six"].fillna(False).astype(bool)
    df["is_boundary"] = df["is_four"] | df["is_six"]
    
    # Bowler extras: bowler is penalized 1 run for wides / no-balls + additional overthrows (extras_2_runs)
    extras_2 = df["extras_2_runs"].fillna(0).astype(np.int8)
    df["bowler_extras"] = np.where(df["is_wide"] | df["is_noball"], 1 + extras_2, 0).astype(np.int8)
    df["bowler_runs_conceded"] = (df["batter_runs"] + df["bowler_extras"]).astype(np.int16)
    
    # Estimated total delivery runs for team score accumulation
    # Normal: batter_runs
    # Wide: 1 + extras_2
    # No-ball: 1 + batter_runs + extras_2
    # Leg-bye: max(1, extras_2)
    # Bye: max(1, extras_2)
    # Penalty: 5
    team_runs = np.where(
        df["is_wide"], 1 + extras_2,
        np.where(
            df["is_noball"], 1 + df["batter_runs"] + extras_2,
            np.where(
                df["is_legbye"] | df["is_bye"], np.maximum(1, extras_2),
                np.where(df["is_penalty"], 5, df["batter_runs"])
            )
        )
    )
    df["est_total_runs"] = team_runs.astype(np.int8)
    
    # Wickets
    df["is_wicket"] = df["is_wicket"].fillna(False).astype(bool)
    df["is_bowler_wicket"] = df["is_wicket"] & df["dismissal_type"].isin(BOWLER_DISMISSAL_TYPES)
    # Batter dismissal: strictly true when the striker is the player dismissed (prevents penalizing striker on non-striker run-out)
    df["is_striker_out"] = df["is_wicket"] & (df["dismissed_player_id"] == df["striker_id"])
    
    # Bowl speed: clean zeros and extreme sensor artifacts
    speed = df["bowl_speed"].replace(0, np.nan)
    # Realistic cricket bowling speed is between 50 and 165 km/h
    df["clean_bowl_speed"] = np.where((speed >= 50) & (speed <= 165), speed, np.nan)
    
    return df

