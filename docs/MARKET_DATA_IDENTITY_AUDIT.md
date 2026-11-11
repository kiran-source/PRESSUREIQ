# PRESSUREIQ — FINAL MARKET INTELLIGENCE EVIDENCE AUDIT DOSSIER
**Audit Phase:** Final Market Intelligence Evidence Audit (Pre-Dashboard Gate)  
**Audit Date:** 11 November 2026 (`2026-11-11`)  
**IPL 2027 Retention Deadline:** 17 November 2026 (`2026-11-17`, 6 days in the future)  
**Branch:** `remediation-phase1-audit`  

---

## 1. Executive Honesty Disclosure & Audit Findings

An adversarial source-by-source inspection of `data/processed/ipl_2027_player_market_template.csv` and `data/processed/ipl_2027_market_change_log.csv` established that **the legacy market ledger was unsuitable for dashboard display** due to synthesized dead links, stale 2024 retentions mislabeled as 2027 status, wrong current franchises, and fabricated release/trade events:

1. **All 14 Prior URLs Audited — 13 Invalid/Unreachable & 1 Nonsubstantiating:** Every URL in the prior ledger failed substantive verification (11 HTTP 404, 2 HTTP 403, 1 generic HTTP 200 hub page containing zero 2027 releases).
2. **Temporal Reality Ahead of Nov 17, 2026 Deadline:** Comprehensive team-by-team IPL 2027 retention and release lists are due on **17 November 2026**. As of **11 November 2026**, **ZERO** 2027 open-auction releases are officially confirmed among the 17 tracked players. A 2024 retention, 2025 retention, or IPL 2026 auction purchase establishes the player's IPL 2026 franchise baseline, NOT 2027 retention confirmation.
3. **Critical Factual Errors Corrected:**
   - **Jos Buttler (813):** Plays for **Gujarat Titans** (retained for IPL 2026), NOT Rajasthan Royals.
   - **Matheesha Pathirana (8661):** Released by CSK and signed by **Kolkata Knight Riders** for INR 18 Cr ahead of IPL 2026, NOT retained by CSK.
   - **Vignesh Puthur (48557):** Released by MI and signed by **Rajasthan Royals** at the December 16, 2025 auction (INR 30 lakh) — NOT a November 6, 2026 trade.
   - **Jitesh Sharma (3916):** Retained by **Royal Challengers Bengaluru** for IPL 2026 — NOT a November 7, 2026 PBKS release.
   - **Romario Shepherd (6726):** Retained by **Royal Challengers Bengaluru** for IPL 2026 — NOT a November 8, 2026 MI release.
   - **Harpreet Brar (7325):** Retained by **Punjab Kings** for IPL 2026 — NOT a November 7, 2026 release.
   - **Haris Rauf (7364):** Reflects longstanding post-2008 geopolitical/BCCI stance on Pakistan-registered players — NOT a fabricated individual ban document from `2008-12-01`.
4. **Strict 6-Status Taxonomy Enforced:** Only `Confirmed Retained`, `Confirmed Released`, `Confirmed Trade`, `Pending Verification`, `Rumour`, and `Policy/Eligibility Review` are permitted. Legacy snapshots are archived separately in `data/processed/snapshots/` and never overwritten.

---

## 2. Unsupported / Invalid Source URLs Found in Legacy Ledger

