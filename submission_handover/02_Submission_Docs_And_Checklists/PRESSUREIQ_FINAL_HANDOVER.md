# PRESSUREIQ — Final Competition Submission Handover Report

**Competition:** Rajasthan Royals SupeRR Selector Season 2 (2026)  
**Submission Deadline:** 18 November 2026  
**Handover Date:** 12 November 2026 (`2026-11-12`)  
**Active Branch:** `remediation-phase1-audit`  
**Frozen Master Baseline:** `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2`  
**Status Verdict:** **`CONDITIONAL — EXTERNAL VERIFICATION REQUIRED`**  
*(Static Model A statistical submission files, methodology report, selection sheet, dashboard, and codebase tests are **READY FOR USER APPROVAL**. Market availability figures are accurately frozen as of the audited 11 Nov 2026 snapshot / 12 Nov 2026 handover date and require execution of the Nov 17 update runbook once BCCI/IPL publishes official 2027 retention lists, followed by user upload to Unstop.)*

---

## 1. Executive Summary & Core Findings

PRESSUREIQ evaluates delivery-level T20 reliability across **200,999 raw deliveries** (`200,961` regular-over balls + `38` Super Over balls across `867` matches, 2022–2026) using continuous **Batting Pressure Index (BPI)** and **Bowling Pressure Index (BoPI)** baselines calibrated via LightGBM on strictly chronological pre-ball state features (`docs/MODEL_BENCHMARK_REPORT.json`). After Empirical Bayes shrinkage (`K = 45.0`, `mu_0 = 0.0`) on high-pressure executions (`P_t >= 50`), five standardized pillars map via `Phi(Z_composite) * 100` to the `0–100` **Reliability Score**. Note explicitly that this score is a standardized normal CDF index, **not** a probability of match success.

### Frozen Model A Official Top 10 Batters (`data/processed/final_batter_rankings.csv`)
1. **Ruturaj Gaikwad** (ID `6059`, `Top_Order`) — Score **97.71** | `77` m, `1822` balls, `45` HP | 95% CI `[76.30, 99.09]`, Top-10 Prob `60.85%`, `Clutch Climber` (`+1.1487`)
2. **Rohit Sharma** (ID `126`, `Top_Order`) — Score **95.27** | `91` m, `1619` balls, `35` HP | 95% CI `[60.01, 98.17]`, Top-10 Prob `33.95%`, `Clutch Climber` (`+1.0831`)
3. **Fakhar Zaman** (ID `2921`, `Top_Order`) — Score **95.25** | `47` m, `863` balls, `52` HP | 95% CI `[52.46, 98.38]`, Top-10 Prob `45.15%`, `Clutch Climber` (`+1.0716`)
4. **Suryakumar Yadav** (ID `1699`, `Middle_Order`) — Score **94.68** | `139` m, `2759` balls, `236` HP | 95% CI `[66.71, 98.64]`, Top-10 Prob `45.90%`, `Clutch Climber` (`+0.7953`)
5. **Romario Shepherd** (ID `6726`, `Finisher`) — Score **93.69** | `68` m, `687` balls, `482` HP | 95% CI `[71.26, 97.62]`, Top-10 Prob `34.80%`, `Pressure Fragile` (`+0.6972`)
6. **Naman Dhir** (ID `37052`, `Top_Order`) — Score **93.30** | `46` m, `589` balls, `184` HP | 95% CI `[58.13, 98.06]`, Top-10 Prob `35.70%`, `Clutch Climber` (`+1.2455`)
7. **Phil Salt** (ID `5553`, `Top_Order`) — Score **93.01** | `84` m, `1643` balls, `49` HP | 95% CI `[14.48, 98.55]`, Top-10 Prob `37.00%`, `Ice Cold Anchor` (`-0.1756`)
8. **Jitesh Sharma** (ID `3916`, `Middle_Order`) — Score **92.79** | `73` m, `894` balls, `218` HP | 95% CI `[63.45, 97.68]`, Top-10 Prob `32.70%`, `Clutch Climber` (`+1.7087`)
9. **Nicholas Pooran** (ID `3125`, `Middle_Order`) — Score **92.58** | `115` m, `1972` balls, `300` HP | 95% CI `[68.33, 97.47]`, Top-10 Prob `31.75%`, `Ice Cold Anchor` (`-0.0465`)
10. **Jos Buttler** (ID `813`, `Top_Order`) — Score **92.45** | `121` m, `2829` balls, `99` HP | 95% CI `[40.62, 98.43]`, Top-10 Prob `34.05%`, `Ice Cold Anchor` (`-0.0538`)

