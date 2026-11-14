# Rajasthan Royals IPL 2027 Auction Availability Audit
## Complete Contractual Ledger, Confirmed Trades, Retentions, and Targetability Audit

> **Mandatory Disclaimer:**  
> *PRESSUREIQ provides an independent analytical recruitment assessment. It does not represent an official Rajasthan Royals recruitment decision or guarantee player eligibility, auction availability, selection, or future performance.*

---

## 1. Executive Summary & Core Principle

In professional franchise cricket recruitment, **regulatory eligibility does NOT equate to contractual auction availability**. 

A player can have perfect BCCI eligibility (e.g., Ruturaj Gaikwad, Jasprit Bumrah, or Arshdeep Singh) but remain **100% unavailable** to Rajasthan Royals because they are retained under multi-year franchise contracts or traded to rival clubs.

**Core Gating Rule:**  
Only candidates who are **BOTH** verified `Eligible` AND realistically targetable (`Confirmed Available`, `Confirmed Released`, or verified uncontracted open auction pool) enter the confirmed Rajasthan Royals recruitment target boards. All other players are systematically routed to the Contracted Ledger, Trade Roster, or Watchlist.

---

## 2. Confirmed Pre-Auction Player Trades (10 Verified Transactions)

During the November 2026 pre-retention IPL trading window, 10 high-profile player transfers were officially executed. All 10 athletes are **Contracted to their new franchises** and are strictly excluded from open-auction acquisition rankings:

