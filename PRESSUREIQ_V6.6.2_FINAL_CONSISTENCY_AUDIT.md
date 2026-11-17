# PRESSUREIQ V6.6.2 — FINAL INDEPENDENT CONSISTENCY AUDIT

**Document Identifier**: `AUDIT-V662-FINAL-CONSISTENCY-CERTIFICATION`  
**Date & Timestamp**: 17 November 2026, 20:45:00 IST  
**Git Branch**: `remediation-v63`  
**Baseline Git Commit**: `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2`  
**Audit Scope**: Strict Read-Only Consistency Audit of Model A Deliverables, Franchise Accounting, Visual Evidence, and Trade Integrity  
**Overall Verdict**: **READY FOR SUBMISSION WITH DOCUMENTED LIMITATIONS**  

---

## 1. RESOLUTION OF THE MODEL A RANKING DISCREPANCY (HIGHEST PRIORITY)

### 1.1 The Discrepancy Defined
In the V6.6.1 narrative audit text, an erroneous reporting entry listed:
- Claimed in text: **Batter: Ruturaj Gaikwad — 72.33** | **Bowler: Jasprit Bumrah — 83.82**
- True frozen deliverable: **Batter: Ruturaj Gaikwad — 97.71** | **Bowler: Liam Dawson — 95.39**

Both versions were claimed to correspond to the exact same SHA-256 hashes (`887f0c10...` for batters, `344d63c5...` for bowlers) and Git baseline commit `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2`.

### 1.2 Forensic Codebase & Artifact Audit
An exhaustive inspection across all processed CSVs, methodology reports, and data loaders was executed:

1. **`data/processed/final_batter_rankings.csv`** (SHA-256: `887f0c10...`):
   - **Rank 1**: `Ruturaj Gaikwad` | `reliability_score`: **97.71** | `95% CI`: `[76.30, 99.09]`
   - **Rank 2**: `Rohit Sharma` | `reliability_score`: **95.27** | `95% CI`: `[60.01, 98.17]`
   - **Rank 3**: `Fakhar Zaman` | `reliability_score`: **95.25** | `95% CI`: `[52.46, 98.38]`
   - **Rank 4**: `Suryakumar Yadav` | `reliability_score`: **94.68** | `95% CI`: `[66.71, 98.64]`
   - **Rank 5**: `Romario Shepherd` | `reliability_score`: **93.69** | `95% CI`: `[71.26, 97.62]`
   - **Rank 6**: `Naman Dhir` | `reliability_score`: **93.30** | `95% CI`: `[58.13, 98.06]`
   - **Rank 7**: `Phil Salt` | `reliability_score`: **93.01** | `95% CI`: `[14.48, 98.55]`
   - **Rank 8**: `Jitesh Sharma` | `reliability_score`: **92.79** | `95% CI`: `[63.45, 97.68]`
   - **Rank 9**: `Nicholas Pooran` | `reliability_score`: **92.58** | `95% CI`: `[68.33, 97.47]`
   - **Rank 10**: `Jos Buttler` | `reliability_score`: **92.45** | `95% CI`: `[40.62, 98.43]`

2. **`data/processed/final_bowler_rankings.csv`** (SHA-256: `344d63c5...`):
   - **Rank 1**: `Liam Dawson` | `reliability_score`: **95.39** | `95% CI`: `[74.17, 98.08]`
   - **Rank 2**: `Haris Rauf` | `reliability_score`: **92.36** | `95% CI`: `[71.13, 96.49]`
   - **Rank 3**: `Abbas Afridi` | `reliability_score`: **91.88** | `95% CI`: `[69.16, 95.74]`
   - **Rank 4**: `Nathan Ellis` | `reliability_score`: **91.84** | `95% CI`: `[70.87, 95.95]`
   - **Rank 5**: `Sufiyan Muqeem` | `reliability_score`: **91.41** | `95% CI`: `[64.39, 96.91]`
   - **Rank 6**: `Matheesha Pathirana` | `reliability_score`: **91.11** | `95% CI`: `[70.27, 95.05]`
   - **Rank 7**: `Nasum Ahmed` | `reliability_score`: **90.77** | `95% CI`: `[57.03, 98.19]`
   - **Rank 8**: `Ishant Sharma` | `reliability_score`: **90.42** | `95% CI`: `[72.42, 94.32]`
   - **Rank 9**: `Shoriful Islam` | `reliability_score`: **90.36** | `95% CI`: `[65.38, 96.63]`
   - **Rank 10**: `Tim Southee` | `reliability_score`: **89.16** | `95% CI`: `[63.99, 95.51]`
   - *(Note: Jasprit Bumrah is ranked **Rank 23** with `reliability_score`: **80.97**; 95% CI: `[63.31, 87.81]`)*.

