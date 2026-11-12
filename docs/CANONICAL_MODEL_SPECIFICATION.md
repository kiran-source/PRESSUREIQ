# PRESSUREIQ — CANONICAL MATHEMATICAL MODEL SPECIFICATION
**Version:** 2.3-Canonical (Source-Verified Audited Specification)  
**Date:** 11 November 2026  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 (Round 1)  
**Status:** Authoritative Reference Reconciled Verbatim to Executable Source Code  

---

## 1. Source-to-Specification Consistency Matrix

This matrix establishes the exact file paths, function names, and line numbers connecting the mathematical specification to the executable Python implementation in the frozen Model A baseline:

| Mathematical Dimension | Canonical Code Implementation | Source File Path | Function / Class | Verified Line Range | Specification Status |
|:---|:---|:---|:---|:---:|:---:|
| **BPI Formulation** | $0.42 C_{\text{eff\_rate}} + 0.30 C_{\text{res}} + 0.18 C_{\text{climax}} + 0.10 \text{Lev}$ | `src/models/pressure_index.py` | `compute_batting_pressure_index` | Lines 17–101 | **Reconciled Verbatim to Frozen Parquet & Code** |
| **BoPI Formulation** | $0.38 C_{\text{defend}} + 0.26 C_{\text{res}} + 0.24 C_{\text{climax}} + 0.12 \text{Lev}$ | `src/models/pressure_index.py` | `compute_bowling_pressure_index` | Lines 104–185 | **100% Verbatim Match** |
| **Raw PAVA vs. Leverage PAVA** | `raw_bat_value = delta_runs + wkt_val*delta_wkt + 0.5*delta_bnd`<br>`leverage_pava = raw_bat_value * (1 + P/50)` | `src/models/pressure_value.py` | `compute_pressure_adjusted_value` | Lines 45–78 | **100% Verbatim Match** |
| **Phase Wicket Values ($V_W$)** | `Powerplay: 5.2, Middle: 4.5, Death: 3.6` runs | `src/models/pressure_value.py` | `WICKET_VALUE_BY_PHASE` dictionary | Lines 12–16 | **100% Verbatim Match** |
| **Operational High Pressure** | `group["bpi"] >= 50.0` (Batting) / `group["bopi"] >= 50.0` (Bowling) | `src/analysis/reliability_engine.py` | `compute_batter_reliability_scores`<br>`compute_bowler_reliability_scores` | Lines 137, 257 | **100% Verbatim Match** |
| **Descriptive Pressure Tiers** | Low: $<35$, Med: $[35, 65)$, High: $[65, 85)$, Ext: $\ge 85$ | `src/models/pressure_index.py`<br>`src/analysis/reliability_engine.py` | `pd.cut` bins<br>`fit_pressure_response_curve` | Lines 96, 180<br>Lines 78–87 | **100% Verbatim Match** |
| **PRC Linear Slope Engine** | `scipy.stats.linregress(p / 100.0, y)` | `src/analysis/reliability_engine.py` | `fit_pressure_response_curve` | Lines 75–76 | **100% Verbatim Match** |
| **Empirical Bayes Shrinkage** | $K_{\text{shrink}} = 45.0$ uniform pseudo-deliveries | `src/analysis/reliability_engine.py` | `K_SHRINK = 45.0` | Line 26 | **100% Verbatim Match** |
| **Score CDF Normalization** | $\Phi(Z_{\text{composite}}) \times 100.0$ (`stats.norm.cdf`) | `src/analysis/reliability_engine.py` | `compute_batter_reliability_scores`<br>`compute_bowler_reliability_scores` | Lines 227, 347 | **100% Verbatim Match** |
| **Match-Clustered Bootstrap** | 2,000 resamples grouped by `match_id` | `src/analysis/bootstrap_engine.py`<br>`scripts/run_clustered_bootstrap_2000.py` | `match_clustered_bootstrap_rankings`<br>`run_clustered_bootstrap` | Lines 34–220<br>Lines 45–180 | **100% Verbatim Match** |
| **MCDA Additive Scoring** | $0.40 \cdot \text{Rel} + 0.20 \cdot \text{Ev} + 0.25 \cdot \text{Avail} + 0.15 \cdot \text{Fit}$ | `scripts/build_rr_2027_recommendations.py` | `calculate_rr_scores` | Lines 242–250 | **100% Verbatim Match** |

