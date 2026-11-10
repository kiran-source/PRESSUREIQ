"""Unit tests for data cleaning and cricket rule enforcement."""

import numpy as np
import pandas as pd
import pytest

from src.data.cleaner import clean_deliveries, clean_matches, clean_playing_eleven
from src.config import BOWLER_DISMISSAL_TYPES, NON_BOWLER_DISMISSAL_TYPES


@pytest.fixture
def sample_raw_deliveries():
    """Create synthetic raw deliveries covering edge cases."""
    data = [
        # Normal single
        {
            "match_id": 1, "innings": 1, "overid": 1, "over_ball_num": 1, "innings_ball_num": 1,
            "batting_team_id": 10, "bowling_team_id": 20,
            "striker_id": 101, "striker_name": "Batter A", "non_striker_id": 102, "non_striker_name": "Batter B",
            "bowler_id": 201, "bowler_name": "Bowler X", "batting_type": "RHB", "bowling_type": "Right-arm Fast",
            "batting_order": 1, "runs": 1, "is_four": False, "is_six": False, "is_wicket": False,
            "dismissal_type_id": np.nan, "dismissal_type": np.nan, "dismissed_player_id": np.nan,
            "extras_type": np.nan, "extras1_runs": 6, "extras_2_runs": 0, "pace_or_spin": "Pace",
            "bowl_speed": 135.5, "stroke": "Push", "delivery_style": "Inswing", "over_or_around": "Over",
            "on_or_off": "Off-side", "delivery_ist_time": "2024-04-01 00:00:00 UTC"
        },
        # Wide
        {
            "match_id": 1, "innings": 1, "overid": 1, "over_ball_num": 2, "innings_ball_num": 2,
            "batting_team_id": 10, "bowling_team_id": 20,
            "striker_id": 101, "striker_name": "Batter A", "non_striker_id": 102, "non_striker_name": "Batter B",
            "bowler_id": 201, "bowler_name": "Bowler X", "batting_type": "RHB", "bowling_type": "Right-arm Fast",
            "batting_order": 1, "runs": 0, "is_four": False, "is_six": False, "is_wicket": False,
            "dismissal_type_id": np.nan, "dismissal_type": np.nan, "dismissed_player_id": np.nan,
            "extras_type": "wide", "extras1_runs": 2, "extras_2_runs": 0, "pace_or_spin": "Pace",
            "bowl_speed": 130.0, "stroke": np.nan, "delivery_style": "Out Swing", "over_or_around": "Over",
            "on_or_off": "Off-side", "delivery_ist_time": "2024-04-01 00:00:00 UTC"
        },
        # No-ball with 4 off the bat
        {
            "match_id": 1, "innings": 1, "overid": 1, "over_ball_num": 3, "innings_ball_num": 3,
            "batting_team_id": 10, "bowling_team_id": 20,
            "striker_id": 101, "striker_name": "Batter A", "non_striker_id": 102, "non_striker_name": "Batter B",
            "bowler_id": 201, "bowler_name": "Bowler X", "batting_type": "RHB", "bowling_type": "Right-arm Fast",
            "batting_order": 1, "runs": 4, "is_four": True, "is_six": False, "is_wicket": False,
            "dismissal_type_id": np.nan, "dismissal_type": np.nan, "dismissed_player_id": np.nan,
            "extras_type": "Overstep", "extras1_runs": 1, "extras_2_runs": 0, "pace_or_spin": "Pace",
            "bowl_speed": 138.0, "stroke": "Cover Drive", "delivery_style": "Straight", "over_or_around": "Over",
            "on_or_off": "Off-side", "delivery_ist_time": "2024-04-01 00:00:00 UTC"
        },
        # Leg bye
        {
            "match_id": 1, "innings": 1, "overid": 1, "over_ball_num": 4, "innings_ball_num": 4,
            "batting_team_id": 10, "bowling_team_id": 20,
            "striker_id": 101, "striker_name": "Batter A", "non_striker_id": 102, "non_striker_name": "Batter B",
            "bowler_id": 201, "bowler_name": "Bowler X", "batting_type": "RHB", "bowling_type": "Right-arm Fast",
            "batting_order": 1, "runs": 0, "is_four": False, "is_six": False, "is_wicket": False,
            "dismissal_type_id": np.nan, "dismissal_type": np.nan, "dismissed_player_id": np.nan,
            "extras_type": "legbyes", "extras1_runs": 3, "extras_2_runs": 0, "pace_or_spin": "Pace",
            "bowl_speed": 132.0, "stroke": "Worked", "delivery_style": "Inswing", "over_or_around": "Over",
            "on_or_off": "On-side", "delivery_ist_time": "2024-04-01 00:00:00 UTC"
        },
        # Bowler wicket (Caught)
        {
            "match_id": 1, "innings": 1, "overid": 1, "over_ball_num": 5, "innings_ball_num": 5,
            "batting_team_id": 10, "bowling_team_id": 20,
            "striker_id": 102, "striker_name": "Batter B", "non_striker_id": 101, "non_striker_name": "Batter A",
            "bowler_id": 201, "bowler_name": "Bowler X", "batting_type": "RHB", "bowling_type": "Right-arm Fast",
            "batting_order": 2, "runs": 0, "is_four": False, "is_six": False, "is_wicket": True,
            "dismissal_type_id": 1.0, "dismissal_type": "Caught", "dismissed_player_id": 102.0,
            "extras_type": np.nan, "extras1_runs": 6, "extras_2_runs": 0, "pace_or_spin": "Pace",
            "bowl_speed": 140.0, "stroke": "Slog", "delivery_style": "Straight", "over_or_around": "Over",
            "on_or_off": "Off-side", "delivery_ist_time": "2024-04-01 00:00:00 UTC"
        },
        # Run out (Non-bowler wicket)
        {
            "match_id": 1, "innings": 1, "overid": 1, "over_ball_num": 6, "innings_ball_num": 6,
            "batting_team_id": 10, "bowling_team_id": 20,
            "striker_id": 101, "striker_name": "Batter A", "non_striker_id": 103, "non_striker_name": "Batter C",
            "bowler_id": 201, "bowler_name": "Bowler X", "batting_type": "RHB", "bowling_type": "Right-arm Fast",
            "batting_order": 1, "runs": 1, "is_four": False, "is_six": False, "is_wicket": True,
            "dismissal_type_id": 4.0, "dismissal_type": "RunOut", "dismissed_player_id": 103.0,
            "extras_type": np.nan, "extras1_runs": 6, "extras_2_runs": 0, "pace_or_spin": "Pace",
            "bowl_speed": 134.0, "stroke": "Push", "delivery_style": "Straight", "over_or_around": "Over",
            "on_or_off": "On-side", "delivery_ist_time": "2024-04-01 00:00:00 UTC"
        }
    ]
    return pd.DataFrame(data)