### Frozen Model A Official Top 10 Bowlers (`data/processed/final_bowler_rankings.csv`)
1. **Liam Dawson** (ID `722`, `Spin`) — Score **95.39** | `22` m, `415` legal (`424` deliv), `83` HP | 95% CI `[74.17, 98.08]`, Top-10 Prob `41.85%`
2. **Haris Rauf** (ID `7364`, `Pace`) — Score **92.36** | `48` m, `1027` legal (`1063` deliv), `444` HP | 95% CI `[71.13, 96.49]`, Top-10 Prob `55.20%`
3. **Abbas Afridi** (ID `7699`, `Pace`) — Score **91.88** | `25` m, `453` legal (`474` deliv), `232` HP | 95% CI `[69.16, 95.74]`, Top-10 Prob `39.55%`
4. **Nathan Ellis** (ID `7920`, `Pace`) — Score **91.84** | `43` m, `916` legal (`959` deliv), `251` HP | 95% CI `[70.87, 95.95]`, Top-10 Prob `48.90%`
5. **Sufiyan Muqeem** (ID `34485`, `Spin`) — Score **91.41** | `25` m, `518` legal (`525` deliv), `213` HP | 95% CI `[64.39, 96.91]`, Top-10 Prob `39.50%`
6. **Matheesha Pathirana** (ID `8661`, `Pace`) — Score **91.11** | `54` m, `1132` legal (`1279` deliv), `400` HP | 95% CI `[70.27, 95.05]`, Top-10 Prob `47.00%`
7. **Nasum Ahmed** (ID `4658`, `Spin`) — Score **90.77** | `29` m, `600` legal (`607` deliv), `122` HP | 95% CI `[57.03, 98.19]`, Top-10 Prob `41.75%`
8. **Ishant Sharma** (ID `28`, `Pace`) — Score **90.42** | `24` m, `422` legal (`456` deliv), `64` HP | 95% CI `[72.42, 94.32]`, Top-10 Prob `22.10%`
9. **Shoriful Islam** (ID `7344`, `Pace`) — Score **90.36** | `39` m, `790` legal (`823` deliv), `279` HP | 95% CI `[65.38, 96.63]`, Top-10 Prob `44.30%`
10. **Tim Southee** (ID `278`, `Pace`) — Score **89.16** | `36` m, `826` legal (`861` deliv), `300` HP | 95% CI `[63.99, 95.51]`, Top-10 Prob `35.40%`

### Phase 4 Defect Fixes & Audits Completed (`2026-11-12`)
- **Methodology PDF Repaired (`scripts/generate_final_comprehensive_pdf.py` -> `docs/PRESSUREIQ_FINAL_METHODOLOGY_REPORT.pdf`):** Replaced stale BPI/BoPI equations with exact `src/models/pressure_index.py` code formulas; replaced ungrounded ML benchmark numbers (`0.0521`, `1.141`) with exact chronological `MODEL_BENCHMARK_REPORT.json` 2025/2026 metrics; replaced broken `₹` font glyphs with `INR`; removed all unrendered `$` / `$$` LaTeX strings (`0` `$` remaining); aligned Page 9 emerging stats with CSV (`Vaibhav Sooryavanshi`: `676` valid / `714` total balls, `223.2` SR, `7` `BPI>=50` balls; `Vignesh Puthur`: `72` legal / `36` HP balls); clarified `Pending Verification` status prior to Nov 17; updated Page 14 date (`12 NOVEMBER 2026`) and test suite count (`89/89`), maintaining strictly `14` pages.
- **New Programmatic Handover PDFs (`scripts/generate_final_handover_pdfs.py`):** Generated `PRESSUREIQ_FINAL_SELECTION_SHEET.pdf` (3 pages) and `PRESSUREIQ_FINAL_MARKET_APPENDIX.pdf` (3 pages) programmatically from frozen Model A CSVs and audited market ledgers with zero manual transcription.

---

## 2. Key Verified Artifact Checksums (SHA-256)

