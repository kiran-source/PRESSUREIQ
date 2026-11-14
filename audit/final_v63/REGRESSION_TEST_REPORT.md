# REGRESSION TEST REPORT
## Automated Test Execution & Quality Assurance Ledger

**Audit Directive:** PRESSUREIQ V6.3 Controlled Remediation  
**Test Suite Executed:** `pytest tests/ -v`  
**Execution Timestamp:** 14 November 2026, 22:28 IST  
**Environment:** Python 3.13.5, Pytest 9.1.1, Windows Sandbox  
**Total Tests Executed:** 107  
**Total Tests Passed:** 107 (100.0%)  
**Total Tests Failed:** 0 (0.0%)  
**Final Test Verdict:** **PASS — ZERO REGRESSIONS**  

---

### 1. Test Execution Breakdown by Module

| Test Module File | Test Count | Passed | Failed | Key Verification Area |
|---|:---:|:---:|:---:|---|
| `tests/test_rr_recruitment_model_b.py` | 12 | 12 | 0 | Model B deliverables, frozen hashes, exclusions, nationality fixes, unknown nationality handling, overseas consistency, availability taxonomy, dual all-rounders. |
| `tests/test_audit_remediation.py` | 6 | 6 | 0 | Dot-ball accounting (excluding wides), legal delivery bowler economy, canonical IDs, Nathan Ellis trade status, MCDA single weighting. |
| `tests/test_bootstrap_baseline_reproducibility.py` | 2 | 2 | 0 | 2,000-iteration bootstrap replication of Model A scores within $\pm 0.05$ tolerance. |
| `tests/test_bowler_illegal_deliveries.py` | 1 | 1 | 0 | Wides & no-balls penalty mechanics, zero legal ball increment on illegal deliveries. |
| `tests/test_dashboard_data.py` | 11 | 11 | 0 | Dashboard bundle loading, frozen hashes, filter idempotency, DuckDB season slicing, market safeguards, Nov 5 trade counterparties. |
| `tests/test_data_cleaning.py` | 4 | 4 | 0 | Legal ball filtering, bowler run concessions, wicket attribution, dismissal type normalization. |
| `tests/test_experimental_pressure.py` | 4 | 4 | 0 | Sigmoid numerical stability, win probability leverage bounds, blowout suppression, chase monotonicity. |
| `tests/test_features.py` | 4 | 4 | 0 | Par model leakage prevention, historical player feature isolation. |
| `tests/test_final_competition_deliverables.py` | 5 | 5 | 0 | Top 10 CSVs, evidence dossier, emerging talent watchlist, methodology PDF, Model A bit-for-bit immutability. |
| `tests/test_hybrid_validation.py` | 8 | 8 | 0 | Sigmoid bounds, blowout suppression, analytical DLS prior, Kish ESS formula, validation gate execution. |
| `tests/test_oof_predictions.py` | 3 | 3 | 0 | Expected calibration error, out-of-fold chronology, future category isolation. |
| `tests/test_pava_pressure_amplification.py` | 7 | 7 | 0 | Monotonic regression guarantees, PAVA pooling, bounded amplification. |
| `tests/test_player_market_intelligence.py` | 8 | 8 | 0 | Market template schema, trade ingestion, duplicate rejection, non-interference with Model A. |
| `tests/test_player_visual_intelligence.py` | 4 | 4 | 0 | Image manifest completeness, base64 encoding, directory builder. |
| `tests/test_prc_archetypes.py` | 5 | 5 | 0 | Pressure Response Curve archetype classification (Clutch Climber, Gradual Decliner, Ice Cold Anchor, Extreme Collapse Fragile, Insufficient Evidence). |
| `tests/test_pressure_directionality.py` | 6 | 6 | 0 | BPI monotonicity with RRR, wickets lost, balls remaining; BoPI monotonicity; first-innings par symmetry. |
| `tests/test_pressure_index.py` | 2 | 2 | 0 | Mathematical bounds ($[0, 100]$), continuous leverage indexing. |
| `tests/test_rr_recommendation_system.py` | 5 | 5 | 0 | Candidate file existence, deduplication, Pakistani policy exclusion, rival discounting, role fit. |
| `tests/test_shortened_innings_dls.py` | 8 | 8 | 0 | First-innings and chase dynamics under shortened overs ($15, 14, 8, 5$ overs). |
| `tests/test_state_reconstruction.py` | 2 | 2 | 0 | Delivery-by-delivery state reconstruction, revised DLS targets. |
| `tests/test_validation_fixes.py` | 4 | 4 | 0 | Runout striker attribution, first innings par score accounting, Empirical Bayes shrinkage extremes ($K=45.0$), PAVA aggregation. |
| **Total Test Suite** | **107** | **107** | **0** | **100.0% Pass Rate** |

---

### 2. Specific Verification of New Remediation Test Cases

```python
# 1. Verification of the 5 defect players
tests/test_rr_recruitment_model_b.py::test_remediated_nationalities_are_correctly_classified_as_overseas PASSED
- Sikandar Raza -> Zimbabwe, is_overseas=True
- Sherfane Rutherford -> West Indies, is_overseas=True
- Moeen Ali -> England, is_overseas=True
- Dasun Shanaka -> Sri Lanka, is_overseas=True
- Glenn Phillips -> New Zealand, is_overseas=True

# 2. Unknown nationality safety check
tests/test_rr_recruitment_model_b.py::test_unknown_nationality_handling_never_defaults_to_domestic_india PASSED
- resolve_player_nationality('Unknown') returns ('Unknown / Requires Verification', None)
- Never defaults to 'India' or is_overseas=False

# 3. Mathematical consistency
tests/test_rr_recruitment_model_b.py::test_overseas_flag_strictly_equals_nationality_not_india PASSED
- Across all 261 rows: is_overseas == (nationality != 'India')

# 4. Strict status taxonomy
tests/test_rr_recruitment_model_b.py::test_canonical_availability_vocabulary PASSED
- All candidates strictly belong to the 6 canonical statuses

# 5. Dual-board all-rounders
tests/test_rr_recruitment_model_b.py::test_target_boards_consistency_and_dual_qualified_allrounders PASSED
- Raza, Moeen, Shanaka, Holder, Nabi present on both boards without data corruption
```
