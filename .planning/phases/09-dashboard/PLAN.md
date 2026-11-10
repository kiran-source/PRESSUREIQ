# PHASE 09: Streamlit Dashboard Plan

## Goal
Build an interactive Streamlit + Plotly application to visualize leaderboards, player profiles, Pressure Response Curves, and validation analytics.

## Tasks
1. Navigation & Layout (`src/dashboard/app.py`):
   - Sidebar for role, format, and threshold filters.
   - Tabs: Leaderboard, Player Dossier, PRC Analysis, Methodology, Provenance.
2. Visualizations:
   - Interactive Plotly tables for Top 10 Batters and Bowlers.
   - Five-Pillar radar charts comparing players to league average.
   - Scatter plots of BPI/BoPI vs PAVA/ball with archetype regression slopes.
   - Model benchmark and ablation metric tables.
3. Local verification:
   - Verify all modules import cleanly and run without runtime exceptions.

## Acceptance Criteria
- Dashboard runs cleanly and renders empirical data interactively.
