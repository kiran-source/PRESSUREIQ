# PRESSUREIQ Premium Interactive Cricket Intelligence Dashboard (`v3.0`)
## Operational Handover, Architecture Guide & User Manual

**Project:** Rajasthan Royals SupeRR Selector Season 2 (2026)  
**Deliverable:** PRESSUREIQ Production Cricket Telemetry Platform  
**Branch:** `dashboard-ui-v3`  
**Base:** `82e77b262aa06802c791c792c1e59507824a15f1`  
**Master Baseline:** `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2` (Untouched & Immutable)  
**Version:** `3.0.0`  
**Date:** 12 November 2026  

---

## 1. Quick Start & Execution

The dashboard is built natively on Streamlit `1.56.0`, Plotly `6.6.0`, and DuckDB `2.0.0` with custom design tokens and SVG primitives. It requires zero external npm packages, node servers, or internet dependencies.

### Launch Command:
```powershell
# From the repository root (c:\Users\kiran\OneDrive\Documents\Desktop\SuperRR):
streamlit run src/dashboard/app.py
```

### Access URL:
- Local Browser: `http://localhost:8501`

---

## 2. Platform Architecture & File Organization

```
SuperRR/
├── src/dashboard/
│   ├── __init__.py
│   ├── app.py                      # Main entrypoint, page routing, global player lookup
│   ├── design_tokens.py            # Dark sports telemetry tokens, color palette, typography
│   ├── styles.py                   # High-contrast CSS, focus states, responsive rules
│   ├── components.py               # Custom UI primitives (hero, KPI cards, badges, callouts)
│   ├── data_loader.py              # Pure data ingestion & DuckDB query layer (uncached + cached)
│   ├── analytics.py                # Statistical calculations, MCDA scoring, 5 pillars, teams
│   ├── charts.py                   # 18 bespoke dark Plotly telemetry charts
│   └── views/
│       ├── __init__.py
│       ├── overview_and_leaderboards.py  # Page 1 (Overview) & Page 2 (Leaderboards)
│       ├── player_views.py               # Page 3 (Player Intel) & Page 4 (Comparison)
│       ├── analytics_and_emerging.py     # Page 5 (Pressure Analytics) & Page 6 (Emerging)
│       ├── rr_and_market.py              # Page 7 (RR Intelligence) & Page 8 (IPL Market)
│       └── methodology_and_provenance.py # Page 9 (Methodology) & Page 10 (Provenance)
├── docs/dashboard/
│   ├── SKILL_USAGE_REPORT.md       # Mandatory skill discovery & application matrix
│   ├── DESIGN_SYSTEM.md            # Typography, palette, spacing, and accessibility spec
│   ├── CODERABBIT_REVIEW_LOG.md    # Multi-pass CodeRabbit review and remediation log
│   ├── DASHBOARD_TEST_REPORT.md    # Automated pytest and Playwright E2E verification
│   ├── DASHBOARD_HANDOVER.md       # This operational manual
│   └── screenshots/                # Rendered desktop, tablet, and mobile UI captures
│       ├── 01_overview_desktop.png
│       ├── 01_overview_mobile_375.png
│       ├── 01_overview_tablet_768.png
│       ├── 02_leaderboards_desktop.png
│       ├── 03_player_intelligence_desktop.png
│       ├── 04_player_comparison_desktop.png
│       ├── 05_pressure_analytics_desktop.png
│       ├── 06_emerging_talent_desktop.png
│       ├── 07_rr_intelligence_desktop.png
│       ├── 08_market_intelligence_desktop.png
│       ├── 09_methodology_desktop.png
│       └── 10_provenance_desktop.png
```

---

## 3. Ten Core Analytical Views