| Legacy Source URL | HTTP Check Result | Legacy Players Cited | Remediation Action |
|:---|:---|:---|:---|
| `https://www.iplt20.com/news/official-retentions-2025-2026` | **HTTP 404 Not Found** | Ruturaj Gaikwad, Matheesha Pathirana | Replaced with live IPLT20 2026 retention release & Business Standard KKR auction report |
| `https://www.mumbaiindians.com/news/retention-announcement` | **HTTP 404 Not Found** | Rohit Sharma, Suryakumar Yadav | Replaced with live MI 2026 squad release (`2025-12-16`) |
| `https://www.espncricinfo.com/story/ipl-retentions-preview` | **HTTP 403 Forbidden** | Naman Dhir | Replaced with live IPLT20 2026 retention release (`2025-11-15`) |
| `https://www.rajasthanroyals.com/news/squad-update` | **HTTP 404 Not Found** | Jos Buttler | Replaced with live IPLT20 2026 retention release (`2025-11-15`, GT) |
| `https://www.rajasthanroyals.com/news/official-retentions` | **HTTP 404 Not Found** | Dhruv Jurel | Replaced with live IPLT20 2026 retention release (`2025-11-15`, RR) |
| `https://www.rajasthanroyals.com/academy/prodigy-announcement` | **HTTP 404 Not Found** | Vaibhav Sooryavanshi | Replaced with live IPLT20 2026 retention release (`2025-11-15`, RR) |
| `https://www.iplt20.com/news/trade-window-updates` | **HTTP 404 Not Found** | Vignesh Puthur | Retracted bogus trade; replaced with live Onmanorama auction report (`2025-12-16`) |
| `https://www.lucknowsupergiants.in/news/retention-list` | **HTTP 404 Not Found** | Nicholas Pooran | Replaced with live IPLT20 2026 retention release (`2025-11-15`, LSG) |
| `https://www.cricbuzz.com/cricket-news/uncapped-retentions-preview` | **HTTP 404 Not Found** | Prince Yadav | Replaced with live IPLT20 2026 retention release (`2025-11-15`, LSG) |
| `https://www.kkr.in/news/retentions-2025` | **HTTP 404 Not Found** | Rinku Singh | Replaced with live IPLT20 2026 retention release (`2025-11-15`, KKR) |
| `https://www.punjabkingsipl.in/news/squad-releases` | **HTTP 200 Generic Page (Unsubstantiated)** | Jitesh Sharma, Harpreet Brar | Retracted false releases; cited live IPLT20 2026 retention release (`2025-11-15`) |
| `https://www.chennaisuperkings.com/news/trade-deal-ellis-khaleel` | **HTTP 403 Forbidden** | Nathan Ellis | Replaced with official IPLT20 trade announcement (`2026-11-05`) |
| `https://www.mumbaiindians.com/news/squad-updates` | **HTTP 404 Not Found** | Romario Shepherd | Retracted false MI release; cited live IPLT20 2026 retention release (`2025-11-15`, RCB) |
| `https://www.bcci.tv/regulatory/ipl-player-regulations` | **HTTP 404 Not Found** | Haris Rauf | Replaced with live Mint report citing BCCI VP Rajeev Shukla (`2025-02-04`) |

---

## 3. Row-by-Row Market Evidence Audit (All 17 Records, Verified 2026-11-11)

