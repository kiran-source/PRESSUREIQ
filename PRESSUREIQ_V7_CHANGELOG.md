# PRESSUREIQ V7.0 — Changelog

All notable changes to this project are documented in this file, in reverse chronological order.

---

## [V7.0] — 2026-11-17 — Production Dashboard Upgrade & Master Methodology Report

### Added
- `streamlit_app.py` — root entry point for Streamlit Community Cloud deployment
- `PRESSUREIQ_MASTER_METHODOLOGY_REPORT_V7.pdf` — 30+ page research-quality methodology PDF
- `PRESSUREIQ_V7_README.md` — comprehensive project documentation
- `PRESSUREIQ_V7_DEPLOYMENT_GUIDE.md` — Streamlit Cloud deployment instructions
- `PRESSUREIQ_V7_DATA_DICTIONARY.md` — complete field-level data documentation
- `PRESSUREIQ_V7_CHANGELOG.md` — this file
- `PRESSUREIQ_V7_VALIDATION_REPORT.md` — test suite and integrity verification

### Changed
- `design_tokens.py` — `PRODUCT_VERSION` updated to `V7.0 — Production Release`
- Dashboard brand version label updated across all views

### Unchanged (Protected)
- `data/processed/final_batter_rankings.csv` — Model A frozen ✅
- `data/processed/final_bowler_rankings.csv` — Model A frozen ✅
- `submission_handover/01_Unstop_Submission_Files/PRESSUREIQ_Final_Submission.zip` — frozen ✅
- All SHA-256 checksums verified identical to baseline

---

## [V6.6.2] — 2026-11-17 — Final Consistency Audit & Discrepancy Resolution

### Fixed
- Resolved Model A ranking discrepancy (old narrative claimed 72.33 / 83.82; frozen CSVs correctly show 97.71 / 95.39)
- Traced erroneous figures to Dasun Shanaka's CI lower bound in historical audit notes and an uncalibrated raw bowler rating
- Generated `audit/final_v66/model_a_discrepancy_register.json` and `.csv`

### Added
- `PRESSUREIQ_V6.6.2_FINAL_CONSISTENCY_AUDIT.md`
- `audit/final_v66/model_a_discrepancy_register.json`

---

## [V6.6.1] — 2026-11-17 — Full Franchise Accounting Reconciliation

### Added
- `data/processed/ipl_2027_franchise_accounting_reconciliation.csv` — 275 records across 10 franchises
- `submission_handover/03_Evidence_CSVs_And_Provenance/ipl_2027_franchise_accounting_reconciliation.csv`
- `submission_handover/03_Evidence_CSVs_And_Provenance/ipl_2027_official_squad_rosters.csv`
- `audit/final_v66/source_evidence_manifest.md`

### Fixed
- Corrected Harshal Patel trade origin: PBKS → GT (not SRH → GT)
- Verified Jack Edwards trade direction: SRH → CSK
- CSK prior squad size corrected from naive 30 to legitimate 25-player ceiling

---

## [V6.6] — 2026-11-17 — Official IPLT20 Retention Graphics Integration

### Added
- Official @iplt20 Instagram post registered as primary retention evidence source
- Extracted player names and statuses from official IPL retention graphics (10 teams)
- `submission_handover/03_Evidence_CSVs_And_Provenance/supplementary_rr_market_leaderboard.csv`
- `submission_handover/03_Evidence_CSVs_And_Provenance/supplementary_rr_batter_leaderboard.csv`
- `submission_handover/03_Evidence_CSVs_And_Provenance/supplementary_rr_bowler_leaderboard.csv`

---

## [V6.5.1] — 2026-11-17 — Independent Acceptance Audit

### Added
- `PRESSUREIQ_V6.5.1_ACCEPTANCE_AUDIT.md` — final independent audit of V6.5 release decision

---

## [V6.5] — 2026-11-17 — Ten-Team Retention/Release Audit

### Added
- `PRESSUREIQ_V6.5_FINAL_RELEASE_AUDIT.md`
- Complete 10-team retention ledger with per-team source evidence

---

## [V6.4.2] — 2026-11-17 — Market Evidence Integrity Audit

### Fixed
- Reclassified unsupported player statuses from `Confirmed Released` to `Pending Verification`
- Corrected 7 unsupported release classifications across all franchises

---

## [V6.4.1] — 2026-11-17 — Retention Evidence Verification

### Added
- System-time-anchored verification timestamps (IST)
- Primary-source URL registry for all retention/release records

---

## [V6.4] — 2026-11-17 — Model A Hash Verification & Dashboard Upgrade

### Fixed
- All 4 Model A baseline checksums confirmed matching:
  - `batter_csv: True`
  - `bowler_csv: True`
  - `zip_file: True`
  - `master_head: True`

### Added
- `audit/v70_backup/` — configuration backups before V7 upgrade
- Branch `feature/pressureiq-v7-dashboard` created

---

## [V3.0] — 2026-11-12 — Dashboard Architecture v3

### Added
- 13-view Streamlit dashboard with editorial luxury aesthetic
- Warm Ivory / Terracotta design system (`design_tokens.py`)
- Empirical Bayes shrinkage visualization
- RR Recruitment Intelligence views (Model B)

---

## [V1.0] — 2026-11-11 — Official Competition Submission

### Added
- Model A frozen competition deliverables
- `PRESSUREIQ_Final_Submission.zip`
- Git baseline commit `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2`
- 107 pytest tests (all green)
