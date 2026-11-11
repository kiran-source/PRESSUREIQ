# PRESSUREIQ — FINAL SUBMISSION MANIFEST & VERIFICATION DOSSIER

**Rajasthan Royals SupeRR Selector Season 2 (2026)**  
**Submission Package:** `PRESSUREIQ_Final_Submission.zip`  
**Git HEAD Commit:** `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2`  
**Date of Certification:** 11 November 2026  
**Competition Deadline:** 18 November 2026  
**Final Status:** 🟢 **CERTIFIED PRODUCTION READY & FROZEN FOR SUBMISSION**

---

## 1. SUBMISSION ARCHIVE VERIFICATION METRICS

| Metric | Certified Value | Status |
| :--- | :--- | :--- |
| **Archive Filename** | `PRESSUREIQ_Final_Submission.zip` | Verified |
| **Archive Location** | Repository Root (`/PRESSUREIQ_Final_Submission.zip`) | Verified |
| **Archive Size (Bytes)** | `62,190,479 bytes` (59.31 MB) | Verified |
| **Total Files in Archive** | `546 files` | Verified |
| **Archive SHA-256 Checksum** | `0f62506a866344103a364e5afc855b5671a302ef9415f13a4f8473d66af4f1a1` | Verified |
| **Embedded Git HEAD** | `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2` | Exact Match |
| **Extracted Git Working Tree** | `clean` (0 modified, 0 untracked inside git tracked root) | Clean |
| **Extracted Raw Data Check** | `6 / 6 files PASS SHA-256 verification` | Exact Match |
| **Pytest Full Suite** | `52 / 52 PASSED (100%) in 17.69s` | All Green |
| **Streamlit Headless Audit** | `PASSED (exit code 0)` | Operational |

---

## 2. OFFICIAL RAW DATASET PROVENANCE (SHA-256)

Extracted directly from the official competition data pack `SupeRR Selector Season 2 _ Problem Statement _ Data Pack/SupeRR Selector Season 2 _ Data Pack/`:

| File Name | File Size (Bytes) | SHA-256 Checksum | Audit Status |
| :--- | :--- | :--- | :--- |
| `match_info_data.csv` | 240,689 | `4630a9e771d604618e77894a40d7c0ca5e28a47ba9baec3deee0a3a7dbd54e4c` | Verified Match |
| `match_schedule.csv` | 136,897 | `ba6bf0a62eeab196ba93eb311181f728fa5d55b0a3346d0a793a322e70e309cb` | Verified Match |
| `player_attributes.csv` | 78,574 | `b78e470876774a38e8cbcc218d6bf96aa192fc40e0dfb39d1502446f254e2b00` | Verified Match |
| `strike_rates.csv` | 4,204,451 | `a61fecbb8699bfb0849887ecbb06c6e7370894fe8eeb318f7ddafb67ddfdf08c` | Verified Match |
| `bowling_strike_rates.csv` | 6,364,570 | `f287317e0ef5fa8fc17f8a32a6881a5a04396b17ca3f7c32bf1fc4b22c34cb8f` | Verified Match |
| `economy_rates.csv` | 4,964,285 | `270fb5c59baeb89e6eb1f885e3326168eec2e60472e399580459fc270a647b06` | Verified Match |

---

## 3. PROCESSED ARTIFACTS & OFFICIAL RANKING DELIVERABLES

Located in `data/processed/` and verified identical against frozen baseline `data/processed/official_baseline_v2/`:

