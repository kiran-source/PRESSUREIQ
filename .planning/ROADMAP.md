# ROADMAP: PRESSUREIQ — Context-Aware Cricket Reliability Intelligence

This roadmap outlines the milestones, phases, atomic tasks, dependencies, acceptance criteria, and verification commands for the PRESSUREIQ framework.

---

## Milestone 1: Data Foundation & Integrity (Phases 00 – 01)
*Goal: Ensure raw data immutability, discover schema anomalies, and build reproducible cleaning and state-reconstruction pipelines.*

### Phase 00: Project Discovery & Data Inventory
- **Goal**: Audit raw CSV files, discover column schemas, data types, missing rates, and data constraints without modifying raw files.
- **Tasks**:
  - `T00.1`: Inspect all 6 competition CSV files in `SupeRR Selector Season 2 _ Data Pack/`.
  - `T00.2`: Profile data quality (missing values, typos, sensor noise, zero counts, revised overs units).
  - `T00.3`: Produce data inventory report and confirm zero data fabrication.
- **Dependencies**: None.
- **Acceptance Criteria**:
  - `docs/DATA_INVENTORY_AND_FEASIBILITY.md` generated.
  - Raw CSV files hash-verified and untouched.
- **Verification Command**:
  ```bash
  python -c "import pandas as pd; print(pd.read_csv('SupeRR Selector Season 2 _ Data Pack/deliveries.csv', nrows=5).shape)"
  ```

### Phase 01: Data Engineering & State Reconstruction
- **Goal**: Clean raw tables, standardize player/match IDs, implement legal-ball accounting, and reconstruct progressive match state.
- **Tasks**:
  - `T01.1`: Build `src/data/cleaner.py` for text normalization, boolean casting, and typo corrections.
  - `T01.2`: Build `src/data/state_reconstruction.py` implementing MCC Laws for legal deliveries, extra runs, and cumulative score state.
  - `T01.3`: Build `src/data/pipeline.py` to produce optimized columnar Parquet tables queried via DuckDB.
  - `T01.4`: Implement unit tests for legal delivery and scoring accounting.
- **Dependencies**: Phase 00.
- **Acceptance Criteria**:
  - `data/processed/deliveries.parquet` (200,999 rows) and `matches.parquet` (883 rows) created.
  - Zero raw files modified.
  - All unit tests pass.
- **Verification Command**:
  ```bash
  python -m pytest tests/test_data_cleaning.py tests/test_state_reconstruction.py -v
  ```

---

## Milestone 2: Feature Engineering & Pressure Quantification (Phases 02 – 03)
*Goal: Derive causal, leakage-free delivery features and formulate continuous 0–100 pressure indices.*

### Phase 02: Match State & Temporal Features
- **Goal**: Engineer delivery-level features strictly from information available *before* the delivery is bowled.
- **Tasks**:
  - `T02.1`: Implement Duckworth-Lewis empirical par resource curve in `src/features/first_innings_par.py` for 1st innings par estimation.
  - `T02.2`: Implement expanding-window career statistics with Empirical Bayes shrinkage in `src/features/player_history.py` (strictly prior matches: `match_date < current_match_date`).
  - `T02.3`: Assemble `src/features/feature_builder.py` generating 93 delivery features in `data/processed/features_deliveries.parquet`.
  - `T02.4`: Implement unit tests verifying zero future leakage and resource curve calibration.
- **Dependencies**: Phase 01.
- **Acceptance Criteria**:
  - 200,961 non-super-over deliveries processed.
  - No post-match attributes present in delivery feature matrix.
- **Verification Command**:
  ```bash
  python -m pytest tests/test_features.py -v
  ```

### Phase 03: Pressure Indices (BPI & BoPI)
- **Goal**: Develop continuous 0–100 Batting Pressure Index and Bowling Pressure Index reflecting contextual difficulty.
- **Tasks**:
  - `T03.1`: Formulate 4-component continuous BPI in `src/models/pressure_index.py` (Rate Demand, Resource Scarcity, Climax, Match Leverage).
  - `T03.2`: Formulate 4-component continuous BoPI in `src/models/pressure_index.py` (Target Defense Urgency, Wickets Remaining, Death Climax, Close Finish Leverage).
  - `T03.3`: Calibrate and normalize indices separately for IPL and T20I, assigning tiers (`Low`, `Medium`, `High`, `Extreme`).
  - `T03.4`: Implement unit tests verifying index bounds $[0, 100]$ and monotonic behavior under rising pressure.