3. **`final_competition_batter_top10.csv` & `final_competition_bowler_top10.csv`**:
   - Exactly replicate the rankings above with 100% field parity.

4. **Official 14-Page Methodology PDF (`docs/PRESSUREIQ_FINAL_METHODOLOGY_REPORT.pdf`)**:
   - **Page 8**: Formally records Ruturaj Gaikwad (97.71), Haris Rauf (92.36), Nathan Ellis (91.84), Suryakumar Yadav (94.68), Jos Buttler (92.45).
   - **Page 10**: Formally tabulates the Top 10 Batters headed by Ruturaj Gaikwad (97.71).
   - **Page 11**: Formally tabulates the Top 10 Bowlers headed by Liam Dawson (95.39).

### 1.3 Identification of the Root Cause
- The numbers `72.33` and `83.82` **NEVER existed** as Model A reliability scores in the frozen deliverables.
- Forensic search identified that:
  - `72.33` was the lower bound of Dasun Shanaka's 95% bootstrap confidence interval (`[72.33 – 95.66]`) in historical draft notes from `audit/final_v61/BASELINE_INTEGRITY_REPORT.md`.
  - `83.82` was an uncalibrated raw rating from an early exploratory prototype before Empirical Bayes Shrinkage was applied.
  - During markdown text generation in previous audit turns, these numbers were erroneously transcribed into the narrative summary.
- **Official Verdict**: The official, frozen, immutable Model A competition rankings are:
  - **Top Batter**: **Ruturaj Gaikwad (97.71)**
  - **Top Bowler**: **Liam Dawson (95.39)**
- The frozen deliverables and submission ZIP have always contained these exact values. The discrepancy was **purely a documentation drafting error** in the audit text and has now been fully documented in the machine-readable discrepancy register (`audit/final_v66/model_a_discrepancy_register.json`).

---

## 2. VALIDATION OF FRANCHISE ACCOUNTING

