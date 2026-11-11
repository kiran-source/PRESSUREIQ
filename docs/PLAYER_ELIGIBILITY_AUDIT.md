# PRESSUREIQ — Player Eligibility & Auction Feasibility Audit

**Document:** `docs/PLAYER_ELIGIBILITY_AUDIT.md`  
**Date:** 15 November 2026  
**Status:** Certified Independent Audit Report  
**Framework:** PRESSUREIQ Competition Re-Audit — Rajasthan Royals SupeRR Selector Season 2  

---

## 1. Executive Summary & Audit Objective

The PRESSUREIQ statistical framework evaluates cricket performance under pressure across 200,999 deliveries (IPL 2022–2026, T20Is 2022–2026, and developmental Asian T20 fixtures). While pure statistical modeling ranks players solely on high-pressure performance value-added (PAVA), a cricket franchise's auction room operates under rigid legal, regulatory, geopolitical, contractual, and budgetary constraints.

An independent audit of the Model A top-10 rankings revealed critical operational discrepancies:
1. **Pakistani Cricketers (Class D):** Model A ranked Fakhar Zaman (#3 Batter), Haris Rauf (#2 Bowler), Abbas Afridi (#3 Bowler), and Sufiyan Muqeem (#5 Bowler) among the top 10 most reliable pressure performers globally. Under prevailing BCCI regulatory policy and geopolitical reality since 2008, Pakistani players are ineligible to participate in the Indian Premier League. Recommending these players as actionable acquisition targets to Rajasthan Royals management would represent an immediate operational failure.
2. **Franchise Marquee Retentions (Class C):** Model A ranked Ruturaj Gaikwad (#1 Batter, CSK Captain), Rohit Sharma (#2 Batter, MI Core), Suryakumar Yadav (#4 Batter, MI Core / India T20I Captain), and Nicholas Pooran (#9 Batter, LSG Core ₹21 Cr) at the top of the batting rankings, alongside Matheesha Pathirana (#6 Bowler, CSK ₹13 Cr) among bowlers. These players are locked into long-term franchise contracts and will not enter the IPL 2027 open auction under normal market conditions.

To resolve this without corrupting statistical integrity, PRESSUREIQ establishes a rigorous two-tier architecture:
- **Leaderboard A (Pure Pressure Reliability):** Preserves the frozen Model A statistical baseline without modification.
- **Leaderboard B (RR IPL 2027 Actionable Acquisition Recommendations):** Applies Multi-Criteria Decision Analysis (MCDA) incorporating player eligibility, auction availability, tactical fit for Rajasthan Royals, and sample evidence.

---

## 2. Six-Tier Player Eligibility Classification Framework

Every player in the 256-candidate evaluation universe is audited and assigned to one of six mutually exclusive eligibility classes:

| Class | Category Name | Definition & Regulatory / Contractual Reality | Auction Feasibility Multiplier ($A_i$) |
|:---:|:---|:---|:---:|
| **Class A** | **RR Core & High-Priority Targets** | Current Rajasthan Royals players or confirmed target priorities with established franchise alignment and tactical synergy. | **1.00** |
| **Class B** | **Actionable Auction Targets** | Unretained domestic or overseas players eligible for the IPL 2027 auction with realistic probability of bidding availability. | **0.85** |
| **Class C** | **Franchise Retentions / Marquee Core** | Players retained by competing IPL franchises (CSK, MI, KKR, LSG, GT, DC, SRH, RCB, PBKS) on top-tier contracts or captaincy roles. Extremely low trade/auction availability. | **0.20** |
| **Class D** | **BCCI Regulatory Policy Ineligible** | Pakistani passport holders and cricketers subject to prevailing BCCI policy restrictions preventing IPL registration. Zero probability of acquisition. | **0.00** |
| **Class E** | **Retired / Defunct / Inactive** | Players who have retired from professional T20 cricket, announced IPL retirement, or ceased active participation. | **0.00** |
| **Class F** | **Untenable Budgetary / Availability** | Players with confirmed multi-year international fixture clashes, ECB/CA central contract restrictions, or prohibitive price-to-utility profiles. | **0.30** |

---

## 3. Deep Regulatory Analysis: Pakistani Cricketers (Class D)

### 3.1 Regulatory Background
Following the November 2008 Mumbai attacks, the Board of Control for Cricket in India (BCCI) and the IPL Governing Council ceased the inclusion of Pakistani cricketers in IPL player auctions. While Sohail Tanvir (Rajasthan Royals' Purple Cap winner in 2008), Shahid Afridi, Shoaib Akhtar, and Kamran Akmal played in IPL 2008, no Pakistani player has featured in an IPL match or auction since (with the sole exception of Azhar Mahmood, who competed as a British citizen holding a UK passport).

### 3.2 Audit Findings on Class D Candidates
In the 256-player PRESSUREIQ dataset, exactly 19 players are Pakistani international cricketers:

| Player Name | Discipline | Model A Rank | Model A Reliability Score | PAVA / Ball | HP Balls | Regulatory Status | Acquisition Feasibility |
|:---|:---:|:---:|:---:|:---:|:---:|:---|:---:|
| **Haris Rauf** | Bowler | **#2** | 92.36 | +0.134 | 444 | Class D (BCCI Policy) | **0.00** |
| **Abbas Afridi** | Bowler | **#3** | 91.88 | +0.128 | 232 | Class D (BCCI Policy) | **0.00** |
| **Sufiyan Muqeem** | Bowler | **#5** | 91.41 | +0.121 | 213 | Class D (BCCI Policy) | **0.00** |
| **Fakhar Zaman** | Batter | **#3** | 95.25 | +0.142 | 52 | Class D (BCCI Policy) | **0.00** |
| **Abrar Ahmed** | Bowler | #23 | 81.92 | +0.076 | 178 | Class D (BCCI Policy) | **0.00** |
| **Mohammad Rizwan** | Batter | #37 | 82.51 | +0.061 | 210 | Class D (BCCI Policy) | **0.00** |
| **Babar Azam** | Batter | #44 | 79.84 | +0.048 | 290 | Class D (BCCI Policy) | **0.00** |
| **Shaheen Shah Afridi** | Bowler | #48 | 76.50 | +0.038 | 312 | Class D (BCCI Policy) | **0.00** |
| **Naseem Shah** | Bowler | #52 | 74.88 | +0.031 | 288 | Class D (BCCI Policy) | **0.00** |
| **Iftikhar Ahmed** | Batter | #58 | 72.10 | +0.024 | 145 | Class D (BCCI Policy) | **0.00** |
| *9 Other PAK Players* | Mixed | > #60 | < 70.00 | — | — | Class D (BCCI Policy) | **0.00** |

**Audit Verdict:** These players possess genuine statistical clutch skill (Haris Rauf at death, Abbas Afridi change of pace, Sufiyan Muqeem wrist spin, Fakhar Zaman power hitting). However, setting their acquisition feasibility $A_i = 0.0$ in Leaderboard B ensures Rajasthan Royals does not waste strategic resources on legally impossible acquisitions, while preserving their ranking in Leaderboard A confirms our statistical objectivity.

---

## 4. Franchise Contract & Retention Audit (Class C)

### 4.1 Marquee Retention Landscape
Ahead of IPL 2025/2026, IPL franchises locked in their core pillars under official retention regulations:
- **Chennai Super Kings (CSK):** Ruturaj Gaikwad (Captain, ₹18 Cr), Matheesha Pathirana (Death Specialist, ₹13 Cr), Ravindra Jadeja (₹18 Cr), Shivam Dube (₹12 Cr).
- **Mumbai Indians (MI):** Jasprit Bumrah (₹18 Cr), Suryakumar Yadav (T20I Captain, ₹16.35 Cr), Hardik Pandya (Captain, ₹16.35 Cr), Rohit Sharma (₹16.30 Cr), Tilak Varma (₹8 Cr).
- **Lucknow Super Giants (LSG):** Nicholas Pooran (Core / Vice-Captain, ₹21 Cr), Mayank Yadav (₹11 Cr), Ravi Bishnoi (₹11 Cr).
- **Kolkata Knight Riders (KKR):** Rinku Singh (Finisher, ₹13 Cr), Sunil Narine (₹12 Cr), Andre Russell (₹12 Cr), Varun Chakaravarthy (₹12 Cr).
- **Gujarat Titans (GT):** Rashid Khan (₹18 Cr), Shubman Gill (Captain, ₹16.5 Cr), Sai Sudharsan (₹8.5 Cr).
- **Delhi Capitals (DC):** Axar Patel (₹16.5 Cr), Tristan Stubbs (₹10 Cr), Kuldeep Yadav (₹13.25 Cr).

### 4.2 Impact on Model A Leaderboard
The table below documents why these players cannot be presented as realistic acquisition targets:

| Player Name | Discipline | Model A Rank | Current Franchise | Retention Slab / Role | Auction Availability Multiplier ($A_i$) |
|:---|:---:|:---:|:---|:---|:---:|
| **Ruturaj Gaikwad** | Batter | **#1** | Chennai Super Kings | Franchise Captain & #1 Retention (₹18 Cr) | **0.20** |
| **Rohit Sharma** | Batter | **#2** | Mumbai Indians | Former MI Captain & Marquee Core (₹16.3 Cr) | **0.20** |
| **Suryakumar Yadav** | Batter | **#4** | Mumbai Indians | India T20I Captain & Key Asset (₹16.35 Cr) | **0.20** |
| **Naman Dhir** | Batter | #6 | Mumbai Indians | Emerging Indian Retention Core | **0.20** |
| **Nicholas Pooran** | Batter | **#9** | Lucknow Super Giants | Marquee Anchor / Wicketkeeper (₹21 Cr) | **0.20** |
| **Matheesha Pathirana** | Bowler | **#6** | Chennai Super Kings | Premier Overseas Death Weapon (₹13 Cr) | **0.20** |
| **Tilak Varma** | Batter | #18 | Mumbai Indians | Indian Middle-Order Core (₹8 Cr) | **0.20** |
| **Rinku Singh** | Batter | #15 | Kolkata Knight Riders | Premier Indian Finisher (₹13 Cr) | **0.20** |
| **Tristan Stubbs** | Batter | #19 | Delhi Capitals | Overseas Finisher/Keeper (₹10 Cr) | **0.20** |
| **Jasprit Bumrah** | Bowler | #22 | Mumbai Indians | Global #1 Pace Anchor (₹18 Cr) | **0.20** |
| **Rashid Khan** | Bowler | #25 | Gujarat Titans | Premier T20 Leg-Spinner (₹18 Cr) | **0.20** |
| **Axar Patel** | Bowler | #28 | Delhi Capitals | Premier Indian All-Rounder (₹16.5 Cr) | **0.20** |

**Audit Verdict:** Assigning $A_i = 0.20$ correctly discounts their priority score ($97.71 \times 0.20 \times \dots \approx 14.5$), acknowledging that while a trade or release is not mathematically 0%, their open auction availability is functionally negligible.

---

## 5. Candidate Population Breakdown

Across the 256 candidates audited in `data/processed/player_eligibility_audit.csv`:
- **Class A (RR Core / Top Priorities):** 5 players (1.95%) — Dhruv Jurel, Jos Buttler, Shimron Hetmyer, Prasidh Krishna, Trent Boult.
- **Class B (Actionable Auction Candidates):** 207 players (80.86%) — The primary open talent pool for RR IPL 2027 recruitment.
- **Class C (Franchise Retentions):** 21 players (8.20%) — High-profile stars locked by rivals.
- **Class D (BCCI Regulatory Restrictions):** 19 players (7.42%) — Pakistani internationals.
- **Class E (Retired / Inactive):** 4 players (1.56%) — Dinesh Karthik, Shikhar Dhawan, etc.
- **Class F (Untenable Logistics):** 0 players in current audited scope.

**Conclusion:** The eligibility classification cleanly disentangles statistical quality from auction feasibility, providing Rajasthan Royals with a realistic, actionable recruitment blueprint.

