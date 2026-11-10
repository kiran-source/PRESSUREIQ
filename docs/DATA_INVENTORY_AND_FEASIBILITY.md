# PRESSUREIQ — Complete Competition Dataset Audit & Feature Feasibility Report

**Audit Date**: 2026-11-10  
**Scope**: All raw competition CSV files in `SupeRR Selector Season 2 _ Data Pack/`  
**Integrity Rule**: Raw files inspected in-place; strictly preserved without modification.

---

## 1. File Inventory & Storage Summary

| File Name | File Size | Row Count | Column Count | Primary / Natural Key | Key Uniqueness |
|---|---|---|---|---|---|
| `competitions.csv` | 7,624 bytes | 141 | 4 | `comp_id` | ✅ 100% Unique (0 dups) |
| `teams.csv` | 6,922 bytes | 353 | 3 | `(comp_id, team_id)` | ✅ 100% Unique (0 dups) |
| `competition_team_player_mapping.csv` | 462,969 bytes | 6,413 | 6 | `(comp_id, team_id, player_id)` | ✅ 100% Unique (0 dups) |
| `matches.csv` | 123,864 bytes | 883 | 22 | `match_id` | ✅ 100% Unique (0 dups) |
| `playing_eleven.csv` | 966,287 bytes | 28,381 | 9 | `(match_id, player_id)` | ⚠️ **40 duplicate pairs (75 rows)** |
| `ball_by_ball.csv` | 41,071,609 bytes | 200,999 | 33 | `(match_id, innings, overid, over_ball_num)` | ✅ 100% Unique (0 dups) |

---

## 2. Comprehensive Schema & Missing Value Audit

### 2.1 `competitions.csv` (141 rows, 4 columns)
- **Columns & Types**: `comp_id` (int64), `comp_name` (object), `match_format` (object), `season` (object).
- **Missing Values**: **0 missing** (100% complete).
- **Format Breakdown**: 134 T20I competitions, 7 T20 competitions (5 IPL seasons: 2022, 2023, 2024, 2025, 2026 + 2 Asian emerging tournaments).
- **Seasons**: 2022, 2022/23, 2023, 2023/24, 2024, 2024/25, 2025, 2026.

### 2.2 `teams.csv` (353 rows, 3 columns)
- **Columns & Types**: `comp_id` (int64), `team_id` (int64), `team_name` (object).
- **Missing Values**: **0 missing** (100% complete).
- **Unique Teams**: 39 unique team names across 141 competitions.

### 2.3 `competition_team_player_mapping.csv` (6,413 rows, 6 columns)
- **Columns & Types**: `comp_id` (int64), `comp_name` (object), `team_id` (int64), `team_name` (object), `player_id` (int64), `player_name` (object).
- **Missing Values**: **0 missing** (100% complete).
- **Coverage**: 1,217 unique players across all registered tournament squads.

### 2.4 `matches.csv` (883 rows, 22 columns)
- **Missing Values**:
  - `home_team_captain_id`: 44 missing (5.0%)
  - `away_team_captain_id`: 45 missing (5.1%)
  - `toss_win_team_id`: 15 missing (1.7%)
  - `toss_opted`: 15 missing (1.7%)
  - `win_team_id`: 41 missing (4.6%) — corresponds to No Result (21), Abandoned (19), Tied (1)
  - `first_inn_revised_overs`: 858 missing (97.2%) — only populated in rain-affected matches
  - `second_inn_revised_overs`: 858 missing (97.2%) — only populated in rain-affected matches
  - `revised_target`: 860 missing (97.4%) — populated in 23 DLS matches
- **Date Coverage**: Continuous from `2022-01-22` to `2026-11-01` (2022: 180, 2023: 140, 2024: 200, 2025: 217, 2026: 146 matches).
- **Stages**: League (620), Others (226), Final (12), Qualifier (10), Super 4 (6), Eliminator (5), Semi Final (4).
- **Venues**: 98 unique venues across 17 host countries.

### 2.5 `playing_eleven.csv` (28,381 rows, 9 columns)
- **Missing Values**:
  - `batting_order`: 8,678 missing (30.6%) — unbatted players / impact substitutes
  - `is_captain`: 8,667 missing (30.5%)
  - `is_wk`: 8,667 missing (30.5%)
