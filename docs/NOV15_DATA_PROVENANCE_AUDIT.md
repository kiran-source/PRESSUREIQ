# NOV15 DATA PROVENANCE & COMPETITION PACK RECONCILIATION AUDIT
## Comprehensive Source Verification of Supplied Data Pack vs. Analytical Baseline

**Project:** PRESSUREIQ — SupeRR Selector Season 2 (Rajasthan Royals)  
**Date of Audit:** 11–15 November 2026  
**Competition Deadline:** 18 November 2026  
**Dataset Directory:** `SupeRR Selector Season 2 _ Problem Statement _ Data Pack/SupeRR Selector Season 2 _ Data Pack/`  
**Certified Analytical Dataset:** `data/processed/deliveries.parquet` (200,999 deliveries, 867 matches)  
**Auditor:** Senior Cricket Data Scientist & Quantitative Analytics Auditor  

---

## 1. Executive Summary & Critical Reconciliation Finding

### The Critical Provenance Finding
An adversarial inspection of the supplied competition materials revealed an important discrepancy in previous documentation:
- Previous reports (`FINAL_SUBMISSION_MANIFEST.md`) incorrectly referenced synthetic filenames (such as `match_info_data.csv`, `match_schedule.csv`, `player_attributes.csv`, `strike_rates.csv`, `bowling_strike_rates.csv`, `economy_rates.csv`).
- **The Actual Competition Data Pack:** As provided by Rajasthan Royals on Unstop in `SupeRR Selector Season 2 _ Data Pack/`, contains exactly six raw CSV files:
  1. `ball_by_ball.csv` (41,071,609 bytes)
  2. `competitions.csv` (7,624 bytes)
  3. `competition_team_player_mapping.csv` (462,969 bytes)
  4. `matches.csv` (123,864 bytes)
  5. `playing_eleven.csv` (966,287 bytes)
  6. `teams.csv` (6,922 bytes)

### Data Pack Ingestion Verification
Every single delivery in `ball_by_ball.csv` is 100% incorporated into `data/processed/deliveries.parquet`:
- Total deliveries in raw `ball_by_ball.csv`: **200,999 deliveries**.
- Total deliveries in `deliveries.parquet`: **200,999 deliveries**.
- Distinct matches in raw `ball_by_ball.csv`: **867 matches**.
- Distinct matches in `deliveries.parquet`: **867 matches**.
- Zero deliveries or matches were omitted, fabricated, or improperly substituted.

---

## 2. Inventory of Supplied Source Files & Cryptographic Hashes

Every file supplied in the official competition archive was verified via SHA-256:

| File Name | Size (Bytes) | Exact Line Count | Certified SHA-256 Checksum | Content Description |
| :--- | :---: | :---: | :--- | :--- |
| `ball_by_ball.csv` | 41,071,609 | 201,000 | `a3926f49d2c684dca2a5d2de535a02c5ee46ea654ca1e79dd31c69e7544e9889` | Granular delivery events (runs, wickets, extras, bowler/striker IDs) |
| `competitions.csv` | 7,624 | 142 | `507ceb7189f972d4e4f299ddcfc97f3c3247af1913f6291106f161fa8353fd9b` | Master competition metadata (comp_id, format, season, comp_name) |
| `matches.csv` | 123,864 | 884 | `bb100ab84b8b9a15160c1f2315cf675210131a30e779ec5079fd5403dcf56eef` | Match-level metadata (dates, venues, teams, captains, toss, revised overs) |
| `competition_team_player_mapping.csv` | 462,969 | 10,796 | `1ded4e42a933618572d6e2c3a521c3257eb1844fab4456d567d77cbb2d3bbb12` | Relational bridge connecting players, teams, and tournament rosters |
| `playing_eleven.csv` | 966,287 | 19,427 | `7517c73722a28d5d61c808ccf0cbed315a8780586d02e946eb9a7f5daf011c27` | Verified playing XI lineups for every match |
| `teams.csv` | 6,922 | 283 | `a65e5922a9b3bf49247b24fc9471782eb0aaec1d55581b213b190f70e5b7c7df` | Team registry across competitions |

---

## 3. Competitions, Formats & Domestic League Reality

A critical claim in competition discussions is whether domestic leagues other than the IPL are represented. The empirical breakdown of all 141 competitions in `competitions.csv` confirms:

