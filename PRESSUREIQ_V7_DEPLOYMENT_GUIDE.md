# PRESSUREIQ V7.0 — Deployment Guide

**Streamlit Community Cloud Public Deployment**

---

## Prerequisites

- Python 3.10+ (tested on 3.13)
- GitHub repository with `streamlit_app.py` at root
- Streamlit Community Cloud account (free tier supports public apps)

---

## 1. Prepare the Repository

### Branch strategy

The production deployment uses the `feature/pressureiq-v7-dashboard` branch until merge to `main`:

```bash
git checkout feature/pressureiq-v7-dashboard
git push origin feature/pressureiq-v7-dashboard
```

### Verify `streamlit_app.py` exists at root

```bash
ls streamlit_app.py    # Must exist
```

### Verify `requirements.txt` is clean

The file must contain only pip-installable packages — no local Windows paths:

```
pandas==2.3.3
numpy==2.2.2
scipy==1.16.3
scikit-learn==1.8.0
lightgbm==4.7.0
xgboost==3.2.0
catboost==1.2.10
duckdb==2.0.0
plotly==6.6.0
streamlit==1.56.0
pyarrow==23.0.1
pytest==9.1.1
pymupdf==2.1
```

> **Note:** `reportlab` and `matplotlib` are needed only for PDF generation (run locally). Remove them from `requirements.txt` if Streamlit Cloud build times are slow.

---

## 2. Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **New app**
3. Connect your GitHub repository
4. Set:
   - **Repository:** `<your-org>/SuperRR`
   - **Branch:** `feature/pressureiq-v7-dashboard` (or `main` after merge)
   - **Main file path:** `streamlit_app.py`
5. Click **Deploy**

No secrets are required — the dashboard uses only local CSV files included in the repository.

---

## 3. Streamlit Configuration

The `.streamlit/config.toml` is pre-configured for production:

```toml
[theme]
base = "light"
primaryColor = "#BD6548"
backgroundColor = "#F8F4EC"
secondaryBackgroundColor = "#F1E9DD"
textColor = "#282321"
font = "sans serif"

[browser]
gatherUsageStats = false

[server]
headless = true
enableCORS = false
enableXsrfProtection = false
port = 8502
```

---

## 4. Local Production Test

Before deploying, run a local production simulation:

```bash
# Install all requirements
pip install -r requirements.txt

# Run with production settings
streamlit run streamlit_app.py --server.headless true --server.port 8502

# In another terminal: verify 107/107 tests pass
python -m pytest tests/ -q
```

---

## 5. Data & File Dependencies

All required data files are committed to the repository under `data/processed/`. No external database connections are needed.

### Critical frozen files (do NOT regenerate):
- `data/processed/final_batter_rankings.csv`
- `data/processed/final_bowler_rankings.csv`
- `data/processed/final_competition_batter_top10.csv`
- `data/processed/final_competition_bowler_top10.csv`
- `submission_handover/01_Unstop_Submission_Files/PRESSUREIQ_Final_Submission.zip`

---

## 6. Post-Deployment Verification

After deployment, verify:

1. **Dashboard loads** — no import errors in Streamlit Cloud logs
2. **Model A integrity banner** shows green (checksums match)
3. **Official Competition Leaderboards** page shows Ruturaj Gaikwad #1 (97.71) and Liam Dawson #1 (95.39)
4. **107 tests** pass in local environment (not run on Streamlit Cloud)

---

## 7. Troubleshooting

| Issue | Solution |
|---|---|
| `ModuleNotFoundError: src` | Ensure `streamlit_app.py` at root correctly sets `sys.path` |
| Slow cold start | Streamlit caches data after first load — normal for large CSVs |
| Missing player images | Run `python scripts/download_player_images.py` locally to populate `data/player_images/` |
| Theme not applying | Ensure `.streamlit/config.toml` is committed to the repository |
| `catboost` install fails | Pin to `catboost==1.2.10` or remove from `requirements.txt` if unused at runtime |

---

*PRESSUREIQ V7.0 — Deployment Guide*
*Rajasthan Royals SupeRR Selector Season 2 | November 2026*
