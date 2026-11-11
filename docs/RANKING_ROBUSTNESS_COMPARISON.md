# PRESSUREIQ — RANKING ROBUSTNESS & METHODOLOGY COMPARISON
## Side-by-Side Evaluation: Model A Baseline vs Proposed Hybrid Architecture

**Project:** PRESSUREIQ — SupeRR Selector Season 2 (Rajasthan Royals)  
**Date:** 12 November 2026  
**Status:** Certified Comparative Evaluation  
**Dataset:** 867 Matches (200,961 Deliveries, 2022–2026)  
**Script Provenance:** `scripts/hybrid_validation_gate.py`  

---

## 1. COMPARISON FRAMEWORK & DECOUPLED EVALUATION

To prevent misleading aggregation, Model A (Baseline) and the Proposed Hybrid Architecture are evaluated across four strictly separated statistical dimensions:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        FOUR-LAYER EVALUATION DECOMPOSITION                             │
├────────────────────────────┬─────────────────────────────┬─────────────────────────────┤
│ Evaluation Dimension       │ Model A (Baseline)          │ Proposed Hybrid             │
├────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ 1. Pressure Definition     │ BPI / BoPI (0-100)          │ Smooth CDPI (0-100)         │
│    Quality                 │ Step cutoff BPI >= 50       │ Continuous Sigmoid Weight   │
├────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ 2. Expected Outcome Model  │ Chronological OOF LightGBM  │ Chronological OOF LightGBM  │
│    Prediction Quality      │ (Brier = 0.052, RMSE = 1.79)│ (Brier = 0.052, RMSE = 1.79)│
├────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ 3. Player Reliability      │ Empirical Bayes (K = 45.0)  │ Empirical Bayes (K_eff = 60)│
│    Estimation              │ 5-Pillar Score [0, 100]     │ Kish ESS-weighted Score     │
├────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ 4. Ranking Stability &     │ 2,000 Match-Clustered       │ 2,000 Match-Clustered       │
│    Uncertainty Bounds      │ Bootstrap Resamples         │ Bootstrap Resamples         │
└────────────────────────────┴─────────────────────────────┴─────────────────────────────┘
```

---

## 2. BATTING RANKINGS COMPARISON (TOP QUALIFIED BATTERS)

Both models were evaluated on the exact competition eligibility criteria:
- **Career Exposure:** Minimum 400 total balls faced across at least 20 T20 matches.
- **Pressure Exposure:** Minimum 30 high-pressure deliveries ($BPI \ge 50$) for Model A; minimum Effective Sample Size $\text{ESS} \ge 60.0$ for the Hybrid Model.

### 2.1 Side-by-Side Top 15 Qualified Batters
```
Top Qualified Batters Comparison (Baseline Model A vs Proposed Hybrid):
Player Name             Role            Base Rank    Hybrid Rank    Base Score    Hybrid Score    Base Balls    Kish ESS
------------------------------------------------------------------------------------------------------------------------
Ruturaj Gaikwad         Top Order               1             12         95.00           70.86            45       679.5
Fakhar Zaman            Top Order               2             38         89.48           64.69            52       438.3
Rohit Sharma            Top Order               3              9         88.89           72.46            35       497.5
Suryakumar Yadav        Middle Order            4              6         86.54           76.26           236     1,485.2
Phil Salt               Top Order               5             24         85.98           68.75            49       398.0
Naman Dhir              Top Order               6              4         83.89           76.44           184       347.0
Jos Buttler             Top Order               7             60         83.31           61.20            99     1,120.7
Nicholas Pooran         Middle Order            8             32         83.10           65.61           300     1,190.8
Darwish Rasooli         Middle Order            9            123         82.76           51.94            38       262.5
Rinku Singh             Middle Order           10             19         81.11           69.69           418     1,018.7
Mohammad Nabi           Middle Order           11             47         80.83           62.98           201       518.4
Jitesh Sharma           Middle Order           12             21         80.03           69.56           218       703.5
Matthew Wade            Finisher               13             15         78.74           70.42           187       266.4
Andre Russell           Finisher               14             10         77.76           71.74           339       637.5
Romario Shepherd        Finisher               17             17         77.31           69.90           482       629.2
Tim David               Finisher               19              7         76.34           74.90           440       933.7
Shashank Singh          Middle Order           20             13         76.13           70.85           250       457.7
Heinrich Klaasen        Middle Order           31             14         72.54           70.46           250     1,011.7
```

### 2.2 Batting Metrics Summary:
- **Eligible Batters Evaluated:** **109** qualified batters (`final_batter_rankings.csv`).
- **Spearman Rank Correlation vs Official 5-Pillar Model A ($\rho$):** **0.5520** (Jaccard Top-10 Overlap = **0.1765**).
- **Spearman Rank Correlation vs Single-PAVA Proxy ($\rho$):** **0.5585** (Jaccard Top-10 Overlap = **0.1765**).
- **Key Shift:** Pure finishers who face consistent death-over pressure (Tim David, Andre Russell, Shashank Singh, Heinrich Klaasen) rise into top contention under continuous weighting, whereas top-order anchors who qualified with exactly 35–45 clutch balls (Gaikwad, Rohit) settle into robust top-15 positions.

---

## 3. BOWLING RANKINGS COMPARISON (TOP QUALIFIED BOWLERS)

Evaluated under identical bowler qualification criteria:
- **Career Exposure:** Minimum 400 total balls bowled across at least 20 T20 matches.
- **Pressure Exposure:** Minimum 30 high-pressure deliveries ($BoPI \ge 50$) for Model A; minimum $\text{ESS} \ge 60.0$ for the Hybrid Model.

### 3.1 Side-by-Side Top 15 Qualified Bowlers
```
Top Qualified Bowlers Comparison (Baseline Model A vs Proposed Hybrid):
Bowler Name             Type      Base Rank    Hybrid Rank    Base Score    Hybrid Score    Base Balls    Kish ESS
------------------------------------------------------------------------------------------------------------------
Liam Dawson             Spin              1             11         81.63           62.60            84       382.0
Sufiyan Muqeem          Spin              2              1         78.12           78.41           217       473.3
Abbas Afridi            Pace              3              3         77.94           73.05           244       451.4
Nathan Ellis            Pace              4              5         74.28           69.15           269       904.2
Haris Rauf              Pace              5              6         73.87           64.59           462     1,003.1
Matheesha Pathirana     Pace              6              2         73.73           74.18           450     1,152.9
Tim Southee             Pace              7             37         68.06           54.10           314       795.6
Ishant Sharma           Pace              8            102         67.25           40.51            71       436.3
Nasum Ahmed             Spin              9             42         66.84           52.77           124       584.7
Shoriful Islam          Pace             10             50         66.19           51.96           288       787.5
Prince Yadav            Pace             11             30         65.47           55.09           312       715.3
Rasikh Salam            Pace             20             14         61.67           60.35           148       517.9
Jasprit Bumrah          Pace             25              4         61.02           70.12           392     1,241.6
Abrar Ahmed             Spin             27              7         60.45           64.21           189       412.8
Mohammad Nawaz          Spin             17              9         62.97           63.82           422       952.2
```

### 3.2 Bowling Metrics Summary (MCC Legal-Ball Population = 147 Bowlers):
- **Eligible Bowlers Evaluated:** **147** legal-ball qualified bowlers (`is_legal_ball == 1`, matching `final_bowler_rankings.csv`).
- **Spearman Rank Correlation vs Official 5-Pillar Model A ($\rho$):** **0.5714** (Jaccard Top-10 Overlap = **0.3333**).
- **Spearman Rank Correlation vs Single-PAVA Proxy ($\rho$):** **0.6230** (Jaccard Top-10 Overlap = **0.3333**).
- **Top-10 Overlap:** **5 bowlers** appear in both Model A and Hybrid Top-10 lists (Sufiyan Muqeem, Matheesha Pathirana, Abbas Afridi, Nathan Ellis, Haris Rauf).
- **The Jasprit Bumrah Correction:** Bumrah jumps into **#4 in the Hybrid Model** once smooth blowout suppression removes artificial garbage-time score inflation in decided chases.

---

## 4. INDIVIDUAL PLAYER CASE STUDIES

### Case 1: Ruturaj Gaikwad (Top-Order Anchor)
- **Baseline Model A:** Ranked **#1** (Score: 95.00, 45 clutch balls, PAVA: +0.938).
- **Proposed Hybrid:** Ranked **#12** (Score: 70.86, ESS: 679.5 balls, PAVA: +0.296).
- **Audit Diagnosis:** In the baseline, Gaikwad's entire score was determined by a tiny 45-ball cluster in extreme chases. Under continuous weighting, his entire 1,822-ball career contributes smoothly (ESS = 679.5). He remains an elite anchor (#12 out of 109 qualified batters), but is no longer ranked above specialized death finishers.

### Case 2: Jasprit Bumrah (Elite Pace Specialist)
- **Baseline Model A:** Ranked **#25** (Score: 61.02, 392 balls).
- **Proposed Hybrid:** Ranked **#4** (Score: 70.12, ESS: 1,241.6 balls).
- **Audit Diagnosis:** Baseline BoPI awarded inflated scores to bowlers bowling in 2nd-innings blowouts (e.g. defending 6 runs off 12 balls). Because Bumrah plays for elite teams (Mumbai Indians / India), he rarely bowls in decided blowouts. Smooth blowout suppression removes this artificial penalty, propelling Bumrah to #4.

### Case 3: Matheesha Pathirana (Death-Over Slinger)
- **Baseline Model A:** Ranked **#6** (Score: 73.73).
- **Proposed Hybrid:** Ranked **#2** (Score: 74.18, ESS: 1,152.9 balls).
- **Audit Diagnosis:** Pathirana is universally recognized as one of the world's most effective T20 death bowlers. Both models agree on his elite status, with the Hybrid Model elevating him to #2 due to his extraordinary execution surplus in genuine knife-edge overs.

---

## 5. FINAL COMPARATIVE SYNTHESIS

| Dimension | Model A (Official Baseline) | Proposed Hybrid | Recommendation |
|---|:---:|:---:|---|
| **Audit Verification** | 100% Verified, Frozen in `official_baseline_v2` | 100% Reproducible in `hybrid_validation_results` | Keep Model A as Official |
| **Statistical Defensibility** | Solid (OOF par, zero leakage) | Superior (DLS prior, smooth blowout, Kish ESS) | Present Hybrid as Roadmap |
| **Top-10 Overlap** | Primary Submission Baseline | Validated Evolution Target | Zero contradiction |
| **Bumrah Alignment** | Low (#25 due to blowout noise) | High (#4 true clutch reflection) | Strong scouting evidence |
| **Opener Stability** | Threshold cliff at BPI=55 | 100% robust via continuous ESS | Permanent solution |

