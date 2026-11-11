# PRESSUREIQ: Context-Aware Cricket Performance & Reliability Intelligence Framework

PRESSUREIQ is a quantitative cricket analytics intelligence framework designed to identify the 10 most reliable batters and 10 most reliable bowlers under match pressure in T20 cricket, using Indian Premier League (IPL) and Men's T20 International (T20I) ball-by-ball records from 2022 to 2026.

---

## Architecture & Design Principles

1. **Strict Temporal Causality**: Zero future information leakage. Every delivery-level feature reflects the exact match context *before* the ball is bowled.
2. **First-Principles Cricket Rules**: Rigorous legal-ball and extras accounting following official MCC Laws of Cricket (wides/no-balls charged to bowler value and runs conceded, distinct from byes/leg-byes).
3. **Decoupled Match Pressure**: Situational difficulty is quantified continuously in $[0, 100]$: Batting Pressure Index (BPI) and Bowling Pressure Index (BoPI).
4. **Unamplified Value Added (PAVA)**: Expected outcome models condition on match pressure to output pure above-expectation execution surplus ($V_{\text{raw}}$ in runs/ball), eliminating pressure double-counting.
5. **Multi-Pillar Reliability & Empirical Bayes Shrinkage**: Combines absolute pressure execution, baseline retention delta, opportunity-adjusted consistency, and cross-competition adaptability, regularized with Empirical Bayes ($K=45$ pseudo-balls).
6. **2,000 Match-Clustered Bootstrap**: Rigorous uncertainty quantification providing empirical 95% confidence intervals and top-10 inclusion probabilities.

---

## Directory Structure

