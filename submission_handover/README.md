# PRESSUREIQ — Submission Handover Directory

**Competition:** Rajasthan Royals SupeRR Selector Season 2 (2026)  
**Submission Deadline:** 18 November 2026  
**Prepared As Of:** 12 November 2026 (Pre-Nov 17 Official IPL Retention Announcements)  
**Branch:** `remediation-phase1-audit` | **Frozen Baseline (`master`):** `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2`

---

## Folder Organization

### `01_Unstop_Submission_Files/` (Primary Competition PDFs)
1. **`PRESSUREIQ_FINAL_SELECTION_SHEET.pdf`** — 3-page landscape summary presenting the frozen Model A **Top 10 Batters** and **Top 10 Bowlers**, complete sample sizes, raw/shrunk PAVA, retention deltas, PRC archetypes, 2,000-match bootstrap 95% CIs, Top-10 inclusion probabilities, near-miss cutoff defenses (#11–#13), and the emerging talent separation note.
2. **`PRESSUREIQ_FINAL_METHODOLOGY_REPORT.pdf`** — 14-page comprehensive technical methodology report audited against the executable codebase (`src/models/pressure_index.py`, `src/analysis/reliability_engine.py`, `docs/MODEL_BENCHMARK_REPORT.json`).
3. **`PRESSUREIQ_FINAL_MARKET_APPENDIX.pdf`** — Separate 3-page IPL 2027 market & retention governance appendix as of **12 November 2026** (anchored to the audited `2026-11-11` snapshot), containing all 17 source-verified URLs, publication dates, verification timestamps, strict 6-status taxonomy, chronological change log, and the 17 November update protocol.

### `02_Submission_Docs_And_Checklists/` (Operational Handover & Verification Docs)
- `PRESSUREIQ_SUBMISSION_CHECKLIST.md` — Final pre-submission and November 17 verification checklist.
- `PRESSUREIQ_FINAL_HANDOVER.md` — Complete project handover report, checksums, reproduction instructions, and readiness verdict.
- `NOV17_RETENTION_UPDATE_RUNBOOK.md` — Deterministic post-retention update instructions (`scripts/import_market_retentions.py`).
- `ROUND1_OFFICIAL_SCOPE_VERIFICATION.md` — Official scope record resolving Unstop brief vs metadata discrepancies.
- `UNSTOP_SUBMISSION_GUIDE.md` — Step-by-step Unstop portal packaging guidance.
- `COMPETITION_READINESS_DECISION.md` — Readiness sign-off criteria and preserved baseline audit.

### `03_Evidence_CSVs_And_Provenance/` (Processed Deliverables & Checksums)
- `final_batter_rankings.csv` — Frozen Model A qualified batter rankings (109 batters).
- `final_bowler_rankings.csv` — Frozen Model A qualified bowler rankings (147 bowlers).
- `final_competition_batter_top10.csv` & `final_competition_bowler_top10.csv` — Top 10 competition extracts.
- `player_evidence_dossier.csv` — 30-player evidence dossier (Top 10 + Near-Miss #11–#15 per discipline).
- `emerging_talent_watchlist.csv` — 10-player emerging/uncapped watchlist separated from Model A rankings.
- `ipl_2027_player_market_template.csv` — Audited 17-player IPL 2027 market ledger.
- `ipl_2027_market_change_log.csv` — 7-event market audit trail.
- `rr_2027_candidate_rankings.csv` — 256-player RR role-fit & market-stratified table.
- `ARTIFACT_CHECKSUMS.sha256` — Cryptographic SHA-256 manifest of all handover deliverables and frozen archives.

*(Raw ball-by-ball competition CSVs, virtual environments, `.env` files, private tokens, and caches are strictly excluded from this handover folder.)*

### `04_Dashboard_Screenshots/` (12 Verified Streamlit Render Captures)
Captured automatically via headless Chromium Playwright QA across desktop (`1440x900`) and laptop (`1280x800`) viewports covering all 10 interactive Streamlit pages.

---

## Reproduction Commands

```powershell
# 1. Regenerate methodology and handover PDFs cleanly
python scripts/generate_final_comprehensive_pdf.py
python scripts/generate_final_handover_pdfs.py

# 2. Verify mathematical & artifact integrity
python -m pytest tests/ -v
python scripts/hybrid_validation_gate.py

# 3. Launch dashboard locally for visual inspection
streamlit run src/dashboard/app.py --server.port 8501 --server.headless true
```

