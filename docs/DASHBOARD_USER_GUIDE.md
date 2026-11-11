# PRESSUREIQ — Dashboard User Guide

**Application Name:** PRESSUREIQ — Cricket Pressure Intelligence  
**Target Competition:** Rajasthan Royals SupeRR Selector Season 2 (Deadline: 18 November 2026)  
**Verified Snapshot Anchor:** 11 November 2026 (Ahead of 17 Nov IPL 2027 Retention Deadline)

---

## 1. Environment Setup Commands

From a clean checkout of branch `remediation-phase1-audit`:

```powershell
# 1. Create an isolated Python 3.13 virtual environment
python -m venv .venv

# 2. Install pinned dependencies
.venv\Scripts\python.exe -m pip install -r requirements.txt

# 3. Verify all automated tests pass
.venv\Scripts\python.exe -m pytest tests/
```

*(Note: If host Windows `ensurepip` fails inside `python -m venv`, install into an isolated venv created via `python -m venv --without-pip .venv` using host pip: `python -m pip --python .venv\Scripts\python.exe install -r requirements.txt`.)*

---

## 2. Dashboard Launch Command

```powershell
# Launch PRESSUREIQ — Cricket Pressure Intelligence
streamlit run src/dashboard/app.py
```

Or with explicit local port & headless server flags:

```powershell
python -m streamlit run src/dashboard/app.py --server.port 8501 --server.address 127.0.0.1
```

---

## 3. Navigation Pages (10 Views)

1. **1. Executive Overview:** Frozen Model A #1 Batter (`Ruturaj Gaikwad`, 97.71) & #1 Bowler (`Liam Dawson`, 95.39), Top-10 previews, evaluated cohort counts (`109` batters / `147` bowlers from `200,961` regular-over deliveries across `867` matches), bootstrap rank-instability disclosure, and 11 Nov market snapshot parity.
2. **2. Top 10 Pressure-Resilient Batters:** Interactive leaderboard featuring Role, Season (`2022–2026`), Format (`IPL`, `T20I`, `Other_T20`), Team, Minimum HP Opportunities (`>=30`), and Name Search filters. Clearly distinguishes raw `HP Opportunities`, `Kish Match ESS`, and `EB Effective HP Balls`.
3. **3. Top 10 Pressure-Resilient Bowlers:** Equivalent filtered leaderboard for the 147 qualified bowlers (`Legal Balls`, `Career Economy`, `BoPI >= 50.0`).
4. **4. Player Intelligence:** Select any qualified batter or bowler to inspect delivery-level Pressure Response Profile (`Low / Medium / High / Extreme`), Five-Pillar Radar vs role peers, Powerplay/Middle/Death phase table & bar chart, and most recent 15 match-level PAVA contributions.
5. **5. Pressure Analytics:** Cohort distributions by PRC archetype, Sample Size vs Reliability Score (`K_shrink = 45` line), Top-15 Bootstrap Rank Uncertainty dumbbell intervals, Batter vs Bowler box comparisons, and league-wide phase pressure table.
6. **6. Emerging Talent:** Separates developmental profiles (`<400` balls or `<30` HP balls) from proven Model A reliability via both the curated watchlist and live DuckDB below-threshold discovery.
7. **7. Rajasthan Royals Squad Intelligence:** Separates RR 2026 qualified core & Sawai Mansingh tactical fit (`rr_priority_score`) from verified market status (`Pending Verification` / `Confirmed Trade` / `Policy/Eligibility Review`).
8. **8. Auction & Market Intelligence:** Audited ledger pinned to the **11 November 2026 Competition Snapshot** alongside a separate **Post-Audit Change Log** tab. Displays strict 6-status badges (`Confirmed Trade`, `Confirmed Retained`, `Confirmed Released`, `Pending Verification`, `Rumour`, `Policy/Eligibility Review`) with publisher, publication date, verification timestamp, evidence excerpt, and HTTP 200 URL.
9. **9. Methodology & Validation:** Accessible explanation of BPI, BoPI, LightGBM expected outcomes (`MODEL_BENCHMARK_REPORT.json`), raw vs leverage PAVA, linear PRC, EB shrinkage, 2,000-bootstrap intervals, and explicit Spec-vs-Code discrepancies (`P >= 50.0` vs `[65, 85)`, linear OLS vs exponential phrasing, cohort lineage).
10. **10. Data Sources & Audit Trail:** Row-count reconciliation (`200,999` raw -> `200,961` regular + `38` Super Over balls), 6 immutable raw CSV SHA-256 digests, frozen Model A & ZIP hashes, and Phase 2 clean-room verification ledger.