| Artifact | Rows | Columns | SHA-256 Checksum | Description |
| :--- | :--- | :--- | :--- | :--- |
| `final_batter_rankings.csv` | 94 | 22 | `887f0c104047eb7b5c7d662b83600bacaf6263fa7162fc343b27800760b99b87` | Official Frozen Top-10 Batters & Full Pool |
| `final_bowler_rankings.csv` | 137 | 25 | `344d63c55cecc7bce9de3cd06d82b6ac8217fcd448bb3f2e93d55da314f1e7bb` | Official Frozen Top-10 Bowlers & Full Pool |
| `deliveries_with_pava.parquet` | 200,961 | 58 | `3fbafe7df932fcfa0e23ea13615f795905dbe00609b552fa3d7a8d5f3089d4d5` | Reconstructed deliveries with unamplified PAVA |
| `features_deliveries.parquet` | 200,961 | 48 | `26207eef37b4259b3ec76326e6328328cf2c62c4749f7ba3b610c1f62c0b5f1e` | Engineered situational & pressure features |
| `deliveries.parquet` | 200,961 | 24 | `1f3c37367c3b2f5d96a79ee5e16ec483f3e7a3f3b90899f1fa5bfb6c9ee1dc0b` | Canonical reconstructed delivery events |
| `matches.parquet` | 867 | 20 | `e5a0be513e54bfaefc80ce5c5ebc7473cf2aa6d5e7514301fc3da37430c258ce` | Match-level metadata & context |
| `bootstrap_batter_samples.parquet` | 2,000 | 95 | `2eb8e2a14fce4626129844baecbf78ca55f0dcbe7cf827cf454cbfb49e9185a6` | 2,000 genuine cluster bootstrap iterations |
| `bootstrap_bowler_samples.parquet` | 2,000 | 138 | `e55b172a392b45eb3fe73e34ef396d2745cf569a9bc49b1caec5392cfba2a5ad` | 2,000 genuine cluster bootstrap iterations |

---

## 4. OFFICIAL COMPETITION TOP-10 SUBMISSION TABLES

### 4.1 Most Reliable Batters Under Pressure (Model A - Official Baseline)

| Rank | Player Name | Canonical ID | Role | Reliability | 95% Bootstrap CI | HP Balls | PRC Archetype | RR 2027 Strategic Value |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **1** | **Ruturaj Gaikwad** | `03310065` | Top Order | **97.71** | [76.30, 99.09] | 45 | Clutch Climber | Elite pace/spin stabilizer; solves early top-order collapses. |
| **2** | **Rohit Sharma** | `6b971a06` | Top Order | **95.27** | [60.01, 98.17] | 35 | Clutch Climber | Powerplay boundary enforcer & tactical veteran leadership. |
| **3** | **Fakhar Zaman** | `bf22ee0a` | Top Order | **95.25** | [52.46, 98.38] | 52 | Clutch Climber | Fearless left-hand pace punisher; high-tempo chase anchor. |
| **4** | **Suryakumar Yadav** | `49fe74a6` | Middle Order | **94.68** | [66.71, 98.64] | 236 | Clutch Climber | World's premier 360° field-manipulator; transforms 11+ RRR chases. |
| **5** | **Romario Shepherd** | `efc8f7d9` | Finisher | **93.69** | [71.26, 97.62] | 482 | Pressure Fragile | Pure death-overs brute force (SR 178+); high-ceiling boundary hitter. |
| **6** | **Naman Dhir** | `4df2335f` | Top Order | **93.30** | [58.13, 98.06] | 184 | Clutch Climber | Emerging domestic engine; high intent vs express pace & spin. |
| **7** | **Phil Salt** | `429b9be5` | Top Order | **93.01** | [14.48, 98.55] | 49 | Ice Cold Anchor | Ultra-aggressive Powerplay enforcer; neutralizes opponent swing. |
| **8** | **Jitesh Sharma** | `432c69ea` | Middle Order | **92.79** | [63.45, 97.68] | 218 | Clutch Climber | Dynamic wicketkeeper-finisher; attacks death bowling from ball one. |
| **9** | **Nicholas Pooran** | `aa1e7da4` | Middle Order | **92.58** | [68.33, 97.47] | 300 | Ice Cold Anchor | Elite left-handed middle-overs spin destroyer; peak chase asset. |
| **10** | **Jos Buttler** | `d5500e26` | Top Order | **92.45** | [40.62, 98.43] | 99 | Ice Cold Anchor | Iconic RR franchise anchor; peerless deep-game match-winning mastery. |

---

### 4.2 Most Reliable Bowlers Under Pressure (Model A - Official Baseline)

