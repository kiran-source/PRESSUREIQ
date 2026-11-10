"""Unit tests for match state reconstruction and strict temporal causality."""

import numpy as np
import pandas as pd
import pytest

from src.data.cleaner import clean_deliveries, clean_matches
from src.data.state_reconstruction import reconstruct_match_states


@pytest.fixture
def mini_match_data():
    """Create a minimal two-innings match to test state counters."""
    # Innings 1: 3 balls (1 single, 1 wide, 1 four)
    # Innings 2: 2 balls (1 dot, 1 six)
    matches_df = pd.DataFrame([{
        "match_id": 999, "comp_id": 1, "match_number": 1, "match_date": "2024-05-01",
        "stage": "League", "venue_id": 10, "venue_country": "India",
        "home_team_id": 1, "home_team": "Team A", "away_team_id": 2, "away_team": "Team B",
        "home_team_captain_id": 101, "away_team_captain_id": 201, "toss_win_team_id": 1,
        "toss_opted": "Batting", "man_of_the_match": 101, "first_inn_revised_overs": np.nan,
        "second_inn_revised_overs": np.nan, "revised_target": np.nan, "knock_out": 0,
        "win_team_id": 2, "result": "Team B Won by 6 Wickets", "is_dls_or_revised": False,
        "outcome_type": "win_by_wickets", "comp_category": "IPL"
    }])
    
    deliv_rows = [
        # Inn 1 Ball 1: single
        {"match_id": 999, "innings": 1, "overid": 1, "over_ball_num": 1, "innings_ball_num": 1,
         "batting_team_id": 1, "bowling_team_id": 2, "striker_id": 101, "striker_name": "A",
         "non_striker_id": 102, "non_striker_name": "B", "bowler_id": 201, "bowler_name": "X",
         "batting_type": "RHB", "bowling_type": "Pace", "batting_order": 1, "runs": 1,
         "is_four": False, "is_six": False, "is_wicket": False, "dismissal_type_id": np.nan,
         "dismissal_type": np.nan, "dismissed_player_id": np.nan, "extras_type": np.nan,
         "extras1_runs": 6, "extras_2_runs": 0, "pace_or_spin": "Pace", "bowl_speed": 130.0,
         "stroke": "Push", "delivery_style": "Inswing", "over_or_around": "Over", "on_or_off": "Off-side",
         "delivery_ist_time": "2024-05-01 00:00:00 UTC"},
        # Inn 1 Ball 2: wide
        {"match_id": 999, "innings": 1, "overid": 1, "over_ball_num": 2, "innings_ball_num": 2,
         "batting_team_id": 1, "bowling_team_id": 2, "striker_id": 101, "striker_name": "A",
         "non_striker_id": 102, "non_striker_name": "B", "bowler_id": 201, "bowler_name": "X",
         "batting_type": "RHB", "bowling_type": "Pace", "batting_order": 1, "runs": 0,
         "is_four": False, "is_six": False, "is_wicket": False, "dismissal_type_id": np.nan,
         "dismissal_type": np.nan, "dismissed_player_id": np.nan, "extras_type": "wide",
         "extras1_runs": 2, "extras_2_runs": 0, "pace_or_spin": "Pace", "bowl_speed": 130.0,
         "stroke": np.nan, "delivery_style": "Inswing", "over_or_around": "Over", "on_or_off": "Off-side",
         "delivery_ist_time": "2024-05-01 00:00:00 UTC"},
        # Inn 1 Ball 3: four
        {"match_id": 999, "innings": 1, "overid": 1, "over_ball_num": 3, "innings_ball_num": 3,
         "batting_team_id": 1, "bowling_team_id": 2, "striker_id": 101, "striker_name": "A",
         "non_striker_id": 102, "non_striker_name": "B", "bowler_id": 201, "bowler_name": "X",
         "batting_type": "RHB", "bowling_type": "Pace", "batting_order": 1, "runs": 4,
         "is_four": True, "is_six": False, "is_wicket": False, "dismissal_type_id": np.nan,
         "dismissal_type": np.nan, "dismissed_player_id": np.nan, "extras_type": np.nan,
         "extras1_runs": 6, "extras_2_runs": 0, "pace_or_spin": "Pace", "bowl_speed": 132.0,
         "stroke": "Drive", "delivery_style": "Inswing", "over_or_around": "Over", "on_or_off": "Off-side",
         "delivery_ist_time": "2024-05-01 00:00:00 UTC"},
        # Inn 2 Ball 1: dot
        {"match_id": 999, "innings": 2, "overid": 1, "over_ball_num": 1, "innings_ball_num": 1,
         "batting_team_id": 2, "bowling_team_id": 1, "striker_id": 201, "striker_name": "X",
         "non_striker_id": 202, "non_striker_name": "Y", "bowler_id": 101, "bowler_name": "A",
         "batting_type": "RHB", "bowling_type": "Pace", "batting_order": 1, "runs": 0,
         "is_four": False, "is_six": False, "is_wicket": False, "dismissal_type_id": np.nan,
         "dismissal_type": np.nan, "dismissed_player_id": np.nan, "extras_type": np.nan,
         "extras1_runs": 6, "extras_2_runs": 0, "pace_or_spin": "Pace", "bowl_speed": 128.0,
         "stroke": "Defend", "delivery_style": "Straight", "over_or_around": "Over", "on_or_off": "Off-side",
         "delivery_ist_time": "2024-05-01 00:00:00 UTC"},
        # Inn 2 Ball 2: six
        {"match_id": 999, "innings": 2, "overid": 1, "over_ball_num": 2, "innings_ball_num": 2,
         "batting_team_id": 2, "bowling_team_id": 1, "striker_id": 201, "striker_name": "X",
         "non_striker_id": 202, "non_striker_name": "Y", "bowler_id": 101, "bowler_name": "A",
         "batting_type": "RHB", "bowling_type": "Pace", "batting_order": 1, "runs": 6,
         "is_four": False, "is_six": True, "is_wicket": False, "dismissal_type_id": np.nan,
         "dismissal_type": np.nan, "dismissed_player_id": np.nan, "extras_type": np.nan,
         "extras1_runs": 6, "extras_2_runs": 0, "pace_or_spin": "Pace", "bowl_speed": 130.0,
         "stroke": "Pull", "delivery_style": "Straight", "over_or_around": "Over", "on_or_off": "On-side",
         "delivery_ist_time": "2024-05-01 00:00:00 UTC"},
    ]
    deliv_df = pd.DataFrame(deliv_rows)
    return matches_df, deliv_df