- **Data Types Caveat**: `is_captain` and `is_wk` are stored as string literals (`"True"`, `"False"`), requiring explicit boolean parsing.
- **Duplicate Key Finding**: Exactly 40 player-match instances (75 rows total) contain duplicate entries in match 13613 where batting order was amended. Pipeline must deduplicate by taking `last` or `min(batting_order)`.

### 2.6 `ball_by_ball.csv` (200,999 rows, 33 columns)
- **Missing Values**:
  - `dismissal_type_id`: 190,118 missing (94.6%) — correctly null when no wicket falls
  - `dismissal_type`: 190,118 missing (94.6%)
  - `dismissed_player_id`: 190,107 missing (94.6%) — 1 wicket missing player ID (Hardik Pandya Retire Out in match 40709)
  - `extras_type`: 189,167 missing (94.1%) — correctly null on normal deliveries
  - `stroke`: 6,158 missing (3.1%)
  - `delivery_style`: 391 missing (0.2%)
  - `over_or_around`: 407 missing (0.2%)
- **Delivery Count Breakdown**:
  - Innings 1: 105,727 deliveries
  - Innings 2: 95,234 deliveries
  - Innings 3: 25 deliveries (Super Overs across 5 matches)
  - Innings 4: 13 deliveries (Super Overs across 5 matches)
- **Sensor Speed Data**:
  - `bowl_speed` has **77,861 zeros (38.7%)** and sensor outliers up to 1,456.1 km/h.

---

## 3. Referential Integrity & Relational Architecture

```
competitions.csv [comp_id]
       │
       ├──► teams.csv [comp_id, team_id]
       ├──► competition_team_player_mapping.csv [comp_id, team_id, player_id]
       └──► matches.csv [match_id, comp_id]
                 │
                 ├──► playing_eleven.csv [match_id, team_id, player_id]
                 └──► ball_by_ball.csv [match_id, batting_team_id, bowling_team_id, striker_id, bowler_id]
```

### Referential Integrity Results
1. **Competitions ↔ Matches**: ✅ 100% of matches reference a valid `comp_id`.
2. **Matches ↔ Ball-by-Ball**:
   - 867 matches have ball-by-ball records.
   - 16 matches in `matches.csv` have zero deliveries in `ball_by_ball.csv` — **all 16 are "Match Abandoned"** without a ball bowled (expected).
3. **Teams ↔ Ball-by-Ball**: ✅ 100% of `batting_team_id` and `bowling_team_id` exist in `teams.csv`.
4. **Players ↔ Ball-by-Ball**:
   - 959 unique players appear in `ball_by_ball.csv`.
   - ✅ 100% of ball-by-ball players exist in `competition_team_player_mapping.csv`.
   - ⚠️ Exactly 2 players appear in `ball_by_ball.csv` but are absent from `playing_eleven.csv`: Player 36153 (Syed Haider, 49 deliveries) and Player 39444 (Basil Hameed, 64 deliveries).

---

## 4. Deep-Dive Field Analysis

### 4.1 Scoring Fields & Run Accounting
- `runs`: Contains **bat-off-bat runs only** (values: 0, 1, 2, 3, 4, 5, 6).
  - Normal ball: batter runs.
  - No-ball (`Overstep`, `other`): batter runs off the bat.
  - Wide: strictly `0`.
  - Leg-bye / Bye: strictly `0`.
- `extras1_runs`: **Not a run value, but a categorical integer code**:
  - `1`: Overstep (no-ball) — 576 occurrences
  - `2`: Wide — 7,714 occurrences
  - `3`: Leg-byes — 2,748 occurrences
  - `4`: Byes — 529 occurrences
  - `5`: Other (no-ball combination) — 264 occurrences
  - `6`: None (normal delivery) — 189,167 occurrences
  - `7`: Penalty — 1 occurrence
- `extras_2_runs`: Additional overthrow / boundary runs on extras. Only 36 deliveries in the entire dataset have non-zero values (20 ones, 16 fours).
- ⚠️ **Critical Data Limitation**: The raw dataset does **not record the actual runs scored on leg-byes or byes**. While wides and no-balls can be precisely calculated ($1 + \text{extras\_2}$), leg-byes and byes are recorded as `runs = 0` regardless of whether 1, 2, 3, or 4 runs were taken.
  - *Impact on Batting*: Zero impact (batters are only credited with bat runs).
  - *Impact on Bowling*: Zero impact (byes and leg-byes are not charged to the bowler).
  - *Impact on Team Score Reconstruction*: Reconstructed team totals exhibit an empirical variance of $\pm 3$ to $5$ runs per innings against scorecard margins.