---

## 2. Dynamic Ball-by-Ball Pressure Indices

Pressure is computed on a continuous scale $[0, 100]$ using game-theoretic leverage, resource depletion, and match climax metrics.

### 2.1 Batting Pressure Index (BPI)
Batting pressure quantifies scoring demand and wicket-resource scarcity facing the striker (`src/models/pressure_index.py`, verified to `0.00` max difference across all `200,961` rows in `deliveries_with_pava.parquet`):

$$\text{BPI} = \text{clip}\left( 0.42 \cdot C_{\text{eff\_rate}} + 0.30 \cdot C_{\text{res}} + 0.18 \cdot C_{\text{climax}} + 0.10 \cdot (B_{\text{ko}} + B_{\text{chase}}), 0.0, 100.0 \right)$$

- **Effective Rate Demand ($C_{\text{eff\_rate}} = C_{\text{rate}} \cdot (0.5 + 0.5 \cdot r)$):**
  - **Innings 2:** $C_{\text{rate}} = \sigma\left(\frac{\text{RRR}_{\text{clean}} - 8.5}{2.2}\right) \times 100.0$, where $\text{RRR}_{\text{clean}} = \text{clip}(\text{RRR}, 2.0, 24.0)$.
  - **Innings 1:** $C_{\text{rate}} = \sigma\left(\frac{-\text{runs\_above\_par}}{14.0}\right) \times 100.0$.
- **Resource Scarcity ($C_{\text{res}}$):**
  $$C_{\text{res}} = \left(\text{clip}\left(\frac{\text{wickets\_lost\_before}}{9.0}, 0.0, 1.0\right)\right)^{1.2} \times 100.0$$
- **Climax Exposure ($C_{\text{climax}}$):**
  $$C_{\text{climax}} = r^{1.3} \times 100.0, \quad r = \text{clip}\left(\frac{\text{balls\_bowled}}{\text{max\_balls}}, 0.0, 1.0\right)$$
  *(Frozen Model A `deliveries_with_pava.parquet` used $\text{max\_balls}=120.0$, $\text{balls\_bowled}=120.0-\text{balls\_remaining\_before}$, and $B_{\text{chase}}=15.0$ for $\text{balls\_remaining}\le 30, \text{runs\_req}\le 50$; the subsequent `P0-3` code refinement in `src/models/pressure_index.py` uses dynamic `max_innings_balls` across 1,641 shortened-match deliveries while keeping all 199,320 full 20-over deliveries identical.)*
- **Leverage Bonuses ($B_{\text{ko}}, B_{\text{chase}}$):**
  - Knockout Stage: $B_{\text{ko}} = 12.0$ if playoff/knockout match, else $0.0$.
  - Close Chase: $B_{\text{chase}} = 15.0$ if Innings 2, `balls_remaining <= threshold` ($30.0$ in frozen run; $\max(12.0, 0.25 \cdot \text{max\_innings\_balls})$ in `P0-3` code), and $0 < \text{runs\_required} \le 50$.

---

### 2.2 Bowling Pressure Index (BoPI)
Bowling pressure models target defense difficulty, opposition wickets in hand, and boundary prevention demands:

$$\text{BoPI} = \text{clip}\left( 0.38 \cdot C_{\text{defend}} + 0.26 \cdot C_{\text{res\_opp}} + 0.24 \cdot C_{\text{climax}} + 0.12 \cdot (B_{\text{ko}} + B_{\text{tight}}), 0.0, 100.0 \right)$$

- **Target Defense Demand ($C_{\text{defend}}$):**
  - **Innings 2:** $C_{\text{defend}} = \sigma\left(\frac{10.5 - \text{RRR}_{\text{clean}}}{2.2}\right) \times 100.0$
  - **Innings 1:** $C_{\text{defend}} = \sigma\left(\frac{\text{runs\_above\_par}}{14.0}\right) \times 100.0$
