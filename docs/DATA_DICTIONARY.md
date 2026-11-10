# PRESSUREIQ — Processed Data Dictionary

## Table 1: `deliveries.parquet` (Cleaned & Feature-Enriched Deliveries)

| Column Name | Data Type | Description |
|---|---|---|
| `match_id` | Int64 | Unique match identifier |
| `innings` | Int8 | Innings number (1 = 1st innings, 2 = 2nd innings chase, 3/4 = Super Over) |
| `overid` | Int8 | Over number (1 to 20) |
| `over_ball_num` | Int8 | Sequential delivery number within over (includes extras) |
| `innings_ball_num` | Int16 | Sequential delivery number in innings (includes extras) |
| `striker_id` | Int64 | Unique player ID of striker |
| `striker_name` | String | Standardized striker name |
| `non_striker_id` | Int64 | Unique player ID of non-striker |
| `non_striker_name` | String | Standardized non-striker name |
| `bowler_id` | Int64 | Unique player ID of bowler |
| `bowler_name` | String | Standardized bowler name |
| `batting_type` | String | Batter stance (`RHB`, `LHB`, `Unknown`) |
| `bowling_type` | String | Bowling style category (12 standardized styles) |
| `pace_or_spin` | String | Classification into `Pace` or `Spin` |
| `batting_order` | Int8 | Batter batting position in innings |
| `batter_runs` | Int8 | Runs scored off the bat (0 to 6) |
| `is_four` | Boolean | Whether delivery resulted in a boundary four |
| `is_six` | Boolean | Whether delivery resulted in a boundary six |
| `is_boundary` | Boolean | Whether delivery resulted in a 4 or 6 |
| `is_wicket` | Boolean | Whether any wicket fell on this delivery |
| `is_bowler_wicket` | Boolean | Whether wicket is accredited to the bowler (excludes run outs, retirements) |
| `dismissal_type` | String | Standardized dismissal type (e.g. `Caught`, `Bowled`, `LBW`, `RunOut`) |
| `is_wide` | Boolean | Wide delivery flag |
| `is_noball` | Boolean | No-ball delivery flag |
| `is_legbye` | Boolean | Leg-bye delivery flag |
| `is_bye` | Boolean | Bye delivery flag |
| `is_penalty` | Boolean | Penalty run delivery flag |
| `is_legal_ball` | Boolean | Legal delivery flag (`not (is_wide or is_noball)`) |
| `bowler_extras` | Int8 | Extra runs conceded by bowler (wides/noballs + overthrows) |
| `bowler_runs_conceded` | Int16 | Total runs charged to bowler (`batter_runs + bowler_extras`) |
| `est_total_runs` | Int8 | Reconstructed total team runs scored on delivery |
| `clean_bowl_speed` | Float64 | Sensor-cleaned delivery speed in km/h (50-165 km/h, outliers/zeros set to NaN) |
| `legal_balls_before` | Int16 | Total legal balls bowled in innings *prior* to this delivery |
| `team_runs_before` | Int16 | Total team score *prior* to this delivery |
| `wickets_lost_before` | Int8 | Total wickets lost in innings *prior* to this delivery |
| `wickets_remaining_before` | Int8 | Remaining batting resources (`10 - wickets_lost_before`) |
| `balls_remaining_before` | Int16 | Remaining legal deliveries in scheduled/revised innings |
| `phase` | String | Innings phase (`Powerplay`, `Middle`, `Death`) |
| `current_run_rate_before` | Float64 | Innings run rate prior to delivery |
| `target_score` | Float64 | Target score for innings 2 (revised target or 1st innings total + 1) |
| `runs_required_before` | Float64 | Runs needed to win *prior* to delivery (innings 2) |
| `required_run_rate_before` | Float64 | Required run rate *prior* to delivery (innings 2) |
| `batter_balls_faced_before` | Int16 | Deliveries faced by striker in innings prior to this ball (excluding wides) |
| `batter_runs_before` | Int16 | Runs scored by striker in innings prior to this ball |
| `batter_strike_rate_before` | Float64 | Striker's current innings strike rate prior to this ball |
| `bowler_legal_balls_before` | Int16 | Legal balls bowled by bowler in current match prior to this ball |
| `bowler_runs_conceded_before` | Int16 | Total runs conceded by bowler in current match prior to this ball |
| `bowler_wickets_before` | Int8 | Total wickets taken by bowler in current match prior to this ball |
| `bowler_economy_before` | Float64 | Bowler's current match economy rate prior to this ball |
| `comp_category` | String | Competition format (`IPL`, `T20I`, `Other_T20`) |
| `match_date` | Date | Official match date |
| `venue_country` | String | Country of venue |
| `venue_id` | Int64 | Standardized venue ID |

## Table 2: `matches.parquet` (Cleaned Match Metadata)

| Column Name | Data Type | Description |
|---|---|---|
| `match_id` | Int64 | Primary key |
| `comp_id` | Int64 | Competition identifier |
| `comp_category` | String | `IPL`, `T20I`, or `Other_T20` |
| `match_date` | Date | Date of match |
| `stage` | String | `League`, `Qualifier`, `Eliminator`, `Semi Final`, `Final`, etc. |
| `knock_out` | Int8 | 1 if playoff / knockout game, 0 otherwise |
| `venue_id` | Int64 | Venue ID |
| `venue_country` | String | Host country |
| `home_team_id` / `away_team_id` | Int64 | Team IDs |
| `is_dls_or_revised` | Boolean | True if rain-shortened or revised target |
| `second_inn_revised_overs` | Float64 | Total revised balls in innings 2 |
| `revised_target` | Float64 | DLS revised target if applicable |
| `outcome_type` | String | `win_by_runs`, `win_by_wickets`, `tie`, `abandoned`, `no_result` |
| `result` | String | Official textual match result |