| ID | Player | Prev Franchise | Current Franchise (Verified 2026/2027) | Status | Verified Mechanism | Official / Opened Source URL (HTTP 200) | Title & Publisher | Pub Date | Verification Timestamp |
|:---:|:---|:---|:---|:---:|:---|:---|:---|:---:|:---:|
| 6059 | Ruturaj Gaikwad | CSK | Chennai Super Kings | `Pending Verification` | 2026 retained; 2027 list due Nov 17 | `https://www.iplt20.com/news/article/tata-ipl-2026-player-retentions-announced` | TATA IPL 2026 Player Retentions Announced — IPLT20 | 2025-11-15 | 2026-11-11 21:35:00 |
| 8661 | Matheesha Pathirana | CSK | **Kolkata Knight Riders** | `Pending Verification` | Released by CSK; signed by KKR at 2026 auction (INR 18 Cr); 2027 list due Nov 17 | `https://www.business-standard.com/cricket/ipl/ipl-2026-auction-kkr-buys-sl-pacer-matheesha-pathirana-for-rs-18-crore-125121600860_1.html` | IPL 2026 Auction: KKR buys SL pacer Matheesha Pathirana for Rs 18 Crore — Business Standard | 2025-12-16 | 2026-11-11 21:35:00 |
| 126 | Rohit Sharma | MI | Mumbai Indians | `Pending Verification` | 2026 retained; 2027 list due Nov 17 | `https://www.mumbaiindians.com/news/squad-of-2026-assembled-mumbai-indians-cricket` | MI's squad of 2026 = ASSEMBLED!!! — Mumbai Indians | 2025-12-16 | 2026-11-11 21:35:00 |
| 1699 | Suryakumar Yadav | MI | Mumbai Indians | `Pending Verification` | 2026 retained; 2027 list due Nov 17 | `https://www.mumbaiindians.com/news/squad-of-2026-assembled-mumbai-indians-cricket` | MI's squad of 2026 = ASSEMBLED!!! — Mumbai Indians | 2025-12-16 | 2026-11-11 21:35:00 |
| 37052 | Naman Dhir | MI | Mumbai Indians | `Pending Verification` | 2026 retained; 2027 list due Nov 17 | `https://www.iplt20.com/news/article/tata-ipl-2026-player-retentions-announced` | TATA IPL 2026 Player Retentions Announced — IPLT20 | 2025-11-15 | 2026-11-11 21:35:00 |
| 813 | Jos Buttler | RR | **Gujarat Titans** | `Pending Verification` | Signed by GT (INR 15.75 Cr) & retained 2026; 2027 list due Nov 17 | `https://www.iplt20.com/news/article/tata-ipl-2026-player-retentions-announced` | TATA IPL 2026 Player Retentions Announced — IPLT20 | 2025-11-15 | 2026-11-11 21:35:00 |
| 7260 | Dhruv Jurel | RR | Rajasthan Royals | `Pending Verification` | 2026 retained; 2027 list due Nov 17 | `https://www.iplt20.com/news/article/tata-ipl-2026-player-retentions-announced` | TATA IPL 2026 Player Retentions Announced — IPLT20 | 2025-11-15 | 2026-11-11 21:35:00 |
| 50284 | Vaibhav Sooryavanshi | RR | Rajasthan Royals | `Pending Verification` | 2026 retained; 2027 list due Nov 17 | `https://www.iplt20.com/news/article/tata-ipl-2026-player-retentions-announced` | TATA IPL 2026 Player Retentions Announced — IPLT20 | 2025-11-15 | 2026-11-11 21:35:00 |
| 48557 | Vignesh Puthur | MI | Rajasthan Royals | `Pending Verification` | 2026 auction signing INR 30L after MI release (NOT a trade); 2027 due Nov 17 | `https://www.onmanorama.com/sports/cricket/2025/12/16/ipl-2026-player-auction-rajasthan-royals-sign-vignesh-puthur.html` | RR get spinner Vignesh Puthur from IPL auction — Onmanorama | 2025-12-16 | 2026-11-11 21:35:00 |
| 3125 | Nicholas Pooran | LSG | Lucknow Super Giants | `Pending Verification` | 2026 retained; 2027 list due Nov 17 | `https://www.iplt20.com/news/article/tata-ipl-2026-player-retentions-announced` | TATA IPL 2026 Player Retentions Announced — IPLT20 | 2025-11-15 | 2026-11-11 21:35:00 |
| 58246 | Prince Yadav | LSG | Lucknow Super Giants | `Pending Verification` | 2026 retained; 2027 list due Nov 17 | `https://www.iplt20.com/news/article/tata-ipl-2026-player-retentions-announced` | TATA IPL 2026 Player Retentions Announced — IPLT20 | 2025-11-15 | 2026-11-11 21:35:00 |
| 4708 | Rinku Singh | KKR | Kolkata Knight Riders | `Pending Verification` | 2026 retained; 2027 list due Nov 17 | `https://www.iplt20.com/news/article/tata-ipl-2026-player-retentions-announced` | TATA IPL 2026 Player Retentions Announced — IPLT20 | 2025-11-15 | 2026-11-11 21:35:00 |
| 3916 | Jitesh Sharma | PBKS | **Royal Challengers Bengaluru** | `Pending Verification` | Retained by RCB 2026; 2027 list due Nov 17 (NOT PBKS release) | `https://www.iplt20.com/news/article/tata-ipl-2026-player-retentions-announced` | TATA IPL 2026 Player Retentions Announced — IPLT20 | 2025-11-15 | 2026-11-11 21:35:00 |
| 7325 | Harpreet Brar | PBKS | **Punjab Kings** | `Pending Verification` | Retained by PBKS 2026; 2027 list due Nov 17 (NOT confirmed release) | `https://www.iplt20.com/news/article/tata-ipl-2026-player-retentions-announced` | TATA IPL 2026 Player Retentions Announced — IPLT20 | 2025-11-15 | 2026-11-11 21:35:00 |
| **7920** | **Nathan Ellis** | **CSK** | **Sunrisers Hyderabad** | **`Confirmed Trade`** | **4-player IPL 2027 trade (CSK -> SRH, INR 2 Cr)** | `https://www.iplt20.com/news/article/csk-and-srh-agree-to-four-player-trade` | **CSK and SRH agree to four-player trade — IPLT20** | **2026-11-05** | **2026-11-11 21:35:00** |
| 6726 | Romario Shepherd | MI | **Royal Challengers Bengaluru** | `Pending Verification` | Retained by RCB 2026; 2027 list due Nov 17 (NOT MI release) | `https://www.iplt20.com/news/article/tata-ipl-2026-player-retentions-announced` | TATA IPL 2026 Player Retentions Announced — IPLT20 | 2025-11-15 | 2026-11-11 21:35:00 |
| 7364 | Haris Rauf | None | None | `Policy/Eligibility Review` | Historical BCCI/diplomatic stance post-2008 on Pakistani players | `https://www.livemint.com/sports/cricket-news/will-pakistani-players-be-allowed-in-ipl-again-bcci-vice-president-rajeev-shuklas-huge-statement-says-they-do-not-11738666052953.html` | Will Pakistani players be allowed in IPL again? — Mint | 2025-02-04 | 2026-11-11 21:35:00 |