def test_temporal_causality_and_state(mini_match_data):
    matches_df, deliv_df = mini_match_data
    cleaned = clean_deliveries(deliv_df)
    state = reconstruct_match_states(cleaned, matches_df)
    
    # Check Innings 1 Ball 1: prior state must be clean zero
    row0 = state.iloc[0]
    assert row0["legal_balls_before"] == 0
    assert row0["team_runs_before"] == 0
    assert row0["wickets_lost_before"] == 0
    assert row0["wickets_remaining_before"] == 10
    assert row0["balls_remaining_before"] == 120
    assert row0["phase"] == "Powerplay"
    
    # Ball 2 (wide): ball 1 was legal and scored 1 run
    row1 = state.iloc[1]
    assert row1["legal_balls_before"] == 1
    assert row1["team_runs_before"] == 1
    assert bool(row1["is_legal_ball"]) is False
    
    # Ball 3 (four): wide did not increment legal balls, but added 1 run to team
    row2 = state.iloc[2]
    assert row2["legal_balls_before"] == 1  # Still 1 legal ball!
    assert row2["team_runs_before"] == 2   # 1 bat + 1 wide = 2 team runs
    
    # Total inn1 score: 1 + 1 (wide) + 4 = 6 runs
    # Target for innings 2 should be 6 + 1 = 7 runs
    row3 = state.iloc[3]  # Innings 2 Ball 1
    assert row3["innings"] == 2
    assert row3["target_score"] == 7
    assert row3["team_runs_before"] == 0
    assert row3["runs_required_before"] == 7
    assert row3["balls_remaining_before"] == 120
    assert np.isclose(row3["required_run_rate_before"], 7 / (120 / 6.0))
    
    # Innings 2 Ball 2: after a dot ball
    row4 = state.iloc[4]
    assert row4["legal_balls_before"] == 1
    assert row4["balls_remaining_before"] == 119
    assert row4["team_runs_before"] == 0
    assert row4["runs_required_before"] == 7
    assert np.isclose(row4["required_run_rate_before"], 7 / (119 / 6.0))


