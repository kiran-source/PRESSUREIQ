# FINAL ML METRIC REPRODUCTION & DISCREPANCY AUDIT
## Chronological Out-of-Fold Verification of LightGBM and Baseline Performance

**Project:** PRESSUREIQ — SupeRR Selector Season 2 (Rajasthan Royals)  
**Date:** 11 November 2026  
**Status:** Certified Adversarial ML Audit  
**Dataset:** 200,961 Deliveries (2022–2026) across 867 T20 matches  
**Reproduction Script:** `scripts/reproduce_ml_metrics.py`  

---

## 1. Executive Summary & Explicit Discrepancy Disclosure

### 1.1 Discrepancy Disclosure
The 11 November Readiness Dossier summary table contained the following statement:
> *"LightGBM achieves superior Brier score (0.1982 vs 0.2291 baseline) and log-loss reduction across high-pressure sequences."*

**Adversarial Audit Finding:**
- **The figure `0.1982`** was an uncalibrated slice metric from an exploratory win-probability model on 2026 Powerplay deliveries in `docs/MODEL_CALIBRATION_AUDIT.md`.
- **The figure `0.2291`** was an ungrounded claim that does not exist in any script, parquet file, or JSON benchmark report in the repository.

### 1.2 The True Grounded Metrics on Untouched 2026 Test Set
Re-evaluation on identical 2026 held-out records reveals the true empirical performance across both delivery-level expected outcomes and match-level win probabilities:

| Modeling Domain | Prediction Target | Sample Size ($N$) | Context Baseline | Machine Learning Model | Improvement |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Delivery Outcome** | **Boundary Probability** | 33,082 | **0.1603** (Brier) | **0.1576** (LightGBM Brier) | -1.7% Brier, AUC 0.5995 |
| **Delivery Outcome** | **Dismissal Probability** | 33,082 | **0.0506** (Brier) | **0.0496** (LightGBM Brier) | -2.0% Brier, AUC 0.5909 |
| **Delivery Outcome** | **Expected Runs** | 33,082 | **1.8075** (RMSE) | **1.7919** (LightGBM RMSE) | -0.0156 runs/ball |
| **Match Leverage** | **2nd Innings Win Prob** | 15,614 | **0.2185** (Stratified Brier) | **0.1866** (Logistic Brier) | -14.6% Brier, AUC 0.8016 |

Both models were evaluated on **strictly identical records** with zero test-fold contamination.

---

## 2. Experimental Setup & Strict Temporal Isolation

### 2.1 Chronological Data Partitioning
To guarantee zero future information leakage into historical performance ratings, the 200,961 deliveries were partitioned strictly by calendar year:
- **Historical Training Split ($\le 2024$):** 120,243 deliveries across 518 matches.
- **Validation Split ($2025$):** 47,636 deliveries across 206 matches.
- **Held-Out Test Split ($2026$):** 33,082 deliveries across 143 matches (completely untouched during training and tuning).

### 2.2 Prediction Targets & Evaluation Populations
1. **Boundary Probability (`is_boundary`):**
   - Target: Binary indicator $\{0, 1\}$ (where runs off bat $\in \{4, 6\}$).
   - Evaluation Population: All delivery records in the chronological 2026 split ($N = 33,082$).
2. **Dismissal Probability (`is_wicket` / `is_striker_out`):**
   - Target: Binary indicator $\{0, 1\}$ of batter dismissal on the delivery.
   - Evaluation Population: All delivery records in the chronological 2026 split ($N = 33,082$).
3. **Expected Runs (`batter_runs`):**
   - Target: Continuous runs scored off the bat $\{0, 1, 2, 3, 4, 5, 6\}$.
   - Evaluation Population: All delivery records in the chronological 2026 split ($N = 33,082$).
4. **2nd Innings In-Game Win Probability (`bat_won`):**
   - Target: Binary indicator $\{0, 1\}$ whether chasing team won the match.
   - Evaluation Population: All 2nd-innings deliveries in 2026 ($N = 15,614$).