---

## 4. Summary of Status Changes Applied

- **`Confirmed Trade` (1):** **Nathan Ellis** (`Officially retained` -> `Confirmed Trade`, CSK -> SRH on `2026-11-05`).
- **`Policy/Eligibility Review` (1):** **Haris Rauf** (`Unknown` -> `Policy/Eligibility Review`).
- **`Pending Verification` (15):**
  - Downgraded from false `"Officially retained"` (cited to 2024): **Ruturaj Gaikwad, Matheesha Pathirana, Rohit Sharma, Suryakumar Yadav, Dhruv Jurel, Vaibhav Sooryavanshi, Nicholas Pooran, Rinku Singh**.
  - Downgraded from false `"Officially traded"`: **Vignesh Puthur** (reclassified as 2026 auction acquisition, `Pending Verification` for 2027).
  - Retracted from false `"Officially released"` into auction pool: **Jitesh Sharma** (`PBKS Unknown` -> `RCB Pending Verification`), **Harpreet Brar** (`PBKS Unknown` -> `PBKS Pending Verification`), **Romario Shepherd** (`MI Unknown` -> `RCB Pending Verification`).
  - Normalized capitalization from legacy `"Pending verification"`: **Naman Dhir, Jos Buttler (RR -> GT), Prince Yadav**.

---

## 5. Players Still `Pending Verification` (15 of 17 Tracked Records)

All 15 players below remain strictly classified as **`Pending Verification`** until official BCCI/franchise retention lists are submitted by **17 November 2026**:
1. Ruturaj Gaikwad (CSK)
2. Matheesha Pathirana (KKR)
3. Rohit Sharma (MI)
4. Suryakumar Yadav (MI)
5. Naman Dhir (MI)
6. Jos Buttler (GT)
7. Dhruv Jurel (RR)
8. Vaibhav Sooryavanshi (RR)
9. Vignesh Puthur (RR)
10. Nicholas Pooran (LSG)
11. Prince Yadav (LSG)
12. Rinku Singh (KKR)
13. Jitesh Sharma (RCB)
14. Harpreet Brar (PBKS)
15. Romario Shepherd (RCB)

**Confirmed Open-Auction Releases as of 2026-11-11:** **None (0 players).** No pending or unverified player may be displayed as `"Confirmed Available"` or `"Confirmed Released"`.
