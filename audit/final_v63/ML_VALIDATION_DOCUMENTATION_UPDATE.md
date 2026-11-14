# ML VALIDATION DOCUMENTATION UPDATE & BENCHMARK TRANSPARENCY
## PressureIQ Model B Predictive Engine Verification

**Audit Directive:** PRESSUREIQ V6.3 Controlled Remediation  
**Target Document:** `docs/RR_MODEL_VALIDATION.md`  
**Evaluation Scope:** Chronological Holdout Match Set (2026 Season, N = 2,252 Batting Innings, 1,656 Bowling Spells, 30,729 Deliveries)  
**Review Status:** Audited, Corrected, and Re-Benchmarked  

---

### 1. Model Framing & Prediction Target

To prevent methodological ambiguity during external review, the machine learning models developed in Model B are formally classified as:

$$\textbf{Innings Execution Efficiency Models: } \mathbb{E}[\text{Runs Scored} \mid \text{Balls Faced}, \text{Pressure Context}]$$
$$\textbf{Spell Execution Efficiency Models: } \mathbb{E}[\text{Runs Conceded} \mid \text{Legal Balls Bowled}, \text{Pressure Context}]$$

#### Key Methodological Boundaries:
1. **In-Innings Feature Dependence:**  
   The prediction target for the batting model is the total runs scored by a batter in a completed innings ($y \in [0, 140]$). The feature set includes `balls_faced`, which is an in-innings opportunity exposure metric rather than a pre-match constant.
2. **Not a Pre-Match Forecast:**  
   The model does not claim to forecast pre-match how many runs a player will score before setting foot on the pitch. Instead, it measures **how efficiently a player converts delivery exposure under situational pressure into runs relative to historical opportunity expectations**.
3. **Strategic Utility for Rajasthan Royals:**  
   This model allows RR recruitment analysts to answer: *"Given 25 balls faced under high match pressure (BPI > 65), how many runs does Candidate A produce compared to Candidate B?"*

---

### 2. Three-Benchmark Holdout Evaluation (2026 Test Set)

To separate delivery opportunity scaling from situational pressure signals, the model is evaluated against three distinct baselines:

| Benchmark Tier | Model Specification | Inputs / Features Available | Holdout MAE | Incremental Error Gain | Total Reduction vs. Mean | Holdout $R^2$ |
|---|---|---|:---:|:---:|:---:|:---:|
| **Tier 1: Naive Global Mean** | $\hat{y} = \bar{y}_{\text{hist}}$ | None (unconditional sample mean: 22.1 runs) | **17.227** | Baseline | 0.00% | 0.000 |
| **Tier 2: Opportunity Volume Baseline** | $\hat{y} = \text{balls\_faced} \times \text{Global Strike Rate}$ | Completed balls faced (Volume scaling only) | **6.262** | -63.65% vs. Mean | 63.65% | 0.812 |
| **Tier 3: Full Contextual LightGBM** | $\hat{y} = f(\text{Volume}, \text{PAVA}, \text{BPI}, \text{Phase}, \text{Venue})$ | Opportunity Volume + Situational Pressure Surplus + Leverage | **5.835** | **-6.81% vs. Volume** | **66.13% vs. Mean** | **0.845** |

#### Analytical Interpretation:
- **The +66.13% Error Reduction ($17.227 \to 5.835$):**  
  This widely cited metric measures the total variance reduction achieved by moving from an unconditional global average to a fully specified opportunity and context-aware execution model.
- **The True Incremental Value of Pressure Intelligence (+6.81%):**  
  Delivery volume alone explains 63.65% of the variance ($17.227 \to 6.262$). Adding PAVA high-pressure surplus (`shrunk_hp_pava`), leverage ratio (`hp_ratio`), and situational leverage indices provides an **additional 6.81% reduction in MAE** ($6.262 \to 5.835$) and increases out-of-sample $R^2$ from $0.812$ to $0.845$.
- **Conclusion:**  
  Pressure intelligence provides statistically significant, reproducible predictive lift beyond opportunity exposure alone. However, marketing claims that pressure features alone account for the entire 66.13% error reduction have been eliminated from all official submission documentation.

---

### 3. Bowling Spell Model Validation (2026 Test Set, N = 1,656 Spells)

| Benchmark Tier | Model Specification | Holdout MAE | Incremental Gain | Holdout $R^2$ |
|---|---|:---:|:---:|:---:|
| **Tier 1: Global Mean** | Unconditional mean runs conceded ($29.4$ runs) | 10.227 | Baseline | 0.000 |
| **Tier 2: Opportunity Baseline** | $\text{legal\_balls} \times \text{Global Economy Rate}$ | 8.114 | -20.66% vs. Mean | 0.285 |
| **Tier 3: Contextual LightGBM** | Legal balls + BoPI + High-Pressure Dot % + Phase | **7.429** | **-8.44% vs. Volume** (+27.36% vs. Mean) | **0.394** |

---

### 4. Chronological Holdout Integrity Certification

- **Training Calendar:** 22 Jan 2022 – 31 Dec 2024 (520 matches, 120,412 balls)
- **Validation Calendar:** 01 Jan 2025 – 31 Dec 2025 (217 matches, 49,820 balls)
- **Blind Test Calendar:** 01 Jan 2026 – 01 Nov 2026 (146 matches, 30,729 balls)
- **Future Leakage Check:** PASS (Zero deliveries or outcomes from 2025 or 2026 were accessible to the model during training).
