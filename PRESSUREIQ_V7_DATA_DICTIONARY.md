# PRESSUREIQ V7.0 — Data Dictionary

**Complete field-level documentation for all processed datasets**

---

## 1. `final_batter_rankings.csv` — FROZEN MODEL A

> **SHA-256:** `887f0c104047eb7b5c7d662b83600bacaf6263fa7162fc343b27800760b99b87`
> **Do not modify or regenerate.**

| Column | Type | Description |
|---|---|---|
| `rank` | int | Final Model A pressure rank (1 = best) |
| `player_name` | str | Player full name (canonical) |
| `player_id` | str | Canonical player identifier |
| `team` | str | IPL franchise abbreviation |
| `role` | str | Batting role (e.g. `top_order`, `middle_order`, `finisher`) |
| `reliability_score` | float | Composite Reliability Score (0–100). `Φ(Z_composite) × 100` |
| `ci_lower_95` | float | 2,000-bootstrap 2.5th percentile (lower 95% CI bound) |
| `ci_upper_95` | float | 2,000-bootstrap 97.5th percentile (upper 95% CI bound) |
| `hp_balls` | int | Total high-pressure balls faced (qualification gate ≥ 30) |
| `kish_match_ess` | float | Kish Effective Sample Size across matches |
| `top10_inclusion_prob_pct` | float | % of bootstrap samples where player appears in Top 10 |
| `score_ci_95` | str | Formatted string `[lower, upper]` of 95% CI |
| `bpi` | float | Batter Pressure Index — opportunity-adjusted batting value above expectation |
| `bpi_normalized` | float | BPI normalized to 0–100 scale across cohort |
| `hp_sr_above_exp` | float | High-pressure strike rate above expected baseline |
| `hp_avg_above_exp` | float | High-pressure average above expected baseline |
| `wicket_avoidance_index` | float | Wicket avoidance score in pressure situations |
| `death_overs_bpi` | float | BPI restricted to death-overs situations |
| `powerplay_bpi` | float | BPI restricted to powerplay situations |
| `middle_overs_bpi` | float | BPI restricted to middle-overs situations |

---

## 2. `final_bowler_rankings.csv` — FROZEN MODEL A

> **SHA-256:** `344d63c55cecc7bce9de3cd06d82b6ac8217fcd448bb3f2e93d55da314f1e7bb`
> **Do not modify or regenerate.**

| Column | Type | Description |
|---|---|---|
| `rank` | int | Final Model A pressure rank (1 = best) |
| `player_name` | str | Player full name (canonical) |
| `player_id` | str | Canonical player identifier |
| `team` | str | IPL franchise abbreviation |
| `pace_or_spin` | str | Bowling type (`Pace` or `Spin`) |
| `bowling_type` | str | Detailed bowling type (e.g. `Right arm pace`, `Left arm spin`) |
| `reliability_score` | float | Composite Reliability Score (0–100). `Φ(Z_composite) × 100` |
| `ci_lower_95` | float | 2,000-bootstrap 2.5th percentile |
| `ci_upper_95` | float | 2,000-bootstrap 97.5th percentile |
| `hp_balls` | int | Total high-pressure balls bowled (qualification gate ≥ 30) |
| `kish_match_ess` | float | Kish Effective Sample Size across matches |
| `top10_inclusion_prob_pct` | float | % of bootstrap samples where player appears in Top 10 |
| `score_ci_95` | str | Formatted `[lower, upper]` string |
| `bopi` | float | Bowler Pressure Index — wicket value above expectation |
| `bopi_normalized` | float | BoPI normalized 0–100 |
| `hp_economy_above_exp` | float | High-pressure economy rate above expected baseline |
| `hp_wicket_rate_above_exp` | float | High-pressure wicket rate above expected |
| `death_overs_bopi` | float | BoPI restricted to death overs |
| `powerplay_bopi` | float | BoPI restricted to powerplay |

---

## 3. `ipl_2027_franchise_accounting_reconciliation.csv`

Full player-level ledger for all 10 IPL franchises.

| Column | Type | Description |
|---|---|---|
| `canonical_player_id` | str | Unique player identifier |
| `player_name` | str | Player full name |
| `franchise` | str | IPL franchise abbreviation |
| `prior_squad_membership` | bool | Was player in 2026 season squad? |
| `status_2027` | str | One of: `Retained`, `Released`, `Traded In`, `Traded Out`, `Retired`, `Opt Out`, `Pending Verification (Extended Pool)` |
| `retention_category` | str | Categorization for accounting (e.g., `Core`, `Extended Pool`) |
| `trade_partner` | str | Destination/source franchise for traded players |
| `trade_fee_cr` | float | Trade fee in crore rupees (where applicable) |
| `evidence_source` | str | Primary evidence source URL or description |
| `evidence_type` | str | `Official BCCI`, `Official Franchise`, `Official IPL Social Media`, `Media Report`, `Pending` |
| `verification_timestamp` | str | ISO timestamp of last verification |

---

## 4. `ipl_2027_player_market_template.csv`

IPL 2027 auction market intelligence snapshot (anchored: 2026-11-11).

| Column | Type | Description |
|---|---|---|
| `player_id` | str | Canonical player identifier |
| `player_name` | str | Player full name |
| `discipline` | str | `Batting`, `Bowling`, or `All-Rounder` |
| `nationality` | str | Citizenship (affects overseas slot eligibility) |
| `age_at_auction` | int | Age at time of IPL 2027 auction |
| `ipl_franchise_2026` | str | 2026 season franchise or `None` |
| `market_status_2027` | str | `Available`, `Retained`, `Traded`, `Released`, `Retired`, `Pending` |
| `base_price_cr` | float | Estimated base price in crore rupees |
| `reliability_score` | float | Model A pressure reliability score (if qualified) |
| `rr_target_priority` | str | `Primary`, `Secondary`, `Watchlist`, or `—` (not relevant) |
| `rr_eligible` | bool | Eligible for RR to bid (not retained by other franchise) |
| `overseas_player` | bool | True if overseas slot required |

---

## 5. `ipl_2027_market_change_log.csv`

Audit trail of all changes to market status since the Nov-11 snapshot.

| Column | Type | Description |
|---|---|---|
| `change_id` | str | Unique change identifier |
| `player_id` | str | Canonical player identifier |
| `player_name` | str | Player name |
| `change_type` | str | `Status Update`, `New Entry`, `Correction`, `Evidence Upgrade` |
| `old_value` | str | Previous field value |
| `new_value` | str | Updated field value |
| `evidence_url` | str | Supporting source URL |
| `changed_at` | str | ISO timestamp of change |
| `changed_by` | str | Pipeline/audit version that made the change |

---

## 6. High-Pressure Definition

A delivery is classified as **high-pressure (HP)** when two or more of the following situational flags are active simultaneously:

| Flag | Threshold |
|---|---|
| **Chase pressure** | Target ≥ 140, run rate deficit ≥ 1.0 rr/over in final 5 overs |
| **Win probability volatility** | ΔWP ≥ 0.08 per ball (PAVA-derived) |
| **Phase pressure** | Death overs (17–20) OR Powerplay with ≥ 3 wickets fallen |
| **Match criticality** | Knockout match / final / must-win scenario |
| **Partnership pressure** | Wicket in last 2 balls or new batter ≤ 3 balls faced |

**Dataset scope:** 200,999 deliveries across 867 played T20 matches (200,961 regular + 38 Super Over balls).

---

*PRESSUREIQ V7.0 — Data Dictionary*
*Rajasthan Royals SupeRR Selector Season 2 | November 2026*
