# REQUIREMENTS: PRESSUREIQ — Cricket Reliability Intelligence

## Functional Requirements (FR)

- **FR-01: Data Cleaning & Schema Normalization**
  - Ingest 6 raw CSV files without modifying original source files.
  - Normalize dismissal types, correct typos (`Obstracting` $\to$ `Obstructing`), standardize string booleans in `playing_eleven.csv`.
  - Export typed, compressed Parquet tables queried via DuckDB.

- **FR-02: Cricket Rule Enforcement & State Reconstruction**
  - Reconstruct legal ball counter: `extras_type NOT IN ('wide', 'Overstep', 'other')`.
  - Reconstruct cumulative team score, wickets lost, wickets remaining, balls remaining.
  - Compute 2nd innings chase target (revised target if DLS, else inn1 + 1), runs required, and required run rate (RRR).
  - Fit empirical first-innings par trajectory based on Duckworth-Lewis resource curves.
  - Guarantee that all delivery-level features reflect state *prior* to that ball.

- **FR-03: Pre-Match Historical Player Statistics**
  - Compute rolling career strike rate, batting average, dot %, boundary %, bowling economy, and bowling strike rate.
  - Restrict computations strictly to matches where `match_date < current_match_date` (zero future leakage).
  - Smooth cold starts via Empirical Bayes priors ($m=30$ pseudo-balls).

- **FR-04: Continuous Pressure Indices (BPI & BoPI)**
  - Formulate continuous 0–100 Batting Pressure Index (BPI): scoring demand, resource scarcity, temporal climax, knockout stakes.
  - Formulate continuous 0–100 Bowling Pressure Index (BoPI): target defense urgency, wickets in hand, death overs exposure, close-finish volatility.
  - Output component scores and categorical tiers (`Low`, `Medium`, `High`, `Extreme`).

- **FR-05: Expected Performance ML Models**
  - Train multi-target models on chronological splits: Train ($\le 2024$), Validation ($2025$), Test ($2026$).
  - Predict $E[\text{batter\_runs}]$, $P(\text{dismissal})$, $P(\text{boundary})$, $E[\text{bowler\_runs\_conceded}]$, and $P(\text{bowler\_wicket})$.
  - Benchmark Baseline vs LightGBM vs XGBoost vs CatBoost.
  - Ensure natural probability calibration ($Brier \approx 0.05$ for wickets).

- **FR-06: Pressure-Adjusted Value Added (PAVA)**
  - Calculate actual-minus-expected delivery runs, accounting for phase-aware wicket values (Powerplay: 5.2, Middle: 4.5, Death: 3.6 runs).
  - Scale delivery value continuously by pressure multiplier: $1.0 + \frac{\text{Pressure}}{50.0}$.
  - Aggregate delivery PAVA to innings and spell levels.

- **FR-07: Original Research Contributions**
  - Fit continuous Pressure Response Curves (PRC): $f(\text{Pressure}) \to \text{PAVA/ball}$.
  - Classify player archetypes: `Clutch Climber`, `Ice Cold Anchor`, `Gradual Decliner`, `Pressure Fragile`.
  - Implement Five-Pillar Reliability Decomposition: Absolute Pressure Performance, Retention Delta ($\Delta_{\text{high}} - \Delta_{\text{low}}$), Match Consistency, Context Adaptability, and Shrinkage Weight.

- **FR-08: Empirical Bayes Shrinkage & Final Rankings**
  - Shrink raw pressure PAVA towards empirical league mean ($K=45$ balls) to eliminate small-sample noise.
  - Apply transparent eligibility filters: $\ge 400$ total balls, $\ge 30$ high-pressure balls, $\ge 20$ matches.
  - Output official ordered Top 10 Batters and Top 10 Bowlers.

- **FR-09: Validation, Confidence Intervals & Ablation**
  - Perform match-clustered bootstrap resampling ($N=30$) to derive 95% confidence intervals for reliability scores.
  - Conduct ablation studies comparing full Five-Pillar model against raw strike rate, no-shrinkage, and no-retention variants.

- **FR-10: Interactive Dashboard & Documentation Package**
  - Interactive Streamlit dashboard with Plotly charts.
  - Methodology Report, Data Dictionary, Decision Log, Model Benchmark Report, and Validation Report.

---

## Non-Functional Requirements (NFR)

- **NFR-01: Performance & Runtime**
  - End-to-end data processing and model inference must execute in $<60$ seconds on standard multi-core CPU.
- **NFR-02: Storage & Efficiency**
  - Columnar Parquet compression reducing raw 41MB CSV to $<10$ MB total storage.
- **NFR-03: Test Coverage & Reproducibility**
  - Automated Pytest suite covering cricket rules, temporal causality, par models, and pressure calibration.
- **NFR-04: Data Integrity & Zero Leakage**
  - Raw CSV files must remain strictly unmodified. No post-match or future-ball leakage into predictors.
- **NFR-05: Code Quality & Provenance**
  - Clean modular package architecture under `src/`, with atomic Git commits per phase.