### 4.2 Legal Ball Counting
- `innings_ball_num`: Increments sequentially across **all** deliveries, including wides and no-balls (reaches up to 136). **Must NOT be used as legal ball count**.
- `is_legal_ball`: Must be derived as `extras_type NOT IN ('wide', 'Overstep', 'other')`.
- Out of 200,999 total deliveries, exactly **192,445 are legal deliveries (95.74%)**.

### 4.3 Dismissal Fields
- Exactly **10,881 wickets** fall in the dataset.
- `is_wicket == True` matches `dismissal_type.notna()` with zero discrepancy.
- Categorization into bowler-credited wickets:
  - **Bowler Wickets** (10,272): `Caught` (7,557), `Bowled` (1,775), `LBW` (709), `Stump` (214), `Hit Wicket` (17).
  - **Team / Non-Bowler Dismissals** (609): `RunOut` (600), `Retire Out` (6), `Obstructing the field` (3).
- **Data Cleaning Requirement**: Correct typographical error in `dismissal_type`: `"Obstracting the field"` (2 rows) $\to$ `"Obstructing the field"`.

### 4.4 Revised-Target & Shortened Match Fields
- `first_inn_revised_overs` and `second_inn_revised_overs`:
  - ⚠️ **Critical Unit Finding**: Despite the column name `"revised_overs"`, values are stored in **total legal BALLS** (e.g. 114.0 = 19 overs, 90.0 = 15 overs, 48.0 = 8 overs, 30.0 = 5 overs). Multiplying by 6 produces an erroneous 6x inflation.
- Exactly 34 matches have revised parameters; 23 matches have an explicit `revised_target`.

---

## 5. Potential Data Leakage Audit & Mitigations

| Leakage Risk Category | High-Risk Fields | Nature of Leakage | Mitigation Enforced |
|---|---|---|---|
| **Post-Match Outcome Leakage** | `win_team_id`, `result`, `man_of_the_match` in `matches.csv` | Knowing who won or who was player-of-the-match leaks the outcome into early-innings predictions. | Strictly excluded from all delivery-level feature sets. |
| **Intra-Match Future Leakage** | `inn1_final_score`, future wickets, future balls | Using the final 1st innings total during over 5 of the 1st innings leaks future team success. | 1st innings state is benchmarked against **par trajectory models** (Duckworth-Lewis resource curves), never the actual final score. |
| **Player Career Statistic Leakage** | Current or future match performance in rolling stats | Using a batter's runs from today's match to predict today's delivery leaks future performance into features. | Historical stats are computed using an **expanding window lagged strictly before the match date** (`match_date < current_match_date`). |
| **Post-Delivery Event Leakage** | `stroke`, `bowl_speed`, `on_or_off` | Predicting whether a ball will be a boundary using the shot chosen or speed bowled introduces post-event information. | Expected outcome models condition strictly on **pre-delivery state**: score, phase, wickets, RRR, prior player form, and matchup style. |

---

## 6. Complete Feature Feasibility Matrix

This matrix establishes which proposed features are directly calculable from the dataset, which require mathematical derivation/estimation, and which are impossible.