- **Dependencies**: Phase 02.
- **Acceptance Criteria**:
  - Delivery-level BPI and BoPI scores generated with median ~45, 90th percentile ~75.
  - Unit tests verify boundary adherence.
- **Verification Command**:
  ```bash
  python -m pytest tests/test_pressure_index.py -v
  ```

---

## Milestone 3: Expected Outcome Models & Value Attribution (Phases 04 – 05)
*Goal: Train chronological ML models to establish baseline expectations and attribute pressure-adjusted value.*

### Phase 04: Expected Performance Models
- **Goal**: Train multi-target ML models predicting delivery outcomes using chronological backtesting splits.
- **Tasks**:
  - `T04.1`: Define chronological splits in `src/models/train_models.py` (Train $\le 2024$, Val $2025$, Test $2026$).
  - `T04.2`: Train Baseline, LightGBM, XGBoost, and CatBoost models for batting runs, dismissal, and boundary.
  - `T04.3`: Train models for bowling runs conceded and bowler wicket probability.
  - `T04.4`: Validate natural probability calibration (avoid uncalibrated class weighting; Brier score $\le 0.06$).
- **Dependencies**: Phase 03.
- **Acceptance Criteria**:
  - `docs/MODEL_BENCHMARK_REPORT.json` generated.
  - LightGBM achieves superior calibration and MAE on out-of-sample test splits.
- **Verification Command**:
  ```bash
  python -c "import json; r = json.load(open('docs/MODEL_BENCHMARK_REPORT.json')); print(r['batting_runs']['test_rmse'])"
  ```

### Phase 05: Pressure-Adjusted Value Added (PAVA)
- **Goal**: Compute delivery-level and aggregated value added adjusted for pressure.
- **Tasks**:
  - `T05.1`: Implement delivery-level actual-minus-expected value in `src/models/pressure_value.py` with phase-aware wicket baselines.
  - `T05.2`: Apply continuous pressure multiplier $1.0 + \frac{\text{Pressure}}{50.0}$.
  - `T05.3`: Aggregate delivery PAVA to player-innings and player-spells in `data/processed/batter_innings_pava.parquet` and `bowler_spell_pava.parquet`.
- **Dependencies**: Phase 04.
- **Acceptance Criteria**:
  - `data/processed/deliveries_with_pava.parquet` created (200,961 deliveries).
  - Delivery, innings, and spell PAVA tables generated.
- **Verification Command**:
  ```bash
  python -c "import pandas as pd; df = pd.read_parquet('data/processed/deliveries_with_pava.parquet'); print(df[['bpi', 'pava_runs_bat', 'pava_runs_bowl']].describe())"
  ```

---

## Milestone 4: Reliability Intelligence & Validation (Phases 06 – 08)
*Goal: Implement research contributions, empirical Bayes shrinkage, official rankings, and validation.*

### Phase 06: Original Research Contributions
- **Goal**: Implement Pressure Response Curves (PRC), Archetype Classification, and Five-Pillar Reliability Decomposition.
- **Tasks**:
  - `T06.1`: Implement smooth PRC modeling estimating $f(\text{Pressure}) \to \text{PAVA/ball}$ in `src/analysis/reliability_engine.py`.
  - `T06.2`: Classify player archetypes (`Clutch Climber`, `Ice Cold Anchor`, `Gradual Decliner`, `Pressure Fragile`).
  - `T06.3`: Compute Five Pillars: Absolute Pressure PAVA, Retention Delta ($\Delta_{\text{high}} - \Delta_{\text{low}}$), Match Consistency, Context Adaptability, and Sample Weight.
- **Dependencies**: Phase 05.
- **Acceptance Criteria**:
  - PRC slopes and archetypes assigned to all qualified players.
  - Five pillars normalized on 0–100 scale.
- **Verification Command**:
  ```bash
  python -c "import pandas as pd; df = pd.read_parquet('data/processed/final_batter_rankings.parquet'); print(df['prc_archetype'].value_counts())"
  ```

### Phase 07: Player Reliability Rankings
- **Goal**: Apply Empirical Bayes shrinkage ($K=45$ balls) and transparent eligibility filters to produce final official rankings.
- **Tasks**:
  - `T07.1`: Apply Empirical Bayes shrinkage to regression parameters in `src/analysis/reliability_engine.py`.
  - `T07.2`: Enforce eligibility filters ($\ge 400$ total balls, $\ge 30$ high-pressure balls, $\ge 20$ matches).
  - `T07.3`: Generate `final_batter_rankings.csv` and `final_bowler_rankings.csv`.