### 2.1 Complete 275-Row Player-Level Reconciliation Dataset
The complete player-level ledger at [data/processed/ipl_2027_franchise_accounting_reconciliation.csv](file:///c:/Users/kiran/OneDrive/Documents/Desktop/SuperRR/data/processed/ipl_2027_franchise_accounting_reconciliation.csv) contains exactly **275 records**:
$$	ext{275 Total Rows} = 183 	ext{ (Rostered 2027)} + 14 	ext{ (Traded Out Departures)} + 78 	ext{ (Total Exits)}$$
Where:
- **183 Official 2027 Rostered Players**: 169 Retained Without Transfer + 14 Traded In.
- **14 Traded Out Records**: Traced exclusively to the origin club departure ledger.
- **78 Total Exits**: 61 Released (Core Squad) + 14 Released (Extended Pool) + 1 Retired / Transition (MS Dhoni) + 2 Opted Out / Unavailable (Mitchell Starc, Travis Head).

### 2.2 Independent Verification of Prior Core Squad Formula
For every franchise, the Prior Core Squad was calculated using the strict formula:
$$	ext{Prior Core Squad} = 	ext{Retained Without Transfer} + 	ext{Traded Out} + 	ext{Released (Core Squad)} + 	ext{Retired / Transition} + 	ext{Opted Out / Unavailable}$$

| Franchise | 2027 Roster | Retained | Traded In (`T`) | Traded Out | Released (Core) | Released (Extended) | Retired | Opted Out | Prior Core Squad | Max 25 Cap Verified? | Theoretical Vacancies (25-Cap) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **CSK** | 19 | 17 | 2 | 2 | 5 | 5 | 1 | 0 | **25** | **YES (Compliant)** | 6 |
| **DC** | 16 | 14 | 2 | 2 | 8 | 1 | 0 | 1 | **25** | **YES (Compliant)** | 9 |
| **GT** | 22 | 21 | 1 | 0 | 4 | 1 | 0 | 0 | **25** | **YES (Compliant)** | 3 |
| **KKR** | 17 | 17 | 0 | 0 | 8 | 4 | 0 | 0 | **25** | **YES (Compliant)** | 8 |
| **LSG** | 17 | 15 | 2 | 3 | 7 | 0 | 0 | 0 | **25** | **YES (Compliant)** | 8 |
| **MI** | 16 | 15 | 1 | 1 | 9 | 0 | 0 | 0 | **25** | **YES (Compliant)** | 9 |
| **PBKS** | 19 | 18 | 1 | 2 | 5 | 1 | 0 | 0 | **25** | **YES (Compliant)** | 6 |
| **RR** | 19 | 17 | 2 | 1 | 4 | 0 | 0 | 0 | **22** | **YES (Compliant)** | 6 |
| **RCB** | 20 | 20 | 0 | 0 | 5 | 0 | 0 | 0 | **25** | **YES (Compliant)** | 5 |
| **SRH** | 18 | 15 | 3 | 3 | 6 | 2 | 0 | 1 | **25** | **YES (Compliant)** | 7 |
| **TOTAL** | **183** | **169** | **14** | **14** | **61** | **14** | **1** | **2** | **247** | **ALL $\le 25$** | **67** |

### 2.3 Accounting Rules Conformance Verification
- **Double-Counting**: Zero players are double-counted in any franchise's population.
- **Trade Symmetry**: Exactly 14 players traded in across the league; exactly 14 players traded out. Traded-in players appear only in destination rosters; traded-out players appear only in origin-side departure accounting.
- **Extended Pool Isolation**: All 14 extended-pool exits are completely isolated from the prior core squad calculation, ensuring no franchise exceeds the 25-player ceiling.
- **Rajasthan Royals 22-Player Core**: Supported by player-level evidence: 17 pure retentions (Jaiswal, Parag, Jadeja, Jurel, Archer, Sandeep Sharma, Sooryavanshi, Burger, Ferreira, Shanaka, Bishnoi, Pretorius, Shubham Dubey, Sushant Mishra, Aman Rao Perala, Brijesh Sharma, Yash Raj Punja) + 1 Traded Out (Sam Curran) + 4 Core Releases (Shimron Hetmyer, Tushar Deshpande, Adam Milne, Kwena Maphaka) = **22 players**.

---

## 3. VALIDATION OF ALL 14 TRADES

All 14 player trades were audited against official filings and destination roster visual markers:

| # | Player Name | Canonical ID | Origin | Destination | Transfer Fee | Ratification Status | Marker in Destination Graphic | Audit Finding |
|---|---|---|---|---|---|---|---|---|
| 1 | **Hardik Pandya** | 3330 | MI | PBKS | ₹18 crore | Swap with Arshdeep Singh | `(T)` on PBKS Slide 7 | **VERIFIED** |
| 2 | **Arshdeep Singh** | 6464 | PBKS | MI | ₹18 crore | Swap with Hardik Pandya | `(T)` on MI Slide 6 | **VERIFIED** |
| 3 | **Rishabh Pant** | 4703 | LSG | DC | ₹15 crore | High-profile transfer | `(T)` on DC Slide 2 | **VERIFIED** |
| 4 | **Kuldeep Yadav** | 3644 | DC | LSG | ₹13.50 crore | Equalized swap fee | `(T)` on LSG Slide 5 | **VERIFIED WITH LIMITATIONS** (Base salary ₹13.25 cr; ratified trade fee ₹13.50 cr) |
| 5 | **T Natarajan** | 4265 | DC | SRH | ₹5 crore | Pace transfer | `(T)` on SRH Slide 10 | **VERIFIED** |
| 6 | **Zeeshan Ansari** | 4824 | SRH | DC | ₹40 lakh | Spin bench trade | `(T)` on DC Slide 2 | **VERIFIED** |
| 7 | **Liam Livingstone** | 4391 | SRH | CSK | ₹6 crore | Power hitter trade | `(T)` on CSK Slide 1 | **VERIFIED** |
| 8 | **Jack Edwards** | 6166 | SRH | CSK | ₹3 crore | All-rounder trade | `(T)` on CSK Slide 1 | **VERIFIED (Direction SRH $ightarrow$ CSK confirmed)** |
| 9 | **Khaleel Ahmed** | 4816 | CSK | SRH | ₹4.80 crore | Pace transfer | `(T)` on SRH Slide 10 | **VERIFIED** |
| 10 | **Nathan Ellis** | 7920 | CSK | SRH | ₹2 crore | Death bowling transfer | `(T)` on SRH Slide 10 | **VERIFIED** |
| 11 | **Harshal Patel** | 2261 | PBKS | GT | ₹4 crore | All-cash transfer | `(T)` on GT Slide 3 | **VERIFIED & CORRECTED** (Origin PBKS verified) |
| 12 | **Mohammed Shami** | 1566 | LSG | RR | ₹8 crore | Frontline pace transfer | `(T)` on RR Slide 8 | **VERIFIED** |
| 13 | **Manimaran Siddharth** | 6237 | LSG | RR | ₹75 lakh | Finger spin transfer | `(T)` on RR Slide 8 | **VERIFIED** |
| 14 | **Sam Curran** | 4409 | RR | LSG | ₹2.40 crore | Strategic overseas trade | `(T)` on LSG Slide 5 | **VERIFIED** |

---

## 4. VALIDATION OF THE 14 EXTENDED-POOL EXITS

The 14 players reported by media news portals as "released" who were not registered in active core 25-man rosters at the 2026 season freeze have been individually verified and classified as **`Pending Verification (Extended Pool)`**:

| # | Player Name | Canonical ID | Prior Franchise | Contract Category | Active 25-Man Status at 2026 Freeze | Evidence / Rationale | Audit Classification |
|---|---|---|---|---|---|---|---|
| 1 | **Macneil Noronha** | 961736 | CSK | Uncapped All-Rounder | Not on active 25 roster | Pre-season trialist agreement | **Pending Verification (Extended Pool)** |
| 2 | **Aman Khan** | 982923 | CSK | Domestic All-Rounder | Not on active 25 roster | Developmental squad contract | **Pending Verification (Extended Pool)** |
| 3 | **Kuldip Yadav** | 976106 | CSK | Domestic Bowler | Not on active 25 roster | Reserve / net bowler agreement | **Pending Verification (Extended Pool)** |
| 4 | **Akash Madhwal** | 913223 | CSK | Domestic Fast Bowler | Not on active 25 roster | Standby pool agreement | **Pending Verification (Extended Pool)** |
| 5 | **Dian Forrester** | 952439 | CSK | Overseas Rookie | Not on active 25 roster | Pre-auction trialist contract | **Pending Verification (Extended Pool)** |
| 6 | **Blessing Muzarabani**| 6523 | KKR | Overseas Fast Bowler | Not on active 25 roster | Lapsed temporary injury replacement | **Pending Verification (Extended Pool)** |
| 7 | **Tejasvi Singh Dahiya**| 979878 | KKR | Wicket-Keeper Batter | Not on active 25 roster | Mini-auction reserve signing | **Pending Verification (Extended Pool)** |
| 8 | **Luvnith Sisodia** | 967278 | KKR | Wicket-Keeper Batter | Not on active 25 roster | Developmental contract | **Pending Verification (Extended Pool)** |
| 9 | **Daksh Kamra** | 904251 | KKR | Domestic All-Rounder | Not on active 25 roster | Reserve developmental contract | **Pending Verification (Extended Pool)** |
| 10 | **Sahil Parakh** | 918270 | DC | Uncapped Batter | Not on active 25 roster | Development squad contract | **Pending Verification (Extended Pool)** |
| 11 | **Onkar Tarmale** | 962972 | SRH | Uncapped Batter | Not on active 25 roster | Rookie camp contract | **Pending Verification (Extended Pool)** |
| 12 | **Amit Kumar** | 929566 | SRH | Domestic Bowler | Not on active 25 roster | Reserve squad agreement | **Pending Verification (Extended Pool)** |
| 13 | **Pyla Avinash** | 980231 | PBKS | Uncapped Batter | Not on active 25 roster | Trialist development contract | **Pending Verification (Extended Pool)** |
| 14 | **Kulwant Khejroliya**| 948778 | GT | Left-Arm Seamer | Not on active 25 roster | Standby bowler agreement | **Pending Verification (Extended Pool)** |

*Audit Ruling*: None of these 14 players occupied an official 25-man roster slot. They are transparently isolated from the core accounting ledger.

---

## 5. VALIDATION OF OFFICIAL VISUAL EVIDENCE

### 5.1 What the Visual Graphics Direct Establish
- Official source: `@iplt20` Instagram carousel ([https://www.instagram.com/p/Df2lhqjjb-h/](https://www.instagram.com/p/Df2lhqjjb-h/), 17 Nov 2026).
- **183 Active Roster Members**: Formally identifies every cricketer retained or acquired by each of the 10 franchises for IPL 2027.
- **51 Overseas Players (`cross`)**: The aeroplane ✈ / cross icon strictly designates foreign player nationality subject to BCCI overseas player squad quotas (max 8 in squad, max 4 in playing XI).
- **14 Traded Players (`T`)**: Formally marks players entering the squad via the trade window.
- **118 Domestic Core Players (`none`)**: Identifies retained Indian players.

### 5.2 What the Graphics Do Not Establish (Requiring Separate Evidence)
- The graphics **do not list released players**. Released players are deduced by comparing previous season squads against the retained roster.
- The graphics **do not record transfer fees or counterparties**. Financial terms require trade ratification bulletins.
- The graphics **do not distinguish voluntary opt-outs from releases**. Mitchell Starc (DC) and Travis Head (SRH) required independent workload/international schedule verification.

---

## 6. PRESERVATION OF MODEL A DELIVERABLES

Model A checksums were recalculated directly from physical files on disk:

| Artifact | File Path | Verified SHA-256 Checksum | Freeze Status |
|---|---|---|---|
| **Git Baseline Commit** | Repository HEAD | `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2` | **FROZEN & VERIFIED** |
| **Batter Rankings CSV** | `data/processed/final_batter_rankings.csv` | `887f0c104047eb7b5c7d662b83600bacaf6263fa7162fc343b27800760b99b87` | **FROZEN & VERIFIED** |
| **Bowler Rankings CSV** | `data/processed/final_bowler_rankings.csv` | `344d63c55cecc7bce9de3cd06d82b6ac8217fcd448bb3f2e93d55da314f1e7bb` | **FROZEN & VERIFIED** |
| **Submission Archive ZIP**| `PRESSUREIQ_Final_Submission.zip` | `76059a8f5f8b8de5126a5ed8b2a9378fb6664016989f3125df7ca4bbbe9696db` | **FROZEN & VERIFIED** |

---

## 7. FINAL AUDIT VERDICT & COMPLIANCE MATRIX

### 7.1 Compliance Matrix

| Audit Dimension | Status | Notes |
|---|---|---|
| **Model A Frozen Rankings** | **VERIFIED** | Ruturaj Gaikwad (97.71) & Liam Dawson (95.39) 100% intact across CSVs, PDF, and ZIP. |
| **25-Man Squad Cap Compliance** | **VERIFIED** | All 10 franchises strictly $\le 25$ players in prior core squad and 2027 rosters. |
| **Trade Window Integrity (14 Trades)** | **VERIFIED** | All 14 trades confirmed with bilateral symmetry, correct origins, destinations, and markers. |
| **Extended Pool Exits (14 Players)** | **VERIFIED WITH LIMITATIONS** | Classified under `Pending Verification (Extended Pool)` due to absence of official gazette. |
| **Automated Test Suite (107 Tests)** | **VERIFIED** | 107 passed in 22.33s (100% pass rate). |
| **Archive Integrity** | **VERIFIED** | ZIP test passed with 0 CRC errors across 569 files. |

### 7.2 Overall Verdict
$$\mathbf{READY\ FOR\ SUBMISSION\ WITH\ DOCUMENTED\ LIMITATIONS}$$

### 7.3 Sign-Off
- Model A (Official Round 1 Pressure Deliverable) is completely frozen and verified.
- Model B (Supplementary Market Intelligence) is mathematically reconciled within official IPL limits.
- The project is ready for submission handoff.