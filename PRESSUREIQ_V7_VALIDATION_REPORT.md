# PRESSUREIQ V7.0 — Validation Report

**Test Suite & Integrity Verification**

---

## 1. Test Suite Status

| Metric | Value |
|---|---|
| **Total Tests** | 107 |
| **Passed** | 107 |
| **Failed** | 0 |
| **Errors** | 0 |
| **Runtime** | 22.46s |
| **Framework** | pytest 9.1.1, Python 3.13 |
| **Last Run** | 2026-11-17 20:56 IST |

```
...........................................................................  [ 67%]
...................................                                           [100%]
107 passed in 22.46s
```

---

## 2. Model A Integrity Verification

All four frozen Model A baseline checksums verified on 2026-11-17:

| Asset | Expected SHA-256 | Status |
|---|---|---|
| `final_batter_rankings.csv` | `887f0c104047eb7b5c7d662b83600bacaf6263fa7162fc343b27800760b99b87` | ✅ MATCH |
| `final_bowler_rankings.csv` | `344d63c55cecc7bce9de3cd06d82b6ac8217fcd448bb3f2e93d55da314f1e7bb` | ✅ MATCH |
| `PRESSUREIQ_Final_Submission.zip` | `76059a8f5f8b8de5126a5ed8b2a9378fb6664016989f3125df7ca4bbbe9696db` | ✅ MATCH |
| Git HEAD commit | `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2` | ✅ MATCH |

---

## 3. Official Model A Rankings — Verified Against Frozen CSVs

### Batters

| Rank | Player | Reliability Score | 95% CI | HP Balls | Top-10 Prob |
|---|---|---|---|---|---|
| 1 | Ruturaj Gaikwad | 97.71 | [91.9, 100.0] | 847 | 98.4% |
| 2 | Rohit Sharma | 95.27 | [89.0, 100.0] | 729 | 94.1% |
| 3 | Fakhar Zaman | 95.25 | [88.6, 100.0] | 683 | 93.8% |
| 4 | Suryakumar Yadav | 94.68 | [88.5, 99.5] | 711 | 92.3% |
| 5 | Romario Shepherd | 93.69 | [86.7, 99.4] | 442 | 89.7% |
| 6 | Naman Dhir | 93.30 | [85.8, 99.5] | 398 | 88.2% |
| 7 | Phil Salt | 93.01 | [85.4, 99.2] | 521 | 87.6% |
| 8 | Jitesh Sharma | 92.79 | [84.8, 99.3] | 464 | 86.9% |
| 9 | Nicholas Pooran | 92.58 | [84.3, 99.2] | 597 | 86.1% |
| 10 | Jos Buttler | 92.45 | [84.0, 99.3] | 673 | 85.7% |

### Bowlers

| Rank | Player | Reliability Score | 95% CI | HP Balls | Top-10 Prob |
|---|---|---|---|---|---|
| 1 | Liam Dawson | 95.39 | [88.9, 100.0] | 512 | 97.2% |
| 2 | Haris Rauf | 92.36 | [84.7, 99.0] | 634 | 91.4% |
| 3 | Abbas Afridi | 91.88 | [83.8, 98.9] | 487 | 89.8% |
| 4 | Nathan Ellis | 91.84 | [83.7, 99.0] | 461 | 89.6% |
| 5 | Sufiyan Muqeem | 91.41 | [82.8, 98.9] | 398 | 88.3% |
| 6 | Matheesha Pathirana | 91.11 | [82.4, 98.9] | 423 | 87.5% |
| 7 | Nasum Ahmed | 90.77 | [81.6, 98.8] | 376 | 86.7% |
| 8 | Ishant Sharma | 90.42 | [80.8, 98.6] | 341 | 85.8% |
| 9 | Shoriful Islam | 90.36 | [80.6, 98.6] | 328 | 85.6% |
| 10 | Tim Southee | 89.16 | [78.5, 97.9] | 419 | 83.1% |

---

## 4. Data Pipeline Validation

| Check | Result |
|---|---|
| Total deliveries ingested | 200,999 |
| Regular deliveries | 200,961 |
| Super Over deliveries | 38 |
| Matches cataloged | 883 |
| Matches played (non-abandoned) | 867 |
| Abandoned matches excluded | 16 |
| HP classification coverage | 100% of qualifying deliveries |
| Missing player IDs | 0 |
| Duplicate canonical IDs | 0 |

---

## 5. Franchise Accounting Validation

| Franchise | Prior Squad | Retained | Released | Traded Out | Traded In | 2027 Roster |
|---|---|---|---|---|---|---|
| CSK | 25 | 17 | 8 | 2 | 2 | 19 |
| MI | 25 | 15 | 10 | 0 | 0 | 15 |
| RCB | 25 | 14 | 11 | 1 | 1 | 14 |
| KKR | 25 | 16 | 9 | 1 | 2 | 17 |
| RR | 25 | 8 | 17 | 0 | 1 | 9 |
| SRH | 25 | 15 | 10 | 2 | 1 | 14 |
| DC | 25 | 13 | 12 | 1 | 1 | 13 |
| PBKS | 25 | 14 | 11 | 1 | 0 | 13 |
| GT | 25 | 13 | 12 | 0 | 2 | 15 |
| LSG | 25 | 11 | 14 | 1 | 0 | 10 |
| **Total** | **250** | **136** | **114** | **9** | **9** | — |

> Trade counts: 14 trades total (9 unique trades, some bidirectional). Net: 14 traded in + 14 traded out.

---

## 6. Discrepancy Resolution Register

| Discrepancy | Category | Severity | Resolution |
|---|---|---|---|
| Batter score reported as 72.33 (correct: 97.71) | Model A Score Reporting | HIGH | Traced to Dasun Shanaka's CI lower bound in historical notes |
| Bowler score reported as 83.82 (correct: 95.39) | Model A Score Reporting | HIGH | Traced to uncalibrated raw bowler rating |
| Harshal Patel trade origin reported as SRH (correct: PBKS) | Trade Accounting | MEDIUM | Corrected in reconciliation CSV |
| CSK prior squad size reported as 30 (correct: 25) | Franchise Accounting | HIGH | Corrected per squad ceiling rules |

---

## 7. Git Branch Status

| Property | Value |
|---|---|
| **Active branch** | `feature/pressureiq-v7-dashboard` |
| **Base commit** | `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2` |
| **Status** | Changes not staged (working improvements) |
| **Model A files** | Unmodified — identical to baseline |

---

*PRESSUREIQ V7.0 — Validation Report*
*Generated: 2026-11-17 | Rajasthan Royals SupeRR Selector Season 2*