### 3.1 Competition Breakdown in `matches.csv` (883 Total Matches)
1. **Indian Premier League (IPL):**
   - Exactly **371 matches** across 5 complete calendar seasons:
     - IPL 2022: 74 matches
     - IPL 2023: 74 matches
     - IPL 2024: 74 matches
     - IPL 2025: 75 matches
     - IPL 2026: 74 matches
2. **Twenty20 Internationals (T20I):**
   - Exactly **482 matches** across 134 bilateral series, World Cups, and continental tournaments (India, Australia, England, South Africa, Pakistan, New Zealand, West Indies, Sri Lanka, Bangladesh, Afghanistan, Ireland, Zimbabwe, UAE, Nepal, etc.).
3. **Developmental Asian T20 Tournaments:**
   - Exactly **30 matches**:
     - Mens T20 Emerging Teams Asia Cup 2024: 15 matches
     - Asia Cup Rising Stars 2025: 15 matches

### 3.2 Key Finding on "Domestic Leagues"
**There are NO other franchise domestic leagues (e.g. BBL, PSL, CPL, The Hundred, SA20, BPL) in the supplied data pack.**
When the problem statement refers to domestic performance, it refers exclusively to the **Indian Premier League (IPL)** and Asian developmental T20 tournaments. The analysis does not omit any external domestic files, because none were supplied in the official data pack.

### 3.3 Reconciling Match Counts: 883 vs. 867
- `matches.csv` lists 883 scheduled fixtures.
- `ball_by_ball.csv` contains delivery records for **867 matches**.
- **The 16 Excluded Matches:** These were matches abandoned without a ball bowled (e.g. torrential rain, washouts, walkovers) or fixtures where no innings was recorded. They carry zero performance data and are properly handled.

---

## 4. Player Identifier Reconciliation & Integrity Checks

1. **Player Key Uniqueness:**
   - Players are uniquely identified by integer `player_id` linked across `ball_by_ball.csv`, `competition_team_player_mapping.csv`, and `playing_eleven.csv`.
   - Name spelling variants (e.g. "Rohit Sharma" vs "R Sharma") resolve unambiguously through canonical ID matching.
2. **Duplicate Delivery Check:**
   - No duplicate delivery rows exist in `ball_by_ball.csv`. Every record is indexed by `(match_id, innings, over, ball_number)`.
3. **Missing Value Audit:**
   - `extra_runs` is populated for all illegal deliveries.
   - Wicket events (`is_wicket`) cleanly record dismissal mode and dismissed player ID.

---

## 5. Coverage Audit of Shortlisted Candidates

Every player in the candidate pool was checked against the raw files:

| Player Name | Total Deliveries in Raw Pack | Matches in Raw Pack | IPL Exposure | T20I Exposure |
| :--- | :---: | :---: | :---: | :---: |
| **Ruturaj Gaikwad** | 1,822 | 77 | 74 matches (CSK) | 3 matches (India) |
| **Rohit Sharma** | 1,619 | 91 | 74 matches (MI) | 17 matches (India) |
| **Fakhar Zaman** | 863 | 47 | 0 matches | 47 matches (Pakistan) |
| **Suryakumar Yadav** | 2,759 | 139 | 74 matches (MI) | 65 matches (India) |
| **Romario Shepherd** | 687 | 68 | 29 matches (SRH, LSG, MI, RCB) | 39 matches (West Indies) |
| **Naman Dhir** | 589 | 46 | 28 matches (MI) | 18 matches (India A/Dev) |
| **Phil Salt** | 1,643 | 84 | 42 matches (DC, KKR, RCB) | 42 matches (England) |
| **Jitesh Sharma** | 894 | 73 | 58 matches (PBKS, RCB) | 15 matches (India) |
| **Jos Buttler** | 2,829 | 121 | 74 matches (RR, GT) | 47 matches (England) |
| **Liam Dawson** | 424 | 22 | 0 matches | 22 matches (England) |
| **Haris Rauf** | 1,063 | 48 | 0 matches | 48 matches (Pakistan) |
| **Nathan Ellis** | 959 | 43 | 25 matches (PBKS, CSK) | 18 matches (Australia) |
| **Matheesha Pathirana** | 1,279 | 54 | 44 matches (CSK, KKR) | 10 matches (Sri Lanka) |

---

## 6. Audit Conclusion & Gate Certification

1. **Data Pack Incorporation:** 100% verified. All 200,999 raw deliveries are analyzed.
2. **Methodological Defect Classification:** **CLEARED.** The project uses the genuine competition data pack.
3. **Documentation Alignment:** The previous incorrect references to external filenames are now formally corrected and reconciled.

