# PROJECT: PRESSUREIQ — Context-Aware Cricket Reliability Intelligence

## 1. Overview & Objective
PRESSUREIQ is a quantitative cricket analytics framework designed for the **SupeRR Selector Season 2** competition. Using ball-by-ball delivery records from the Indian Premier League (IPL) and Men's T20 Internationals (T20I) from 2022 onwards (200,999 deliveries across 867 matches), the system identifies and ranks the **10 most reliable batters** and **10 most reliable bowlers** under match pressure.

### Submission Targets
1. **Top 10 Batters Under Pressure**: Ordered 1 to 10 for Unstop selection.
2. **Top 10 Bowlers Under Pressure**: Ordered 1 to 10 for Unstop selection.
3. **Methodology Report**: Complete academic/scouting report documenting pressure definitions, expected outcome models, fair comparisons, ranking evidence, confidence intervals, and limitations.

---

## 2. Core Architectural & Methodological Principles

1. **Strict Temporal Causality (Zero Future Leakage)**:
   - A delivery's pressure and context must reflect the exact match situation *before* the ball is bowled.
   - Historical player statistics for match $M$ must only use matches played *prior* to match $M$ (`match_date < current_match_date`).
   - Post-match fields (`win_team_id`, `result`, `man_of_the_match`) and end-of-innings totals are strictly barred from delivery-level features.
2. **First-Principles Cricket Rules (MCC Laws)**:
   - Wides and no-balls do not count as legal balls (`is_legal_ball = False`).
   - Wides and no-balls charge extra runs to the bowler (`bowler_runs_conceded = bat_runs + bowler_extras`).
   - Byes and leg-byes are legal balls but do NOT charge runs to the bowler.
   - Bowler dismissals strictly include Caught, Bowled, LBW, Stumped, and Hit Wicket (Run Outs and Retire Outs are team dismissals).
3. **Pressure as Contextual Difficulty (Not Player Outcome)**:
   - Pressure is an external environmental state variable (0–100 scale), completely independent of whether the player scores a six or gets out on that delivery.
4. **Natural Probability Calibration**:
   - Classifiers predicting rare events ($P(\text{wicket}) \approx 5.4\%$, $P(\text{boundary}) \approx 18\%$) must preserve natural prior calibration ($Brier \approx 0.05$). No uncalibrated balanced class weighting in value equations.
5. **Empirical Bayes Shrinkage**:
   - Small sample sizes in extreme pressure are regressed towards empirical league priors to prevent 10-ball flukes from dominating leaderboards.
6. **CPU-First & Storage-Efficient**:
   - Columnar Parquet + DuckDB analytical views. No heavy deep learning dependencies or distributed clusters.

---

## 3. Technology Stack

- **Runtime**: Python 3.13.5 (x86_64, Windows)
- **Data Engineering**: Pandas 2.3.3, Polars 2.1.0, DuckDB 2.0.0, PyArrow (Parquet)
- **Modeling & ML**: scikit-learn 1.8.0, LightGBM 4.7.0, XGBoost 3.2.0, CatBoost 1.2.10, SHAP 0.54.1
- **Mathematics & Statistics**: SciPy 1.16.3, Statsmodels 0.15.0
- **Interactive Visualization**: Plotly 6.6.0, Streamlit 1.56.0
- **Testing & Verification**: Pytest 9.1.1
- **VCS**: Git

---

## 4. Known Data Limitations & Mitigations

1. **Leg-bye / Bye Run Count Omission**:
   - *Limitation*: The raw dataset records `runs = 0` for all byes and leg-byes. Actual runs scored (1–4) are omitted from the data.
   - *Mitigation*: Zero impact on batter performance or bowler runs conceded. For team score accumulation, each event is credited with `max(1, extras_2_runs)`, with an acknowledged $\pm 3\text{--}5$ run variance per innings.
2. **Bowl Speed Sensor Noise**:
   - *Limitation*: 38.7% zeros and sensor outliers up to 1,456 km/h.
   - *Mitigation*: Cleaned by clipping outside 50–165 km/h to NaN. Excluded from primary predictive models.
3. **Shortened Matches (DLS)**:
   - *Limitation*: 34 matches have revised parameters; `second_inn_revised_overs` is stored in **balls**, not overs.
   - *Mitigation*: Directly cast as legal balls without 6x multiplier.

