# PRESSUREIQ — Competition Submission Checklist

**Competition:** Rajasthan Royals SupeRR Selector Season 2 (2026)  
**Submission Deadline:** 18 November 2026  
**Prepared As Of:** 12 November 2026 (Pre-Nov 17 Retention Baseline)  
**Git Branch:** `remediation-phase1-audit`  
**Overall Readiness Status:** `CONDITIONAL — EXTERNAL VERIFICATION REQUIRED` *(Static Model A statistical deliverables and PDFs are verified and ready; final market-availability refresh awaits official 17 November 2026 IPL retention announcements and human Unstop submission.)*

---

## 1. Frozen Baseline & Mathematical Integrity Checks

- [x] `master` Git HEAD unmodified (`fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2`)
- [x] Original baseline archive `PRESSUREIQ_Final_Submission.zip` untouched (`62,296,913` bytes; SHA-256 `76059a8f5f8b8de5126a5ed8b2a9378fb6664016989f3125df7ca4bbbe9696db`)
- [x] Frozen Model A batter rankings `data/processed/final_batter_rankings.csv` untouched (`18,444` bytes; SHA-256 `887f0c104047eb7b5c7d662b83600bacaf6263fa7162fc343b27800760b99b87`)
- [x] Frozen Model A bowler rankings `data/processed/final_bowler_rankings.csv` untouched (`27,959` bytes; SHA-256 `344d63c55cecc7bce9de3cd06d82b6ac8217fcd448bb3f2e93d55da314f1e7bb`)
- [x] Pre-retention market snapshot `data/processed/snapshots/ipl_2027_market_snapshot_2026-11-11.csv` untouched (`12,066` bytes; SHA-256 `8d1e1bdaa57eb3491abc78139e234420477f1414c448b5a68f4897f07b7efd4d`)
- [x] Standardized score `Phi(Z_composite) * 100` explicitly disclosed as NOT a probability of match success across selection sheets, methodology report, and Streamlit UI

## 2. Primary Competition PDF Deliverables (`01_Unstop_Submission_Files/`)

- [x] `PRESSUREIQ_FINAL_SELECTION_SHEET.pdf` (3 pages; SHA-256 `d8d4e380539299b95b16834dc5d97edec8d4a8ff00edbcbb2579f80db3b0aaae`; generated directly from frozen Model A CSVs via `scripts/generate_final_handover_pdfs.py`)
- [x] `docs/PRESSUREIQ_FINAL_METHODOLOGY_REPORT.pdf` (14 pages; SHA-256 `64f1ef6aa3b0bf99f3cc887761419b1b658f9cd61877b91dfa245b2363f0f7c2`; audited and regenerated cleanly with canonical `src/models/pressure_index.py` BPI/BoPI math, `docs/MODEL_BENCHMARK_REPORT.json` 2026 holdout metrics, verified dataset stats, `INR` formatting, and zero raw LaTeX `$`)
- [x] `PRESSUREIQ_FINAL_MARKET_APPENDIX.pdf` (3 pages; SHA-256 `99677b53f320c8925530fdf5851432a8e8100e2fbd3991d757d30583aabc22ba`; separates IPL 2027 market status as of 12 Nov 2026 with verified source URLs, publication dates, verification timestamps, audit log, and Nov 17 update protocol)

## 3. Automated Verification & Dashboard QA

- [x] Full pytest suite passed (`89/89` passed, `0` failed, `0` skipped)
- [x] Hybrid Validation Gate `scripts/hybrid_validation_gate.py` passed (`ALL_NUMBERS_VERIFIED_EXACT_MATCH`, `Monotonicity=100.0%`, `Violations=0`)
- [x] Headless Playwright 10-page dashboard QA passed (`10 pages, 2 interactions, zero_mutation: True, errors: []`) across desktop (`1440x900`) and laptop (`1280x800`) viewports; 12 screenshots copied to `submission_handover/04_Dashboard_Screenshots/`
- [x] No `.env`, secrets, tokens, virtual environments, caches, or raw competition CSVs placed in `submission_handover/`

## 4. Mandatory External / User Actions (17–18 November 2026)

- [ ] **On 17 November 2026 (after official BCCI/IPL 2027 announcements):** Collect verified official announcement URLs and run:
  1. `python scripts/import_market_retentions.py --input <official_nov17_updates.csv> --dry-run`
  2. `python scripts/import_market_retentions.py --input <official_nov17_updates.csv> --apply`
  3. `python scripts/generate_final_handover_pdfs.py` (refreshes `PRESSUREIQ_FINAL_MARKET_APPENDIX.pdf` without altering Model A selection CSVs/rankings)
  4. `python -m pytest tests/ -v`
- [ ] **On 17–18 November 2026 (before Unstop deadline):** Review the final PDFs in `submission_handover/01_Unstop_Submission_Files/`, optionally prepare the companion ZIP (`docs/UNSTOP_SUBMISSION_GUIDE.md`), and manually submit via the Unstop competition portal. *(Automated submission was intentionally not performed.)*

