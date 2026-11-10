# PRESSUREIQ: Context-Aware Cricket Performance & Reliability Intelligence Framework

PRESSUREIQ is a quantitative cricket analytics system designed to identify the 10 most reliable batters and 10 most reliable bowlers under match pressure in T20 cricket, using IPL and T20 International (T20I) ball-by-ball records from 2022 onwards.

---

## Architecture & Design Principles

1. **Strict Temporal Causality**: Zero future information leakage. Every delivery-level feature reflects the exact match context *before* the ball is bowled.
2. **First-Principles Cricket Rules**: Rigorous legal-ball and extras accounting following official MCC Laws of Cricket (wides/noballs vs byes/legbyes).
3. **High-Performance Parquet & DuckDB Data Pipeline**: Scalable, memory-efficient, CPU-friendly data transformation (~84% compression from raw CSV).
4. **Empirical Validation**: All indices, metrics, and models are validated against out-of-sample chronological splits with confidence intervals.
5. **Reproducibility**: Tested with automated unit tests (`pytest`).

---

## Directory Structure

```
SuperRR/
├── src/
│   ├── config.py                 # Project paths, schemas, and cricket constants
│   ├── data/
│   │   ├── cleaner.py            # Dataset cleaning, extras decoding, rule standardization
│   │   ├── state_reconstruction.py # Cumulative score, legal ball, and chase dynamics
│   │   └── pipeline.py           # End-to-end data processing to Parquet + DuckDB
│   ├── features/                 # Feature engineering & par trajectory models
│   ├── models/                   # Expected outcome models & pressure indices
│   ├── analysis/                 # Reliability ranking, PRC, shrinkage & backtesting
│   └── dashboard/                # Interactive Streamlit + Plotly application
├── data/
│   └── processed/                # Optimized Parquet data store
├── tests/
│   ├── test_data_cleaning.py     # Unit tests for legal balls, extras, wickets
│   └── test_state_reconstruction.py # Unit tests for temporal causality & match state
├── docs/
│   ├── DECISION_LOG.md           # Engineering & methodological decision records
│   ├── DATA_DICTIONARY.md        # Comprehensive column & feature reference
│   └── PROVENANCE.json           # Data transformation lineage & validation statistics
└── README.md
```

---

## Quickstart & Reproduction

### 1. Requirements & Environment
Python 3.11+ / 3.13 with packages:
```bash
pip install pandas numpy polars duckdb scikit-learn lightgbm xgboost catboost shap scipy statsmodels plotly streamlit pytest
```

### 2. Run Data Processing Pipeline
Transforms raw CSV files into typed, indexed Parquet tables:
```bash
python -m src.data.pipeline
```

### 3. Run Unit Tests
```bash
python -m pytest -v
```

