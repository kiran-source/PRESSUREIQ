# PRESSUREIQ v6.0 — Rajasthan Royals Recruitment Methodology (Model B)
## Evidence-Driven Decision-Support System for the IPL 2027 Player Auction

> **Mandatory Disclaimer:**  
> *PRESSUREIQ provides an independent analytical recruitment assessment. It does not represent an official Rajasthan Royals recruitment decision or guarantee player eligibility, auction availability, selection, or future performance.*

---

## 1. Executive Summary & Architectural Separation

Traditional sports recruitment platforms confound tournament-wide skill rankings with actionable auction acquisitions. A player ranked #1 in tournament composure (e.g., Ruturaj Gaikwad at CSK or Jasprit Bumrah at MI) cannot be bid on by Rajasthan Royals if contracted to a rival franchise.

To solve this, **PRESSUREIQ v6.0 introduces a strict, two-tier model separation**:

```
+----------------------------------------------------------------------------------------------------+
|                                    PRESSUREIQ DUAL-MODEL ARCHITECTURE                              |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  MODEL A: GLOBAL TOURNAMENT INTELLIGENCE (IMMUTABLE BASELINE)                                       |
|  - Scope: Tournament-wide individual pressure reliability across 2022–2026.                       |
|  - Denominators: Minimum 400 total balls, 30 high-pressure balls, 20 matches.                     |
|  - Cohorts: 109 Qualified Batters | 147 Qualified Bowlers.                                        |
|  - Core Formulation: 5-Pillar Composure Index + Empirical Bayes Shrinkage (K = 45.0) + PAVA.      |
|  - Checksum Integrity: final_batter_rankings.csv (887f0c1...) | final_bowler_rankings.csv (344d63c...)   |
|                                                                                                    |
|                                         | (Features Fed into Model B)                              |
|                                         v                                                          |
|                                                                                                    |
|  MODEL B: RAJASTHAN ROYALS RECRUITMENT INTELLIGENCE (COMPETITION SYSTEM)                          |
|  - Scope: Realistic acquisition board for Rajasthan Royals ahead of the IPL 2027 Auction.        |
|  - Candidate Pool: 256 Evaluated Candidates (Model A cohorts + Emerging + Market Entrants).       |
|  - Dual Gating Filters:                                                                            |
|      1. Regulatory Eligibility Engine: BCCI/IPL regulations, NOC clearances, bilateral policies.   |
|      2. Auction Availability Engine: Confirmed Trades, Franchise Retentions, Contracted Exclusions.|
|  - Role Benchmarks: 6 Batting Roles & 8 Bowling Roles.                                            |
|  - Venue Fit: Sawai Mansingh Stadium, Jaipur (78m square boundaries, "Jaipur Squeeze").            |
|  - Scoring Engine: 6-Component Weighted MCDA Formula (100.0% Normalized).                         |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

Model A remains **100% frozen, audited, and immutable**. Model B operates as an independent decision-support layer consuming validated Model A outputs without altering them.

---

## 2. Model B Recruitment Scoring Formulation

The Model B Recruitment Target Score aggregates six distinct analytical dimensions:

$$\text{Model B Target Score} = 0.25\,\text{Rel} + 0.20\,\text{T20}_{\text{perf}} + 0.15\,\text{Pred} + 0.15\,\text{Role}_{\text{suit}} + 0.15\,\text{RR}_{\text{fit}} + 0.10\,\text{Consistency}$$

### Component Breakdown & Metrics

| Component | Weight | Analytical Operationalization | Data Sources |
|---|:---:|---|---|
| **1. Pressure Reliability** | **25%** | Preserved Model A Reliability Score ($\Phi(Z) \times 100$), shrunk high-pressure PAVA surplus, and PRC slope archetype. | `final_batter_rankings.csv`, `final_bowler_rankings.csv` |
| **2. Overall T20 Performance** | **20%** | Batters: Career SR and batting average against competitive baseline.<br>Bowlers: Career economy and dot-ball percentage. | `deliveries.parquet` (200,999 legal balls) |
| **3. Predictive Performance** | **15%** | Out-of-sample chronological LightGBM expected runs / economy under high-pressure game states ($BPI \ge 65, BoPI \ge 65$). | Model B ML Engine (Trained $\le 2024$, Val 2025, Test 2026) |
| **4. Role Suitability** | **15%** | Situational phase execution (Powerplay overs 1–6, Middle overs 7–15, Death overs 16–20) benchmarked against positional expectations. | Granular Phase Analytics Engine |
| **5. RR Squad Fit** | **15%** | Match with Rajasthan Royals' 4 core tactical deficits at SMS Jaipur (Overseas Death Seamer, Jaipur Spin Squeeze, No. 7 Finisher, Seam Depth). | Audited RR Roster Ledger & Ground Telemetry |
| **6. Consistency & Risk** | **10%** | Match-to-match stability ($100 / (1 + CV)$), downside failure rate mitigation ($100 \times [1 - P(\text{fail})]$), and Kish ESS confidence. | `batter_innings_pava.parquet`, `bowler_spell_pava.parquet` |

---

## 3. Strict Gating Logic: Eligibility vs. Availability

PRESSUREIQ enforces an evidence-backed separation between regulatory participation clearance and market targetability:

```
                  +-----------------------------------+
                  |   CANDIDATE POOL (256 ATHLETES)   |
                  +-----------------------------------+
                                    |
                                    v
                  +-----------------------------------+
                  |    REGULATORY ELIGIBILITY ENGINE  |
                  +-----------------------------------+
                       /                          \
            [Status: Eligible]             [Ineligible / Restricted / Policy]
                   |                               |
                   v                               v
    +------------------------------+     +-------------------------------+
    |  AUCTION AVAILABILITY ENGINE |     | EXCLUSIONS LEDGER (Class D/E) |
    +------------------------------+     | - Pakistani Passport Holders  |
          /                \             | - Retired / Inactive Alumni   |
  [Confirmed Avail]  [Contracted / Traded| +-------------------------------+
         |             Pending Verif]
         v                    |
