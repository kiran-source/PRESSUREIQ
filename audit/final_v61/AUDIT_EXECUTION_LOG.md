# AUDIT EXECUTION LOG & VERBATIM TERMINAL RECORDS
## Chronological Record of Commands, Hashes, Test Passes, and Reproductions

**Audit Protocol:** PRESSUREIQ V6.1 Independent Certification  
**Audit Directory:** `audit/final_v61/`  
**Timestamp:** 2026-11-14T21:49:00+05:30  
**Operating System:** Windows (Python 3.13.5, pytest-9.1.1, git 2.45+)  

---

### 1. Git Repository & Working Tree Audit

```powershell
PS C:\Users\kiran\OneDrive\Documents\Desktop\SuperRR> git rev-parse HEAD; git branch -v; git status
ff0a25bf838e18b906a11bae660cf0eac8d34165
  backup-editorial-v4      d8fbd2d fix(dashboard): cast benchmark metrics to strings to prevent PyArrow conversion failures
  dashboard-ui-v3          d98d1af docs: finalize v3 documentation before editorial redesign
  master                   fc0e622 [behind 34] docs: finalize readiness report with exact lineage c313057, 468 files, 13.54s test evidence, and pyarrow/duckdb boundary notes
* redesign-editorial-v4    ff0a25b fix(dashboard): ensure repo root is prepended to sys.path in app.py to resolve ModuleNotFoundError
  remediation-phase1-audit 82e77b2 Phase 4 review: address CodeRabbit minor findings (PRC guards and dynamic URL verification scope)
On branch redesign-editorial-v4
Your branch is up to date with 'origin/redesign-editorial-v4'.

nothing to commit, working tree clean
```

---

### 2. Cryptographic Baseline Hashes Verification

```powershell
PS C:\Users\kiran\OneDrive\Documents\Desktop\SuperRR> python -c "import hashlib
def h(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
print('Batters:', h('data/processed/final_batter_rankings.csv'))
print('Bowlers:', h('data/processed/final_bowler_rankings.csv'))
print('Archive:', h('PRESSUREIQ_Final_Submission.zip'))"

Batters: 887f0c104047eb7b5c7d662b83600bacaf6263fa7162fc343b27800760b99b87
Bowlers: 344d63c55cecc7bce9de3cd06d82b6ac8217fcd448bb3f2e93d55da314f1e7bb
Archive: 76059a8f5f8b8de5126a5ed8b2a9378fb6664016989f3125df7ca4bbbe9696db
```

---

### 3. Chronological Machine Learning Model Reproduction

```powershell
PS C:\Users\kiran\OneDrive\Documents\Desktop\SuperRR> python -c "from pathlib import Path; from src.recruitment.ml_pipeline import load_and_prepare_ml_datasets, RecruitmentPredictiveEngine
matches, bat_inn, bowl_spell, deliv = load_and_prepare_ml_datasets(Path('.'))
engine = RecruitmentPredictiveEngine(Path('.'))
b_res = engine.train_and_evaluate_batting_models(bat_inn)
print('BATTING RESULT:', b_res)
print('BATTING FEATURE IMPORTANCE:', engine.feature_importances.get('batter_expected_runs'))
bw_res = engine.train_and_evaluate_bowling_models(bowl_spell)
print('BOWLING RESULT:', bw_res)
print('BOWLING FEATURE IMPORTANCE:', engine.feature_importances.get('bowler_runs_conceded'))"

BATTING RESULT: {
  'baseline_mae': 17.227, 
  'baseline_rmse': 23.273, 
  'lgb_mae': 5.835, 
  'lgb_rmse': 9.145, 
  'lgb_r2': 0.845, 
  'mae_improvement_pct': 66.13, 
  'rmse_improvement_pct': 60.7, 
  'test_samples': 2252
}
BATTING FEATURE IMPORTANCE: {'balls_faced': 0.5036, 'avg_bpi': 0.42, 'high_pressure_balls': 0.0329, 'hp_ratio': 0.0436}

BOWLING RESULT: {
  'baseline_mae': 10.227, 
  'baseline_rmse': 12.708, 
  'lgb_mae': 7.429, 
  'lgb_rmse': 9.67, 
  'lgb_r2': 0.394, 
  'mae_improvement_pct': 27.36, 
  'rmse_improvement_pct': 23.9, 
  'test_samples': 1656
}
BOWLING FEATURE IMPORTANCE: {'legal_balls': 0.2376, 'avg_bopi': 0.57, 'high_pressure_balls': 0.1224, 'hp_ratio': 0.07}
```

