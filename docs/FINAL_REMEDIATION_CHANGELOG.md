# PRESSUREIQ — Final CodeRabbit Remediation Changelog

**Branch:** `remediation-phase1-audit`  
**Base Commit (Frozen Official Baseline):** `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2` (`master`)  
**Scope:** Two-cycle CodeRabbit CLI review & controlled remediation (`CR-01`..`CR-15` in Cycle 1; `CR2-01`..`CR2-19` in Cycle 2).

---

## 1. Cycle 1 Summary (Commit `ece2cc7` — Remediates `CR-01` through `CR-15`)

### Code & Pipeline Fixes
1. **Dashboard Bowler Economy MCC Parity (`CR-03`, `CR-14`):**
   - `src/dashboard/analytics.py` (`compute_player_phase_summary`): Included all deliveries (`is_legal_ball == 0` wides/no-balls included) in `bowler_runs_conceded` and `is_bowler_wicket` sums while restricting `Legal Balls`, `HP Balls (BoPI>=50)`, `Avg BoPI`, and `Raw PAVA / Ball` to `is_legal_ball == 1`.
   - `src/dashboard/data_loader.py` (`query_season_format_stats`): Removed `d.is_legal_ball = 1` from the DuckDB `WHERE` filter for bowling slices so wide/no-ball runs are counted in `slice_rate_stat` over legal ball denominators.
   - `tests/test_dashboard_data.py`: Added `test_bowler_economy_includes_illegal_delivery_runs` verifying exact Matheesha Pathirana (`8661`) parity (`1,132` legal balls, `1,630` conceded runs, `8.64` career & slice economy).
2. **Market Overwrite Safeguard (`CR-10`):**
   - `scripts/build_market_intelligence.py`: Added CLI flags preventing accidental overwrite of existing `ipl_2027_player_market_template.csv` without `--force`.
3. **Competition Dossier ID & Status Correction (`CR-13`):**
   - `scripts/build_competition_dossier.py`: Corrected all stale player IDs in `strat_b`, `strat_w`, and watchlist (`1699`, `6726`, `5553`, `3916`, `3125`, `7699`, `7920`, `34485`, `8661`, `4658`, `28`, `7344`, `278`, `32862`, `4708`, `7325`), aligned Nathan Ellis (`Confirmed Trade` SRH), Pathirana (KKR), and Buttler (GT), added missing-ID assertions, dynamically pulled dataset counts, and regenerated `final_competition_*_top10.csv`, `player_evidence_dossier.csv`, and `emerging_talent_watchlist.csv`.
4. **Validation Gate & ML Reproduction Fixes (`CR-08`, `CR-09`, `CR-12`, `CR-15`):**
   - `scripts/reproduce_ml_metrics.py`: Replaced `("team_runs_before", "last")` with `("cum_team_runs", "max")` for `bat_won` chase outcomes and evaluated pickled LightGBM models live on `test_df` via `engine.preprocess_features(test_df, fit=False)`.
   - `scripts/hybrid_validation_gate.py`: Fixed `cum_team_runs` chase outcomes, removed hardcoded validation strings (`ALL_NUMBERS_VERIFIED_EXACT_MATCH`, `Violations=0`, literal `raw_test_2026`, `0.0514`), and integrated official `final_*_rankings.csv` comparison alongside clearly labeled single-PAVA proxy sensitivity metrics.