---

## 3. Baseline vs. ML Architectures

### 3.1 Context Baseline Specification
The empirical context baseline stratifies historical performance into contextual buckets:
- Stratum: $(\text{innings}, \lfloor \text{balls\_remaining} / 30 \rfloor, \lfloor \text{wickets\_remaining} / 3 \rfloor \times 3)$.
- For each delivery in the test set, the baseline assigns the empirical historical mean of that exact stratum computed exclusively on the $\le 2024$ training split.
- If a stratum has no training observations, it defaults to the global historical mean.

### 3.2 LightGBM Specification
- Estimator: `LGBMClassifier` / `LGBMRegressor`
- Hyperparameters: `n_estimators=140`, `learning_rate=0.05`, `num_leaves=31`, `random_state=42`.
- Categorical Encoding: Scikit-Learn `OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)` fitted **strictly on the $\le 2024$ training fold**.
- Features: 14 pre-delivery contextual and historical ability features (innings, balls remaining, wickets remaining, current run rate, BPI, BoPI, knockout stage, batter historical SR/avg/dot%/bnd%, bowler historical economy/SR/dot%).

---

## 4. Exact Reproduction Command & Output

### Reproduction Command
```bash
python scripts/reproduce_ml_metrics.py
```

### Actual Command Output
```
==========================================================================================
1. EXPECTED OUTCOMES REPRODUCTION (DELIVERY-LEVEL)
==========================================================================================
Dataset split: Train (<=2024) = 120,243, Val (2025) = 47,636, Test (2026) = 33,082
Boundary Prob (Test 2026): Baseline Brier = 0.1603 (AUC=0.5679) | LightGBM Brier = 0.1576 (AUC=0.5995)
Dismissal Prob (Test 2026): Baseline Brier = 0.0506 (AUC=0.5680) | LightGBM Brier = 0.0496 (AUC=0.5909)
Expected Runs (Test 2026):  Baseline RMSE  = 1.8075 | LightGBM RMSE  = 1.7919

==========================================================================================
2. IN-GAME WIN PROBABILITY (2ND INNINGS CHASE OUTCOME)
==========================================================================================
2nd Innings split: Train = 57,396, Val = 22,224, Test = 15,614
Full Test 2026 (N=15,614):
  Unconditional Chase Baseline Brier: 0.2419
  Stratified Context Baseline Brier:  0.2185
  Logistic Win-Prob Model Brier:      0.1866

Powerplay Sub-Population (N=5,120):
  Stratified Context Baseline Brier:  0.2378
  Logistic Win-Prob Model Brier:      0.2301
```

---

## 5. Verification of Zero Test-Fold Leakage

1. **No In-Sample Contamination:** Neither LightGBM nor the Logistic regression model saw a single delivery from the 2026 test fold during training, and LightGBM metrics above are evaluated live via `engine.preprocess_features(test_df, fit=False)`.
2. **Categorical Preprocessing Isolation:** Ordinal encoders were fitted strictly on the $\le 2024$ slice. Any novel categories appearing in 2025 or 2026 were assigned the unknown index `-1`.
3. **Chronological Chase Label Fix (`cum_team_runs`):** Following the CodeRabbit remediation fixing `bat_won` from `team_runs_before` last to `cum_team_runs` max, 2nd-innings test Brier improved cleanly from stratified baseline `0.2185` to logistic regression `0.1866`. Note also that 2025 Platt scaling slightly worsened 2026 ECE (`0.0894 -> 0.0963`), so raw un-Platt-scaled chronological logistic probabilities remain preferred (`hybrid_validation_gate.py`).
4. **Conclusion:** While the previously reported `0.1982 vs 0.2291` comparison was incorrect and is now formally retracted, the genuine ML models demonstrate rigorous out-of-sample superiority over context baselines across all prediction targets on identical records.

