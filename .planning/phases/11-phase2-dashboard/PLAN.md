# PHASE 11: Phase 2 Clean-Room Verification & Jury-Grade Dashboard

## Goal
Complete Phase A clean-room verification (`docs/PHASE2_INDEPENDENT_VERIFICATION.md`, `data/processed/phase2_verification_manifest.json`), modularize the **PRESSUREIQ — Cricket Pressure Intelligence** Streamlit application (`data_loader.py`, `analytics.py`, `charts.py`, `app.py`) across all 10 required jury views, capture live desktop/laptop screenshots across all 10 pages via Playwright, run automated & security/code-review checks, and finalize Phase D handover deliverables.

## Tasks
1. **Phase A Clean-Room Verification (Completed):**
   - Audit `PRESSUREIQ_Phase1_Remediation.zip` SHA-256 (`f0bf9672...`), CRC, 223-file manifest, and secrets scan.
   - Verify Git state on `remediation-phase1-audit` vs frozen `master` (`fc0e622c...`).
   - Run isolated `prq_venv` clean-room pytest & byte-identical ranking regeneration (`887f0c10...`, `344d63c5...`).
   - Document blockers transparently in `docs/PHASE2_INDEPENDENT_VERIFICATION.md` and `data/processed/phase2_verification_manifest.json`.
2. **Modular Dashboard Architecture (`src/dashboard/`):**
   - `src/dashboard/data_loader.py`: Cached data loading (`@st.cache_data`), defensive missing-file handling, frozen hash attestation, bootstrap CI + median rank merges, DuckDB season/team aggregations, and 11 Nov 2026 market snapshot isolation.
   - `src/dashboard/analytics.py`: Pure functions for filtering (role, season/format, team, min sample size), Kish Effective Sample Size vs raw HP opportunities, Five-Pillar breakdown, peer comparisons, phase-wise metrics, emerging talent discovery, and RR squad fit vs strictly separated verified market availability.
   - `src/dashboard/charts.py`: Publication-grade Plotly builders using an intentional cricket broadcast / RR visual palette (`#004BA0`, `#EA1B88`, `#0F172A`, `#10B981`, `#D97706`).
   - `src/dashboard/app.py`: 10-page Streamlit interface ("PRESSUREIQ — Cricket Pressure Intelligence") with strict UI wording guardrails (`Pending Verification` never labeled `Confirmed Available`, standardized score never interpreted as probability).
3. **Phase C QA & Playwright Verification:**
   - Write comprehensive unit tests in `tests/test_dashboard_data.py`.
   - Launch Streamlit locally and capture desktop (`1440x900`) and laptop (`1280x800`) Playwright screenshots across all 10 pages, checking console errors, chart rendering, filter interaction, market badges, and zero dataset mutation.
   - Invoke `gsd-code-reviewer` for structured code and security review and record CodeRabbit CLI availability accurately.
4. **Phase D Final Handover:**
   - Author `docs/DASHBOARD_USER_GUIDE.md`, `docs/PHASE2_COMPLETION_REPORT.md`, and `docs/FINAL_COMPETITION_CHECKLIST.md`.
   - Commit cleanly on `remediation-phase1-audit`, rebuild `PRESSUREIQ_Phase1_Remediation.zip`, and verify frozen artifacts untouched.

## Acceptance Criteria
- All 10 dashboard pages render cleanly with real project metrics, zero uncaught runtime errors, and responsive layout.
- Frozen rankings (`final_batter_rankings.csv`, `final_bowler_rankings.csv`) and `PRESSUREIQ_Final_Submission.zip` remain byte-for-byte unchanged.
- All automated tests pass (including `tests/test_dashboard_data.py`).

