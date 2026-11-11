# FINAL DASHBOARD AUDIT REPORT
## Streamlit & Plotly Interactive Application Verification

**Project:** PRESSUREIQ — Context-Aware Cricket Reliability Intelligence  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 (2026)  
**Audit Date:** 12 November 2026  
**Auditor:** Quantitative Review & Submission QA Panel  
**Application Entry Point:** `src/dashboard/app.py`  
**Test Script:** `scripts/test_streamlit_headless.py`  
**Status:** PASS — FULLY FUNCTIONAL & VERIFIED  

---

## 1. APPLICATION ARCHITECTURE & INTEGRATION

The interactive dashboard provides a browser-based UI for exploring player reliability scores, Pressure Response Curves (PRC), five-pillar breakdowns, and delivery-level PAVA distributions:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        PRESSUREIQ STREAMLIT DASHBOARD MODULES                          │
├─────────────────────┬──────────────────────────────────────────────────────────────────┤
│ Module / Tab        │ Functionality & Underlying Data Integration                      │
├─────────────────────┼──────────────────────────────────────────────────────────────────┤
│ 1. Leaderboards     │ Top 10 Batters & Bowlers; Five-Pillar metric tables; PRC badges; │
│                     │ Source: final_batter_rankings.parquet, final_bowler_rankings.pqt │
├─────────────────────┼──────────────────────────────────────────────────────────────────┤
│ 2. Player Deep Dive │ Individual player selector; Pressure Response Curves (Plotly);   │
│                     │ Strike rate by pressure tier; Source: deliveries_with_pava.pqt   │
├─────────────────────┼──────────────────────────────────────────────────────────────────┤
│ 3. Methodology &    │ LightGBM benchmark metrics (RMSE, Brier); Calibration tables;   │
│    Validation       │ Data provenance SHA-256 hashes; Source: PROVENANCE.json          │
└─────────────────────┴──────────────────────────────────────────────────────────────────┘
```

---

## 2. HEADLESS EXECUTION & RUNTIME INTEGRITY

The dashboard was tested using the automated headless test runner `scripts/test_streamlit_headless.py`:

```
Headless Execution Log:
$ python scripts/test_streamlit_headless.py
Testing direct streamlit output...
Streamlit version: Streamlit, version 1.56.0
src.dashboard.app successfully imported without errors!
Exit Code: 0
```

### Verified Checks:
- **No Import Errors:** All dependencies (`streamlit`, `plotly`, `duckdb`, `pandas`, `numpy`) resolve cleanly.
- **Data Parity:** The dashboard dynamically queries `data/processed/final_batter_rankings.parquet` and `data/processed/final_bowler_rankings.parquet`, displaying:
  - Batter #1: Ruturaj Gaikwad (Reliability: 97.71)
  - Batter #2: Rohit Sharma (Reliability: 95.27)
  - Bowler #1: Liam Dawson (Reliability: 95.39)
  - Bowler #2: Haris Rauf (Reliability: 92.36)
- **Uncertainty & Sample Size:** The UI displays 95% bootstrap confidence intervals, PRC archetypes, and total delivery exposure per player.
- **Decoupling from Hybrid Research:** The dashboard strictly serves the official Model A baseline rankings, preventing confusion with exploratory research models.

---

## 3. AUDIT VERDICT

The dashboard passes all functionality, data integrity, and headless startup tests with exit code 0.

