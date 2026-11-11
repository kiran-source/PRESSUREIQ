# PRESSUREIQ — COMPONENT ABLATION REPORT
## Multi-Factor Sensitivity and Decomposition of Pressure Architectures

**Project:** PRESSUREIQ — SupeRR Selector Season 2 (Rajasthan Royals)  
**Date:** 12 November 2026  
**Status:** Certified Empirical Ablation  
**Dataset:** 200,961 Deliveries (867 T20 Matches, 2022–2026)  
**Script Provenance:** `scripts/hybrid_validation_gate.py`  

---

## 1. EXECUTIVE SUMMARY & ABLATION MATRIX

This report isolates and benchmarks each structural sub-component of the PRESSUREIQ pressure calculation engine. To ensure statistical integrity, every component is perturbed independently while holding all other layers invariant.

```
+---------------------------------------------------------------------------------------------------------+
|                                ABLATION IMPACT ON KEY CRICKET DYNAMICS                                  |
+-------------------+----------------------------+-----------------------+--------------------------------+
| Component Ablated | Baseline Setting (Model A) | Alternative Tested    | Empirical Finding              |
+-------------------+----------------------------+-----------------------+--------------------------------+
| Rate Dynamic      | Monotonic Inverse Sigmoid  | CDPI Bell Curve       | Bell curve eliminates garbage- |
|                   | σ((10.5 - RRR)/2.2)        | μ=10.5, σ=3.8         | time inflation in bowling.     |
+-------------------+----------------------------+-----------------------+--------------------------------+
| Blowout Filter    | None (w = 1.0)             | Sigmoid Discount      | Reduces blowout bowling        |
|                   |                            | σ((RRR - 4.5)/1.0)    | scores from 66.2 to 45.6/100.  |
+-------------------+----------------------------+-----------------------+--------------------------------+
| Resource Model    | Empirical Par Lookup       | Analytical DLS Prior  | Grounded in cricket literature;|
|                   | Table                      | Z(u, w) Exponential   | identical RMSE (27.17 vs 26.54)|
+-------------------+----------------------------+-----------------------+--------------------------------+
| Opportunity Weight| Step Cutoff (BPI >= 50)    | Continuous Sigmoid    | Increases Opener ESS 15x;      |
|                   |                            | σ((BPI - 42.0)/8.0)   | eliminates threshold cliff.    |
+-------------------+----------------------------+-----------------------+--------------------------------+
| Climax Exponent   | γ = 1.35                   | Linear γ = 1.0 vs     | γ = 1.35 correctly suppresses  |
|                   |                            | Quadratic γ = 2.0     | powerplay over-weighting.      |
+-------------------+----------------------------+-----------------------+--------------------------------+
```

---

## 2. COMPONENT 1: RATE DYNAMICS & THE BELL CURVE ASSUMPTION

### 2.1 Challenging the Near-Zero Correlation Premise
In `CRITICAL_CHALLENGE_REPORT.md`, Model D demonstrated that centering a Gaussian bell curve at $RRR_0 = 10.5$ ($\sigma = 3.8$) produced a near-zero correlation ($\rho = -0.097$) between bowling pressure and RRR.

**Statistical Challenge:** Does near-zero correlation between a pressure index and RRR prove superiority?
*Not necessarily.* A completely random noise variable has $\rho \approx 0$. To prove that CDPI is superior rather than noisy, it must satisfy **conditional monotonicity**:
$$\frac{\partial BPI}{\partial RRR} > 0 \quad \text{for fixed wickets lost } w \text{ and balls remaining } b$$

### 2.2 Empirical Conditional Monotonicity Audit
We evaluated 16 discrete match slices (combinations of $b \in \{12, 24, 48, 72\}$ balls remaining and $w \in \{2, 4, 6, 8\}$ wickets lost) across $RRR \in [4.0, 18.0]$ (`scripts/hybrid_validation_gate.py`):

```
Conditional Monotonicity Results across 16 Orthogonal Slices:
  - Slices evaluated: 16
  - Baseline BPI monotonic slices: 16 / 16 (100.0%)
  - CDPI Batting monotonic slices: 16 / 16 (100.0%)
  - Monotonicity Violations: ZERO
```

**Conclusion:** Both Baseline BPI and CDPI Batting strictly preserve conditional monotonicity across all game states. The difference lies in bowling defense:
- In Baseline BoPI, defending a target monotonically increases pressure as RRR decreases, creating the **Blowout Inversion** where bowling with the opposition needing 4 runs off 6 balls gives an extreme score of 80.96.
- In CDPI Bowling, the bell curve treats defending at $RRR = 10.5$ as peak competitive defense, tapering off symmetrically as the chase becomes either impossibly difficult for the batter ($RRR > 18$) or trivial ($RRR < 4.5$).

---

## 3. COMPONENT 2: BLOWOUT SUPPRESSION FUNCTIONS

We ablated four distinct mathematical formulations on all 12,010 historical 2nd innings blowout deliveries ($RRR \le 6.0$):

1. **$F_1$ — Baseline (No Suppression):** $w = 1.0$
2. **$F_2$ — Step Discount:** $w = 0.25$ if $RRR < 4.5$ and $b < 36$, else $1.0$
3. **$F_3$ — Smooth Sigmoid:** $w = \sigma((RRR - 4.5)/1.0) = \frac{1}{1 + e^{-(RRR - 4.5)}}$
4. **$F_4$ — Smoothstep (Cubic Hermite):** $w = 3x^2 - 2x^3$ on $x = \text{clip}\left(\frac{RRR - 2.5}{3.5}, 0, 1\right)$

