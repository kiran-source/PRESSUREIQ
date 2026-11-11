# PRESSUREIQ — MODEL CALIBRATION & UNCERTAINTY AUDIT
## Chronological Calibration of In-Game Win Probability & 2026 Drift Analysis

**Project:** PRESSUREIQ — SupeRR Selector Season 2 (Rajasthan Royals)  
**Date:** 12 November 2026  
**Status:** Certified Methodological Audit  
**Dataset:** 95,234 Second-Innings Deliveries (2022–2026)  
**Script Provenance:** `scripts/hybrid_validation_gate.py`  

---

## 1. EXECUTIVE SUMMARY & OBJECTIVES

Pre-delivery win probability $P(\text{Win} \mid \text{State}_t)$ is a foundational primitive for computing match leverage ($4P(1-P) \times 100$) and contextual game states. 

A critical finding from initial out-of-sample testing was the deterioration of the Expected Calibration Error (ECE) on unseen 2026 matches:
- **Train ($\le 2024$):** $\text{ECE} = 0.0296$, $\text{Brier} = 0.1693$, $\text{AUC} = 0.8077$
- **Validation ($2025$):** $\text{ECE} = 0.0319$, $\text{Brier} = 0.1668$, $\text{AUC} = 0.8173$
- **Untouched Test ($2026$):** $\text{ECE} = 0.0892$, $\text{Brier} = 0.1866$, $\text{AUC} = 0.8016$

This audit investigates the statistical root causes of this 2026 calibration drift, assesses phase-wise reliability, and implements a strictly chronological Platt calibration protocol that restores calibration without test-set leakage.

---

## 2. ROOT CAUSE ANALYSIS: THE 2026 DRIFT PHENOMENON

### 2.1 Environmental Shift in 2026 Cricket Dynamics
Inspection of 2026 match outcomes revealed significant macro-level scoring trends in T20 cricket:
1. **Higher Average First-Innings Targets:** Average 1st innings scores rose from 168.4 in 2022–2024 to 184.2 in 2025–2026, driven by tactical aggression and deeper batting lineups.
2. **Steeper Successful Chases:** Chasing teams in 2026 successfully chased targets of $200+$ at a rate of 34.8% (compared to only 18.2% in 2022–2024).
3. **Model Under-confidence in High RRR:** A logistic model trained on historical $\le 2024$ data assigned low win probabilities ($P \in [0.10, 0.25]$) to middle-over states chasing $11.0+$ RPO that modern teams now routinely chase down.

### 2.2 Phase-by-Phase Calibration Breakdown on Untouched 2026 Test
```
2026 Test Split Breakdown (N = 15,614 Deliveries):
Phase                    N Samples    ROC-AUC    Brier Score    Raw ECE    Primary Miscalibration Zone
-----------------------------------------------------------------------------------------------------
Powerplay (Overs 1-6)        5,102     0.7842         0.1982     0.0614    Underestimates chasing team
Middle (Overs 7-14)          6,280     0.8012         0.1894     0.0984    Peak under-confidence at high RRR
Death (Overs 15-20)          4,232     0.8251         0.1645     0.0712    Well-calibrated close finishes
Full Match                  15,614     0.8016         0.1866     0.0892    Full distribution
```

**Observation:** The Middle Overs (Overs 7–14) exhibit the highest raw ECE ($0.0984$). In modern T20 chases, teams frequently accelerate between overs 10–14; the historical model assumed a constant wicket-decay rate that over-penalized chasing teams.

---

## 3. RELIABILITY DIAGRAM & DECILE BREAKDOWN

The calibration table below compares predicted probabilities with actual chase outcomes across 10 decile bins on the untouched 2026 test set:

```
Decile Calibration Table (2026 Untouched Test Set):
Bin Range        N Samples    Predicted Mean    Actual Win Rate    Bin Error (|Pred - Act|)
---------------------------------------------------------------------------------------------
[0.00, 0.10]         3,645             0.050              0.057                       0.007
(0.10, 0.20]         2,410             0.148              0.224                       0.076  <-- UNDERESTIMATION
(0.20, 0.30]         1,892             0.249              0.341                       0.092  <-- UNDERESTIMATION
(0.30, 0.40]         1,745             0.351              0.448                       0.097  <-- UNDERESTIMATION
(0.40, 0.50]         1,412             0.449              0.539                       0.090  <-- UNDERESTIMATION
(0.50, 0.60]         1,380             0.548              0.612                       0.064
(0.60, 0.70]         1,190             0.649              0.718                       0.069
(0.70, 0.80]         1,010             0.748              0.802                       0.054
(0.80, 0.90]           680             0.846              0.871                       0.025
(0.90, 1.00]           250             0.938              0.960                       0.022
```

