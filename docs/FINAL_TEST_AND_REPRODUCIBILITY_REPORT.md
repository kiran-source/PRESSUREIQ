# FINAL TEST & REPRODUCIBILITY AUDIT REPORT
## Automated Test Execution, Environment Specifications & Test Evidence

**Project:** PRESSUREIQ — Context-Aware Cricket Reliability Intelligence  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 (2026)  
**Audit Date:** 12 November 2026  
**Auditor:** Quantitative Review & Submission QA Panel  
**Test Suite Status:** 🎉 **52 / 52 TESTS PASSED (100%) IN 17.69s**  
**Streamlit Headless Status:** 🎉 **PASSED (EXIT CODE 0)**  
**Raw Hash Verification:** 🎉 **PASSED (ALL 6 FILES VERIFIED, EXIT CODE 0)**  

---

## 1. ENVIRONMENT & PINNED DEPENDENCY AUDIT

The test environment was audited to ensure full reproducibility on a clean Python 3.13 installation:
- **Operating System:** Windows 11 (build 26100)
- **Python Version:** Python 3.13.5 (`C:\Users\kiran\AppData\Local\Programs\Python\Python313\python.exe`)
- **Pytest Version:** pytest 9.1.1, pluggy 1.6.0
- **Key Pinned Dependencies:**
  - `pandas==2.2.3`
  - `numpy==2.2.3`
  - `scipy==1.15.2`
  - `scikit-learn==1.6.1`
  - `lightgbm==4.6.0`
  - `pyarrow==23.0.1`
  - `duckdb==2.0.0`
  - `streamlit==1.56.0`
  - `plotly==6.0.0`

---

## 2. AUTOMATED PYTEST EXECUTION LOG

### Command:
```powershell
python -m pytest -v
```

