# PRESSUREIQ: A Context-Aware Cricket Performance & Reliability Intelligence Framework
## Official Methodology & Competition Verification Report

**Project:** PRESSUREIQ — Quantitative Cricket Performance & Reliability Intelligence  
**Authors:** Senior Cricket Data Scientist & Quantitative Analytics Panel  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 (2026)  
**Scope:** IPL & T20 International (T20I) Ball-by-Ball Data (2022–2026)  
**Deliverable:** Master Competition Methodology & Player Recommendation Report  
**Submission Version:** Final Competition Freeze (Commit `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2`)  

---

## EXECUTIVE SUMMARY

Conventional cricket analytics (such as batting strike rate or bowling economy) fail under pressure because they treat a boundary hit in an unpressurized league match identically to a boundary hit requiring 12 runs off 5 balls in an IPL playoff.

**PRESSUREIQ** is an end-to-end quantitative framework built on 200,961 valid deliveries across 867 matches (371 IPL matches and 496 T20Is) from January 2022 to November 2026. The framework introduces:
1. **Continuous Match Pressure Indices (BPI / BoPI)**: Calibrated 0–100 scales quantifying match context without outcome leakage.
2. **Expected Performance ML Ensembles**: Multi-target LightGBM models trained on chronological splits (2022–2024 train, 2025 val, 2026 test) predicting expected runs, boundary probability, and dismissal probability per delivery.
3. **Unamplified Execution Surplus (PAVA)**: Quantifying runs added above contextual expectation, strictly decoupling performance above par from situational leverage.
4. **Five-Pillar Reliability Scoring System**: Integrating Absolute Pressure Performance (50%), Baseline Retention Delta (20%), Match-to-Match Consistency (15%), Context Adaptability (15%), and Empirical Bayes Shrinkage ($K = 45.0$ deliveries).
5. **2,000 Match-Clustered Bootstrap Iterations**: Rigorous uncertainty estimation establishing 95% Confidence Intervals and Top-10 Inclusion Probabilities.

---

## OFFICIAL COMPETITION RANKINGS (MODEL A BASELINE)

### The 10 Most Reliable Batters Under Pressure
1. **Ruturaj Gaikwad** (Top Order | Reliability: **97.71** | 95% CI: [76.30, 99.09] | Top-10 Prob: 0.6085 | Shrunk PAVA/ball: +0.469 | Archetype: Clutch Climber)
2. **Rohit Sharma** (Top Order | Reliability: **95.27** | 95% CI: [60.01, 98.17] | Top-10 Prob: 0.3395 | Shrunk PAVA/ball: +0.383 | Archetype: Clutch Climber)
3. **Fakhar Zaman** (Top Order | Reliability: **95.25** | 95% CI: [52.46, 98.38] | Top-10 Prob: 0.4515 | Shrunk PAVA/ball: +0.407 | Archetype: Clutch Climber)
4. **Suryakumar Yadav** (Middle Order | Reliability: **94.68** | 95% CI: [66.71, 98.64] | Top-10 Prob: 0.4590 | Shrunk PAVA/ball: +0.424 | Archetype: Clutch Climber)
5. **Romario Shepherd** (Finisher | Reliability: **93.69** | 95% CI: [71.26, 97.62] | Top-10 Prob: 0.3480 | Shrunk PAVA/ball: +0.323 | Archetype: Pressure Fragile)
6. **Naman Dhir** (Top Order | Reliability: **93.30** | 95% CI: [58.13, 98.06] | Top-10 Prob: 0.3570 | Shrunk PAVA/ball: +0.385 | Archetype: Clutch Climber)
7. **Phil Salt** (Top Order | Reliability: **93.01** | 95% CI: [14.48, 98.55] | Top-10 Prob: 0.3700 | Shrunk PAVA/ball: +0.361 | Archetype: Ice Cold Anchor)
8. **Jitesh Sharma** (Middle Order | Reliability: **92.79** | 95% CI: [63.45, 97.68] | Top-10 Prob: 0.3270 | Shrunk PAVA/ball: +0.342 | Archetype: Clutch Climber)
9. **Nicholas Pooran** (Middle Order | Reliability: **92.58** | 95% CI: [68.33, 97.47] | Top-10 Prob: 0.3175 | Shrunk PAVA/ball: +0.387 | Archetype: Ice Cold Anchor)
10. **Jos Buttler** (Top Order | Reliability: **92.45** | 95% CI: [40.62, 98.43] | Top-10 Prob: 0.3405 | Shrunk PAVA/ball: +0.357 | Archetype: Ice Cold Anchor)

