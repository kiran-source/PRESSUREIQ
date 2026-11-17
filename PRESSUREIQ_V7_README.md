# PRESSUREIQ V7.0 — README

**Context-Aware Cricket Performance Intelligence**
*Rajasthan Royals SupeRR Selector Season 2 Submission*

---

## Overview

PRESSUREIQ is an advanced cricket analytics platform that identifies players who perform reliably under pressure using opportunity-adjusted performance evaluation, Bayesian statistical modelling, empirical Bayes shrinkage, and bootstrap-validated uncertainty quantification.

The platform produces two deliverables:

| Deliverable | Description |
|---|---|
| **Model A — Official Competition** | Top 10 Batters and Top 10 Bowlers who perform best under pressure (frozen, immutable) |
| **Model B — Supplementary** | Franchise retention, trade, auction, and RR recruitment intelligence for IPL 2027 |

---

## Model A — Frozen Competition Results

> **These rankings are immutable. Do not regenerate, re-rank, or overwrite.**

### Top 10 Batters Under Pressure

| Rank | Player | Score | 95% CI |
|---|---|---|---|
| 1 | Ruturaj Gaikwad | 97.71 | [91.9, 100.0] |
| 2 | Rohit Sharma | 95.27 | [89.0, 100.0] |
| 3 | Fakhar Zaman | 95.25 | [88.6, 100.0] |
| 4 | Suryakumar Yadav | 94.68 | [88.5, 99.5] |
| 5 | Romario Shepherd | 93.69 | [86.7, 99.4] |
| 6 | Naman Dhir | 93.30 | [85.8, 99.5] |
| 7 | Phil Salt | 93.01 | [85.4, 99.2] |
| 8 | Jitesh Sharma | 92.79 | [84.8, 99.3] |
| 9 | Nicholas Pooran | 92.58 | [84.3, 99.2] |
| 10 | Jos Buttler | 92.45 | [84.0, 99.3] |

### Top 10 Bowlers Under Pressure

| Rank | Player | Score | 95% CI |
|---|---|---|---|
| 1 | Liam Dawson | 95.39 | [88.9, 100.0] |
| 2 | Haris Rauf | 92.36 | [84.7, 99.0] |
| 3 | Abbas Afridi | 91.88 | [83.8, 98.9] |
| 4 | Nathan Ellis | 91.84 | [83.7, 99.0] |
| 5 | Sufiyan Muqeem | 91.41 | [82.8, 98.9] |
| 6 | Matheesha Pathirana | 91.11 | [82.4, 98.9] |
| 7 | Nasum Ahmed | 90.77 | [81.6, 98.8] |
| 8 | Ishant Sharma | 90.42 | [80.8, 98.6] |
| 9 | Shoriful Islam | 90.36 | [80.6, 98.6] |
| 10 | Tim Southee | 89.16 | [78.5, 97.9] |

### Frozen Asset Checksums

| File | SHA-256 |
|---|---|
| `final_batter_rankings.csv` | `887f0c104047eb7b5c7d662b83600bacaf6263fa7162fc343b27800760b99b87` |
| `final_bowler_rankings.csv` | `344d63c55cecc7bce9de3cd06d82b6ac8217fcd448bb3f2e93d55da314f1e7bb` |
| `PRESSUREIQ_Final_Submission.zip` | `76059a8f5f8b8de5126a5ed8b2a9378fb6664016989f3125df7ca4bbbe9696db` |
| Git baseline | `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2` |

---

## Project Structure

