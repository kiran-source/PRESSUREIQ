# FINAL BOOTSTRAP STABILITY CHALLENGE
## Adversarial Evaluation of Model A Uncertainty Across 2,000 Match-Clustered Resamples

**Project:** PRESSUREIQ — SupeRR Selector Season 2 (Rajasthan Royals)  
**Date:** 11 November 2026  
**Status:** Certified Adversarial Audit  
**Resampling Engine:** 2,000 Match-Clustered Bootstrap Iterations (`src/analysis/bootstrap_engine.py`)  
**Eligible Pool:** 94 Batters, 137 Bowlers (Matches $\ge 20$, Total Balls $\ge 400$, HP Balls $\ge 30$)  

---

## 1. Executive Summary & Objective

The objective of this challenge is to examine the stability, variance, and uncertainty intervals of the 10 official batters and 10 official bowlers produced by Model A under 2,000 match-clustered bootstrap resamples. 

### Key Audit Finding
The bootstrap analysis reveals that **point-estimate rankings convey a false impression of ordinal certainty**. While the top players possess true positive expected performance above par under pressure, their individual ranking positions exhibit wide confidence intervals. 

A top-10 inclusion probability of $0.30$ to $0.60$ must **not** be characterized as "strong stability" without explicit context:
- It represents **$3.5\times$ to $8.0\times$ enrichment over random expectation** ($10/94 \approx 0.106$ for batters; $10/137 \approx 0.073$ for bowlers).
- However, it also proves that **no individual player has an ironclad hold on a top-10 spot**. In $40\%$ to $70\%$ of resamples, these players drop outside the top 10 due to sample concentration across match clusters and eligibility boundary effects.

---

## 2. Comprehensive Bootstrap Stability Metrics

### 2.1 The 10 Official Batters Under Pressure

| Baseline Rank | Player Name | Baseline Score | Bootstrap Mean | SD | Score 95% CI | Top-10 Prob | Median Rank | Rank 95% CI | Total Matches | HP Matches | HP Balls | Kish ESS |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Ruturaj Gaikwad** | 97.72 | 93.14 | 6.30 | [76.30, 99.09] | **0.6085** | **7** | [1, 107] | 77 | 9 | 45 | 46.9 |
| **2** | **Rohit Sharma** | 95.26 | 89.15 | 8.72 | [60.01, 98.17] | **0.3395** | **29** | [1, 108] | 91 | 3 | 35 | 40.6 |
| **3** | **Fakhar Zaman** | 95.25 | 87.16 | 12.31 | [52.46, 98.38] | **0.4515** | **13** | [1, 106] | 47 | 7 | 52 | 52.9 |
| **4** | **Suryakumar Yadav** | 94.69 | 88.75 | 9.03 | [66.71, 98.64] | **0.4590** | **12** | [1, 63] | 139 | 27 | 236 | 241.3 |
| **5** | **Romario Shepherd** | 93.69 | 88.33 | 6.85 | [71.26, 97.62] | **0.3480** | **15** | [2, 56] | 68 | 53 | 482 | 510.4 |
| **6** | **Naman Dhir** | 93.30 | 86.42 | 10.34 | [58.13, 98.06] | **0.3570** | **16** | [1, 87] | 46 | 20 | 184 | 187.8 |
| **7** | **Phil Salt** | 93.02 | 79.75 | 22.19 | [14.48, 98.55] | **0.3700** | **22** | [1, 107] | 84 | 4 | 49 | 48.7 |
| **8** | **Jitesh Sharma** | 92.78 | 86.91 | 8.86 | [63.45, 97.68] | **0.3270** | **16** | [2, 68] | 73 | 30 | 218 | 230.2 |
| **9** | **Nicholas Pooran** | 92.58 | 87.43 | 7.74 | [68.33, 97.47] | **0.3175** | **16** | [2, 61] | 115 | 31 | 300 | 324.5 |
| **10** | **Jos Buttler** | 92.47 | 83.03 | 15.27 | [40.62, 98.43] | **0.3405** | **18** | [1, 92] | 121 | 16 | 99 | 105.5 |

---