```
SuperRR/
├── .streamlit/
│   └── config.toml               # Streamlit server and headless configuration
├── src/
│   ├── __init__.py
│   ├── config.py                 # Paths, schemas, and cricket domain constants
│   ├── data/
│   │   ├── cleaner.py            # Dataset cleaning, extras decoding, rule standardization
│   │   ├── state_reconstruction.py # Score reconstruction, legal balls, and chase dynamics
│   │   └── pipeline.py           # End-to-end data transformation to Parquet
│   ├── features/
│   │   ├── feature_builder.py    # Zero-leakage chronological feature engineering
│   │   ├── first_innings_par.py  # Expanding-window chronological par estimation
│   │   └── player_history.py     # Pre-match cumulative rolling player metrics
│   ├── models/
│   │   ├── pressure_index.py     # Calibrated BPI and BoPI (0–100 scale)
│   │   ├── expected_outcomes.py  # Walk-forward chronological out-of-fold LightGBM models
│   │   ├── pressure_value.py     # Unamplified PAVA and leverage equity impact
│   │   └── train_models.py       # Full training and PAVA calculation runner
│   ├── analysis/
│   │   ├── reliability_engine.py # Five-pillar reliability scoring & empirical Bayes
│   │   ├── bootstrap_engine.py   # Vectorized 2,000 match-clustered bootstrap engine
│   │   ├── generate_final_rankings.py # Unified official rankings & validation generator
│   │   ├── validation.py         # Multi-component ablation study suite
│   │   └── extract_case_studies.py # Player case study & radar chart generators
│   └── dashboard/
│       └── app.py                # Interactive Streamlit + Plotly multi-page application
├── scripts/
│   ├── verify_raw_hashes.py      # SHA-256 provenance hash verifier for raw CSV files
│   ├── run_clustered_bootstrap_2000.py # Runner for 2,000-resample bootstrap stability
│   ├── test_streamlit_headless.py # Headless validation of Streamlit dashboard
│   ├── export_submission.py      # Artifact verification and Unstop dropdown exporter
│   ├── audit_full_match_invariants.py # Automated invariants across all 867 matches
│   ├── audit_byes_margins.py     # Bye/leg-bye uncertainty and sensitivity audit
│   └── audit_same_date_matches.py # Chronological ordering and split validator
├── data/
│   └── processed/                # Production Parquet store & final rankings
│       ├── matches.parquet
│       ├── deliveries.parquet
│       ├── features_deliveries.parquet
│       ├── deliveries_with_pava.parquet
│       ├── final_batter_rankings.csv & .parquet
│       ├── final_bowler_rankings.csv & .parquet
│       ├── bootstrap_2000_batters.parquet & .csv
│       ├── bootstrap_2000_bowlers.parquet & .csv
│       └── baseline_v1_backup/   # Immutable baseline reference preserved for audit
├── tests/
│   ├── test_bootstrap_baseline_reproducibility.py # Exact score reproducibility test
│   ├── test_bowler_illegal_deliveries.py          # Wides/no-balls penalization test
│   ├── test_data_cleaning.py                      # Cricket rule & boundary tests
│   ├── test_features.py                           # Par and history non-leakage tests
│   ├── test_oof_predictions.py                    # Walk-forward OOF & categorical tests
│   ├── test_pava_pressure_amplification.py        # Unamplified execution surplus tests
│   ├── test_prc_archetypes.py                     # Pressure response curve fitting tests
│   ├── test_pressure_directionality.py            # Decoupled BPI/BoPI directional tests
│   ├── test_pressure_index.py                     # Index bounds and tier tests
│   ├── test_shortened_innings_dls.py              # DLS dynamic legal-ball tests
│   ├── test_state_reconstruction.py               # Monotonic score reconstruction tests
│   └── test_validation_fixes.py                   # Ablation study integrity tests
├── docs/
│   ├── FINAL_READINESS_REPORT.md # Comprehensive 8-pillar verification audit report
│   ├── UNSTOP_SUBMISSION_GUIDE.md # Fast copy-paste Unstop dropdown guide
│   ├── EXECUTIVE_SUMMARY.md      # Concise 2-page executive brief
│   ├── METHODOLOGY_REPORT.md     # Full mathematical & architectural specification
│   ├── RANKING_STABILITY_REPORT.md # 2,000-bootstrap stability & sensitivity report
│   ├── INDEPENDENT_REAUDIT_REPORT.md # Independent re-audit closure report
│   ├── DECISION_LOG.md           # Engineering & methodological decision records
│   ├── DATA_DICTIONARY.md        # Comprehensive column & feature reference
│   ├── MODEL_BENCHMARK_REPORT.json # Out-of-fold & test evaluation metrics
│   └── VALIDATION_REPORT.json    # Full ablation study outputs & Jaccard metrics
├── requirements.txt              # Pinned Python 3.13 production dependencies
└── README.md
```

---

## Quickstart & Reproduction

### 1. Requirements & Clean Environment Setup
Python 3.13 (or 3.11+) is required. Install all pinned dependencies:
```bash
pip install -r requirements.txt
```

### 2. Raw Data Placement & Verification
The raw competition dataset files must reside at:
`SupeRR Selector Season 2 _ Problem Statement _ Data Pack/SupeRR Selector Season 2 _ Data Pack/`
*(or alternatively in `data/raw/`)*

Verify the cryptographic SHA-256 integrity of all 6 raw CSV files:
```bash
python scripts/verify_raw_hashes.py
```

### 3. Run End-to-End Pipeline
To regenerate all processed datasets from raw CSV files:
```bash
# Step A: Data cleaning & match-state reconstruction
python -m src.data.pipeline

# Step B: Walk-forward OOF models & delivery PAVA calculation
python -m src.models.train_models

# Step C: 2,000 match-clustered bootstrap stability analysis
python scripts/run_clustered_bootstrap_2000.py

# Step D: Final reliability score computation & official ranking generation
python -m src.analysis.generate_final_rankings
```

### 4. Run Automated Test Suite
Execute the complete automated test suite across all 12 modules:
```bash
python -m pytest -v
```

### 5. Launch Interactive Dashboard
Run the interactive Streamlit + Plotly application:
```bash
streamlit run src/dashboard/app.py
```
*(Headless verification: `python scripts/test_streamlit_headless.py`)*