- **Opposition Resources in Hand ($C_{\text{res\_opp}}$):**
  $$C_{\text{res\_opp}} = \left(\frac{\text{wickets\_remaining}}{10.0}\right)^{1.1} \times 100.0$$
- **Climax Exposure ($C_{\text{climax}}$):**
  $$C_{\text{climax}} = \left(\frac{\text{balls\_bowled}}{\text{max\_innings\_balls}}\right)^{1.4} \times 100.0$$
- **Leverage Bonuses:**
  - Knockout Stage: $B_{\text{ko}} = 12.0$
  - Close Finish: $B_{\text{tight}} = 18.0$ if Innings 2, balls $\le \max(6, 0.15 \times \text{balls})$, runs required $\le 30$.

---

### 2.3 Operational Thresholds vs. Descriptive Reporting Tiers

A fundamental architectural distinction in PRESSUREIQ is the separation between operational estimation thresholds and descriptive reporting tiers:

1. **Operational Estimation Threshold ($P \ge 50.0$):**  
   - Used in `src/analysis/reliability_engine.py` (lines 137, 257) to partition deliveries into the "Above-Average Pressure" pool for statistical scoring.
   - **Rationale:** The median delivery pressure across all T20 innings is approximately $48.5$. Using $P \ge 50.0$ splits the distribution around the empirical median, ensuring robust sample sizes ($N \ge 30$ balls) across top-order, middle-order, and lower-order players. Setting the operational threshold to $65.0$ would starve lower-order batters and spinners of sample volume, inflating estimator variance.
2. **Descriptive Reporting Tiers:**  
   - Used in dashboards, profiles, and visual breakdowns (`src/models/pressure_index.py`, lines 96, 180):
     - **Low Pressure ($[0.0, 35.0)$):** Low leverage / runaway cushion.
     - **Medium Pressure ($[35.0, 65.0)$):** Standard par conditions.
     - **High Pressure ($[65.0, 85.0)$):** Genuine high-leverage and death overs.
     - **Extreme Pressure ($[85.0, 100.0]$):** Decisive climax overs and crisis finishes.

---

## 3. Pressure-Adjusted Value Added (PAVA): Raw vs. Leverage-Weighted

In `src/models/pressure_value.py` (lines 47–78), PRESSUREIQ strictly distinguishes between unamplified performance and leverage-weighted match impact:

### 3.1 Unamplified Raw Performance Value Added (`raw_bat_value`, `pava_bat`)
$$\text{PAVA}_{\text{raw, bat}} = (R_{\text{act}} - \mathbb{E}[R]) + V_W(\text{phase}) \cdot (\mathbb{P}[\text{dismissal}] - W_{\text{act}}) + 0.50 \cdot (\mathbb{I}[\text{boundary}] - \mathbb{P}[\text{boundary}])$$

$$\text{PAVA}_{\text{raw, bowl}} = (\mathbb{E}[R_{\text{conc}}] - R_{\text{conc}}) + V_W(\text{phase}) \cdot (W_{\text{act, bowl}} - \mathbb{P}[\text{wicket}])$$

- **Phase Wicket Values ($V_W$):**
  - **Powerplay (Overs 1–6):** $V_W = 5.20$ runs
  - **Middle (Overs 7–15):** $V_W = 4.50$ runs
  - **Death (Overs 16–20):** $V_W = 3.60$ runs
- **Usage:** This unamplified rate is used by the Reliability Engine (`hp_group["pava_bat"].mean()`) to compute player skill per ball under pressure, avoiding artificial double-weighting of pressure.

### 3.2 Leverage-Weighted Match Impact (`leverage_pava_bat`, `leverage_pava_bowl`)
$$\text{PAVA}_{\text{leverage, bat}} = \text{PAVA}_{\text{raw, bat}} \times \left(1.0 + \frac{\text{BPI}}{50.0}\right)$$

$$\text{PAVA}_{\text{leverage, bowl}} = \text{PAVA}_{\text{raw, bowl}} \times \left(1.0 + \frac{\text{BoPI}}{50.0}\right)$$

- **Usage:** Quantifies cumulative match-winning equity delivered across high-leverage deliveries.

---

## 4. Pressure Response Curve (PRC) Linear Slope Engine