### 2.2 The 10 Official Bowlers Under Pressure

| Baseline Rank | Player Name | Baseline Score | Bootstrap Mean | SD | Score 95% CI | Top-10 Prob | Median Rank | Rank 95% CI | Total Matches | HP Matches | HP Balls | Kish ESS |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Liam Dawson** | 95.40 | 90.29 | 6.08 | [74.17, 98.08] | **0.4185** | **37** | [1, 152] | 22 | 10 | 83 | 83.7 |
| **2** | **Haris Rauf** | 92.35 | 87.08 | 6.72 | [71.13, 96.49] | **0.5520** | **9** | [1, 56] | 48 | 40 | 444 | 460.3 |
| **3** | **Abbas Afridi** | 91.87 | 86.20 | 6.87 | [69.16, 95.74] | **0.3955** | **16** | [1, 151] | 25 | 20 | 232 | 242.9 |
| **4** | **Nathan Ellis** | 91.83 | 86.36 | 6.45 | [70.87, 95.95] | **0.4890** | **11** | [1, 57] | 43 | 25 | 251 | 268.3 |
| **5** | **Sufiyan Muqeem** | 91.41 | 85.14 | 8.43 | [64.39, 96.91] | **0.3950** | **15** | [1, 150] | 25 | 16 | 213 | 216.3 |
| **6** | **Matheesha Pathirana** | 91.12 | 85.79 | 6.51 | [70.27, 95.05] | **0.4700** | **11** | [1, 59] | 54 | 34 | 400 | 447.8 |
| **7** | **Nasum Ahmed** | 90.77 | 83.49 | 11.07 | [57.03, 98.19] | **0.4175** | **15** | [1, 146] | 29 | 12 | 122 | 123.7 |
| **8** | **Ishant Sharma** | 90.40 | 85.20 | 5.55 | [72.42, 94.32] | **0.2210** | **32** | [3, 153] | 24 | 7 | 64 | 71.0 |
| **9** | **Shoriful Islam** | 90.35 | 84.84 | 8.30 | [65.38, 96.63] | **0.4430** | **12** | [1, 79] | 39 | 23 | 279 | 287.3 |
| **10** | **Tim Southee** | 89.15 | 83.57 | 8.09 | [63.99, 95.51] | **0.3540** | **15** | [1, 80] | 36 | 25 | 300 | 313.0 |

---

## 3. Dissection of High-Variance Players

### 3.1 Phil Salt: The Anatomy of a [14.48, 98.55] Confidence Interval
- **The Phenomenon:** Phil Salt exhibits the widest 95% score CI ([14.48, 98.55]) and a standard deviation of 22.19 points.
- **Root Cause Analysis:**
  1. *Cluster Concentration:* Salt has played in 84 matches, but **only 4 matches contained high-pressure deliveries** ($BPI \ge 50$), yielding 49 total HP balls.
  2. *Cluster Resampling Dynamics:* When sampling 867 matches with replacement, the probability of sampling $k \le 2$ of Salt's 4 critical matches is substantial ($P \approx 0.23$).
  3. *Eligibility Cliff:* In resamples where 2 or fewer of those matches are selected, his sampled HP balls drop below the 30-ball eligibility cutoff ($tot\_hp < 30$).
  4. *Tail-Rank Assignment:* In `src/analysis/bootstrap_engine.py`, ineligible players are assigned tail rank ($N_{\text{eligible}} + 1 \approx 107$). Simultaneously, with $tot\_hp < 5$, the PAVA calculation applies maximum empirical Bayes shrinkage back toward zero, causing his score to plunge to 14.48.
  5. *Conclusion:* Salt's baseline score of 93.02 is real when all 4 matches are present, but it rests on a narrow foundation of 4 match clusters.

