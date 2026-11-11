# CodeRabbit Initial CLI Review Capture & Findings Registry

**Execution Timestamp:** 2026-11-11 23:34–00:22 IST  
**Command Executed:** `"C:\Users\kiran\AppData\Local\Programs\coderabbit\cr.exe" review --committed --base master --agent`  
**Branch / Base:** `remediation-phase1-audit` (`8678089b9a267aa54c2f6434224470e8c939b775`) vs `master` (`fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2`)  
**Outcome:** `review_completed` | **Total Findings Reported:** `15` (all tagged `major` by CodeRabbit; `0` critical/minor)  
**Raw Log Archive:** `.system_generated/steps/3733/output.txt`  

---

## Summary Index of Initial CodeRabbit Findings

| Finding ID | CodeRabbit Severity | File | Lines | Title |
|:---|:---|:---|:---|:---|
| `CR-01` | `major` | `docs/NOV17_RETENTION_UPDATE_RUNBOOK.md` | 54–57, 65, 79–80 | The runbook instructs status values that the import script rejects |
| `CR-02` | `major` | `docs/FINAL_SUBMISSION_MANIFEST.md` | 18–24, 33–40 | The submission manifest certifies a superseded archive and synthetic raw files |
| `CR-03` | `major` | `src/dashboard/analytics.py` | 128–131, 159–160 | The bowler phase economy leaves out wide and no-ball runs |
| `CR-04` | `major` | `docs/PUBLIC_PLAYER_INTELLIGENCE.md` | 70–79, 97–108 | Ledger states Tier 1 facts contradicting audited ledger and cites future verification dates |
| `CR-05` | `major` | `docs/ROUND1_OFFICIAL_SCOPE_VERIFICATION.md` | 50, 64, 83 | Document tells user to upload a different methodology PDF than the handover does |
| `CR-06` | `major` | `scripts/generate_methodology_pdf.py` | 335–353, 495 | Official 5-page report states methodology code does not run and cites superseded archive hash |
| `CR-07` | `major` | `docs/FINAL_PLAYER_CLAIMS_VERIFICATION.md` | 28–31, 95–97, 122–125, 134–137 | Certified availability claims contradict audited 11 Nov market ledger and CSV stats |
| `CR-08` | `major` | `scripts/hybrid_validation_gate.py` | 446–452 | Chase label `bat_won` comes from `team_runs_before` on final delivery |
| `CR-09` | `major` | `scripts/hybrid_validation_gate.py` | 104–122, 211–218, 538–561 | Validation gate writes hard-coded verdicts and metrics, not computed results |
| `CR-10` | `major` | `scripts/build_market_intelligence.py` | 391–397, 480–482 | Rerun overwrites master ledger, immutable 11 Nov snapshot, and change log |
| `CR-11` | `major` | `docs/CRITICAL_CHALLENGE_REPORT.md` | 286–287 | Official Top-10 lists do not match the frozen CSVs |
| `CR-12` | `major` | `scripts/hybrid_validation_gate.py` | 671–688, 741–755 | Baseline Model A comparison is a simplified reimplementation, not frozen Model A |
| `CR-13` | `major` | `scripts/build_competition_dossier.py` | 28–53 | Wrong player IDs in `strat_b` and `strat_w` cause 13/20 top-10 players to fall back to defaults |
| `CR-14` | `major` | `src/dashboard/data_loader.py` | 196–212 | Bowler slice economy leaves out wide and no-ball runs |
| `CR-15` | `major` | `scripts/reproduce_ml_metrics.py` | 75–77, 84–88 | `bat_won` uses `team_runs_before` on last row; LightGBM values copied from stored dict |

---

## Verbatim Captured CLI Output (Key Records)

```text
{"type":"review_context","reviewType":"committed","currentBranch":"remediation-phase1-audit","baseBranch":"master","workingDirectory":"C:/Users/kiran/OneDrive/Documents/Desktop/SuperRR"}
{"type":"complete","status":"review_completed","findings":15,"outcome":"completed","message":"Review completed"}
```

### Detailed Verbatim Comments by Finding

#### `CR-01` — `docs/NOV17_RETENTION_UPDATE_RUNBOOK.md` (lines 54–57, 65, 79–80)
> Step 1 tells analysts to set `official_retention_status` to `Officially retained` or `Officially released`. `VALID_STATUSES` in `import_market_retentions.py` accepts only the six strict values, so the 17 Nov import fails with "Status validation error". The runbook has three more errors:
> - Line 65 says 14 required columns. `REQUIRED_COLUMNS` has 19.
> - Line 79 says the import updates a dashboard "View E". `app.py` shows only the pinned `market_snapshot_nov11`, so applied updates do not appear outside the change-log tab.
> - Line 80 promises a byte-for-byte check. The script only compares the top player names.