### The 10 Most Reliable Bowlers Under Pressure
1. **Liam Dawson** (Spin / SLA | Reliability: **95.39** | 95% CI: [74.17, 98.08] | Top-10 Prob: 0.4185 | Shrunk PAVA/ball: +0.324 | Economy: 7.79 | Archetype: Clutch Climber)
2. **Haris Rauf** (Pace / Fast | Reliability: **92.36** | 95% CI: [71.13, 96.49] | Top-10 Prob: 0.5520 | Shrunk PAVA/ball: +0.242 | Economy: 8.58 | Archetype: Clutch Climber)
3. **Abbas Afridi** (Pace / Medium-Fast | Reliability: **91.88** | 95% CI: [69.16, 95.74] | Top-10 Prob: 0.3955 | Shrunk PAVA/ball: +0.288 | Economy: 8.34 | Archetype: Ice Cold Anchor)
4. **Nathan Ellis** (Pace / Medium | Reliability: **91.84** | 95% CI: [70.87, 95.95] | Top-10 Prob: 0.4890 | Shrunk PAVA/ball: +0.255 | Economy: 8.25 | Archetype: Ice Cold Anchor)
5. **Sufiyan Muqeem** (Spin / Chinaman | Reliability: **91.41** | 95% CI: [64.39, 96.91] | Top-10 Prob: 0.3950 | Shrunk PAVA/ball: +0.283 | Economy: **6.00** | Archetype: Ice Cold Anchor)
6. **Matheesha Pathirana** (Pace / Sling | Reliability: **91.11** | 95% CI: [70.27, 95.05] | Top-10 Prob: 0.4700 | Shrunk PAVA/ball: +0.258 | Economy: 8.64 | Archetype: Ice Cold Anchor)
7. **Nasum Ahmed** (Spin / SLA | Reliability: **90.77** | 95% CI: [57.03, 98.19] | Top-10 Prob: 0.4175 | Shrunk PAVA/ball: +0.178 | Economy: 7.64 | Archetype: Clutch Climber)
8. **Ishant Sharma** (Pace / Fast-Medium | Reliability: **90.42** | 95% CI: [72.42, 94.32] | Top-10 Prob: 0.2210 | Shrunk PAVA/ball: +0.199 | Economy: 9.53 | Archetype: Ice Cold Anchor)
9. **Shoriful Islam** (Pace / Left-Arm Medium | Reliability: **90.36** | 95% CI: [65.38, 96.63] | Top-10 Prob: 0.4430 | Shrunk PAVA/ball: +0.167 | Economy: 8.23 | Archetype: Ice Cold Anchor)
10. **Tim Southee** (Pace / Medium-Fast | Reliability: **89.16** | 95% CI: [63.99, 95.51] | Top-10 Prob: 0.3540 | Shrunk PAVA/ball: +0.187 | Economy: 8.32 | Archetype: Ice Cold Anchor)

---

## 1. DEFINING MATCH PRESSURE (BPI & BoPI)

### 1.1 Core Principle
Pressure is defined as **the contextual execution demand facing the player prior to delivery release**, completely independent of the delivery's eventual outcome.

### 1.2 Batting Pressure Index (BPI)
The BPI maps pre-delivery match state into a continuous $[0, 100]$ index:
$$C_{\text{rate}} = \begin{cases} \sigma\left(\frac{RRR - 8.5}{2.2}\right) \times 100 & (\text{Innings 2}) \\ \sigma\left(\frac{-\Delta_{\text{par}}}{14.0}\right) \times 100 & (\text{Innings 1}) \end{cases}$$
$$C_{\text{resource}} = \left(\frac{w_{\text{lost}}}{9}\right)^{1.2} \times 100, \quad C_{\text{climax}} = \left(\frac{120 - b}{120}\right)^{1.35} \times 100$$
$$\text{BPI} = \text{clip}\Big(0.45 \cdot C_{\text{rate}} + 0.35 \cdot C_{\text{resource}} + 0.20 \cdot C_{\text{climax}}, 0, 100\Big)$$