| Artifact | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `PRESSUREIQ_FINAL_SELECTION_SHEET.pdf` | 14,419 | `b16f28e77681153dfb92ea2b61f5c5bba7113a53db863fcad93f3e9b078b0752` | Primary Selection Sheet |
| `docs/PRESSUREIQ_FINAL_METHODOLOGY_REPORT.pdf` | 40,098 | `044f89a9db2c56b22d474cfe9e55b2d2db4a54517d8ae3a0549a4efa8e60d9a3` | Audited 14-Page Methodology PDF |
| `PRESSUREIQ_FINAL_MARKET_APPENDIX.pdf` | 11,411 | `05615747d9065646d1a6336a93a5055ce30ac959eb67efe989bc11d7f82947af` | Separate Market Appendix (Nov 12) |
| `data/processed/final_batter_rankings.csv` | 18,444 | `887f0c104047eb7b5c7d662b83600bacaf6263fa7162fc343b27800760b99b87` | Frozen Model A Batters |
| `data/processed/final_bowler_rankings.csv` | 27,959 | `344d63c55cecc7bce9de3cd06d82b6ac8217fcd448bb3f2e93d55da314f1e7bb` | Frozen Model A Bowlers |
| `data/processed/snapshots/ipl_2027_market_snapshot_2026-11-11.csv` | 12,066 | `8d1e1bdaa57eb3491abc78139e234420477f1414c448b5a68f4897f07b7efd4d` | Audited Pre-Nov 17 Market Snapshot |
| `PRESSUREIQ_Final_Submission.zip` | 62,296,913 | `76059a8f5f8b8de5126a5ed8b2a9378fb6664016989f3125df7ca4bbbe9696db` | Frozen Original Submission ZIP |

*(Full per-file manifest inside `submission_handover/03_Evidence_CSVs_And_Provenance/ARTIFACT_CHECKSUMS.sha256`.)*

---

## 3. Verification & Quality Results Summary

- **Automated Test Suite (`python -m pytest tests/ -v`):** **89 passed**, 0 failed, 0 skipped (`20.74s`).
- **Hybrid Validation Gate (`python scripts/hybrid_validation_gate.py`):** Exited `0` — `ALL_NUMBERS_VERIFIED_EXACT_MATCH` (`200,961` regular deliveries, `867` matches, monotonicity `100.0%`, `0` violations).
- **Live Browser QA (Playwright Chromium):** `10 pages, 2 interactions, zero_mutation: True, errors: []` across desktop (`1440x900`) and laptop (`1280x800`) viewports, visually confirming Top-10 tables, uncertainty charts, Market Intelligence strict labels (`Confirmed Trade 1`, `Confirmed Retained 0`, `Confirmed Released 0`, `Pending Verification 15`, `Rumour 0`, `Policy/Eligibility Review 1`), and RR Squad separation.

---

## 4. Authoritative References & Evidence Links

- Competition Scope & Problem Definition: `docs/ROUND1_OFFICIAL_SCOPE_VERIFICATION.md`
- Executable Model Specification & Benchmarks: `src/models/pressure_index.py`, `src/analysis/reliability_engine.py`, `docs/MODEL_BENCHMARK_REPORT.json`
- Official Market Intelligence Sources (documented with URLs, pub dates & timestamps in `PRESSUREIQ_FINAL_MARKET_APPENDIX.pdf`): `https://www.iplt20.com/news/article/tata-ipl-2026-player-retentions-announced`, `https://www.iplt20.com/news/article/csk-and-srh-agree-to-four-player-trade`, `https://www.business-standard.com/cricket/ipl/ipl-2026-auction-kkr-buys-sl-pacer-matheesha-pathirana-for-rs-18-crore-125121600860_1.html`, `https://www.onmanorama.com/sports/cricket/2025/12/16/ipl-2026-player-auction-rajasthan-royals-sign-vignesh-puthur.html`, `https://www.livemint.com/sports/cricket-news/will-pakistani-players-be-allowed-in-ipl-again-bcci-vice-president-rajeev-shuklas-huge-statement-says-they-do-not-11738666052953.html`
- Nov 17 Retention Ingestion Protocol: `docs/NOV17_RETENTION_UPDATE_RUNBOOK.md` and `scripts/import_market_retentions.py`

---

## 5. Exact Reproduction & November 17 Readiness Commands

```powershell
# Re-verify baseline & tests
python -m pytest tests/ -v
python scripts/hybrid_validation_gate.py

# Regenerate all PDFs from code & CSVs
python scripts/generate_final_comprehensive_pdf.py
python scripts/generate_final_handover_pdfs.py

# Post-Nov 17 official retention update workflow (do NOT fabricate before Nov 17)
python scripts/import_market_retentions.py --input <official_nov17_csv> --dry-run
python scripts/import_market_retentions.py --input <official_nov17_csv> --apply
python scripts/generate_final_handover_pdfs.py
python -m pytest tests/ -v
```