#### `CR-02` — `docs/FINAL_SUBMISSION_MANIFEST.md` (lines 18–24, 33–40)
> Lines 18-20 give a size of 62,190,479 bytes, 546 files, and SHA `0f62506a...`. Every later audit certifies 62,296,913 bytes, 569 files, and SHA `76059a8f...`. Lines 35-40 list the six synthetic CSV names that `NOV15_DATA_PROVENANCE_AUDIT.md` retracts.

#### `CR-03` — `src/dashboard/analytics.py` (lines 128–131, 159–160)
> `sub` keeps only rows with `is_legal_ball == 1`. `runs_c` therefore sums `bowler_runs_conceded` over legal balls only. The project's MCC rule, stated in `FINAL_BOWLER_RANKING_AUDIT.md` §2, charges illegal-delivery runs to the bowler. Sum runs over all deliveries in the phase, and divide by the legal balls.

#### `CR-04` — `docs/PUBLIC_PLAYER_INTELLIGENCE.md` (lines 70–79, 97–108)
> Shepherd is "Unretained / Open Auction" (line 70) [ledger: RCB `Pending Verification`]; Jitesh is "Open Auction" (line 73) [ledger: RCB]; Buttler is "Rajasthan Royals" (line 75) [ledger: GT]; Ellis is "Open Auction" (line 79) [ledger: `Confirmed Trade` SRH]. Lines 98, 102, 104, 108 cite verification dates of 12 and 14 November 2026 and a CSK CEO statement without URLs.

#### `CR-05` — `docs/ROUND1_OFFICIAL_SCOPE_VERIFICATION.md` (lines 50, 64, 83)
> Says to upload `docs/PRESSUREIQ_FINAL_METHODOLOGY_REPORT.pdf` (14-page report) while `NOV14_SUBMISSION_HANDOVER.md` lines 143 and 183 and `NOV13` line 143 say to upload `PRESSUREIQ_METHODOLOGY_REPORT.pdf` (5-page report). The two generators describe different formulas.

#### `CR-06` — `scripts/generate_methodology_pdf.py` (lines 335–353, 495)
> States legacy formulas (`BPI = 0.40/0.30/0.15/0.15`, `lambda_wkt = 2.50`, pillar weights `35/20/20/15/10`, `K = 15`, `beta +-0.50`) and cites ZIP SHA `0f62506a...` instead of `76059a8f...`, plus prints literal `$$...$$` in ReportLab.

#### `CR-07` — `docs/FINAL_PLAYER_CLAIMS_VERIFICATION.md` (lines 28–31, 95–97, 122–125, 134–137)
> Claims Pathirana is CSK retention (ledger: KKR), Buttler is RR icon (ledger: GT), Ellis has High Auction Availability (ledger: `Confirmed Trade` SRH), Shepherd is with MI (ledger: RCB); plus Naman Dhir 826 runs / 140.2 SR instead of 992 / 168.4 and Pooran raw PAVA +0.320 instead of +0.445.

#### `CR-08` — `scripts/hybrid_validation_gate.py` (lines 446–452)
> `final_runs=("team_runs_before", "last")` takes the score before the last ball, classifying final-ball chase wins as `bat_won = 0`.

#### `CR-09` — `scripts/hybrid_validation_gate.py` (lines 104–122, 211–218, 538–561)
> Hard-codes `verification_status = "ALL_NUMBERS_VERIFIED_EXACT_MATCH"`, `"Violations=0"`, `raw_test_2026` literal dict, and `0.0514` vs `0.0766`.

#### `CR-10` — `scripts/build_market_intelligence.py` (lines 391–397, 480–482)
> Unconditionally overwrites master template, 11 Nov snapshot, and change log on rerun without `--force` guard.

#### `CR-11` — `docs/CRITICAL_CHALLENGE_REPORT.md` (lines 286–287)
> Lists wrong Official Top-10 Batters and Bowlers inconsistent with frozen `final_*_rankings.csv`.

#### `CR-12` — `scripts/hybrid_validation_gate.py` (lines 671–688, 741–755)
> Reimplements a simplified proxy baseline (153 total-delivery bowlers, single PAVA, cohort-mean prior) rather than comparing against frozen `final_*_rankings.csv`.

#### `CR-13` — `scripts/build_competition_dossier.py` (lines 28–53)
> `strat_b`, `strat_w`, and watchlist map outdated player IDs causing 13 of 20 official top-10 players to fall back to `("Target", "Key player")`, with stale Ellis/Pathirana notes.

#### `CR-14` — `src/dashboard/data_loader.py` (lines 196–212)
> Filters `d.is_legal_ball = 1`, excluding wides/no-balls from `SUM(d.bowler_runs_conceded)` in Slice Econ.

#### `CR-15` — `scripts/reproduce_ml_metrics.py` (lines 75–77, 84–88)
> Same `team_runs_before` chase label bug and reads stored `engine.benchmark_results` instead of computing LightGBM predictions on identical records.