### Documentation & PDF Alignment
- `docs/NOV17_RETENTION_UPDATE_RUNBOOK.md` (`CR-01`)
- `docs/FINAL_SUBMISSION_MANIFEST.md` (`CR-02`)
- `docs/PUBLIC_PLAYER_INTELLIGENCE.md` (`CR-04`)
- `docs/ROUND1_OFFICIAL_SCOPE_VERIFICATION.md`, `docs/NOV13_FINAL_COMPETITION_READINESS.md`, `docs/NOV14_SUBMISSION_HANDOVER.md` (`CR-05`)
- `scripts/generate_methodology_pdf.py` (`CR-06`) & `scripts/generate_final_comprehensive_pdf.py` (regenerated `docs/PRESSUREIQ_METHODOLOGY_REPORT.pdf` [5 pages] and `docs/PRESSUREIQ_FINAL_METHODOLOGY_REPORT.pdf` [14 pages], leaving `PRESSUREIQ_Final_Submission.zip` untouched)
- `docs/FINAL_PLAYER_CLAIMS_VERIFICATION.md` (`CR-07`)
- `docs/CRITICAL_CHALLENGE_REPORT.md` (`CR-11`)
- `docs/FINAL_ML_METRIC_REPRODUCTION.md`, `docs/HYBRID_VALIDATION_REPORT.md`, `docs/RANKING_ROBUSTNESS_COMPARISON.md` (updated to recomputed metrics: 2nd-innings Brier `0.2185` -> `0.1866`, Platt ECE check `0.0894` -> `0.0963`, 147 legal-ball bowlers)

---

## 2. Cycle 2 Summary (Remediates `CR2-01` through `CR2-19`)

1. **`src/dashboard/app.py` (`CR2-01`):** Removed relative `(`6 days away`)` countdown from Market Intelligence deadline warning.
2. **`src/dashboard/analytics.py` & `tests/test_dashboard_data.py` (`CR2-18`):** Decoupled `audit_df.empty` from `candidates_df.empty` in `summarize_rr_squad_intelligence()` and added `test_rr_core_visible_when_candidates_empty`.
3. **`scripts/build_market_intelligence.py` (`CR2-05`):** Restricted `--force` to rebuildable `ipl_2027_player_market_template.csv` only, protecting pinned Nov 11 snapshot and append-only change log unless `--overwrite-history` is explicitly specified.
4. **`scripts/hybrid_validation_gate.py` (`CR2-12`, `CR2-14`):** Added live value-level `np.isclose` checks against freshly recomputed CDPI sweep, win-prob AUCs, and Gaikwad/Rohit step counts before certifying `ALL_NUMBERS_VERIFIED_EXACT_MATCH` (`failed_checks: []`); preserved illegal-delivery `pava_bowl` numerator contributions alongside `is_legal_ball == 1` denominator/ESS parity in hybrid bowling comparison and re-ran gate (`Spearman(ModelA)=0.5699`, `Proxy=0.6220`).
5. **Documentation Alignment (`CR2-02`, `CR2-03`, `CR2-04`, `CR2-06`, `CR2-07`, `CR2-08`, `CR2-09`, `CR2-10`, `CR2-11`, `CR2-13`, `CR2-15`, `CR2-16`, `CR2-17`, `CR2-19`):** Reconciled `docs/NOV15_INDEPENDENT_COMPETITION_REAUDIT.md` (played match counts `367/470/30 = 867` + verified Leaderboard B CSV tables), `docs/EMERGING_TALENT_REVIEW.md` (relative CSV link + canonical player IDs), `docs/FINAL_LIMITATIONS_AND_RESEARCH_INTEGRITY.md` (`K_shrink = 45.0`), `docs/FINAL_ML_METRIC_REPRODUCTION.md` (`33,082` full 2026 split rows), `docs/NOV13_FINAL_COMPETITION_READINESS.md` (Ellis removed from auction targets), `docs/INDEPENDENT_MODEL_CHALLENGE.md` (live `K=90` sensitivity runs + Shepherd OLS `+0.6972` / Extreme-tier collapse `-1.606`), `docs/FINAL_BATTER_RANKING_AUDIT.md` (`6/3/1` role split), `docs/DATA_PROVENANCE_AND_VALIDATION.md` (date + delivery-level Parquet handling), and `docs/TOP_20_PLAYER_EVIDENCE_PROFILES.md` (verified 2026/2027 teams & Pakistani policy benchmark framing).