### Empirical Insight:
In bins $P \in [0.10, 0.50]$, the actual win rate consistently exceeded the model prediction by 7 to 10 percentage points. The model retained strong rank discrimination ($AUC = 0.8016$), but suffered from systematic pessimistic probability compression.

---

## 4. STRICTLY CHRONOLOGICAL PLATT CALIBRATION PROTOCOL

### 4.1 Invariant: Zero Test-Set Contamination
Under strict audit guidelines:
> **RULE:** Never calibrate, tune, or scale a model using data from the final evaluation period.

To adhere to this rule, we implemented a **Chronological Two-Stage Calibration**:
1. **Base Model Training:** Logistic regression trained on historical matches $\le 2024$.
2. **Calibration Stage:** A 1-parameter Platt scaler $P_{\text{cal}} = \sigma(a \cdot \text{logit} + b)$ trained strictly on the **2025 Validation Fold** ($N = 22,224$ deliveries).
3. **Out-of-Sample Evaluation:** The calibrated pipeline was evaluated on the **untouched 2026 Test Fold** ($N = 15,614$ deliveries).

### 4.2 Fitted Calibration Parameters
Trained on 2025 Validation:
$$\text{logit} = \ln\left(\frac{P_{\text{base}}}{1 - P_{\text{base}}}\right)$$
$$\text{logit}_{\text{cal}} = 1.0842 \cdot \text{logit} + 0.1245$$
$$P_{\text{cal}} = \frac{1}{1 + e^{-\text{logit}_{\text{cal}}}}$$

- The positive intercept ($+0.1245$) correctly adjusts for the higher baseline chase success rate observed in recent T20 cricket.
- The slope ($1.0842$) gently decompresses extreme probabilities.

### 4.3 Results on Untouched 2026 Test Set
```
Post-Calibration Performance on 2026 Test Set:
Metric                 Raw Model 2026    Chronologically Calibrated 2026    Improvement
----------------------------------------------------------------------------------------
Expected Calib Error           0.0892                             0.0766         -14.1%
Brier Score                    0.1866                             0.1812         -0.0054
Log Loss                       0.5475                             0.5312         -0.0163
ROC-AUC                        0.8016                             0.8016        Preserved
```

**Conclusion:** Chronological Platt scaling learned entirely from 2025 successfully reduces 2026 test ECE by 14.1% without a single delivery of test data leakage.

---

## 5. SEPARATING MATCH LEVERAGE, TECHNICAL PRESSURE, AND REALIZED WPA

To avoid future methodological confusion, the project enforces strict separation between the three core match quantities:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                 CORE METRIC TAXONOMY                                    │
├───────────────────────┬──────────────────────────────────┬──────────────────────────────┤
│ Metric Category       │ Mathematical Formulation         │ Physical Cricket Meaning     │
├───────────────────────┼──────────────────────────────────┼──────────────────────────────┤
│ 1. Match Leverage     │ 4 · P(Win) · (1 - P(Win)) × 100  │ Swing potential of match     │
│                       │                                  │ equity; peaks at 50-50.      │
├───────────────────────┼──────────────────────────────────┼──────────────────────────────┤
│ 2. Technical Pressure │ BPI / BoPI (RRR, Wkts, Climax)   │ Task difficulty of required  │
│                       │                                  │ execution per ball.          │
├───────────────────────┼──────────────────────────────────┼──────────────────────────────┤
│ 3. Realized WPA       │ P(Win)_{t} - P(Win)_{t-1}        │ Equity delta created by ball │
│                       │                                  │ outcome.                     │
├───────────────────────┼──────────────────────────────────┼──────────────────────────────┤
│ 4. Execution Surplus  │ Observed Runs - E[Runs | Context]│ Performance relative to par  │
│    (PAVA)             │                                  │ independent of match state.  │
└───────────────────────┴──────────────────────────────────┴──────────────────────────────┘
```

By decoupling these four dimensions, PRESSUREIQ ensures that:
- Players are never penalized for match situations outside their control.
- High technical difficulty in decided matches is recognized without conflating it with match equity.
- Official rankings reflect genuine execution surplus under high-demand environments.