### Page 1: Executive Overview (`#/overview`)
- **Top Bar:** Fixed breadcrumb navigation with live Model A SHA-256 integrity indicator and market snapshot anchor date (`2026-11-11`).
- **Hero Banner:** Professional franchise branding with quick-status filters.
- **Top KPIs:** Model A #1 Batter (Ruturaj Gaikwad, 97.71), Model A #1 Bowler (Liam Dawson, 95.39), Evaluated Qualified Cohort counts (109 Bat / 147 Bowl), and Dataset Scope (200,999 Balls across 867 Matches).
- **Executive Telemetry:** Official Top 10 Batters and Bowlers cards paired with 95% bootstrap confidence interval bars.
- **Governance Disclosure:** Clear statement explaining that composite reliability is a standardized norm-referenced index ($\Phi(Z) \times 100$) rather than a win probability.

### Page 2: Pressure Leaderboards (`#/leaderboards`)
- **Dual Discipline Tabs:** Batting and Bowling leaderboards with distinct franchise accent themes (RR Royal Blue `#2563EB` vs RR Impact Pink `#E11D48`).
- **Population Controls:** Toggle between `Featured Top 10` and `Full Qualified Cohort` (109 Batters / 147 Bowlers).
- **Multidimensional Filters:** Role / Bowling Style, Dataset Team, Minimum High-Pressure Balls ($P \ge 50.0$), Season Slice (2022–2026), and Format Slice (IPL, T20I, Other T20).
- **Sort Dropdown:** Allows sorting by score, inclusion probability, volume, or Kish ESS without ever modifying the frozen official rank column.
- **Interactive Visualizations:** Top-10 CI error bars and 2,000-bootstrap rank uncertainty intervals.

### Page 3: Player Intelligence (`#/player-intelligence`)
- **Profile Selector:** Select any player from the qualified cohort or jump directly from the global sidebar search.
- **Audited Market Status Pill:** Shows official retention status (`Confirmed Trade`, `Confirmed Retained`, `Confirmed Released`, `Pending Verification`).
- **Telemetry Visuals:**
  - Overlaid 5-Pillar Spider Radar (vs peer role average).
  - Empirical Pressure Response Curve (Mean Raw PAVA across leverage bands with OLS regression slope).
  - Phase-Wise Telemetry Bar Chart (Powerplay, Middle, Death).
  - Expected vs Observed Outcome Rates (Run rate, boundary %, dismissal %).
  - Individual Delivery Exposure Histogram ($P \ge 50$ threshold marker).
- **Sample Governance Notes:** Distinguishes raw HP balls, Kish ESS, and match count; prevents small-sample overinterpretation.

### Page 4: Player Comparison (`#/player-comparison`)
- **Comparable-Only Rule:** Strictly enforces comparisons within the same discipline (Batters vs Batters OR Bowlers vs Bowlers).
- **Multi-Player Selector:** Choose 2 to 4 players for head-to-head evaluation.
- **Deterministic Color Harmony:** Colors assigned by original selection order remain identical across the radar chart, sorted CI error bars, and PRC overlay.
- **Overlaid Metrics:** Five-pillar profile overlay, 95% bootstrap CI comparison, pressure-response trajectory overlay, and phase-wise PAVA grouping.

### Page 5: Pressure Analytics (`#/pressure-analytics`)
- **Continuous Distribution:** Grouped frequency bars of batting BPI and bowling BoPI across 200,961 deliveries.
- **PAVA Across Leverage Bands:** Mean raw value added in Low ($<35$), Medium ($35\text{--}65$), High ($65\text{--}85$), and Extreme ($\ge 85$) leverage tiers.
- **Calibration Curves:** Observed vs Expected outcomes across pressure tiers demonstrating model reliability.
- **Empirical Bayes Shrinkage Curve:** Interactive visualization showing how raw scores shrink toward the prior as a function of sample size ($K = 45$ balls).
- **Methodological Guidance:** Explicit warning distinguishing statistical association under pressure from individual psychological causality.

### Page 6: Emerging Talent Watchlist (`#/emerging-talent`)
- **Sub-Threshold Prospects:** Evaluates players with $\ge 30$ balls who did not meet the full Model A eligibility threshold ($<400$ total balls, $<30$ HP balls, or $<20$ matches).
- **Tier C Classification:** Identifies high-upside prospects (e.g., Vaibhav Sooryavanshi, Vignesh Puthur) with strong leverage metrics.
- **Opportunity Matrix:** Scatter plot of High-Pressure Volume vs High-Pressure Raw PAVA.