- **Dependencies**: Phase 06.
- **Acceptance Criteria**:
  - 58 eligible batters and 72 eligible bowlers ranked.
  - Official Top 10 Batters and Top 10 Bowlers identified.
- **Verification Command**:
  ```bash
  python -c "import pandas as pd; print(pd.read_csv('data/processed/final_batter_rankings.csv')[['rank', 'player_name', 'reliability_score']].head(10))"
  ```

### Phase 08: Validation & Bootstrap Uncertainty
- **Goal**: Compute match-clustered bootstrap confidence intervals ($N=30$) and run ablation studies.
- **Tasks**:
  - `T08.1`: Implement match-clustered bootstrap resampling in `src/analysis/validation.py` to compute 95% CIs.
  - `T08.2`: Run ablation studies (Full Model vs Raw SR vs No Shrinkage vs No Retention) and save `docs/VALIDATION_REPORT.json`.
- **Dependencies**: Phase 07.
- **Acceptance Criteria**:
  - 95% CIs populated in final rankings tables.
  - Ablation confirms raw SR has only 10% overlap with pressure reliability.
- **Verification Command**:
  ```bash
  python -c "import json; r = json.load(open('docs/VALIDATION_REPORT.json')); print(r['top10_overlap_with_raw_sr'])"
  ```

---

## Milestone 5: UI & Final Submission Package (Phases 09 – 10)
*Goal: Deploy interactive dashboard and complete all formal documentation and submission assets.*

### Phase 09: Streamlit Dashboard
- **Goal**: Develop interactive dashboard featuring leaderboards, PRC curves, 5-pillar radar charts, and methodology.
- **Tasks**:
  - `T09.1`: Build `src/dashboard/app.py` with multi-page navigation (Leaderboard, Player Dossier, PRC Analysis, Methodology, Provenance).
  - `T09.2`: Add interactive Plotly radar charts, scatter plots, and distribution histograms.
  - `T09.3`: Test dashboard launch locally.
- **Dependencies**: Phase 08.
- **Acceptance Criteria**:
  - Dashboard launches without syntax errors and renders data accurately.
- **Verification Command**:
  ```bash
  python -c "import src.dashboard.app as app; print('Dashboard module imported successfully')"
  ```

### Phase 10: Deliverables & Submission Package
- **Goal**: Finalize Methodology Report, Player Decision Dossiers, Data Dictionary, Decision Log, export scripts, and Git repository.
- **Tasks**:
  - `T10.1`: Complete `docs/METHODOLOGY_REPORT.md` and `docs/PLAYER_DECISION_DOSSIERS.md`.
  - `T10.2`: Generate `docs/ROLE_AND_FORMAT_BREAKDOWNS.md`.
  - `T10.3`: Build `scripts/export_submission.py` to verify all assets and print the official Unstop dropdown list.
  - `T10.4`: Run complete automated test suite and record clean passing status.
  - `T10.5`: Commit all changes cleanly to Git.
- **Dependencies**: Phase 09.
- **Acceptance Criteria**:
  - All test cases pass ($100\%$).
  - Official Top 10 Batters and Bowlers validated and documented.
- **Verification Command**:
  ```bash
  python -m pytest -v
  ```

---

## Milestone 6: Phase 2 Clean-Room Verification & Jury-Grade Dashboard (Phase 11)
*Goal: Execute isolated clean-room verification and build the modular 10-view PRESSUREIQ Streamlit dashboard with strict market-status safeguards.*

### Phase 11: Clean-Room Audit, Modular Dashboard & Jury Handover
- **Goal**: Complete Phase A verification, modularize `src/dashboard/` (`data_loader.py`, `analytics.py`, `charts.py`, `app.py`), run Playwright visual QA across all 10 pages, and deliver Phase D documentation.
- **Dependencies**: Milestone 5 & Phase 1 Market Audit.
- **Acceptance Criteria**:
  - `docs/PHASE2_INDEPENDENT_VERIFICATION.md` and `data/processed/phase2_verification_manifest.json` recorded.
  - All 10 views operational with DuckDB/Plotly/Pandas and unit-tested in `tests/test_dashboard_data.py`.
  - Zero frozen baseline mutations.