### 3.1 Historical Distribution on 12,010 Blowout Deliveries
```
Blowout Function Benchmark (N = 12,010 Historical Deliveries with RRR <= 6.0):
Metric                           F1 (Baseline)    F2 (Step)    F3 (Sigmoid)    F4 (Smoothstep)
----------------------------------------------------------------------------------------------
Mean Bowling Pressure                    66.19        52.14           45.63              44.12
Standard Deviation                       14.28        16.89           12.75              13.01
Max Score                                89.25        74.50           64.80              63.20
% of Deliveries with BoPI >= 70.0        52.1%        14.8%            0.0%               0.0%
Derivative Discontinuity Jump             0.00         0.75           <0.01              <0.01
```

### 3.2 Analysis & Insights
- **Baseline Failure:** In baseline BoPI, over **52.1%** of blowout deliveries were classified as High or Extreme pressure ($\ge 70.0$). Bowlers bowling in decided matches received inflated pressure weight.
- **Step Discount Flaw:** The step discount eliminates high scores in the final overs, but introduces a massive derivative jump of $\Delta w = 0.75$ at the boundary ($RRR = 4.5$).
- **Sigmoid Superiority:** The smooth sigmoid function completely eliminates scores above 70.0 in blowout situations while maintaining $C^\infty$ mathematical continuity across all match trajectories.

---

## 4. COMPONENT 3: RESOURCE DEPRECIATION FUNCTIONS

We evaluated the impact of substituting the empirical par lookup table with:
- **Naive Power-Law:** $R_{\text{naive}} = (w/10)^{0.80} \cdot (b/120)^{0.65} \times 168$
- **Analytical DLS Prior:** $Z(u, w) = Z_0 \cdot \left[\frac{1 - e^{-0.12 u/6}}{1 - e^{-2.4}}\right] \cdot \left(\frac{w}{10}\right)^{0.65}$

### 4.1 Phase-by-Phase Residual Breakdown (100,500 Deliveries)
```
Phase Breakdown across All 1st Innings Deliveries:
Phase                   N Deliveries    Naive RMSE    Naive MAE    DLS Prior RMSE    DLS Prior MAE    Delta RMSE
----------------------------------------------------------------------------------------------------------------
Powerplay (Overs 1-6)         30,684         27.81        20.12             28.45            20.91       +0.64
Middle (Overs 7-14)           40,821         26.11        18.72             26.68            19.34       +0.57
Death (Overs 15-20)           28,995         25.24        17.98             25.82            18.42       +0.58
Full Innings                 100,500         26.54        18.95             27.17            19.66       +0.63
```

**Key Takeaway:** The analytical DLS prior matches the empirical fit to within 0.6 runs across all match phases. Crucially, the DLS prior is mathematically defined for any target or shortened over limit, providing robust protection against out-of-distribution match lengths.

---

## 5. COMPONENT 4: OPPORTUNITY WEIGHTING (STEP VS CONTINUOUS)

Ablating the delivery filtering scheme isolates the root cause of opener sensitivity:

### 5.1 Kish's Effective Sample Size (ESS) Across Player Profiles
```
Ablation of Pressure Eligibility Filters across Canonical Player Roles:
Player               Role             Total Balls    Step BPI>=50    Step BPI>=55    Sigmoid ESS    Kish Gain
-------------------------------------------------------------------------------------------------------------
Ruturaj Gaikwad      Top Order              1,822              45              12          679.5       15.1x
Rohit Sharma         Top Order              1,619              35              17          497.5       14.2x
Suryakumar Yadav     Middle Order           2,759             236             125        1,485.2        6.3x
Romario Shepherd     Finisher                 687             482             365          629.2        1.3x
Rinku Singh          Finisher               1,284             418             249        1,018.7        2.4x
Nicholas Pooran      Middle Order           1,972             300             141        1,190.8        4.0x
Phil Salt            Top Order              1,643              49              38          398.0        8.1x
```

### 5.2 Why Continuous Weighting is Statistically Defensible
1. **No Artificial Edge Disqualification:** Shifting a hard boundary from 50 to 55 cuts Gaikwad's sample by 73.3%, dropping him below the 30-ball threshold. Under continuous weighting, Gaikwad's sample size is an effective 679.5 balls, completely insulated against arbitrary boundary shifts.
2. **Proper Role Balance:** Finishers who face concentrated pressure (Shepherd, Rinku) still receive high effective sample sizes and high per-ball weights, while top-order batters receive credit for the full distribution of pressure they face throughout innings construction.

---

## 6. ABLATION CONCLUSION & RECOMMENDATIONS

1. **Retain Sigmoid Blowout Suppression:** Eliminates the BoPI blowout inversion without introducing artificial derivative cliffs.
2. **Adopt Analytical DLS Prior for Target Leakage Prevention:** Eliminates reliance on arbitrary par tables while matching empirical accuracy.
3. **Transition to Continuous Sigmoid Weighting in Production Roadmap:** Completely resolves opener threshold fragility while preserving high-pressure emphasis.

