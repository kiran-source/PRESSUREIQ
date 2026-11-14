# MACHINE LEARNING LEAKAGE & REPRODUCIBILITY AUDIT (CHECK 1)
## Adversarial Investigation of the Claimed 66.1% MAE Improvement & In-Innings Opportunity Features

**Audit Protocol:** PRESSUREIQ V6.2 Final Evidence Challenge  
**Audit Directory:** `audit/final_v62/`  
**Reviewer Role:** Adversarial Quantitative Research Auditor & ML Forensic Engineer  
**Focus Area:** Holdout Performance, Predictor Timeliness, Baseline Comparability, and Leakage Analysis  
**Overall Status:** **REPRODUCIBLE BUT REQUIRES BENCHMARK QUALIFICATION**

---

### 1. Verification of the 10 Core Adversarial Questions

| # | Forensic Question | Auditor Finding & Empirical Evidence | Classification |
|---|---|---|---|
| **1** | **What exactly is the prediction target?** | The target is `runs` (per batter-innings) in `batter_innings_pava.parquet` and `runs_conceded` (per bowler-spell) in `bowler_spell_pava.parquet`. | **VERIFIED** |
| **2** | **What information is available at prediction time?** | The features utilized in `train_and_evaluate_batting_models` are `balls_faced`, `avg_bpi`, `high_pressure_balls`, and `hp_ratio`. | **VERIFIED** |
| **3** | **Are any input features calculated from the target innings outcome?** | **YES.** `balls_faced`, `high_pressure_balls`, and `hp_ratio` represent the completed delivery volume of that specific innings, which is an in-innings outcome feature, not a pre-match feature. | **FINDING (QUALIFICATION NEEDED)** |
| **4** | **Are innings totals, runs scored, wickets, balls faced or derived statistics included as predictors?** | `balls_faced` and `high_pressure_balls` are included. Target `runs` and derived strike rate `sr` are strictly excluded from predictors. However, completed innings volume (`balls_faced`) acts as a massive proxy for runs. | **FINDING (OPPORTUNITY PROXY)** |
| **5** | **Are training and test matches strictly separated chronologically?** | **YES.** Partitions strictly follow match dates: Train ($\le 2024$, $N=7,758$), Validation ($2025$, $N=2,714$), Test Holdout ($\ge 2026$, $N=2,252$). Zero temporal overlap. | **VERIFIED (PASS)** |
| **6** | **Are player identities or match-specific features creating leakage?** | **NO.** Player IDs, team names, match IDs, and categorical encoders are excluded from tree splits. Features are purely continuous physical context metrics. | **VERIFIED (PASS)** |
| **7** | **Was the baseline evaluated on exactly the same 2,252 observations?** | **YES.** `base_pred_test = np.full(len(test_df), train_df['runs'].mean())` evaluated across all 2,252 test holdout rows. | **VERIFIED (PASS)** |
| **8** | **Can both MAE values be reproduced from a clean run?** | **YES.** Clean run reproduces exact values: Baseline MAE $= 17.227$, LightGBM MAE $= 5.835$, MAE Gain $= 66.13\%$, $R^2 = 0.845$. | **REPRODUCIBLE (PASS)** |
| **9** | **Was the test set used for model tuning or feature selection?** | **NO.** Early stopping callbacks exclusively monitored `val_df` (2025). The 2026 test partition was isolated until final scoring. | **VERIFIED (PASS)** |
| **10** | **Is the improvement statistically and practically meaningful?** | **QUALIFIED.** Practically meaningful as a *contextual execution efficiency model* (expected runs given $N$ balls under pressure $P$). However, when compared against an opportunity-adjusted baseline (`balls_faced * global_sr`), the baseline is $6.262$ MAE, meaning pressure features provide $+6.81\%$ incremental gain over volume alone. | **QUALIFIED FINDING** |

---

### 2. Deep Dive: Unconditional Mean vs. Opportunity-Adjusted Baselines

The adversarial audit executed an experiment comparing the LightGBM model against both an unconditional historical mean and an opportunity-adjusted baseline:

```
[EXPERIMENTAL RESULTS ON 2,252 HOLDOUT INNINGS (2026 Matches)]
┌───────────────────────────────────────────────────┬────────────┬─────────────┐
│ Model Formulation                                 │ Test MAE   │ vs Baseline │
├───────────────────────────────────────────────────┼────────────┼─────────────┤
│ 1. Unconditional Historical Mean (Current Base)   │ 17.227 runs│ 0.00%       │
│ 2. Opportunity-Adjusted Base (Balls * Global SR)  │  6.262 runs│ +63.65%     │
│ 3. LightGBM Contextual Engine (Balls + Pressure)  │  5.835 runs│ +66.13%     │
└───────────────────────────────────────────────────┴────────────┴─────────────┘
```

#### Analytical Breakdown:
1. **The 66.13% Reduction:**
   - Shifting from predicting an unconditional $\approx 18.5$ runs for every batter (regardless of whether they batted for 1 ball or 50 balls) to knowing how many balls they faced reduces MAE from **$17.227$ to $6.262$** (accounting for $96.8\%$ of the error reduction).
2. **The Incremental Pressure Contribution:**
   - Incorporating contextual pressure variables (`avg_bpi`, `high_pressure_balls`, `hp_ratio`) further reduces MAE from **$6.262$ to $5.835$** (an incremental gain of **$+0.427$ runs MAE / $+6.81\%$ error reduction** over opportunity alone).

---

### 3. Adversarial Risk Assessment for Competition Submission

| Audit Risk | Severity | Potential Judge Challenge | Required Analytical Clarification |
|---|---|---|---|
| **Ambiguity in Model Framing** | MEDIUM | A quantitative judge may object: *"You claimed a 66.1% MAE improvement in predicting player runs, but your model used completed innings balls faced as an input, which is unknown before the match."* | Explicitly define the model as an **Innings Execution Efficiency Model** ($\mathbb{E}[\text{Runs} \mid \text{Balls}, \text{Pressure}]$), rather than an unconditional pre-match outcome forecaster. |
| **Baseline Calibration** | LOW | Claiming 66.1% against an unconditional mean makes the gain look enormous compared to opportunity-adjusted benchmarks. | State transparently: *"Achieves a 66.13% error reduction over the unconditional historical mean, and a 6.81% incremental error reduction over opportunity-adjusted volume baselines."* |

---

### 4. Recommendation for Competition Readiness
The ML reproduction is mathematically verified down to the decimal point ($5.835$ vs $17.227$). To ensure total defense against skeptical peer reviewers, update the documentation in `docs/RR_MODEL_VALIDATION.md` to include both the unconditional ($17.227$) and opportunity-adjusted ($6.262$) benchmarks.
