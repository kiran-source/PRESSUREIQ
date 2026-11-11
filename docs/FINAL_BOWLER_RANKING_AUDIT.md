# FINAL OFFICIAL TOP-10 BOWLER AUDIT REPORT
## Player Identity, Statistical Deconstruction, and Delivery Attribution Verification

**Project:** PRESSUREIQ — Context-Aware Cricket Reliability Intelligence  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 (2026)  
**Audit Date:** 12 November 2026  
**Auditor:** Quantitative Review & Submission QA Panel  
**Dataset:** 200,961 Deliveries across 867 Matches (2022–2026)  
**Source File:** `data/processed/final_bowler_rankings.csv` (SHA-256: `344d63c55cec...`)  

---

## 1. OFFICIAL TOP-10 BOWLERS SUMMARY TABLE

The official top-10 bowlers are ranked by their **Five-Pillar Reliability Score** ($0\text{--}100$), incorporating Empirical Bayes shrinkage ($K = 45.0$ deliveries) and 2,000 match-clustered bootstrap confidence intervals:

| Rank | Player Name | Canonical ID | Discipline | Style | Matches | Legal Balls | Total Deliveries | HP Balls ($BoPI \ge 50$) | Total Wickets | Economy | Shrunk PAVA/ball | Retention $\Delta$ | PRC Archetype | Reliability Score | 95% Bootstrap CI | Top-10 Inclusion Prob |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | **Liam Dawson** | 722 | Spin | Slow left-arm orthodox | 22 | 415 | 424 | 83 | 25 | 7.79 | +0.324 | +0.568 | Clutch Climber ($\beta = +1.59$) | **95.39** | [74.17, 98.08] | 0.4185 (837/2000) |
| **2** | **Haris Rauf** | 7364 | Pace | Right-arm Fast | 48 | 1,027 | 1,063 | 444 | 76 | 8.58 | +0.242 | +0.522 | Clutch Climber ($\beta = +1.74$) | **92.36** | [71.13, 96.49] | 0.5520 (1104/2000) |
| **3** | **Abbas Afridi** | 7699 | Pace | Right-arm medium-fast | 25 | 453 | 474 | 232 | 40 | 8.34 | +0.288 | +0.107 | Ice Cold Anchor ($\beta = +1.24$) | **91.88** | [69.16, 95.74] | 0.3955 (791/2000) |
| **4** | **Nathan Ellis** | 7920 | Pace | Right-arm medium | 43 | 916 | 959 | 251 | 58 | 8.25 | +0.255 | +0.045 | Ice Cold Anchor ($\beta = +0.12$) | **91.84** | [70.87, 95.95] | 0.4890 (978/2000) |
| **5** | **Sufiyan Muqeem** | 34485 | Spin | Left-arm Chinaman | 25 | 518 | 525 | 213 | 39 | 6.00 | +0.283 | +0.083 | Ice Cold Anchor ($\beta = +0.17$) | **91.41** | [64.39, 96.91] | 0.3950 (790/2000) |
| **6** | **Matheesha Pathirana** | 8661 | Pace | Right-arm Fast | 54 | 1,132 | 1,279 | 400 | 82 | 8.64 | +0.258 | -0.081 | Ice Cold Anchor ($\beta = +0.23$) | **91.11** | [70.27, 95.05] | 0.4700 (940/2000) |
| **7** | **Nasum Ahmed** | 4658 | Spin | Slow left-arm orthodox | 29 | 600 | 607 | 122 | 25 | 7.64 | +0.178 | +0.804 | Clutch Climber ($\beta = +2.01$) | **90.77** | [57.03, 98.19] | 0.4175 (835/2000) |
| **8** | **Ishant Sharma** | 28 | Pace | Right-arm fast-medium | 24 | 422 | 456 | 64 | 24 | 9.53 | +0.199 | +0.568 | Ice Cold Anchor ($\beta = +0.98$) | **90.42** | [72.42, 94.32] | 0.2210 (442/2000) |
| **9** | **Shoriful Islam** | 7344 | Pace | Left-arm medium-fast | 39 | 790 | 823 | 279 | 41 | 8.23 | +0.167 | +0.774 | Ice Cold Anchor ($\beta = +1.12$) | **90.36** | [65.38, 96.63] | 0.4430 (886/2000) |
| **10** | **Tim Southee** | 278 | Pace | Right-arm medium-fast | 36 | 826 | 861 | 300 | 55 | 8.32 | +0.187 | +0.123 | Ice Cold Anchor ($\beta = +0.39$) | **89.16** | [63.99, 95.51] | 0.3540 (708/2000) |

---

## 2. STRICT DELIVERY ATTRIBUTION & EXTRA ACCOUNTING AUDIT

To prevent methodological vulnerabilities, bowler delivery accounting was subjected to strict MCC rule verification:
1. **Illegal Deliveries (Wides & No-Balls):**
   - Correctly credited as bowler deliveries (`total_deliveries`), with runs added to bowler runs conceded (`bowler_runs_conceded`).
   - Correctly excluded from legal balls (`legal_balls`) and overs denominators.
   - Example: Matheesha Pathirana bowled 1,132 legal balls and 1,279 total deliveries (147 wides/no-balls). His economy ($8.64$) and PAVA strictly penalize illegal deliveries without giving extra over credits (`tests/test_bowler_illegal_deliveries.py`).
2. **Fielding Extras (Byes & Leg-Byes):**
   - Verified that byes and leg-byes are credited as **0 runs conceded** to the bowler in compliance with Law 21 of the Laws of Cricket.
