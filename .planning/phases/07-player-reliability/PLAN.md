# PHASE 07: Player Reliability Rankings Plan

## Goal
Apply Empirical Bayes shrinkage ($K=45$ balls) and transparent eligibility filters to produce final official rankings for batters and bowlers.

## Tasks
1. Empirical Bayes Shrinkage:
   - Shrink raw high-pressure PAVA towards empirical population prior:
     $$\text{Shrunk PAVA} = \frac{N_{\text{hp}}}{N_{\text{hp}} + K} \cdot \text{PAVA}_{\text{hp}} + \frac{K}{N_{\text{hp}} + K} \cdot \mu_{\text{prior}}$$
   - Prevents small sample anomalies (e.g. 10 balls) from skewing leaderboard.
2. Eligibility Filters:
   - Batters: $\ge 400$ total career balls, $\ge 30$ high-pressure balls, $\ge 20$ innings.
   - Bowlers: $\ge 400$ total career balls, $\ge 30$ high-pressure balls, $\ge 20$ spells.
3. Official Rankings Output:
   - Generate `data/processed/final_batter_rankings.csv` (58 qualified).
   - Generate `data/processed/final_bowler_rankings.csv` (72 qualified).
   - Output official Top 10 Batters and Top 10 Bowlers.

## Acceptance Criteria
- Official Top 10 Batters and Bowlers finalized without manual intervention or data fabrication.
