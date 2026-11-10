# PHASE 00: Project Discovery & Schema Audit Plan

## Goal
Audit all 6 raw CSV files in `SupeRR Selector Season 2 _ Data Pack/`, profile column schemas, data types, missing values, foreign key integrity, and temporal coverage without modifying raw files.

## Tasks
1. Audit row counts, file sizes, column schemas for:
   - `matches.csv` (883 rows)
   - `deliveries.csv` (200,999 rows)
   - `playing_eleven.csv` (19,426 rows)
   - `players.csv` (959 rows)
   - `competitions.csv` (141 rows)
   - `venues.csv` (107 rows)
2. Identify data anomalies:
   - `runs` stores only bat runs.
   - `extras1_runs` is a categorical integer code.
   - Leg-bye and bye actual run quantities are omitted.
   - `second_inn_revised_overs` is stored in legal balls.
   - Bowl speed sensor noise (outliers up to 1456 km/h, 38.7% zeros).
3. Produce `docs/DATA_INVENTORY_AND_FEASIBILITY.md`.

## Acceptance Criteria
- Full data inventory generated.
- Raw CSV files remain 100% untouched.