def test_legal_ball_classification(sample_raw_deliveries):
    cleaned = clean_deliveries(sample_raw_deliveries)
    
    # Delivery 0: Normal single -> Legal
    assert bool(cleaned.loc[0, "is_legal_ball"]) is True
    # Delivery 1: Wide -> NOT legal
    assert bool(cleaned.loc[1, "is_legal_ball"]) is False
    # Delivery 2: No-ball -> NOT legal
    assert bool(cleaned.loc[2, "is_legal_ball"]) is False
    # Delivery 3: Leg bye -> Legal
    assert bool(cleaned.loc[3, "is_legal_ball"]) is True
    # Delivery 4: Caught -> Legal
    assert bool(cleaned.loc[4, "is_legal_ball"]) is True
    # Delivery 5: RunOut -> Legal
    assert bool(cleaned.loc[5, "is_legal_ball"]) is True


def test_bowler_runs_conceded_rules(sample_raw_deliveries):
    cleaned = clean_deliveries(sample_raw_deliveries)
    
    # Ball 0: Normal single -> 1 run conceded
    assert cleaned.loc[0, "bowler_runs_conceded"] == 1
    # Ball 1: Wide -> 1 run conceded
    assert cleaned.loc[1, "bowler_runs_conceded"] == 1
    # Ball 2: No-ball with 4 off bat -> 1 (NB extra) + 4 (bat) = 5 runs conceded
    assert cleaned.loc[2, "bowler_runs_conceded"] == 5
    # Ball 3: Leg bye -> 0 runs conceded to bowler (cricket law)
    assert cleaned.loc[3, "bowler_runs_conceded"] == 0
    # Ball 4: Dot ball wicket -> 0 runs conceded
    assert cleaned.loc[4, "bowler_runs_conceded"] == 0
    # Ball 5: Single + Run Out -> 1 run conceded
    assert cleaned.loc[5, "bowler_runs_conceded"] == 1


def test_wicket_attribution(sample_raw_deliveries):
    cleaned = clean_deliveries(sample_raw_deliveries)
    
    # Caught is accredited to bowler
    assert bool(cleaned.loc[4, "is_wicket"]) is True
    assert bool(cleaned.loc[4, "is_bowler_wicket"]) is True
    
    # Run out is team wicket, NOT accredited to bowler
    assert bool(cleaned.loc[5, "is_wicket"]) is True
    assert bool(cleaned.loc[5, "is_bowler_wicket"]) is False


def test_dismissal_type_normalization():
    df = pd.DataFrame([{
        "match_id": 1, "innings": 1, "overid": 1, "over_ball_num": 1, "innings_ball_num": 1,
        "batting_team_id": 1, "bowling_team_id": 2, "striker_id": 10, "striker_name": "P1",
        "non_striker_id": 11, "non_striker_name": "P2", "bowler_id": 20, "bowler_name": "B1",
        "batting_type": "RHB", "bowling_type": "Pace", "batting_order": 1, "runs": 0,
        "is_four": False, "is_six": False, "is_wicket": True,
        "dismissal_type_id": 8.0, "dismissal_type": "Obstracting the field", "dismissed_player_id": 10.0,
        "extras_type": np.nan, "extras1_runs": 6, "extras_2_runs": 0, "pace_or_spin": "Pace",
        "bowl_speed": 0.0, "stroke": np.nan, "delivery_style": "Straight", "over_or_around": "Over",
        "on_or_off": "Off-side", "delivery_ist_time": "2024-04-01 00:00:00 UTC"
    }])
    cleaned = clean_deliveries(df)
    assert cleaned.loc[0, "dismissal_type"] == "Obstructing the field"
    assert bool(cleaned.loc[0, "is_bowler_wicket"]) is False
