# PHASE 03: Pressure Indices (BPI & BoPI) Plan

## Goal
Formulate continuous 0–100 Batting Pressure Index (BPI) and Bowling Pressure Index (BoPI) reflecting contextual difficulty.

## Tasks
1. Batting Pressure Index (BPI) components:
   - Rate Demand: RRR relative to baseline par.
   - Resource Scarcity: Wickets lost vs balls remaining.
   - Temporal Climax: Innings over progression weighting death overs.
   - Match Leverage: Closeness of required score and tournament stakes.
2. Bowling Pressure Index (BoPI) components:
   - Target Defense Urgency: Defending low total or defending tight margin.
   - Resource Scarcity: Batter wickets in hand.
   - Death Climax: Volatility of late overs.
   - Close Finish Leverage: High boundary penalty situations.
3. Normalization and calibration:
   - Rescale to continuous $[0, 100]$ interval with calibrated median ~45.
   - Categorize into tiers (`Low`, `Medium`, `High`, `Extreme`).
4. Unit Tests:
   - `tests/test_pressure_index.py` verifying monotonicity, bounds, and tier mapping.

## Acceptance Criteria
- BPI and BoPI populated for all 200,961 deliveries.
- 100% of unit tests pass.