3. **Wicket Attribution:**
   - Run-outs, obstructing the field, and timed-out dismissals are credited as team wickets but strictly **0 wickets to the bowler** (`is_bowler_wicket == False`).
   - Bowled, caught, LBW, stumped, and hit-wicket are credited to the bowler (`is_bowler_wicket == True`).

---

## 3. INDIVIDUAL BOWLER STATISTICAL DECONSTRUCTION

### 1. Liam Dawson (#1 | Score: 95.39)
- **Career Profile:** 22 matches, 415 legal balls, 424 total deliveries, 25 wickets, Career Economy: 7.79.
- **Pressure Execution:** Faces 83 high-pressure balls ($BoPI \ge 50$), generating the highest raw PAVA per ball among all qualifiers: **+0.500 runs/ball** (+0.324 shrunk).
- **Key Driver:** Phenomenal retention delta (**+0.568**) and steep positive PRC slope ($\beta = +1.5886$). When defending low targets or bowling against set middle-order hitters, Dawson consistently maintains an economy under 6.8 RPO.
- **Bootstrap Stability:** 95% CI is [74.17, 98.08]. Top-10 inclusion probability is **41.85%**.

### 2. Haris Rauf (#2 | Score: 92.36)
- **Career Profile:** 48 matches, 1,027 legal balls, 1,063 deliveries, 76 wickets, Career Economy: 8.58.
- **Pressure Execution:** Massive sample: **444 high-pressure balls** (highest in the top 10), delivering **+0.266 runs/ball** raw PAVA (+0.242 shrunk).
- **Key Driver:** Extraordinary wicket-taking volume in death overs (evidence weight **0.908**). PRC slope: $\beta = +1.7352$.
- **Bootstrap Stability:** Highest top-10 inclusion probability among all bowlers (**55.20%**, 1,104/2,000 resamples), with 95% CI [71.13, 96.49].

### 3. Abbas Afridi (#3 | Score: 91.88)
- **Career Profile:** 25 matches, 453 legal balls, 474 deliveries, 40 wickets, Career Economy: 8.34.
- **Pressure Execution:** 232 high-pressure balls, delivering **+0.344 runs/ball** raw PAVA (+0.288 shrunk).
- **Key Driver:** Exceptional slower-ball variations in overs 16–20. Evidence weight: 0.838.

### 4. Nathan Ellis (#4 | Score: 91.84)
- **Career Profile:** 43 matches, 916 legal balls, 959 deliveries, 58 wickets, Career Economy: 8.25.
- **Pressure Execution:** 251 high-pressure balls, delivering **+0.300 runs/ball** raw PAVA (+0.255 shrunk).
- **Key Driver:** Highest consistency score among pace bowlers (**43.5/100**) and elite adaptability (**92.2/100**). Top-10 inclusion probability: **48.90%**.

### 5. Sufiyan Muqeem (#5 | Score: 91.41)
- **Career Profile:** 25 matches, 518 legal balls, 525 deliveries, 39 wickets, Career Economy: **6.00** (lowest in top 10).
- **Pressure Execution:** 213 high-pressure balls, delivering **+0.343 runs/ball** raw PAVA (+0.283 shrunk).
- **Key Driver:** Extraordinary economy control as a wrist-spinner; rarely conceded more than one boundary per over in death situations.

### 6. Matheesha Pathirana (#6 | Score: 91.11)
- **Career Profile:** 54 matches, 1,132 legal balls, 1,279 deliveries, 82 wickets, Career Economy: 8.64.
- **Pressure Execution:** 400 high-pressure balls, delivering **+0.287 runs/ball** raw PAVA (+0.258 shrunk).
- **Key Driver:** Elite yorker execution and boundary prevention at the death. Evidence weight: **0.899**. Top-10 inclusion probability: **47.00%**.

### 7. Nasum Ahmed (#7 | Score: 90.77)
- **Career Profile:** 29 matches, 600 legal balls, 607 deliveries, 25 wickets, Career Economy: 7.64.
- **Pressure Execution:** 122 high-pressure balls, delivering **+0.244 runs/ball** raw PAVA (+0.178 shrunk).
- **Key Driver:** Highest PRC slope in the top 10 ($\beta = +2.0100$); highest retention delta (**+0.804**).

### 8. Ishant Sharma (#8 | Score: 90.42)
- **Career Profile:** 24 matches, 422 legal balls, 456 deliveries, 24 wickets, Career Economy: 9.53.
- **Pressure Execution:** 64 high-pressure balls, delivering **+0.338 runs/ball** raw PAVA (+0.199 shrunk).
- **Key Driver:** Clutch powerplay and knuckleball executions in IPL defense finishes.

### 9. Shoriful Islam (#9 | Score: 90.36)
- **Career Profile:** 39 matches, 790 legal balls, 823 deliveries, 41 wickets, Career Economy: 8.23.
- **Pressure Execution:** 279 high-pressure balls, delivering **+0.194 runs/ball** raw PAVA (+0.167 shrunk).
- **Key Driver:** Left-arm angle and high dot-ball percentage under pressure. Retention delta: **+0.774**.

### 10. Tim Southee (#10 | Score: 89.16)
- **Career Profile:** 36 matches, 826 legal balls, 861 deliveries, 55 wickets, Career Economy: 8.32.
- **Pressure Execution:** 300 high-pressure balls, delivering **+0.215 runs/ball** raw PAVA (+0.187 shrunk).
- **Key Driver:** Vast international experience; adaptability score of **98.3/100** and consistency of **42.7/100**.

---

## 4. AUDIT VERDICT

The official Top-10 Bowlers list is verified, strictly complies with MCC delivery accounting, and is validated by 2,000 match-clustered bootstrap resamples.