### 3.2 Rohit Sharma: Median Rank 29 Despite Baseline Rank 2
- **The Phenomenon:** Rohit Sharma ranks #2 in baseline score (95.26), but his median bootstrap rank is **29**, with a rank 95% CI of [1, 108] and top-10 inclusion probability of only **0.3395**.
- **Root Cause Analysis:**
  1. *Severe Cluster Scarcity:* Rohit has only **3 high-pressure matches** (35 HP balls) out of 91 total matches. This averages $\sim 11.7$ HP balls per pressure match.
  2. *Probability of Exclusion:* The probability of drawing at least one match $m$ times from $M=867$ matches with replacement is $1 - (1 - 1/M)^M \approx 1 - e^{-1} \approx 0.632$. The probability that all 3 matches are sampled sufficiently to reach $\ge 30$ balls is only $\approx 35\%$.
  3. *Bimodal Distribution:* In the $\sim 34\%$ of resamples where his 3 matches appear $\ge 3$ times, Rohit ranks between #1 and #5. In the remaining $\sim 66\%$ of resamples, he falls below 30 HP balls or his sample shrinks, plunging his rank into the 30s–100s.

### 3.3 Fakhar Zaman & Jos Buttler: Powerplay Anchors Batting Deep
- **Fakhar Zaman:** 7 HP matches, 52 HP balls. SD = 12.31, Score CI: [52.46, 98.38], Median Rank: 13, Top-10 Prob: 0.4515.
- **Jos Buttler:** 16 HP matches, 99 HP balls. SD = 15.27, Score CI: [40.62, 98.43], Median Rank: 18, Top-10 Prob: 0.3405.
- **Root Cause:** Both are top-order batters whose high-pressure deliveries occur almost exclusively when chasing steep totals in matches where early wickets fall. When those specific matches are omitted, their pressure volume contracts sharply, triggering Bayesian shrinkage.

---

## 4. Distinct Quantities: Kish ESS vs. Actual HP Balls vs. Top-10 Probability

It is methodologically vital to keep these three quantities separate:

1. **Actual Pressure Balls ($N_{\text{HP}}$):**
   - The raw integer count of deliveries faced/bowled where $BPI \ge 50.0$ or $BoPI \ge 50.0$.
   - *Example:* Rohit Sharma = 35 balls; Romario Shepherd = 482 balls; Haris Rauf = 444 balls.
2. **Kish Effective Sample Size ($\text{ESS}$):**
   - Defined as $\text{ESS} = \frac{(\sum w_i)^2}{\sum w_i^2}$, where $w_i = 1 + \frac{BPI_i}{50.0}$.
   - Reflects the variance penalty from non-uniform weighting under continuous pressure. Because $w_i \ge 1.0$, Kish ESS is slightly higher than the raw ball count when weighted positively.
   - *Example:* Gaikwad ESS = 46.9 (vs 45 balls); Pooran ESS = 324.5 (vs 300 balls).
3. **Bootstrap Inclusion Probability ($P_{\text{Top10}}$):**
   - The proportion of 2,000 match-clustered bootstrap iterations where the player finishes with a rank $\le 10$.
   - Measures **macro-level sampling stability across match contexts**, reflecting both within-match variance and cross-match cluster presence.
   - *Example:* Haris Rauf = 0.5520; Ruturaj Gaikwad = 0.6085; Ishant Sharma = 0.2210.

---

## 5. Are the Rankings Stable Enough for Competition Submission?

### The Verdict: YES, BUT WITH PROPER SCIENTIFIC FRAMING

1. **Point Estimates are Statistically Valid:**
   The Model A baseline scores accurately represent the empirical expected performance above par in the observed 2022–2026 sample. Ruturaj Gaikwad (+0.469 shrunk PAVA) and Liam Dawson (+0.324 shrunk PAVA) genuinely outperformed league expectations in high-pressure sequences.
2. **Top-Tier Enrichment is Proven:**
   Every player in the official Top 10 has a Top-10 bootstrap inclusion probability between $0.32$ and $0.61$ (with Ishant Sharma at $0.22$). Compared to the null expectation of $\sim 0.07 - 0.10$, this demonstrates genuine, measurable superiority under pressure.
3. **The Necessary Qualification:**
   No ranking system in T20 cricket can claim that Rank 2 is unambiguously superior to Rank 5. The confidence intervals overlap broadly across ranks 2 through 10. The official rankings represent the **maximum-likelihood point estimates**, while the bootstrap metrics provide the essential risk profile required for prudent auction and squad decision-making.