### Page 7: Rajasthan Royals Intelligence (`#/rr-intelligence`)
- **Strategic SMS Jaipur Context:** Highlights venue-specific requirements (large square boundaries, middle-overs grip, death seam execution).
- **Squad Core Audit:** Verified current RR squad profiles (excluding departed alumni such as Jos Buttler, Trent Boult, and Prasidh Krishna).
- **Role Depth Matrix:** Batting and bowling breakdown across squad roles.
- **Watchlist Separator:** Statistical role fit (`rr_priority_score`) strictly separated from auction availability; displays clear pre-Nov 17 status indicating 0 confirmed releases.

### Page 8: IPL 2027 Market Intelligence (`#/market-intelligence`)
- **10-Franchise Overview:** Complete roster counts, Model A qualifiers, candidate pool mappings, and audited transaction statuses for all 10 IPL teams.
- **Strict Verification Badges:** Confirmed Trade, Confirmed Retained, Confirmed Released, Pending Verification, Rumour, and Policy Review.
- **Source Audit Trail:** Direct HTTP 200-verified publisher URLs, publication dates, and verification timestamps.
- **Non-Interference Rule:** Rumours and speculations never alter official player rankings.

### Page 9: Methodology & Validation (`#/methodology`)
- **Authoritative Formulas:** Frozen BPI ($0.42R + 0.30W + 0.18C + 0.10L$) and BoPI ($0.38D + 0.26W + 0.24C + 0.12L$).
- **Benchmark Suite:** Out-of-fold LightGBM validation metrics (Brier = 0.052, Log-loss = 0.174, AUC = 0.771).
- **Ablation Matrix:** Quantifies accuracy impact when removing match state, pressure, or player historical features.
- **Reconciliation Disclosure:** Documents legacy fixed-120-ball calculation reproducing frozen rankings vs dynamic `max_innings_balls`.

### Page 10: Data Sources & Provenance (`#/provenance`)
- **Cryptographic Registry:** Runtime verification of immutable SHA-256 hashes for batter rankings, bowler rankings, submission ZIP, and market snapshot.
- **Dataset Flow:** Layer-by-layer accounting from raw competition CSVs to cleaned Parquet files and bootstrap samples.
- **Telemetry Missingness Audit:** Exact DuckDB missing-value counts across 200,961 regular deliveries.

---

## 4. Skills Applied

- **`ui-ux-pro-max`**: Design system tokens, telemetry typography, palette selection, spacing scales.
- **`frontend-design` & `impeccable`**: Dark sports telemetry styling, card elevations, contrast ratios, and typography hierarchy.
- **`emil-design-eng`**: Smooth CSS transitions, zero layout shift, `:focus-visible` outlines.
- **`web-accessibility`**: WCAG AA compliance ($>4.5:1$ text contrast), keyboard focus outlines, reduced motion support.
- **`web-design-guidelines`**: Clean component structure, responsive grids, explicit empty/error states.
- **`playwright-browser-automation`**: Automated headless browser testing across desktop, tablet, and mobile viewports.
- **`code-review` (CodeRabbit)**: Automated multi-pass code audit resolving 10 findings with zero regressions.

---

## 5. Non-Negotiable Governance Compliance

1. **Frozen Rankings Unmodified:** `final_batter_rankings.csv` and `final_bowler_rankings.csv` retain their exact submission SHA-256 checksums.
2. **Submission Archive Untouched:** `PRESSUREIQ_Final_Submission.zip` remains intact with SHA-256 `76059a8f5f8b8de5...`.
3. **Master Branch Clean:** Base commit `fc0e622c10d49b4b...` is completely preserved.
4. **Market Separation Maintained:** Statistical performance is strictly segregated from open-auction availability.
5. **No External Deployment:** Dashboard runs locally without external publishing or deployment.