| Feature Name | Category | Status | Derivation Logic / Data Source | Caveats / Limitations |
|---|---|:---:|---|---|
| `innings` | Match State | ✅ **Calculable** | `ball_by_ball.innings` (1, 2) | Super overs (3, 4) excluded |
| `overid` / `over_ball_num` | Match State | ✅ **Calculable** | `ball_by_ball.overid`, `over_ball_num` | Includes extras |
| `legal_balls_bowled_before` | Match State | ✅ **Calculable** | `cumsum(~(is_wide | is_noball)) - current` | Reconstructed per innings |
| `balls_remaining_before` | Match State | ✅ **Calculable** | `max_balls - legal_balls_bowled_before` | Adjusted by `second_inn_revised_overs` |
| `wickets_lost_before` | Match State | ✅ **Calculable** | `cumsum(is_wicket) - current` | 0 to 9 |
| `wickets_remaining_before` | Match State | ✅ **Calculable** | `10 - wickets_lost_before` | 1 to 10 |
| `phase` | Match State | ✅ **Calculable** | Powerplay (<36), Middle (36-89), Death (90-120) | Based on legal balls bowled |
| `team_runs_before` | Match State | ⚠️ **Estimated** | `cumsum(est_total_runs) - current` | $\pm 3\text{--}5$ run variance from leg-bye gap |
| `current_run_rate_before` | Match State | ⚠️ **Estimated** | `team_runs_before / (legal_balls / 6.0)` | Subject to small leg-bye variance |
| `runs_required_before` | Chase Dynamic | ⚠️ **Estimated** | `target_score - team_runs_before` (Inn 2) | Exact when revised target provided |
| `required_run_rate_before` | Chase Dynamic | ⚠️ **Estimated** | `runs_required / (balls_remaining / 6.0)` | Clipped to $[2, 24]$ for stability |
| `first_innings_par_score` | 1st Inn Trajectory | 💡 **Modeled** | Empirical Duckworth-Lewis resource curves | Calibrated on 105K 1st inn deliveries |
| `runs_above_par_trajectory` | 1st Inn Trajectory | 💡 **Modeled** | `team_runs_before - par_expected_at_ball` | Replaces RRR in 1st innings |
| `batting_order` | Player Context | ✅ **Calculable** | `ball_by_ball.batting_order` (1 to 13) | 12/13 are impact substitutions |
| `batting_role` | Player Context | ✅ **Calculable** | Top Order (1-3), Middle (4-6), Finisher (7+) | Derived from batting order |
| `batting_type` | Matchup | ✅ **Calculable** | `RHB` vs `LHB` | 100% complete in data |
| `bowling_type` | Matchup | ✅ **Calculable** | 12 standardized styles | 100% complete in data |
| `pace_or_spin` | Matchup | ✅ **Calculable** | `Pace` vs `Spin` | 100% complete in data |
| `stage` / `is_knockout_stage` | Match Leverage | ✅ **Calculable** | `matches.stage`, `knock_out == 1` | Playoff/Knockout flag |
| `comp_category` | Context | ✅ **Calculable** | `IPL`, `T20I`, `Other_T20` | Derived from `comp_name` & `match_format` |
| `venue_id` / `venue_country` | Context | ✅ **Calculable** | `matches.venue_id`, `matches.venue_country` | 98 venues, 17 countries |
| `hist_batter_sr` / `avg` | Historical Ability | 💡 **Modeled** | Expanding window strictly on `date < match_date` | Empirical Bayes smoothed ($m=30$) |
| `hist_bowler_econ` / `sr` | Historical Ability | 💡 **Modeled** | Expanding window strictly on `date < match_date` | Empirical Bayes smoothed ($m=30$) |
| `bpi` (Batting Pressure Index) | Pressure Model | 💡 **Modeled** | 4-component continuous $[0, 100]$ index | External difficulty only |
| `bopi` (Bowling Pressure Index) | Pressure Model | 💡 **Modeled** | 4-component continuous $[0, 100]$ index | External difficulty only |
| `expected_runs` / `wicket_prob` | Expected Outcome | 💡 **Modeled** | Multi-target LightGBM models | Calibrated probabilities ($Brier \approx 0.05$) |
| `pava_bat` / `pava_bowl` | Value Added | 💡 **Modeled** | $(\text{Actual} - \text{Expected}) \times (1 + \text{Pressure}/50)$ | Phase-aware wicket run equivalents |
| `exact_leg_bye_runs` | Scoring | ❌ **Impossible** | Not stored in any column | Defaults to $1$ run per event |
| `exact_delivery_time` | Match Time | ❌ **Impossible** | All timestamps set to `00:00:00 UTC` | Only calendar date is usable |
| `bowl_speed` | Sensor Data | ❌ **Unusable** | 38.7% zeros; extreme sensor errors | Excluded from predictive models |
| `field_placements` / `lengths` | Spatial Context | ❌ **Impossible** | No tracking coordinates provided | Only categorical stroke/side recorded |