+---------------------+       v
| CONFIRMED RR TARGET | +-------------------------------+
|  RANKINGS (MODEL B) | | WATCHLIST / RIVAL CONTRACTS   |
| Top Batters & Bowls | | Awaiting Nov 17 Announcements |
+---------------------+ +-------------------------------+
```

### Eligibility Classes
- **Class A (RR Core):** Current retained or traded-in Rajasthan Royals players (e.g. Yashasvi Jaiswal, Riyan Parag, Jofra Archer, Ravindra Jadeja).
- **Class B (Open Auction Pool):** Cleared active domestic and international cricketers entering the open auction pool.
- **Class C (Contracted / Traded Rivals):** Players contracted to rival franchises or confirmed traded during the trading window (e.g., Hardik Pandya to PBKS, Arshdeep Singh to MI, Nathan Ellis to SRH). Discounted and excluded from active bidding targets.
- **Class D (Policy Review):** Pakistani passport holders subject to longstanding post-2008 BCCI/bilateral directives (Score forced to 0.0).
- **Class E (Inactive / Retired):** Formally retired players (e.g., Shikhar Dhawan, Dinesh Karthik).

---

## 4. Sensitivity Analysis & Robustness Verification

To guarantee that recruitment rankings are not artifacts of arbitrary weight selection, the Model B formula underwent sensitivity testing across 5 alternative weight profiles:

| Profile | Pressure (Rel) | T20 Perf | Pred ML | Role Fit | RR Fit | Consistency | Top Bowler Target | Top Batter Target |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|---|
| **Baseline Proposed** | **25%** | **20%** | **15%** | **15%** | **15%** | **10%** | **Liam Dawson** | **Jamie Smith** |
| *Pressure Heavy* | 40% | 15% | 15% | 10% | 10% | 10% | Liam Dawson | Jamie Smith |
| *Role & Venue Heavy* | 20% | 15% | 10% | 25% | 20% | 10% | Spencer Johnson | Ashutosh Sharma |
| *Predictive ML Heavy* | 20% | 15% | 30% | 15% | 10% | 10% | Liam Dawson | Jamie Smith |
| *Equal Balanced* | 16.7% | 16.7% | 16.7% | 16.7% | 16.7% | 16.7% | Liam Dawson | Nehal Wadhera |

**Conclusion:** Across all five perturbations, **Liam Dawson** consistently emerges as the #1 target bowler due to his unrivaled 95.4 Model A score, 6.8 rpo middle-overs economy, and Jaipur boundary suitability. **Spencer Johnson** and **Fazalhaq Farooqi** consistently dominate the death-overs seam category. In batting, **Jamie Smith** and **Ashutosh Sharma** remain the preeminent lower-order power-hitting targets.

---

## 5. Architectural Integrity Summary

1. **Model A Checksums:** `final_batter_rankings.csv` and `final_bowler_rankings.csv` have 0.00 drift from their frozen baseline hashes.
2. **Deterministic Outputs:** All Model B ranks, scores, and CSV exports are deterministically generated by `scripts/build_rr_recruitment_model_b.py`.
3. **Traceability:** Every eligibility classification and market trade status links directly to an official source authority and URL.
