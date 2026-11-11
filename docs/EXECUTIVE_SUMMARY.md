# EXECUTIVE SUMMARY: PRESSUREIQ
## SupeRR Selector Season 2 (Round 1) — Rajasthan Royals Submission Dossier

**Framework Name**: PRESSUREIQ — A Context-Aware Cricket Reliability Intelligence Framework  
**Author**: Lead Data Scientist & Cricket Analytics Researcher  
**Target Competitions**: Indian Premier League (IPL) & Men's T20 Internationals (T20I), 2022–2026  
**Data Volume**: 200,999 Deliveries | 867 Matches | 959 Players  
**Status**: Fully Built, Tested, Validated, and Reproducible  

---

## 1. Executive Brief & Core Objective

The central challenge of the **SupeRR Selector Season 2** competition is to look beyond surface-level aggregates (raw batting strike rates, career averages, aggregate wickets) and isolate true player reliability when match leverage is at its highest.

Traditional statistics suffer from two fatal distortions:
1. **Context Insensitivity**: A boundary scored when needing 14 off 18 balls is counted identically to a boundary scored when needing 38 off 14 balls against high-velocity death bowling.
2. **Stat-Padding / Low-Stakes Inflation**: Batters and bowlers frequently accumulate volume during low-leverage phases (e.g. chasing dead rubbers or batting in low-pressure first-innings phases), masking severe vulnerabilities during critical climax deliveries.

**PRESSUREIQ** resolves this by building a causal, leakage-free intelligence pipeline that:
- Quantifies contextual difficulty on a continuous 0–100 scale: **Batting Pressure Index (BPI)** and **Bowling Pressure Index (BoPI)**.
- Models expected baseline outcomes ($E[\text{runs}]$, $P(\text{dismissal})$, $P(\text{boundary})$) through calibrated chronological walk-forward machine learning models.
- Measures **Pressure-Adjusted Value Added (PAVA)** per delivery as pure unamplified execution surplus (runs/ball), completely accounting for illegal deliveries.
- Deconstructs player performance into **Five Quantitative Pillars** (Absolute Pressure Value, Retention Delta, Match Consistency, Context Adaptability, and Empirical Bayes Sample Weight).
- Fits **Pressure Response Curves (PRC)** to distinguish *Clutch Climbers*, *Ice Cold Anchors*, and *Pressure Fragile* players.
- Assesses ranking stability through **2,000 match-clustered bootstrap resamples**.

---

## 2. Official Unstop Selections (Ranked 1 to 10)

These selections are strictly computed from empirical data, shrunk using Empirical Bayes ($K=45$ balls) to penalize small samples, and bounded by 95% match-clustered bootstrap confidence intervals ($N=2,000$).

### 🏏 10 Most Reliable Batters Under Pressure
| Rank | Player Name | Tactical Role | Reliability Score | 95% Confidence Interval | Top-10 Inclusion Prob | HP Deliveries | Shrunk HP PAVA/ball | Retention Delta ($\Delta$) | PRC Archetype | Primary Franchise / Country |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---|
| **1** | **Ruturaj Gaikwad** | Top Order | **97.71** | `[76.30, 99.09]` | 60.85% | 45 | +0.469 | +0.867 | *Clutch Climber* | Chennai Super Kings / India |
| **2** | **Rohit Sharma** | Top Order | **95.27** | `[60.01, 98.17]` | 33.95% | 35 | +0.383 | +0.770 | *Clutch Climber* | Mumbai Indians / India |
| **3** | **Fakhar Zaman** | Top Order | **95.25** | `[52.46, 98.38]` | 45.15% | 52 | +0.407 | +0.770 | *Clutch Climber* | Lahore Qalandars / Pakistan |
| **4** | **Suryakumar Yadav** | Middle Order | **94.68** | `[66.71, 98.64]` | 45.90% | 236 | +0.424 | +0.300 | *Clutch Climber* | Mumbai Indians / India |
| **5** | **Romario Shepherd** | Finisher | **93.69** | `[71.26, 97.62]` | 34.80% | 482 | +0.323 | +0.849 | *Pressure Fragile* | Mumbai Indians / West Indies |
| **6** | **Naman Dhir** | Top Order | **93.30** | `[58.13, 98.06]` | 35.70% | 184 | +0.385 | +0.459 | *Clutch Climber* | Mumbai Indians / India |
| **7** | **Phil Salt** | Top Order | **93.01** | `[14.48, 98.55]` | 37.00% | 49 | +0.361 | +0.396 | *Ice Cold Anchor* | Kolkata Knight Riders / England |
| **8** | **Jitesh Sharma** | Middle Order | **92.79** | `[63.45, 97.68]` | 32.70% | 218 | +0.342 | +0.506 | *Clutch Climber* | Punjab Kings / India |
| **9** | **Nicholas Pooran** | Middle Order | **92.58** | `[68.33, 97.47]` | 31.75% | 300 | +0.387 | +0.199 | *Ice Cold Anchor* | Lucknow Super Giants / West Indies |
| **10** | **Jos Buttler** | Top Order | **92.45** | `[40.62, 98.43]` | 34.05% | 99 | +0.357 | +0.365 | *Ice Cold Anchor* | Rajasthan Royals / England |

