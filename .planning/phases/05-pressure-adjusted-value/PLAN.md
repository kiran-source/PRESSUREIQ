# PHASE 05: Pressure-Adjusted Value Added (PAVA) Plan

## Goal
Quantify performance above or below expected outcomes weighted continuously by delivery pressure.

## Tasks
1. Delivery Value Formulation:
   - Batting: $(\text{bat\_runs} - E[\text{bat\_runs}]) - (\text{is\_dismissal} - P(\text{dismissal})) \times V_{\text{wicket}}(\text{phase})$.
   - Bowling: $(E[\text{runs\_conceded}] - \text{runs\_conceded}) + (\text{is\_wicket} - P(\text{wicket})) \times V_{\text{wicket}}(\text{phase})$.
   - Phase-aware wicket valuations: Powerplay: 5.2 runs, Middle: 4.5 runs, Death: 3.6 runs.
2. Continuous Pressure Multiplier:
   - Scale delivery value by $1.0 + \frac{\text{Pressure}}{50.0}$.
3. Aggregation:
   - Aggregate delivery PAVA into player-innings (`data/processed/batter_innings_pava.parquet`) and player-spells (`data/processed/bowler_spell_pava.parquet`).
   - Store delivery table with PAVA in `data/processed/deliveries_with_pava.parquet`.

## Acceptance Criteria
- Full delivery PAVA calculated across all 200,961 deliveries.
- Aggregated innings and spell tables created.