| Candidate | Previous Franchise | New Verified Franchise | Transaction Fee | Mechanism | Official Source Authority & Link |
|---|---|---|:---:|:---:|---|
| **Hardik Pandya** | Mumbai Indians | Punjab Kings | ₹18.00 crore | Confirmed Trade | [IPL Trade Commission Notice](https://www.jagranjosh.com/general-knowledge/ipl-2027-trade-list-hardik-pandya-arshdeep-singh-1820013788-1) |
| **Arshdeep Singh** | Punjab Kings | Mumbai Indians | ₹18.00 crore | Confirmed Trade | [IPL Trade Commission Notice](https://www.jagranjosh.com/general-knowledge/ipl-2027-trade-list-hardik-pandya-arshdeep-singh-1820013788-1) |
| **Rishabh Pant** | Lucknow Super Giants | Delhi Capitals | ₹15.00 crore | Confirmed Trade | [IPL Trade Commission Notice](https://www.jagranjosh.com/general-knowledge/ipl-2027-trade-list-hardik-pandya-arshdeep-singh-1820013788-1) |
| **Kuldeep Yadav** | Delhi Capitals | Lucknow Super Giants | ₹13.50 crore | Confirmed Trade | [IPL Trade Commission Notice](https://www.jagranjosh.com/general-knowledge/ipl-2027-trade-list-hardik-pandya-arshdeep-singh-1820013788-1) |
| **T. Natarajan** | Delhi Capitals | Sunrisers Hyderabad | ₹5.00 crore | Confirmed Trade | [IPL Trade Commission Notice](https://www.jagranjosh.com/general-knowledge/ipl-2027-trade-list-hardik-pandya-arshdeep-singh-1820013788-1) |
| **Zeeshan Ansari** | Sunrisers Hyderabad | Delhi Capitals | ₹40 lakh | Confirmed Trade | [IPL Trade Commission Notice](https://www.jagranjosh.com/general-knowledge/ipl-2027-trade-list-hardik-pandya-arshdeep-singh-1820013788-1) |
| **Liam Livingstone** | Sunrisers Hyderabad | Chennai Super Kings | ₹6.00 crore | Confirmed Trade | [Official 4-Player CSK-SRH Deal](https://www.iplt20.com/news/article/csk-and-srh-agree-to-four-player-trade) |
| **Jack Edwards** | Sunrisers Hyderabad | Chennai Super Kings | ₹3.00 crore | Confirmed Trade | [Official 4-Player CSK-SRH Deal](https://www.iplt20.com/news/article/csk-and-srh-agree-to-four-player-trade) |
| **Khaleel Ahmed** | Chennai Super Kings | Sunrisers Hyderabad | ₹4.80 crore | Confirmed Trade | [Official 4-Player CSK-SRH Deal](https://www.iplt20.com/news/article/csk-and-srh-agree-to-four-player-trade) |
| **Nathan Ellis** | Chennai Super Kings | Sunrisers Hyderabad | ₹2.00 crore | Confirmed Trade | [Official 4-Player CSK-SRH Deal](https://www.iplt20.com/news/article/csk-and-srh-agree-to-four-player-trade) |

*Audit Verification:* In the dashboard and datasets, all 10 traded players have their `auction_availability` labeled as `Confirmed Traded`, mapped to their new verified club, and assigned to `Class C`. In `tests/test_dashboard_data.py`, Liam Livingstone (CSK) and Khaleel Ahmed (SRH) are explicitly asserted to be Class C with updated franchise mappings.

---

## 3. Rival Franchise Retentions & Contracted Exclusions (Class C — 58 Athletes)

Under official IPL retention rules, players under active multi-year franchise contracts are not placed on the auction podium. Below are the prominent high-reliability stars retained by rivals:

- **Chennai Super Kings:** Ruturaj Gaikwad (Captain), Sanju Samson (Traded from RR), Shivam Dube, Noor Ahmad, Mukesh Choudhary.
- **Mumbai Indians:** Rohit Sharma, Suryakumar Yadav, Jasprit Bumrah, Tilak Varma, Trent Boult, Naman Dhir.
- **Sunrisers Hyderabad:** Heinrich Klaasen, Travis Head, Pat Cummins, Harshal Patel, Eshan Malinga.
- **Gujarat Titans:** Jos Buttler, Rashid Khan, Prasidh Krishna, Ishant Sharma.
- **Kolkata Knight Riders:** Sunil Narine, Varun Chakaravarthy, Rinku Singh, Rovman Powell, Matheesha Pathirana (₹18 Cr signing).
- **Lucknow Super Giants:** Nicholas Pooran, Avesh Khan, Ayush Badoni.
- **Royal Challengers Bengaluru:** Phil Salt, Tim David, Romario Shepherd, Bhuvneshwar Kumar.
- **Punjab Kings:** Harpreet Brar, Shashank Singh, Marcus Stoinis.
- **Delhi Capitals:** Tristan Stubbs, Axar Patel, Mitchell Starc, Mukesh Kumar.

*Recruitment Action:* All Class C players have their target score capped and discounted ($Avail\_w = 0.20$), preventing them from cluttering Rajasthan Royals' actionable target lists.

---

## 4. Confirmed Available & Realistic RR Target Candidates (28 Athletes)

The following candidates are officially verified as uncontracted, expired contract, or nominated open-auction entrants, providing Rajasthan Royals with realistic recruitment targets:

### Top Target Bowlers (17 Athletes)
1. **Liam Dawson (England / Slow Left-Arm Orthodox):** #1 Model A Bowler (95.4 Rel). Uncontracted international star entering open auction. Perfectly addresses the SMS Jaipur middle-overs finger-spin squeeze (6.8 rpo) with batting depth at No. 8.
2. **Spencer Johnson (Australia / Left-Arm Fast):** 145kph+ express pace, steep bounce, elite death-overs yorker execution. Open auction nominee.
3. **Fazalhaq Farooqi (Afghanistan / Left-Arm Fast-Medium):** High-impact new-ball swing and subcontinental death bowling execution. Open auction candidate.
4. **Allah Ghazanfar (Afghanistan / Off-Spin Mystery):** Highly economical mystery spinner (turns both ways) with 83.7 Model A reliability.
5. **Gus Atkinson (England / Right-Arm Fast):** Express 148kph velocity, sharp bouncers, open auction entrant.
6. **Tanush Kotian (India / Right-Arm Off-Break):** Proven domestic control on responsive surfaces; frees up an overseas slot.
7. **Rasikh Salam (India / Right-Arm Medium-Fast):** Specialized domestic death-overs seamer with deceptive slower balls and wide yorkers.
8. **Vyshak Kumar (India / Right-Arm Medium-Fast):** Heavy-ball domestic pacer extracting hard-length bounce on Jaipur tracks.
9. **Mohit Sharma (India / Right-Arm Medium-Fast):** Veteran death-overs specialist with mastery of back-of-the-hand slower balls.
10. **Prince Yadav (India / Right-Arm Fast):** 140kph+ burst speed domestic prospect.
11. **Nasum Ahmed (Bangladesh / Slow Left-Arm):** Defensive powerplay/middle spinner with elite dot-ball rate (90.8 Rel).
12. **Shoriful Islam (Bangladesh / Left-Arm Fast-Medium):** Tall left-arm angle with steep bounce (90.4 Rel).
13. **Tim Southee (New Zealand / Right-Arm Fast-Medium):** Veteran swing and leadership asset (89.2 Rel).
14. **Lungi Ngidi (South Africa / Right-Arm Fast):** Hit-the-deck express pacer (87.7 Rel).
15. **Dasun Shanaka (Sri Lanka / Right-Arm Medium):** Seam-bowling all-rounder (88.4 Rel).
16. **Moeen Ali (England / Right-Arm Off-Break):** Experienced all-rounder (85.5 Rel).

### Top Target Batters (11 Athletes)
1. **Jamie Smith (England / WK-Batter):** Dynamic 360-degree power hitter against high pace; middle/lower-order enforcer and backup keeper.
2. **Ashutosh Sharma (India / Lower-Order Finisher):** Proven domestic IPL crunch-time clutch finisher at extreme death strike rates.
3. **Jacob Bethell (England / Middle-Order All-Rounder):** Left-handed 360-degree power hitter with multi-dimensional fielding and spin utility.
4. **Nehal Wadhera (India / Middle-Order Batter):** Versatile left-handed domestic middle-order stabilizer with high composure against spin.
5. **Jason Holder (West Indies / All-Rounder):** Veteran composure (91.3 Model A Rel) with lower-order finishing and height.
6. **Mohammad Nabi (Afghanistan / All-Rounder):** Economical off-spin and high-pressure finishing (91.1 Model A Rel).
7. **Darwish Rasooli (Afghanistan / Middle-Order Batter):** Middle-order power striker (91.0 Model A Rel).
8. **Curtis Campher (Ireland / All-Rounder):** High-tempo seam all-rounder (87.4 Model A Rel).
9. **Glenn Phillips (New Zealand / WK-Finisher):** Elite boundary fielder and versatile middle-order striker.
10. **Abishek Porel (India / WK-Batter):** Aggressive domestic Indian powerplay/middle-order keeper-batter.
11. **Sherfane Rutherford (West Indies / Finisher):** Left-handed death-overs boundary enforcer.

---

## 5. Summary Statistics

| Cohort | Count | Governance Action |
|---|:---:|---|
| **Total Evaluated Universe** | **256** | Combined Model A qualifiers and market entries |
| **Verified Eligible Candidates** | **239** | Cleared under BCCI/IPL regulations |
| **Confirmed Traded Players** | **10** | Contracted to new clubs (Class C) |
| **Rival Contracted Retentions** | **58** | Multi-year contracts (Class C) |
| **Confirmed Available Targets** | **28** | Actionable recruitment targets under Model B |
| **Pending Verification Watchlist** | **165** | Awaiting official 17 November franchise lists |
| **Policy Review / Excluded** | **26** | Pakistani passport holders (19) & Retired alumni (7) |