### 1.3 Bowling Pressure Index (BoPI)
The BoPI measures defensive task demand:
$$C_{\text{defend}} = \begin{cases} \sigma\left(\frac{10.5 - RRR}{2.2}\right) \times 100 & (\text{Innings 2}) \\ \sigma\left(\frac{\Delta_{\text{par}}}{14.0}\right) \times 100 & (\text{Innings 1}) \end{cases}$$
$$\text{BoPI} = \text{clip}\Big(0.40 \cdot C_{\text{defend}} + 0.35 \cdot \left(\frac{10 - w_{\text{lost}}}{10} \times 100\right) + 0.25 \cdot C_{\text{climax}}, 0, 100\Big)$$

---

## 2. EXPECTED-OUTCOME MACHINE LEARNING MODELS

Expected performance is established using chronological out-of-fold LightGBM gradient boosted trees:
- $\mathbb{E}[\text{Batter Runs}]$: Test RMSE = 1.7919 (vs Context Baseline 1.8075).
- $\mathbb{P}(\text{Dismissal})$: Test Brier Score = 0.0520 (naturally calibrated to 5.4% wicket frequency).
- $\mathbb{P}(\text{Boundary})$: Test Brier Score = 0.1441.
- $\mathbb{E}[\text{Bowler Runs Conceded}]$: Test RMSE = 1.7075.
- $\mathbb{P}(\text{Bowler Wicket})$: Test Brier Score = 0.0495.

### Zero Information Leakage Guarantee
1. **Chronological Splits:** Models are trained on $\le 2024$, validated on 2025, and tested on untouched 2026 data.
2. **First-Innings Par:** Par curves are fitted strictly on prior matches using chronological walk-forward par estimators.
3. **Categorical Encoders:** Encoders are fitted only on training sets; unseen categories in evaluation are mapped to missing (`-1`).

---

## 3. UNAMPLIFIED EXECUTION SURPLUS (PAVA)

In compliance with audit resolution P0-3, PAVA measures pure **unamplified execution surplus relative to expected contextual par**:
$$\text{PAVA}_{\text{bat}} = (\text{Runs} - \mathbb{E}[\text{Runs}]) + \lambda_{\text{phase}} \cdot (\mathbb{P}(\text{Wicket}) - \text{IsWicket}) + 0.5 \cdot (\text{IsBoundary} - \mathbb{P}(\text{Boundary}))$$
$$\text{PAVA}_{\text{bowl}} = (\mathbb{E}[\text{Runs Conceded}] - \text{Runs Conceded}) + \lambda_{\text{phase}} \cdot (\text{IsBowlerWicket} - \mathbb{P}(\text{BowlerWicket}))$$
where $\lambda_{\text{phase}} = [5.2 \text{ (Powerplay)}, 4.5 \text{ (Middle)}, 3.6 \text{ (Death)}]$ represents the empirical run-equivalent value of a wicket.

Double-counting of pressure is eliminated: PAVA represents raw surplus in runs, while pressure thresholds ($BPI \ge 50$) and leverage weights are isolated independently.

---

## 4. THE FIVE PILLARS OF RELIABILITY & SHRINKAGE

Player reliability is evaluated across five distinct dimensions:
1. **Absolute Pressure Performance (50%):** Standardized shrunk PAVA per delivery under high pressure ($BPI / BoPI \ge 50$).
2. **Baseline Retention Delta (20%):** Difference between high-pressure PAVA and low-pressure PAVA ($\text{PAVA}_{\text{high}} - \text{PAVA}_{\text{low}}$).
3. **Match-to-Match Consistency (15%):** Penalty on opportunity-adjusted per-match performance variance.
4. **Context Adaptability (15%):** Stability across IPL vs T20I competitions and 1st vs 2nd innings.
5. **Empirical Bayes Shrinkage:** Adjusts small samples toward the league prior using pseudo-count $K = 45.0$ deliveries:
   $$\tilde{v}_{\text{hp}} = \frac{n_{\text{hp}}}{n_{\text{hp}} + 45.0} \cdot \bar{v}_{\text{hp}} + \frac{45.0}{n_{\text{hp}} + 45.0} \cdot 0.0$$