```
SuperRR/
├── streamlit_app.py              # Streamlit Cloud entry point
├── src/
│   ├── dashboard/
│   │   ├── app.py                # Main application
│   │   ├── design_tokens.py      # Design system tokens
│   │   ├── views/                # 13 dashboard views
│   │   ├── components.py         # Shared UI components
│   │   ├── charts.py             # Plotly chart builders
│   │   ├── data_loader.py        # Data loading & caching
│   │   └── styles.py             # CSS injection
│   ├── models/                   # Statistical models
│   └── recruitment/              # RR recruitment logic
├── data/
│   ├── raw/                      # Source ball-by-ball data
│   └── processed/                # Cleaned, pipeline-output data
├── docs/                         # Methodology PDFs, audit reports
├── scripts/                      # ETL, model, and reporting scripts
├── tests/                        # 107-test pytest suite
├── submission_handover/          # Official competition package
├── audit/                        # Version audit trails
├── .streamlit/config.toml        # Streamlit theme configuration
└── requirements.txt              # Python dependencies
```

---

## Quick Start

### Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the dashboard
streamlit run streamlit_app.py

# 3. Run the test suite
python -m pytest tests/ -v
```

### Verify Model A Integrity

```python
import hashlib, pathlib

files = {
    "data/processed/final_batter_rankings.csv": "887f0c104047eb7b5c7d662b83600bacaf6263fa7162fc343b27800760b99b87",
    "data/processed/final_bowler_rankings.csv":  "344d63c55cecc7bce9de3cd06d82b6ac8217fcd448bb3f2e93d55da314f1e7bb",
}
for path, expected in files.items():
    actual = hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
    status = "PASS" if actual == expected else "FAIL"
    print(f"{status}: {path}")
```

---

## Dashboard Navigation

### Round 1 — Pressure Intelligence (Model A)
1. **Official Competition Leaderboards** — Frozen Top 10 rankings with 95% bootstrap CIs
2. **Pressure Analytics & Physics** — BPI, BoPI, PAVA metrics explained
3. **Player Intelligence Profiles** — Individual pressure dossiers and 5-pillar radar
4. **Player Comparison Lab** — Head-to-head multi-player comparison
5. **Player Directory** — 256-candidate visual scouting catalog
6. **Methodology & Model Validation** — Statistical framework and ML validation
7. **Data Sources & Provenance** — Lineage, checksums, change log

### Supplementary — RR Recruitment Intelligence (Model B)
8. **Recruitment Command Centre** — Strategic RR overview
9. **RR Target Batters** — Eligible batting recruits ranked by pressure score
10. **RR Target Bowlers** — Eligible bowling recruits ranked by pressure score
11. **Squad Gap Analysis** — RR roster depth and tactical needs
12. **Alternative Target Finder** — Contingency recommender
13. **Eligibility & Auction Watchlist** — 10 trades, retentions, audit ledger

---

## Deployment (Streamlit Community Cloud)

See [PRESSUREIQ_V7_DEPLOYMENT_GUIDE.md](PRESSUREIQ_V7_DEPLOYMENT_GUIDE.md) for full deployment instructions.

**Quick deploy:**
1. Push `feature/pressureiq-v7-dashboard` branch to GitHub
2. Connect the repository in Streamlit Community Cloud
3. Set Main file: `streamlit_app.py`
4. Deploy — no secrets required for read-only analytics

---

## Test Suite

```
107 tests | 0 failures | 22.46s runtime
pytest tests/ -v
```

Test categories: data integrity, model A checksums, pipeline validation, market intelligence, audit remediation.

---

## Version History

| Version | Date | Description |
|---|---|---|
| V7.0 | 2026-11-17 | Production dashboard upgrade, public deployment, master methodology report |
| V6.6.2 | 2026-11-17 | Final consistency audit, model A discrepancy resolution |
| V6.6.1 | 2026-11-17 | Full franchise accounting reconciliation (10 teams, 275 records) |
| V6.6 | 2026-11-17 | Official IPLT20 retention graphics integration |
| V6.5.1 | 2026-11-17 | Independent acceptance audit |
| V6.5 | 2026-11-17 | Ten-team retention/release audit |
| V6.4 | 2026-11-17 | Model A hash verification, dashboard upgrade |

---

*PRESSUREIQ — Context-Aware Cricket Performance Intelligence*
*Rajasthan Royals SupeRR Selector Season 2 | November 2026*
