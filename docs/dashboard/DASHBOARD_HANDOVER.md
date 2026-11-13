# PRESSUREIQ Luxury Editorial Cricket Intelligence Dashboard (`v4.0`)
## Operational Handover, Architecture Guide & Competition User Manual

**Project:** Rajasthan Royals SupeRR Selector Season 2 (2026)  
**Deliverable:** PRESSUREIQ Production Cricket Telemetry Platform  
**Branch:** `redesign-editorial-v4`  
**Master Baseline:** `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2` (Untouched & Cryptographically Verified)  
**Version:** `4.0.0`  
**Date:** 13 November 2026  

---

## 1. Quick Start & Execution

The dashboard is built natively on Streamlit `1.56.0`, Plotly `6.6.0`, and DuckDB `2.0.0` with a bespoke **Kinfolk-inspired Contemporary Luxury Editorial Design System**. It requires zero external npm packages, node servers, or external internet runtime dependencies.

### Launch Command:
```powershell
# From the repository root (c:\Users\kiran\OneDrive\Documents\Desktop\SuperRR):
streamlit run src/dashboard/app.py --server.port 8502
```

### Access URL:
- Local Browser: `http://localhost:8502`
- Direct View Linking: `http://localhost:8502/?page=Player+Intelligence`, `http://localhost:8502/?page=Pressure+Leaderboards`, etc.

---

## 2. Visual & Editorial Architecture

| Design Dimension | Specification |
|---|---|
| **Editorial Direction** | Contemporary Luxury Print Editorial & Kinfolk Magazine Aesthetic |
| **Color Tokens** | Warm Ivory (`#F8F4EC`), Soft Cream (`#F1E9DD`), Terracotta (`#BD6548`), Burnt Earth (`#A94F36`), Deep Ink (`#282321`), Muted Gold (`#C5A46D`), Sage (`#84927A`) |
| **Typography** | Headings: **Playfair Display** (High-contrast serifs) · Body: **Inter** · Telemetry Numerals: **JetBrains Mono** (Tabular numbers) |
| **Chart Styling** | Bespoke `plotly_white` theme: transparent parchment backgrounds, subtle `#EAE1D5` hairlines, terracotta batter traces, muted gold bowler traces, sage surplus indicators |
| **Responsive Layout** | Fluid CSS Grid + flexbox with zero horizontal overflow across Desktop (`1440px`), Laptop (`1366px`), Tablet (`768px`), and Mobile (`375px`) |

---

## 3. Directory Layout & Key Files

```
SuperRR/
├── src/dashboard/
│   ├── app.py                      # Application shell, routing, query param sync, sidebar
│   ├── design_tokens.py            # Warm editorial color tokens, typography scales, palette maps
│   ├── styles.py                   # High-contrast luxury CSS, responsive rules, chart captions
│   ├── components.py               # Reusable UI primitives (editorial hero, KPI cards, badges, callouts, captions)
│   ├── data_loader.py              # Pure data ingestion & DuckDB query layer (uncached + cached)
│   ├── analytics.py                # Statistical calculations, MCDA scoring, 5 pillars, teams
│   ├── charts.py                   # 18 bespoke warm Plotly editorial telemetry charts
│   └── views/
│       ├── overview_and_leaderboards.py  # Page 1 (Overview) & Page 2 (Leaderboards)
│       ├── player_views.py               # Page 3 (Player Intel) & Page 4 (Comparison)
│       ├── analytics_and_emerging.py     # Page 5 (Pressure Analytics) & Page 6 (Emerging)
│       ├── rr_and_market.py              # Page 7 (RR Intelligence) & Page 8 (IPL Market)
│       └── methodology_and_provenance.py # Page 9 (Methodology) & Page 10 (Provenance)
├── docs/dashboard/
│   ├── DESIGN_SYSTEM.md            # Detailed v4.0 luxury editorial design system specification
│   ├── CODERABBIT_REVIEW_LOG.md    # Multi-pass CodeRabbit CLI audit log (clean 0 findings)
│   ├── DASHBOARD_TEST_REPORT.md    # Automated pytest (91/91) & Playwright browser verification
│   ├── DASHBOARD_HANDOVER.md       # This operational manual
│   ├── audit_report.json           # Automated 40-screenshot cross-viewport audit results
│   └── screenshots/                # Rendered UI captures across desktop, tablet, and mobile
│       └── audit/                  # 40 high-resolution view captures (4 viewports x 10 views)
```

---

## 4. Ten Analytical Views Guide

### Page 1: Executive Overview (`?page=Overview`)
- **Master Editorial Masthead:** *"Beyond Performance. Measuring composure under pressure."*
- **Brand Emblem:** Inline vector emblem featuring warm terracotta cricket seam curves.
- **Featured Performers:** Responsive feature cards for Model A #1 Batter (**Ruturaj Gaikwad**, 97.71) and Model A #1 Bowler (**Liam Dawson**, 95.39).
- **Core Metrics:** Evaluated Qualified Cohorts (109 Batters / 147 Bowlers), Dataset Scope (200,999 Balls across 867 Matches, 2,000 Bootstraps).
- **Analytical Charts:** Top 10 Batters and Bowlers confidence interval error bars, batter vs bowler score distribution comparison, paired with contextual analytical takeaways.

### Page 2: Pressure Leaderboards (`?page=Pressure+Leaderboards`)
- **Discipline Tabs:** Batters Leaderboard (109 Qualified) and Bowlers Leaderboard (147 Qualified).
- **Controls & Slicing:** Role/Style multiselect, Season slice (2022–2026), Format slice (IPL, T20I, Other T20), Dataset Team filter, Min HP Balls slider ($P \ge 50$), and Player Search.
- **Frozen Integrity:** Sorting and filtering alter the display table without ever modifying frozen official rank integers.
- **Rank Uncertainty Plot:** Displays 95% bootstrap rank intervals alongside Model A frozen rank markers.

