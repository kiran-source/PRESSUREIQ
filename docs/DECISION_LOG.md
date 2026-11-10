# PRESSUREIQ — Architecture & Data Engineering Decision Log

## Decision 001: Data Ingestion and Parquet Architecture
- **Date**: 2026-11-10
- **Context**: The raw data pack contains 6 CSV files including a 41MB `ball_by_ball.csv` (200,999 rows). Querying large CSVs repeatedly in ML pipelines causes high I/O latency and type coercion overhead.
- **Decision**: Convert all cleaned datasets to columnar Parquet files with compressed snacky encoding and load via DuckDB / Polars / Pandas. The raw CSV files are strictly preserved unmodified in their original directory.
- **Consequences**: Delivery dataset size reduced from 41.1 MB CSV to 6.5 MB Parquet (~84% compression). Querying and filtering speeds improved by >10x.

## Decision 002: Legal Ball and Extras Accounting
- **Date**: 2026-11-10
- **Context**: In `ball_by_ball.csv`, `innings_ball_num` increments sequentially across all deliveries, including non-legal balls (wides, no-balls). `extras1_runs` represents a categorical code (1=Overstep, 2=Wide, 3=Legbyes, 4=Byes, 5=Other, 6=None, 7=Penalty) rather than raw run values.
- **Decision**:
  - `is_legal_ball`: Defined as `extras_type NOT IN ('wide', 'Overstep', 'other')`. Leg byes and byes are legal balls.
  - `batter_runs`: Mapped directly from `runs` (bat-off-bat runs).
  - `bowler_extras`: Wides and no-balls incur 1 run penalty + `extras_2_runs` (overthrows). Byes and leg-byes are not attributed to bowlers (adhering to official MCC Laws of Cricket Law 21 & 22).
  - `cum_legal_balls`: Calculated intra-innings via cumulative sum of `is_legal_ball`.

## Decision 003: Handling Leg-Bye and Bye Run Limitations
- **Date**: 2026-11-10
- **Context**: In Phase 0 data discovery, empirical validation against 345 non-DLS match score margins revealed that actual run values for leg-byes and byes (which can range from 1 to 4 runs) are not explicitly stored in any column.
- **Decision**:
  - For batter performance metrics: completely unaffected, as batter runs only come from bat contact (`runs` column).
  - For bowler performance metrics: completely unaffected, as byes and leg-byes are excluded from bowler runs conceded.
  - For team score accumulation: each leg-bye and bye event is credited with `max(1, extras_2_runs)` runs. The ±3 to 5 run variance across a full innings is transparently documented in model limitations.

## Decision 004: Revised Overs Column Semantics
- **Date**: 2026-11-10
- **Context**: `matches.csv` contains `first_inn_revised_overs` and `second_inn_revised_overs`. Inspection showed values such as 114.0, 90.0, 48.0, 30.0.
- **Decision**: These values are already expressed in total BALLS (e.g. 114 balls = 19 overs, 90 balls = 15 overs, 30 balls = 5 overs). They must NOT be multiplied by 6.
- **Consequences**: Prevented an overt 6x overestimation of available balls in shortened/DLS matches.

## Decision 005: Strict Temporal Validity (No Future Leakage)
- **Date**: 2026-11-10
- **Context**: Machine learning models and pressure metrics must only use information available before the delivery occurs.
- **Decision**: Every delivery-level feature reflects the state strictly *before* the delivery is bowled (`team_runs_before`, `wickets_lost_before`, `balls_remaining_before`, `required_run_rate_before`, `batter_balls_faced_before`, `bowler_economy_before`).
- **Consequences**: Zero leakage of post-delivery or post-match outcomes into contextual pressure features.

## Decision 006: Super Overs Exclusion
- **Date**: 2026-11-10
- **Context**: Innings 3 and 4 appear in 5 matches (38 total deliveries). Super overs operate under completely separate game mechanics, player selection constraints, and risk-reward profiles.
- **Decision**: Filter out innings >= 3 from standard 20-over pressure modeling and player evaluation rankings to preserve metric consistency.