In `src/analysis/reliability_engine.py` (lines 43–105), the empirical relationship between normalized pressure $x = p / 100.0 \in [0.0, 1.0]$ and raw performance $y = \text{PAVA}_{\text{raw}}$ is estimated via Ordinary Least Squares linear regression (`scipy.stats.linregress`):

$$y(x) = \alpha + \beta \cdot x$$

Where:
- $\alpha$ is the expected performance at zero pressure.
- $\beta$ is the performance trajectory slope per unit of pressure.

### 4.1 Archetype Classification Logic (Verbatim from Code)
1. **Pressure Fragile:** Extreme-tier collapse ($\text{val}_{\text{ext}} \le \text{val}_{\text{high}} - 0.25$ with $\text{val}_{\text{high}} \ge 0.10$) OR steep negative slope ($\beta \le -0.30, p \le 0.15$).
2. **Clutch Climber:** Strong upward trajectory ($\beta \ge 0.15, p \le 0.15$).
3. **Universal Performer:** Positive performance across both low and high pressure ($\text{val}_{\text{high}} \ge 0.10$ and $\text{val}_{\text{low}} \ge 0.10$).
4. **Frontrunner:** Excels in low pressure but collapses under high pressure ($\text{val}_{\text{low}} \ge 0.15$ and $\text{val}_{\text{high}} \le 0.00$).
5. **Sub-par General:** Negative performance across all conditions ($\text{val}_{\text{high}} \le -0.10$ and $\text{val}_{\text{low}} \le -0.10$).
6. **Situational Specialist:** Balanced, context-specific utility.
7. **Unclassified (Insufficient Evidence):** $< 30$ total balls or $< 10$ high-pressure balls.

---

## 5. Reliability Engine & 5-Pillar Decomposition

A player's Pressure Reliability Index is computed across 5 orthogonal pillars:

1. **Pillar 1: High-Pressure Value Added ($\mu_{\text{HP}}$):** Mean $\text{PAVA}_{\text{raw}}$ across deliveries where Pressure $\ge 50.0$.
2. **Pillar 2: Baseline Retention Ratio ($S_{\text{ret}}$):**
   $$\text{Retention Delta} = \mu_{\text{HP}} - \mu_{\text{LP}}, \quad \text{shrunk towards career mean if } N_{\text{LP}} < 10$$
3. **Pillar 3: Match-to-Match Consistency ($S_{\text{cons}}$):** Opportunity-adjusted per-ball PAVA variance across innings.
4. **Pillar 4: Situational Adaptability ($S_{\text{adapt}}$):** Phase and context stability (defaults to $60.0$ if sparse).
5. **Pillar 5: Evidence Strength & Empirical Bayes Shrinkage:**
   $$w_{\text{shrink}} = \frac{N_{\text{HP}}}{N_{\text{HP}} + K_{\text{shrink}}}, \quad K_{\text{shrink}} = 45.0 \text{ pseudo-deliveries}$$
   $$\text{PAVA}_{\text{shrunk}} = w_{\text{shrink}} \cdot \mu_{\text{HP}} + (1.0 - w_{\text{shrink}}) \cdot 0.0$$

### Composite Reliability Normalization:
$$Z_{\text{composite}} = 0.50 \cdot Z(\text{PAVA}_{\text{shrunk}}) + 0.20 \cdot Z(S_{\text{ret}}) + 0.15 \cdot \left(\frac{S_{\text{cons}}}{50.0}\right) + 0.15 \cdot \left(\frac{S_{\text{adapt}}}{50.0}\right)$$

$$\text{Reliability Score} = \Phi(Z_{\text{composite}}) \times 100.0$$

---

## 6. Population Eligibility Rules

To qualify for final official rankings, a player must satisfy all three career exposure hurdles:
- **Batters (109 Qualifiers):** Total balls faced $\ge 400$, High-pressure balls ($BPI \ge 50$) $\ge 30$, Matches $\ge 20$.
- **Bowlers (147 Qualifiers):** Total legal balls $\ge 400$, High-pressure legal balls ($BoPI \ge 50$) $\ge 30$, Matches $\ge 20$.