### Page 3: Player Intelligence (`?page=Player+Intelligence`)
- **Player Selector:** Dynamic selection across all 256 qualified cohort players.
- **Profile KPIs:** Official Rank, Reliability Score & 95% CI, High-Pressure Opportunities, Kish Match ESS, Shrunk HP PAVA/ball, and PRC Archetype.
- **Telemetry Suite:**
  - 5-Pillar Spider Radar vs positional peer averages.
  - Empirical Pressure Response Curve across leverage bands with OLS regression slope.
  - Phase-Wise Telemetry Bar Chart (Powerplay, Middle, Death).
  - Expected vs Observed Outcome Rates (LightGBM baseline contrast).
  - Continuous Delivery Exposure Histogram.
  - Match-Level PAVA Contributions (chronological match drilldown).

### Page 4: Player Comparison (`?page=Player+Comparison`)
- **Comparable-Only Rule:** Strictly enforces comparisons within the same discipline (Batters vs Batters OR Bowlers vs Bowlers).
- **Multi-Player Selector:** Choose 2 to 4 players for head-to-head evaluation.
- **Comparative Visuals:**
  - Overlaid 5-Pillar Spider Radar with consistent player color mappings.
  - Reliability Scores with 95% bootstrap confidence intervals.
  - Overlaid Leverage Band Pressure-Response Trajectories.
  - Grouped Phase-Wise Mean PAVA Breakdown.

### Page 5: Pressure Analytics (`?page=Pressure+Analytics`)
- **Contextual Distributions:** BPI vs BoPI delivery distributions across 200,961 balls.
- **Calibration Verification:** LightGBM expected vs observed scoring rates across pressure tiers.
- **Empirical Bayes Shrinkage Curve:** Illustrates sample weight progression ($K=45.0$ balls).
- **League-Wide Scatter:** High-pressure sample volume vs Reliability Score for all qualified players.

### Page 6: Emerging Talent (`?page=Emerging+Talent`)
- **Quarantined Watchlist:** Protects Model A rankings by isolating developmental prospects with $<400$ balls, $<30$ HP balls, or $<20$ matches.
- **Tier Structure:**
  - **Tier A (Qualified Leaders):** Naman Dhir (#6 Batter, 93.30).
  - **Tier B (Near-Miss Prospects):** Prince Yadav (#11 Bowler, 88.87).
  - **Tier C (Developmental Seeds):** Vaibhav Sooryavanshi (7 HP), Vignesh Puthur (72 balls).
- **Opportunity Scatter Matrix:** Visualizes exposure vs HP eligibility cutoffs.

### Page 7: Rajasthan Royals Intelligence (`?page=Rajasthan+Royals+Intelligence`)
- **Audited Core Squad:** 10 qualified RR players verified on the 2026 roster (led by Jofra Archer, Dhruv Jurel, Riyan Parag).
- **Jaipur SMS Strategy:** Mapped against 3 priority tactical deficits:
  1. #7 Seam Power Finisher fit.
  2. Middle-Overs Finger Spin Squeeze (large square boundaries).
  3. Domestic Death Seam depth.
- **Audited Candidates:** Evaluates target role fit without assuming open-auction availability ahead of the official 17 November 2026 retention filing.

### Page 8: IPL 2027 Market Intelligence (`?page=IPL+2027+Market+Intelligence`)
- **Audited Ledger:** Tracks 265 profiles anchored to the 11 November 2026 snapshot.
- **Strict Status Taxonomy:**
  - `Confirmed Trade Active`: Verified trade agreements (e.g., Nathan Ellis PBKS $\to$ CSK, Mayank Markande KKR $\to$ MI).
  - `Confirmed Retention Active`: Verified franchise retentions.
  - `Confirmed Release Active`: Verified releases.
  - `Pending Verification`: Pre-deadline players awaiting official 17 November 2026 filings.
- **Non-Interference Rule:** Rumours and speculations never alter frozen Model A rankings or team rosters.

### Page 9: Methodology & Validation (`?page=Methodology+&+Validation`)
- **Exact Equations:** Full LaTeX display of BPI, BoPI, and PAVA formulations.
- **Variant Reconciliation:** Authoritative table reconciling the frozen legacy fixed-120-ball calculation with the dynamic `max_innings_balls` research implementation ($0.00$ difference across standard 20-over games).
- **Validation Reports:** Out-of-sample chronological holdout benchmarks and 5-pillar ablation metrics.

### Page 10: Data Sources & Provenance (`?page=Data+Sources+&+Provenance`)
- **Cryptographic Checksum Registry:** Live SHA-256 verification of `final_batter_rankings.csv`, `final_bowler_rankings.csv`, `PRESSUREIQ_Final_Submission.zip`, and `ipl_2027_market_snapshot_2026-11-11.csv`.
- **System Lineage:** Complete table of upstream match sources, ball counts, and pipeline execution logs.

---

## 5. Quality Assurance & Verification

- **Pytest Suite:** 91 of 91 tests passed in 31.86s (`pytest tests/ -v`).
- **Playwright Cross-Viewport Audit:** All 40 viewport captures verified (0 horizontal overflow, 0 exceptions, 0 console errors).
- **CodeRabbit Review:** Clean Pass (**0 findings**) across all dashboard source files.
- **Baseline Immutability:** 100% cryptographic match to frozen baseline commits.
