# PRESSUREIQ — INDEPENDENT REMEDIATION CHANGELOG
**Phase:** Phase 1 Final Closure Remediation  
**Date:** 11 November 2026  
**Git Branch:** `remediation-phase1-audit`  
**Git Baseline Commit:** `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2` (Preserved Official Baseline)  
**Test Suite Status:** 74 / 74 Unit Tests Passing (100%)  

---

## 1. Summary of Remediations (Phase 1 Final Closure)

This changelog records the full audit trail of technical remediations, source-to-specification reconciliations, market chronology repairs, and population audits completed for the official Phase 1 Closure.

---

## 2. File Modification Details

### 2.1 `src/analysis/reliability_engine.py` & `src/models/pressure_value.py`
- **Reconciliation 1 (Operational High Pressure Threshold):** Documented that `compute_batter_reliability_scores` and `compute_bowler_reliability_scores` use $P \ge 50.0$ (empirical median-split) as the operational calculation threshold for sample volume preservation ($N \ge 30$ balls), while $[65.0, 85.0)$ serves as the descriptive display tier in reporting.
- **Reconciliation 2 (PRC Methodology):** Verified that `fit_pressure_response_curve` uses `scipy.stats.linregress(p / 100.0, y)` for linear slope estimation across continuous pressure, assigning players into 7 empirical archetypes based on slope $\beta$ and tier deltas.
- **Reconciliation 3 (Raw vs. Leverage PAVA):** Documented the strict separation between unamplified performance added (`pava_bat = raw_bat_value`, `pava_bowl = raw_bowl_value`) and leverage-weighted match equity (`leverage_pava_bat`, `leverage_pava_bowl`).

---

### 2.2 `data/processed/ipl_2027_player_market_template.csv` & `ipl_2027_market_change_log.csv`
- **Remediation 1 (Chronology Repair):** Quarantined all future-dated 15 November 2026 claims; updated all verification timestamps and last updated fields to $\le$ `2026-11-11 18:00:00`.
- **Remediation 2 (Nathan Ellis CSK-to-SRH Trade Date):** Set official trade announcement date to **5 November 2026 (`2026-11-05`)**, exactly 6 days prior to audit date. Classified Ellis as `Officially traded` and contracted to SRH (Class C).
- **Remediation 3 (Traceable Source Taxonomy):** Every player assigned traceable URLs, publication dates, and clean categories (Confirmed Trade, Confirmed Release, Retained/Contracted, Pending verification, or Ineligible).

---

### 2.3 `scripts/import_market_retentions.py`
- **Remediation:** Added `"Pending verification"` to `VALID_STATUSES` to support rigorous classification of unconfirmed uncapped/mini-auction entries without speculative inflation.

---

### 2.4 `scripts/build_rr_2027_recommendations.py`
- **Remediation:** Added Nathan Ellis to `FRANCHISE_RETENTIONS` under SRH via trade agreement. Recomputed candidate rankings: Ellis receives score 72.85 (Class C) and is excluded from RR Top 10 bowler targets; Bhuvneshwar Kumar enters at Rank 10 (Priority Score: 87.64).

---

### 2.5 `docs/` Specifications & Reports
- **`CANONICAL_MODEL_SPECIFICATION.md`:** Expanded to Version 2.3-Canonical, including the source-to-specification consistency matrix with line numbers, operational vs. descriptive thresholds, raw vs. leverage PAVA, and PRC linear slope equations.
- **`MARKET_DATA_IDENTITY_AUDIT.md`:** Updated with row-by-row evidence audit table for all 17 players and segregated available vs. pending cohorts.
- **`INDEPENDENT_REMEDIATION_REPORT.md`:** Updated with comprehensive Phase 1 Closure Dossier, population reconciliation table, and final PASS verdict.

---

## 3. Cryptographic Baseline Verification

| File | Status | SHA-256 Hash | Notes |
|:---|:---:|:---|:---|
| `data/processed/final_batter_rankings.csv` | **PRESERVED** | `887f0c104047eb7b5c7d662b83600bacaf6263fa7162fc343b27800760b99b87` | Official Model A Baseline |
| `data/processed/final_bowler_rankings.csv` | **PRESERVED** | `344d63c55cecc7bce9de3cd06d82b6ac8217fcd448bb3f2e93d55da314f1e7bb` | Official Model A Baseline |
| `PRESSUREIQ_Final_Submission.zip` | **PRESERVED** | `76059a8f5f8b8de5126a5ed8b2a9378fb6664016989f3125df7ca4bbbe9696db` | Frozen Submission Archive |