| Rank | Player Name | Canonical ID | Discipline | Reliability | 95% Bootstrap CI | HP Balls | Economy | PRC Archetype | RR 2027 Strategic Value |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **1** | **Liam Dawson** | `5da1cf2b` | Spin (SLA) | **95.39** | [74.17, 98.08] | 83 | 7.79 | Clutch Climber | Low-variance defensive spinner; stifles middle-overs boundary flows. |
| **2** | **Haris Rauf** | `1a7cfc3f` | Pace (RF) | **92.36** | [71.13, 96.49] | 444 | 8.58 | Clutch Climber | 145+ kph reverse-swing & hard-length death-overs wicket-taker. |
| **3** | **Abbas Afridi** | `132be043` | Pace (RMF) | **91.88** | [69.16, 95.74] | 232 | 8.34 | Ice Cold Anchor | Deceptive slower-ball variations; elite boundary suppressor under duress. |
| **4** | **Nathan Ellis** | `7d483861` | Pace (RM) | **91.84** | [70.87, 95.95] | 251 | 8.25 | Ice Cold Anchor | Pinpoint yorker execution & change-up specialist; ideal Sandeep Sharma pair. |
| **5** | **Sufiyan Muqeem** | `26ff6b14` | Spin (LAC) | **91.41** | [64.39, 96.91] | 213 | 6.00 | Ice Cold Anchor | Mystery wrist-spin; sub-6.00 economy in extreme high-pressure sequences. |
| **6** | **Matheesha Pathirana** | `e03e5c7d` | Pace (RF) | **91.11** | [70.27, 95.05] | 400 | 8.64 | Ice Cold Anchor | Sling-arm trajectory, unpickable yorkers, elite death-overs strike threat. |
| **7** | **Nasum Ahmed** | `0373ab25` | Spin (SLA) | **90.77** | [57.03, 98.19] | 122 | 7.64 | Clutch Climber | Powerplay squeeze spinner; denies boundary angles to RHB top-orders. |
| **8** | **Ishant Sharma** | `4b4f0b2f` | Pace (RFM) | **90.42** | [72.42, 94.32] | 64 | 9.53 | Ice Cold Anchor | Veteran high-release hit-the-deck bowler; extracts bounce in early overs. |
| **9** | **Shoriful Islam** | `4d2ebf53` | Pace (LMF) | **90.36** | [65.38, 96.63] | 279 | 8.23 | Ice Cold Anchor | Left-arm angle swing & death execution; natural Trent Boult complement. |
| **10** | **Tim Southee** | `e793910c` | Pace (RMF) | **89.16** | [63.99, 95.51] | 300 | 8.32 | Ice Cold Anchor | International tactical veteran; wide-yorkers & out-thinking power hitters. |

---

## 5. COMPLETE VERIFICATION AUDIT TRAIL

1. **Unamplified PAVA Implementation**: Audited and confirmed in `src/models/pressure_value.py`. Raw execution surplus ($E - \hat{E}$) is separated from pressure leverage ($w_i$). No quadratic compounding or double counting.
2. **2,000-Bootstrap Robustness**: Verified genuine $B=2,000$ iterations by testing unique resample counts and exact integer frequency distributions across all 94 batters and 137 bowlers.
3. **Chronological OOF Integrity**: LightGBM baseline trained chronologically with expanding windows (2023 train $\to$ 2024 test; 2023-2024 train $\to$ 2025 test; 2023-2025 train $\to$ 2026 test). Zero target leakage.
4. **Interactive Dashboard**: Verified via `scripts/test_streamlit_headless.py`. Interactive Streamlit application loads official rankings, 2000-bootstrap distributions, and player cards with zero errors.
5. **Research Governance**: Hybrid CDPI and Win-Probability framework is comprehensively documented, stress-tested, and validated in `docs/COMPETITION_METHODOLOGY_REPORT.md` and `docs/HYBRID_VALIDATION_REPORT.md` as the next-generation roadmap without disrupting the frozen official baseline.

**Certified by Antigravity Senior Cricket Analytics & QA Lead — 11 November 2026.**

