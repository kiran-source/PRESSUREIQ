# PHASE 02: Match State & Temporal Features Plan

## Goal
Engineer delivery-level features using strictly causal pre-delivery information (zero future leakage).

## Tasks
1. `src/features/first_innings_par.py`:
   - Empirical Duckworth-Lewis resource depletion curve for 1st innings par score estimation based on balls and wickets remaining.
2. `src/features/player_history.py`:
   - Expanding-window career statistics for batters and bowlers.
   - Filter strictly to prior matches (`match_date < current_match_date`).
   - Empirical Bayes shrinkage ($m=30$ pseudo-balls) for cold starts.
3. `src/features/feature_builder.py`:
   - Combine match context, score state, phase, bowler role, batter order, and player historical statistics into 93 features.
   - Save to `data/processed/features_deliveries.parquet`.
4. Unit Tests:
   - `tests/test_features.py` verifying zero leakage and resource model behavior.

## Acceptance Criteria
- 200,961 deliveries processed (super overs excluded).
- Zero post-match fields present as features.