def test_revised_target_dls():
    """Verify that matches with revised target use revised_target instead of inn1 + 1."""
    matches_df = pd.DataFrame([{
        "match_id": 888, "comp_id": 1, "match_number": 2, "match_date": "2024-05-02",
        "stage": "League", "venue_id": 10, "venue_country": "India",
        "home_team_id": 1, "home_team": "Team A", "away_team_id": 2, "away_team": "Team B",
        "home_team_captain_id": 101, "away_team_captain_id": 201, "toss_win_team_id": 1,
        "toss_opted": "Batting", "man_of_the_match": 101, "first_inn_revised_overs": np.nan,
        "second_inn_revised_overs": 90.0, "revised_target": 140.0, "knock_out": 0,
        "win_team_id": 2, "result": "Team B Won by DLS", "is_dls_or_revised": True,
        "outcome_type": "win_by_wickets", "comp_category": "IPL"
    }])
    
    deliv_rows = [
        # Inn 1 delivery (score 100)
        {"match_id": 888, "innings": 1, "overid": 1, "over_ball_num": 1, "innings_ball_num": 1,
         "batting_team_id": 1, "bowling_team_id": 2, "striker_id": 101, "striker_name": "A",
         "non_striker_id": 102, "non_striker_name": "B", "bowler_id": 201, "bowler_name": "X",
         "batting_type": "RHB", "bowling_type": "Pace", "batting_order": 1, "runs": 6,
         "is_four": False, "is_six": True, "is_wicket": False, "dismissal_type_id": np.nan,
         "dismissal_type": np.nan, "dismissed_player_id": np.nan, "extras_type": np.nan,
         "extras1_runs": 6, "extras_2_runs": 0, "pace_or_spin": "Pace", "bowl_speed": 130.0,
         "stroke": "Pull", "delivery_style": "Straight", "over_or_around": "Over", "on_or_off": "On-side",
         "delivery_ist_time": "2024-05-02 00:00:00 UTC"},
        # Inn 2 delivery (target should be 140, max balls 90)
        {"match_id": 888, "innings": 2, "overid": 1, "over_ball_num": 1, "innings_ball_num": 1,
         "batting_team_id": 2, "bowling_team_id": 1, "striker_id": 201, "striker_name": "X",
         "non_striker_id": 202, "non_striker_name": "Y", "bowler_id": 101, "bowler_name": "A",
         "batting_type": "RHB", "bowling_type": "Pace", "batting_order": 1, "runs": 0,
         "is_four": False, "is_six": False, "is_wicket": False, "dismissal_type_id": np.nan,
         "dismissal_type": np.nan, "dismissed_player_id": np.nan, "extras_type": np.nan,
         "extras1_runs": 6, "extras_2_runs": 0, "pace_or_spin": "Pace", "bowl_speed": 130.0,
         "stroke": "Defend", "delivery_style": "Straight", "over_or_around": "Over", "on_or_off": "Off-side",
         "delivery_ist_time": "2024-05-02 00:00:00 UTC"}
    ]
    deliv_df = pd.DataFrame(deliv_rows)
    cleaned = clean_deliveries(deliv_df)
    state = reconstruct_match_states(cleaned, matches_df)
    
    row1 = state[state["innings"] == 2].iloc[0]
    assert row1["target_score"] == 140.0
    assert row1["balls_remaining_before"] == 90
    assert row1["runs_required_before"] == 140.0
    assert np.isclose(row1["required_run_rate_before"], 140.0 / (90 / 6.0))