---

### 4. Full Automated Test Suite Execution (102 Tests)

```powershell
PS C:\Users\kiran\OneDrive\Documents\Desktop\SuperRR> python -m pytest tests/ -v
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\kiran\OneDrive\Documents\Desktop\SuperRR
configfile: pytest.ini
plugins: anyio-4.10.0, asyncio-1.4.0
collected 102 items

tests/test_audit_remediation.py::test_batter_dot_ball_accounting_excludes_wides PASSED [  0%]
tests/test_audit_remediation.py::test_bowler_dot_ball_accounting_isolated_to_legal_balls PASSED [  1%]
tests/test_audit_remediation.py::test_market_template_all_players_match_canonical_ids PASSED [  2%]
tests/test_audit_remediation.py::test_nathan_ellis_trade_and_contracted_status PASSED [  3%]
tests/test_audit_remediation.py::test_mcda_single_availability_weighting PASSED [  4%]
tests/test_audit_remediation.py::test_canonical_mathematical_parameters PASSED [  5%]
tests/test_bootstrap_baseline_reproducibility.py::test_bootstrap_baseline_reproduces_batting_scores PASSED [  6%]
tests/test_bootstrap_baseline_reproducibility.py::test_bootstrap_baseline_reproduces_bowling_scores PASSED [  7%]
tests/test_bowler_illegal_deliveries.py::test_illegal_deliveries_worsen_economy_and_pava_without_increasing_legal_balls PASSED [  8%]
tests/test_dashboard_data.py::test_dashboard_bundle_loads_and_preserves_frozen_hashes PASSED [  9%]
tests/test_dashboard_data.py::test_effective_sample_distinguished_from_raw_opportunities PASSED [ 10%]
tests/test_dashboard_data.py::test_filters_preserve_official_rank_without_mutation PASSED [ 11%]
tests/test_dashboard_data.py::test_duckdb_season_slice_and_unestablished_queries PASSED [ 12%]
tests/test_dashboard_data.py::test_market_safeguards_and_nov5_trade_counterparties PASSED [ 13%]
tests/test_dashboard_data.py::test_missing_file_and_edge_case_resilience PASSED [ 14%]
tests/test_dashboard_data.py::test_charts_and_player_intelligence_render_cleanly PASSED [ 15%]
tests/test_dashboard_data.py::test_bowler_economy_includes_illegal_delivery_runs PASSED [ 16%]
tests/test_dashboard_data.py::test_rr_core_visible_when_candidates_empty PASSED [ 17%]
tests/test_dashboard_data.py::test_v3_teams_comparison_pressure_analytics_and_charts PASSED [ 18%]
tests/test_dashboard_data.py::test_coderabbit_findings_remediation PASSED [ 19%]
tests/test_data_cleaning.py::test_legal_ball_classification PASSED       [ 20%]
tests/test_data_cleaning.py::test_bowler_runs_conceded_rules PASSED      [ 21%]
tests/test_data_cleaning.py::test_wicket_attribution PASSED              [ 22%]
tests/test_data_cleaning.py::test_dismissal_type_normalization PASSED    [ 23%]
tests/test_experimental_pressure.py::test_sigmoid_numerical_stability PASSED [ 24%]
tests/test_experimental_pressure.py::test_win_probability_leverage_bounds PASSED [ 25%]
tests/test_experimental_pressure.py::test_blowout_suppression_in_cdpi PASSED [ 26%]
tests/test_experimental_pressure.py::test_chase_monotonicity_in_cdpi_batting PASSED [ 27%]
tests/test_features.py::test_first_innings_par_model PASSED              [ 28%]
tests/test_features.py::test_par_no_same_match_leakage PASSED            [ 29%]
tests/test_features.py::test_par_no_future_match_leakage PASSED          [ 30%]
tests/test_features.py::test_player_history_zero_future_leakage PASSED   [ 31%]
tests/test_final_competition_deliverables.py::test_final_top10_csvs PASSED [ 32%]
tests/test_final_competition_deliverables.py::test_player_evidence_dossier PASSED [ 33%]
tests/test_final_competition_deliverables.py::test_emerging_talent_watchlist PASSED [ 34%]
tests/test_final_competition_deliverables.py::test_final_methodology_pdf PASSED [ 35%]
tests/test_final_competition_deliverables.py::test_frozen_baseline_integrity PASSED [ 36%]
tests/test_hybrid_validation.py::test_sigmoid_monotonicity_and_bounds PASSED [ 37%]
tests/test_hybrid_validation.py::test_smooth_blowout_continuity_and_suppression PASSED [ 38%]
tests/test_hybrid_validation.py::test_analytical_dls_prior_bounds PASSED [ 39%]
tests/test_hybrid_validation.py::test_kish_effective_sample_size_formula PASSED [ 40%]
tests/test_hybrid_validation.py::test_validation_gate_main_succeeds_on_valid_data PASSED [ 41%]
tests/test_hybrid_validation.py::test_validation_gate_missing_weighting_csv_returns_nonzero PASSED [ 42%]
tests/test_hybrid_validation.py::test_validation_gate_mismatched_values_return_nonzero PASSED [ 43%]
tests/test_oof_predictions.py::test_expected_calibration_error PASSED    [ 44%]
tests/test_oof_predictions.py::test_oof_predictions_chronology_and_provenance PASSED [ 45%]
tests/test_oof_predictions.py::test_future_category_isolation_and_completeness PASSED [ 46%]
tests/test_pava_pressure_amplification.py::test_positive_and_negative_outcomes_across_pressure_tiers PASSED [ 47%]
tests/test_pava_pressure_amplification.py::test_baseline_retention_invariance PASSED [ 48%]
tests/test_pava_pressure_amplification.py::test_symmetric_execution_surplus PASSED [ 49%]
tests/test_player_market_intelligence.py::test_market_template_schema_and_strict_statuses PASSED [ 50%]
tests/test_player_market_intelligence.py::test_pending_and_unverified_records_cannot_be_confirmed_available PASSED [ 50%]
tests/test_player_market_intelligence.py::test_verified_player_franchises_and_mechanisms PASSED [ 51%]
tests/test_player_market_intelligence.py::test_historical_snapshots_preserved_without_overwrite PASSED [ 52%]
tests/test_player_market_intelligence.py::test_market_change_log_structure PASSED [ 53%]
tests/test_player_market_intelligence.py::test_duplicate_detection_rejects_invalid_csv PASSED [ 54%]
tests/test_player_market_intelligence.py::test_invalid_status_rejects_import PASSED [ 55%]
tests/test_player_market_intelligence.py::test_non_interference_rumours_do_not_change_model_a PASSED [ 56%]
tests/test_player_market_intelligence.py::test_frozen_baseline_artifacts_unmodified PASSED [ 57%]
tests/test_player_visual_intelligence.py::test_player_image_manifest_exists_and_complete PASSED [ 58%]
tests/test_player_visual_intelligence.py::test_get_player_image_path PASSED [ 59%]
tests/test_player_visual_intelligence.py::test_get_player_image_b64 PASSED [ 60%]
tests/test_player_visual_intelligence.py::test_unified_directory_builder PASSED [ 61%]
tests/test_prc_archetypes.py::test_prc_clutch_climber PASSED             [ 62%]
tests/test_prc_archetypes.py::test_prc_gradual_decliner PASSED           [ 63%]
tests/test_prc_archetypes.py::test_prc_ice_cold_anchor PASSED            [ 64%]
tests/test_prc_archetypes.py::test_prc_extreme_collapse_fragile PASSED   [ 65%]
tests/test_prc_archetypes.py::test_prc_insufficient_evidence PASSED      [ 66%]
tests/test_pressure_directionality.py::test_bpi_monotonic_with_rrr PASSED [ 67%]
tests/test_pressure_directionality.py::test_bpi_monotonic_with_wickets_lost PASSED [ 68%]
tests/test_pressure_directionality.py::test_bpi_monotonic_with_balls_remaining PASSED [ 69%]
tests/test_pressure_directionality.py::test_bopi_monotonic_with_opposition_wickets_in_hand PASSED [ 70%]
tests/test_pressure_directionality.py::test_bopi_monotonic_with_chase_comfort PASSED [ 71%]
tests/test_pressure_directionality.py::test_first_innings_par_pressure_symmetry PASSED [ 72%]
tests/test_pressure_index.py::test_bpi_monotonicity_and_bounds PASSED    [ 73%]
tests/test_pressure_index.py::test_bopi_monotonicity_and_bounds PASSED   [ 74%]
tests/test_rr_recommendation_system.py::test_files_exist PASSED          [ 75%]
tests/test_rr_recommendation_system.py::test_no_duplicate_players_in_top10 PASSED [ 76%]
tests/test_rr_recommendation_system.py::test_pakistani_players_ineligible PASSED [ 77%]
tests/test_rr_recommendation_system.py::test_franchise_retentions_properly_discounted PASSED [ 78%]
tests/test_rr_recommendation_system.py::test_rr_role_fit_field_presence PASSED [ 79%]
tests/test_rr_recruitment_model_b.py::test_model_b_deliverable_files_exist PASSED [ 80%]
tests/test_rr_recruitment_model_b.py::test_model_a_hashes_remain_strictly_frozen PASSED [ 81%]
tests/test_rr_recruitment_model_b.py::test_traded_and_contracted_stars_excluded_from_target_rankings PASSED [ 82%]
tests/test_rr_recruitment_model_b.py::test_policy_restricted_pakistani_players_zero_score PASSED [ 83%]
tests/test_rr_recruitment_model_b.py::test_targetable_bowlers_lead_with_liam_dawson PASSED [ 84%]
tests/test_rr_recruitment_model_b.py::test_death_seam_targets_present PASSED [ 85%]
tests/test_rr_recruitment_model_b.py::test_target_batters_contain_no7_finishers PASSED [ 86%]
tests/test_shortened_innings_dls.py::test_first_innings_shortened_balls_and_elapsed[90] PASSED [ 87%]
tests/test_shortened_innings_dls.py::test_first_innings_shortened_balls_and_elapsed[84] PASSED [ 88%]
tests/test_shortened_innings_dls.py::test_first_innings_shortened_balls_and_elapsed[48] PASSED [ 89%]
tests/test_shortened_innings_dls.py::test_first_innings_shortened_balls_and_elapsed[30] PASSED [ 90%]
tests/test_shortened_innings_dls.py::test_second_innings_shortened_chase_dynamics[90] PASSED [ 91%]
tests/test_shortened_innings_dls.py::test_second_innings_shortened_chase_dynamics[84] PASSED [ 92%]
tests/test_shortened_innings_dls.py::test_second_innings_shortened_chase_dynamics[48] PASSED [ 93%]
tests/test_shortened_innings_dls.py::test_second_innings_shortened_chase_dynamics[30] PASSED [ 94%]
tests/test_state_reconstruction.py::test_temporal_causality_and_state PASSED [ 95%]
tests/test_state_reconstruction.py::test_revised_target_dls PASSED       [ 96%]
tests/test_validation_fixes.py::test_striker_out_attribution_on_runout PASSED [ 97%]
tests/test_validation_fixes.py::test_first_innings_par_model_final_score_accounting PASSED [ 98%]
tests/test_validation_fixes.py::test_empirical_bayes_shrinkage_extremes PASSED [ 99%]
tests/test_validation_fixes.py::test_pava_aggregation_consistency PASSED [100%]

============================ 102 passed in 22.56s =============================
```
