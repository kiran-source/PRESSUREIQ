import pytest
import pandas as pd
import numpy as np
from src.data.state_reconstruction import reconstruct_match_states
from src.models.pressure_index import compute_batting_pressure_index, compute_bowling_pressure_index


@pytest.mark.parametrize("revised_balls", [90, 84, 48, 30])
def test_first_innings_shortened_balls_and_elapsed(revised_balls):
    """
    P0-3 Requirement: Ensure start of shortened innings has zero elapsed balls,
    and balls_remaining_before correctly initializes to revised_balls (90, 84, 48, 30).
    """
    # Create synthetic match with Innings 1 shortened
    match_id = 99001
    matches_df = pd.DataFrame([{
        "match_id": match_id,
        "first_inn_revised_overs": revised_balls,
        "second_inn_revised_overs": np.nan,
        "revised_target": np.nan,
        "is_dls_or_revised": True
    }])

    # Build deliveries for full scheduled length
    deliv_rows = []
    for b in range(revised_balls):
        over = b // 6
        ball_in_over = (b % 6) + 1
        deliv_rows.append({
            "match_id": match_id,
            "innings": 1,
            "overid": over,
            "over_ball_num": ball_in_over,
            "innings_ball_num": b + 1,
            "is_legal_ball": True,
            "is_wide": False,
            "is_noball": False,
            "est_total_runs": 1,
            "batter_runs": 1,
            "bowler_runs_conceded": 1,
            "is_wicket": False,
            "striker_id": 101,
            "bowler_id": 201,
            "is_bowler_wicket": False,
        })
    deliv_df = pd.DataFrame(deliv_rows)

    res = reconstruct_match_states(deliv_df, matches_df)

    # 1. At the very first delivery (index 0):
    first_ball = res.iloc[0]
    assert first_ball["legal_balls_before"] == 0, "Elapsed balls must be 0 at start of shortened innings"
    assert first_ball["balls_remaining_before"] == revised_balls, f"Balls remaining must be {revised_balls} at ball 1"
    assert first_ball["max_innings_balls"] == revised_balls

    # 2. At the final delivery (index revised_balls - 1):
    last_ball = res.iloc[-1]
    assert last_ball["legal_balls_before"] == revised_balls - 1
    assert last_ball["balls_remaining_before"] == 1

    # 3. Test pressure index climax computation on shortened innings:
    res["runs_above_par_trajectory"] = 0.0
    res["is_knockout_stage"] = False
    bpi_df = compute_batting_pressure_index(res)
    bopi_df = compute_bowling_pressure_index(res)

    # At start of innings, completion ratio is 0.0 -> climax comp is 0.0
    assert bpi_df.iloc[0]["bpi_climax_comp"] == 0.0
    assert bopi_df.iloc[0]["bopi_climax_comp"] == 0.0

    # At final ball of shortened innings, climax comp should be close to 100.0
    assert bpi_df.iloc[-1]["bpi_climax_comp"] > 90.0
    assert bopi_df.iloc[-1]["bopi_climax_comp"] > 90.0


@pytest.mark.parametrize("revised_balls", [90, 84, 48, 30])
def test_second_innings_shortened_chase_dynamics(revised_balls):
    """
    P0-3 Requirement: Innings 2 shortened chase correctly calculates RRR,
    balls remaining, and climax urgency using the shortened ball limit.
    """
    match_id = 99002
    target_score = 100
    matches_df = pd.DataFrame([{
        "match_id": match_id,
        "first_inn_revised_overs": 120,
        "second_inn_revised_overs": revised_balls,
        "revised_target": target_score,
        "is_dls_or_revised": True
    }])

    deliv_rows = []
    # Deliveries for innings 2
    for b in range(revised_balls):
        over = b // 6
        ball_in_over = (b % 6) + 1
        deliv_rows.append({
            "match_id": match_id,
            "innings": 2,
            "overid": over,
            "over_ball_num": ball_in_over,
            "innings_ball_num": b + 1,
            "is_legal_ball": True,
            "is_wide": False,
            "is_noball": False,
            "est_total_runs": 1,
            "batter_runs": 1,
            "bowler_runs_conceded": 1,
            "is_wicket": False,
            "striker_id": 101,
            "bowler_id": 201,
            "is_bowler_wicket": False,
        })
    deliv_df = pd.DataFrame(deliv_rows)

    res = reconstruct_match_states(deliv_df, matches_df)

    # Ball 1:
    b1 = res.iloc[0]
    assert b1["legal_balls_before"] == 0
    assert b1["balls_remaining_before"] == revised_balls
    assert b1["max_innings_balls"] == revised_balls
    assert b1["runs_required_before"] == target_score
    # Expected RRR = target / (revised_balls / 6.0)
    expected_rrr = target_score / (revised_balls / 6.0)
    assert pytest.approx(b1["required_run_rate_before"], 0.01) == expected_rrr