The composite score is converted to a percentile metric: $\text{Reliability Score} = \Phi(\text{Composite}) \times 100.0$.

---

## 5. MATCH-CLUSTERED BOOTSTRAP UNCERTAINTY (N = 2,000)

Reliability scores were tested using **2,000 match-clustered bootstrap resamples** (fixed seed 42):
- Entire matches are sampled with replacement, preserving intra-match correlation structures.
- Generates 95% Confidence Intervals for scores and ranks, and computes exact Top-10 Inclusion Probabilities.
- Vectorized baseline reproduction tests prove that setting $k = 1$ across all matches reproduces official scores within 0.05 points.

---

## 6. RAJASTHAN ROYALS IPL 2027 STRATEGIC APPLICATION

The selected players address core tactical requirements for Rajasthan Royals' IPL 2027 squad construction:

1. **Death Bowling Mastery:**
   - **Haris Rauf (#2)** and **Nathan Ellis (#4)** offer world-class execution in overs 18–20. Pairing Ellis with Sandeep Sharma gives RR two elite defensive executors capable of defending targets under 10 RPO.
   - **Matheesha Pathirana (#6)** provides a generational slinging yorker strike weapon (58 death-over wickets, 8.97 Econ).
2. **Spin Depth & Powerplay Control:**
   - **Liam Dawson (#1)** and **Nasum Ahmed (#7)** provide left-arm powerplay economy (7.38 and 6.77 Econ), exploiting large boundary dimensions at the Sawai Mansingh Stadium.
   - **Sufiyan Muqeem (#5)** provides an unpickable left-arm wrist-spinner (6.00 career economy, 34 middle-overs wickets at 5.90 Econ).
3. **Clutch Hitting & Chasing Firepower:**
   - **Romario Shepherd (#5)** and **Jitesh Sharma (#8)** resolve late-order finishing needs, offering 180+ strike rates when chasing steep death-over totals.
   - **Suryakumar Yadav (#4)** and **Naman Dhir (#6)** deliver dominant, high-ceiling Indian middle-order batting.
   - **Ruturaj Gaikwad (#1)** and **Rohit Sharma (#2)** demonstrate ice-cold, elite top-order anchor-acceleration capability in high-voltage chases.

---

## 7. SUPPLEMENTARY RESEARCH: OPTION B HYBRID ARCHITECTURE

As part of the continuous validation mission, the research team developed the **Option B Hybrid Architecture** as Rajasthan Royals' technical roadmap:
- **Smooth Blowout Suppression:** Continuous sigmoid discount $\sigma((RRR - 4.5)/1.0)$ eliminates the BoPI blowout inversion, suppressing decided match scores from 80.96 to 55.4/100 without derivative cliffs.
- **Continuous Kish ESS Weighting:** Weighting deliveries by $w_i = \sigma((BPI_i - 42.0)/8.0)$ increases opener effective sample sizes by $15\times$ (Gaikwad ESS = 679.5 balls), permanently eliminating threshold edge cliffs.
- **Chronological Platt Calibration:** Reduces 2026 test win-probability ECE by 14.1% without test leakage.
- **Jasprit Bumrah Insight:** Eliminating blowout inflation elevates Jasprit Bumrah from #25 in Baseline to #4 in the Hybrid Model, reflecting his true clutch dominance.

---

## 8. CONCLUSION & SUBMISSION CERTIFICATION

Model A is certified as the official competition baseline, backed by 52 passing automated tests, verified SHA-256 raw data provenance, and 2,000-resample bootstrap stability. The Option B Hybrid Architecture provides an advanced, scientifically validated roadmap for Rajasthan Royals' future analytics operations.