### Full Execution Output (52 / 52 Passed):
```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\kiran\OneDrive\Documents\Desktop\SuperRR
plugins: anyio-4.10.0, asyncio-1.4.0

tests/test_bootstrap_baseline_reproducibility.py::test_bootstrap_baseline_reproduces_batting_scores PASSED [  1%]
tests/test_bootstrap_baseline_reproducibility.py::test_bootstrap_baseline_reproduces_bowling_scores PASSED [  3%]
tests/test_bowler_illegal_deliveries.py::test_illegal_deliveries_worsen_economy_and_pava_without_increasing_legal_balls PASSED [  5%]
tests/test_data_cleaning.py::test_legal_ball_classification PASSED       [  7%]
tests/test_data_cleaning.py::test_bowler_runs_conceded_rules PASSED      [  9%]
tests/test_data_cleaning.py::test_wicket_attribution PASSED              [ 11%]
tests/test_data_cleaning.py::test_dismissal_type_normalization PASSED    [ 13%]
tests/test_experimental_pressure.py::test_sigmoid_numerical_stability PASSED [ 15%]
tests/test_experimental_pressure.py::test_win_probability_leverage_bounds PASSED [ 17%]
tests/test_experimental_pressure.py::test_blowout_suppression_in_cdpi PASSED [ 19%]
tests/test_experimental_pressure.py::test_chase_monotonicity_in_cdpi_batting PASSED [ 21%]
tests/test_features.py::test_first_innings_par_model PASSED              [ 23%]
tests/test_features.py::test_par_no_same_match_leakage PASSED            [ 25%]
tests/test_features.py::test_par_no_future_match_leakage PASSED          [ 26%]
tests/test_features.py::test_player_history_zero_future_leakage PASSED   [ 28%]
tests/test_hybrid_validation.py::test_sigmoid_monotonicity_and_bounds PASSED [ 30%]
tests/test_hybrid_validation.py::test_smooth_blowout_continuity_and_suppression PASSED [ 32%]
tests/test_hybrid_validation.py::test_analytical_dls_prior_bounds PASSED [ 34%]
tests/test_hybrid_validation.py::test_kish_effective_sample_size_formula PASSED [ 36%]
tests/test_oof_predictions.py::test_expected_calibration_error PASSED    [ 38%]
tests/test_oof_predictions.py::test_oof_predictions_chronology_and_provenance PASSED [ 40%]
tests/test_oof_predictions.py::test_future_category_isolation_and_completeness PASSED [ 42%]
tests/test_pava_pressure_amplification.py::test_positive_and_negative_outcomes_across_pressure_tiers PASSED [ 44%]
tests/test_pava_pressure_amplification.py::test_baseline_retention_invariance PASSED [ 46%]
tests/test_pava_pressure_amplification.py::test_symmetric_execution_surplus PASSED [ 48%]
tests/test_prc_archetypes.py::test_prc_clutch_climber PASSED             [ 50%]
tests/test_prc_archetypes.py::test_prc_gradual_decliner PASSED           [ 51%]
tests/test_prc_archetypes.py::test_prc_ice_cold_anchor PASSED            [ 53%]
tests/test_prc_archetypes.py::test_prc_extreme_collapse_fragile PASSED   [ 55%]
tests/test_prc_archetypes.py::test_prc_insufficient_evidence PASSED      [ 57%]
tests/test_pressure_directionality.py::test_bpi_monotonic_with_rrr PASSED [ 59%]
tests/test_pressure_directionality.py::test_bpi_monotonic_with_wickets_lost PASSED [ 61%]
tests/test_pressure_directionality.py::test_bpi_monotonic_with_balls_remaining PASSED [ 63%]
tests/test_pressure_directionality.py::test_bopi_monotonic_with_opposition_wickets_in_hand PASSED [ 65%]
tests/test_pressure_directionality.py::test_bopi_monotonic_with_chase_comfort PASSED [ 67%]
tests/test_pressure_directionality.py::test_first_innings_par_pressure_symmetry PASSED [ 69%]
tests/test_pressure_index.py::test_bpi_monotonicity_and_bounds PASSED    [ 71%]
tests/test_pressure_index.py::test_bopi_monotonicity_and_bounds PASSED   [ 73%]
tests/test_shortened_innings_dls.py::test_first_innings_shortened_balls_and_elapsed[90] PASSED [ 75%]
tests/test_shortened_innings_dls.py::test_first_innings_shortened_balls_and_elapsed[84] PASSED [ 76%]
tests/test_shortened_innings_dls.py::test_first_innings_shortened_balls_and_elapsed[48] PASSED [ 78%]
tests/test_shortened_innings_dls.py::test_first_innings_shortened_balls_and_elapsed[30] PASSED [ 80%]
tests/test_shortened_innings_dls.py::test_second_innings_shortened_chase_dynamics[90] PASSED [ 82%]
tests/test_shortened_innings_dls.py::test_second_innings_shortened_chase_dynamics[84] PASSED [ 84%]
tests/test_shortened_innings_dls.py::test_second_innings_shortened_chase_dynamics[48] PASSED [ 86%]
tests/test_shortened_innings_dls.py::test_second_innings_shortened_chase_dynamics[30] PASSED [ 88%]
tests/test_state_reconstruction.py::test_temporal_causality_and_state PASSED [ 90%]
tests/test_state_reconstruction.py::test_revised_target_dls PASSED       [ 92%]
tests/test_validation_fixes.py::test_striker_out_attribution_on_runout PASSED [ 94%]
tests/test_validation_fixes.py::test_first_innings_par_model_final_score_accounting PASSED [ 96%]
tests/test_validation_fixes.py::test_empirical_bayes_shrinkage_extremes PASSED [ 98%]
tests/test_validation_fixes.py::test_pava_aggregation_consistency PASSED [100%]

============================= 52 passed in 17.69s =============================
```

---

## 3. SUPPORTING TEST VERIFICATIONS

1. **Streamlit Headless Import:**
   - Command: `python scripts/test_streamlit_headless.py`
   - Exit Code: `0`
   - Result: `src.dashboard.app successfully imported without errors!`
2. **Raw Hash Verification:**
   - Command: `python scripts/verify_raw_hashes.py`
   - Exit Code: `0`
   - Result: `SUCCESS: All raw dataset files match immutable provenance SHA-256 hashes exactly.`
3. **Bootstrap Reproducibility Test:**
   - Verified that setting $k = 1$ in vectorized bootstrap evaluation reproduces canonical reliability scores within 0.05 score points for all players.

---

## 4. AUDIT VERDICT

The automated test suite passes with a 100% success rate across all 52 unit, integration, and statistical invariant tests. Zero regressions or failures detected.