---

### 🎯 10 Most Reliable Bowlers Under Pressure
| Rank | Player Name | Discipline | Reliability Score | 95% Confidence Interval | Top-10 Inclusion Prob | HP Deliveries | Shrunk HP PAVA/ball | Retention Delta ($\Delta$) | PRC Archetype | Primary Franchise / Country |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---|
| **1** | **Liam Dawson** | Spin | **95.39** | `[74.17, 98.08]` | 41.85% | 83 | +0.324 | +0.568 | *Clutch Climber* | England |
| **2** | **Haris Rauf** | Pace | **92.36** | `[71.13, 96.49]` | 55.20% | 444 | +0.242 | +0.522 | *Clutch Climber* | Lahore Qalandars / Pakistan |
| **3** | **Abbas Afridi** | Pace | **91.88** | `[69.16, 95.74]` | 39.55% | 232 | +0.288 | +0.107 | *Ice Cold Anchor* | Pakistan |
| **4** | **Nathan Ellis** | Pace | **91.84** | `[70.87, 95.95]` | 48.90% | 251 | +0.255 | +0.045 | *Ice Cold Anchor* | Punjab Kings / Australia |
| **5** | **Sufiyan Muqeem** | Spin | **91.41** | `[64.39, 96.91]` | 39.50% | 213 | +0.283 | +0.083 | *Ice Cold Anchor* | Pakistan |
| **6** | **Matheesha Pathirana** | Pace | **91.11** | `[70.27, 95.05]` | 47.00% | 400 | +0.258 | -0.081 | *Ice Cold Anchor* | Chennai Super Kings / Sri Lanka |
| **7** | **Nasum Ahmed** | Spin | **90.77** | `[57.03, 98.19]` | 41.75% | 122 | +0.178 | +0.804 | *Clutch Climber* | Bangladesh |
| **8** | **Ishant Sharma** | Pace | **90.42** | `[72.42, 94.32]` | 22.10% | 64 | +0.199 | +0.568 | *Ice Cold Anchor* | Delhi Capitals / India |
| **9** | **Shoriful Islam** | Pace | **90.36** | `[65.38, 96.63]` | 44.30% | 279 | +0.167 | +0.774 | *Ice Cold Anchor* | Bangladesh |
| **10** | **Tim Southee** | Pace | **89.16** | `[63.99, 95.51]` | 35.40% | 300 | +0.187 | +0.123 | *Ice Cold Anchor* | Kolkata Knight Riders / New Zealand |

---

## 3. Five Methodological Breakthroughs of PRESSUREIQ

1. **Elimination of PAVA Double-Counting**:
   Because baseline models already include pressure difficulty features, PAVA isolates pure above-expectation execution surplus ($V_{\text{raw}}$), ensuring retention deltas represent true clutch ability rather than formulaic scale inflation.
2. **Complete Zero-Leakage Chronological Pipeline**:
   All features (first-innings par, player histories, expected outcomes, and categorical encodings) are strictly time-isolated, preventing future and same-match visibility.
3. **Rigorous Handling of Cricket Laws**:
   Includes full DLS revised legal-ball allocations for shortened innings and complete penalization of wides and no-balls against bowlers.
4. **Empirical Bayes Variance Regularization ($K=45$)**:
   Prevents low-sample distortion by pulling volatile estimates toward reliable player priors.
5. **Full Probabilistic Stability Reporting**:
   2,000 match-clustered bootstrap iterations provide empirical 95% confidence intervals and candidate inclusion probabilities rather than misleading deterministic single-rank assertions.
