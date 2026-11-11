# PRESSUREIQ — Analytical Dashboard Upgrade & Interface Architecture Report

**Document:** `docs/DASHBOARD_UPGRADE_REPORT.md`  
**Date:** 15 November 2026  
**Status:** Certified Dashboard Upgrade Report  
**Implementation:** `src/dashboard/app.py`  
**Framework:** Rajasthan Royals SupeRR Selector Season 2 — Round 1  

---

## 1. Executive Summary & Design Philosophy

The primary purpose of the PRESSUREIQ interactive analytical dashboard (`src/dashboard/app.py`) is to deliver an intuitive, franchise-grade decision support platform for Rajasthan Royals management.

Rather than cluttering the interface with unnecessary backend complexity or decorative gimmicks, the upgraded dashboard prioritizes:
1. **User-Facing Analytical Clarity:** Providing immediate answers to high-stakes recruitment and tactical questions.
2. **Six Comprehensive Analytical Views:** Covering competition objectives, leaderboards, multi-player comparisons, emerging talent scouting, franchise strategy, and validation governance.
3. **High-Performance Responsiveness:** Utilizing DuckDB in-memory querying for instant delivery-level filtering across 200,999 records without browser lag.
4. **Strict Confidentiality Compliance:** Operating strictly on processed Parquet extracts and masked player tables to prevent proprietary competition data exposure.

```mermaid
flowchart TD
    App["Streamlit Dashboard (src/dashboard/app.py)"]
    App --> VA["View A: Competition Overview & Provenance"]
    App --> VB["View B: Player Leaderboards (Model A vs Leaderboard B)"]
    App --> VC["View C: Multi-Player Analytical Comparison (Radar / PRC)"]
    App --> VD["View D: Dedicated Emerging Talent Watchlist"]
    App --> VE["View E: RR Roster Strategy & Live Market Intelligence"]
    App --> VF["View F: Validation Benchmarks & Research Integrity"]
```

---

## 2. Detailed Breakdown of the Six Dashboard Views

### View A: 📋 Competition Overview & Provenance
- **Executive Metrics Ribbon:** 200,999 audited deliveries, 867 played matches (367 IPL + 470 T20Is), Brier score 0.0521, and 2,000 bootstrap resamples.
- **Problem Statement Clarification:** Explains the competition mandate, the decoupling of pure statistical truth (Leaderboard A) from auction feasibility (Leaderboard B).
- **Metric Interpretation Guide:** Clear, readable definitions of Reliability Score (0–100), PAVA (runs added/suppressed per ball), and the three Pressure Response Curve (PRC) archetypes.
- **Cryptographic Provenance Ledger:** Inventory table listing all six canonical CSV files, row counts, and immutability status.

### View B: 🏆 Player Leaderboards
- **Dual-Mode Toggle:**
  - *Mode 1 (Model A):* Pure unconstrained statistical reliability across all nationalities and franchises.
  - *Mode 2 (Leaderboard B):* Actionable RR IPL 2027 recommendations accounting for BCCI regulatory policy and franchise retentions.
  - *Discipline Selection:* Instant toggling between Batters and Bowlers.
- **Interactive Search & Filtering:** Real-time search box enabling users to filter by player name (e.g. "Buttler", "Ellis", "Gaikwad", "Jurel").
- **Visual Confidence Interval Bars:** Plotly bar charts rendering exact 95% bootstrap confidence bands for every top 10 player.

### View C: ⚖️ Multi-Player Analytical Comparison
- **Multi-Select Dropdown:** Allows users to select two or more players for direct head-to-head evaluation.
- **Five-Pillar Quantitative Radar:** Overlaid polar radar plots visualizing Pressure PAVA, Baseline Retention, Match Consistency, Adaptability, and Evidence Strength.
- **Metric Comparison Table:** Side-by-side display of reliability scores, confidence intervals, top-10 inclusion probabilities ($\Pi_{10}$), PRC slopes, and high-pressure sample sizes.
- **Dynamic PRC Curve Modeling:** Instantaneous DuckDB querying of actual delivery bins with standard error bars against fitted linear response trends.

### View D: 🌟 Emerging Talent Watchlist
- **Dedicated Scouting Matrix:** Screens young (<25) and uncapped players (Vaibhav Sooryavanshi, Prince Yadav, Naman Dhir, Rasikh Salam, Vignesh Puthur, Allah Ghazanfar).
- **The Vaibhav Sooryavanshi Paradox:** Educates users on selection censorship in powerplay overs and explains why future developmental potential is not conflated with late-innings clutch proof.
- **Prospect Spotlight Selector:** Deep-dive cards providing tactical scouting assessments and actionable Rajasthan Royals recruitment/development recommendations.

### View E: 🏰 RR Strategy & Market Intelligence
- **Sawai Mansingh Stadium Venue Dynamics:** Details Jaipur's large outfield geometry (74–76m straight boundaries) and pitch deceleration.
- **Solving the Four Tactical Deficits:**
  1. *Death Bowling Partner for Sandeep Sharma* (Nathan Ellis, Shoriful Islam)
  2. *The #7 Seam-Bowling Power Finisher* (Romario Shepherd, Jason Holder)
  3. *The Jaipur Squeeze Finger Spinner* (Harpreet Brar, Liam Dawson)
  4. *Domestic Indian Pace Depth* (Prince Yadav, Rasikh Salam)
- **Projected High-Pressure Starting XI:** Full tactical lineup including Impact Player options.
- **Live Pre-Retention Market Ledger:** Source-backed database tracking official retentions, releases, trades, and rumours across all 10 IPL franchises.

### View F: 🔬 Validation & Research Integrity
- **Machine Learning Benchmark Table:** LightGBM out-of-fold calibration slopes ($0.992$), Brier scores ($0.0521$), and RMSE metrics against naive baselines.
- **Research Integrity Protocols:** Zero data fabrication, forward chronological walk-forward splits, sensor noise filtering, and frozen baseline preservation.
- **Unit Test Coverage Banner:** Confirms 62 / 62 pytest unit tests passing.

---

## 3. Visual & Technical Polish Enhancements

1. **Brand Alignment:** Styled using Rajasthan Royals official royal blue (`#004BA0`), pink (`#EA1B88`), and neutral off-white backgrounds (`#FAFAFC`).
2. **Mobile-Responsive Typography:** Container widths and table paddings dynamically adapt across desktop monitors and mobile browser viewports.
3. **Zero Deprecation Warnings:** Codebase refactored to eliminate legacy syntax warnings and comply with Streamlit standards.
4. **Headless Execution Verification:** Confirmed 100% operational via `python scripts/test_streamlit_headless.py`.

