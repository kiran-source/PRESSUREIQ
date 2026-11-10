# PHASE 01: Data Engineering & State Reconstruction Plan

## Goal
Build reproducible data cleaning, normalization, legal delivery accounting, and match state reconstruction pipelines. Convert raw CSVs into typed, compressed Parquet tables queried with DuckDB.

## Tasks
1. `src/data/cleaner.py`:
   - Text normalization, string boolean conversions.
   - Clean dismissal typos (`Obstracting` $\to$ `Obstructing`).
2. `src/data/state_reconstruction.py`:
   - Reconstruct legal balls (`is_legal_ball = extras_type NOT IN ('wide', 'Overstep', 'other')`).
   - Reconstruct cumulative team score, wickets lost, wickets remaining, and balls remaining.
   - Reconstruct 2nd innings targets (DLS revised targets where applicable).
   - Reconstruct bowler runs conceded (bat runs + wide/no-ball extras).
3. `src/data/pipeline.py`:
   - Orchestrate end-to-end ingestion and write to `data/processed/`.
4. Unit Tests:
   - `tests/test_data_cleaning.py` and `tests/test_state_reconstruction.py`.

## Acceptance Criteria
- `data/processed/deliveries.parquet` (200,999 rows) and `matches.parquet` (883 rows) created.
- All unit tests pass.
