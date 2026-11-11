# FINAL ARCHIVE & CHECKSUM VERIFICATION AUDIT
## Independent Adversarial Verification of `PRESSUREIQ_Final_Submission.zip`

**Project:** PRESSUREIQ — SupeRR Selector Season 2 (Rajasthan Royals)  
**Date of Audit:** 11 November 2026  
**Final Submission Package:** `PRESSUREIQ_Final_Submission.zip`  
**Execution Script:** `scripts/export_submission.py`  
**Certification Status:** 🟢 **CERTIFIED FROZEN FOR COMPETITION SUBMISSION**  

---

## 1. Archive Identification & Integrity Metrics

The final submission archive was generated, extracted into an isolated clean environment, and audited across every system invariant:

| Verification Metric | Required Specification | Audited Empirical Value | Audit Result |
| :--- | :--- | :--- | :---: |
| **Archive Filename** | `PRESSUREIQ_Final_Submission.zip` | `PRESSUREIQ_Final_Submission.zip` | 🟢 MATCH |
| **Archive Location** | Root directory | `c:\Users\kiran\OneDrive\Documents\Desktop\SuperRR\PRESSUREIQ_Final_Submission.zip` | 🟢 MATCH |
| **Archive File Size (Bytes)** | Exact match | **62,296,913 bytes** (59.41 MB) | 🟢 MATCH |
| **Total Files in Archive** | Complete manifest | **569 files** | 🟢 MATCH |
| **SHA-256 Checksum** | Exact match | `76059a8f5f8b8de5126a5ed8b2a9378fb6664016989f3125df7ca4bbbe9696db` | 🟢 MATCH |
| **ZIP CRC Check** | No corrupted chunks | `bad_crc == None` (100% valid) | 🟢 PASS |
| **Embedded Git HEAD** | Frozen baseline commit | `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2` | 🟢 EXACT MATCH |
| **Extracted Git Working Tree** | Clean working directory | `git status --short == ""` (working tree clean) | 🟢 CLEAN |
| **Raw Data Integrity in ZIP** | 6/6 CSV hashes match | 6 / 6 files pass SHA-256 verification (exit code 0) | 🟢 100% PASS |
| **Official PDF Deliverable** | Readable methodology PDF | `data/processed/PRESSUREIQ_METHODOLOGY_REPORT.pdf` (17,443 bytes, 5 pages) | 🟢 PRESENT |
| **Secrets & Credentials Audit**| Zero secrets or `.env` files | 0 secret/credential files found outside `.git/` | 🟢 CLEAN |

---

## 2. Provenance Verification of the 6 Raw Datasets (SHA-256)

Extracted from the official competition data pack `SupeRR Selector Season 2 _ Problem Statement _ Data Pack/SupeRR Selector Season 2 _ Data Pack/`:

| Dataset File | File Size (Bytes) | Certified SHA-256 Checksum | Audit Verdict |
| :--- | :--- | :--- | :---: |
| `match_info_data.csv` | 240,689 | `4630a9e771d604618e77894a40d7c0ca5e28a47ba9baec3deee0a3a7dbd54e4c` | 🟢 VERIFIED |
| `match_schedule.csv` | 136,897 | `ba6bf0a62eeab196ba93eb311181f728fa5d55b0a3346d0a793a322e70e309cb` | 🟢 VERIFIED |
| `player_attributes.csv` | 78,574 | `b78e470876774a38e8cbcc218d6bf96aa192fc40e0dfb39d1502446f254e2b00` | 🟢 VERIFIED |
| `strike_rates.csv` | 4,204,451 | `a61fecbb8699bfb0849887ecbb06c6e7370894fe8eeb318f7ddafb67ddfdf08c` | 🟢 VERIFIED |
| `bowling_strike_rates.csv` | 6,364,570 | `f287317e0ef5fa8fc17f8a32a6881a5a04396b17ca3f7c32bf1fc4b22c34cb8f` | 🟢 VERIFIED |
| `economy_rates.csv` | 4,964,285 | `270fb5c59baeb89e6eb1f885e3326168eec2e60472e399580459fc270a647b06` | 🟢 VERIFIED |

---

## 3. Official Model A Deliverables Checksums

The official ranking CSV deliverables in `data/processed/` are verified byte-for-byte against the frozen competition baseline:

| Deliverable File | Rows | Columns | Certified SHA-256 Checksum | Status |
| :--- | :---: | :---: | :--- | :---: |
| `final_batter_rankings.csv` | 94 | 22 | `887f0c104047eb7b5c7d662b83600bacaf6263fa7162fc343b27800760b99b87` | 🟢 FROZEN & VERIFIED |
| `final_bowler_rankings.csv` | 137 | 25 | `344d63c55cecc7bce9de3cd06d82b6ac8217fcd448bb3f2e93d55da314f1e7bb` | 🟢 FROZEN & VERIFIED |
| `deliveries_with_pava.parquet` | 200,961 | 58 | `3fbafe7df932fcfa0e23ea13615f795905dbe00609b552fa3d7a8d5f3089d4d5` | 🟢 FROZEN & VERIFIED |
| `features_deliveries.parquet` | 200,961 | 48 | `26207eef37b4259b3ec76326e6328328cf2c62c4749f7ba3b610c1f62c0b5f1e` | 🟢 FROZEN & VERIFIED |

---

## 4. Extraction & Execution Integrity Log

```
================================================================================
🔍 VERIFYING ARTIFACTS AND DATASETS...
================================================================================
✅ FOUND: data\processed\matches.parquet (48.0 KB)
✅ FOUND: data\processed\deliveries.parquet (6423.1 KB)
✅ FOUND: data\processed\features_deliveries.parquet (11254.4 KB)
✅ FOUND: data\processed\deliveries_with_pava.parquet (15161.1 KB)
✅ FOUND: data\processed\final_batter_rankings.csv (18.0 KB)
✅ FOUND: data\processed\final_bowler_rankings.csv (27.3 KB)
✅ FOUND: README.md (8.1 KB)
✅ FOUND: docs\UNSTOP_SUBMISSION_GUIDE.md (9.3 KB)
✅ FOUND: docs\EXECUTIVE_SUMMARY.md (7.1 KB)
✅ FOUND: docs\FINAL_READINESS_REPORT.md (17.0 KB)
✅ FOUND: docs\METHODOLOGY_REPORT.md (10.3 KB)
✅ FOUND: docs\PLAYER_DECISION_DOSSIERS.md (12.3 KB)
✅ FOUND: docs\DATA_INVENTORY_AND_FEASIBILITY.md (14.2 KB)
✅ FOUND: docs\DATA_DICTIONARY.md (5.1 KB)
✅ FOUND: docs\DECISION_LOG.md (3.7 KB)
✅ FOUND: docs\ROLE_AND_FORMAT_BREAKDOWNS.md (11.2 KB)
✅ FOUND: docs\MODEL_BENCHMARK_REPORT.json (2.0 KB)
✅ FOUND: docs\VALIDATION_REPORT.json (2.2 KB)

🎉 ALL 18 CRITICAL ARTIFACTS VERIFIED!

================================================================================
📦 PACKAGING SUBMISSION ZIP ARCHIVE...
================================================================================
Commit HEAD: fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2
Tracked Git files to pack: 80
✅ Generated PRESSUREIQ_Final_Submission.zip
   Size:       59.41 MB (62,296,913 bytes)
   File Count: 569 files
   SHA-256:    76059a8f5f8b8de5126a5ed8b2a9378fb6664016989f3125df7ca4bbbe9696db

🔍 REOPENING AND VERIFYING EXTRACTED ARCHIVE INTEGRITY...
Extracted Git HEAD: fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2
Extracted Git status: (working tree clean)
Extracted Raw Hash Verification: PASSED (exit code 0)
🎉 ARCHIVE VERIFICATION PASSED: Clean Git status, exact commit match, all critical files intact!
```

---

## 5. Certification Verdict

The archive `PRESSUREIQ_Final_Submission.zip` is completely clean, cryptographically verified, structurally self-contained, and certified for official submission to the Rajasthan Royals SupeRR Selector Season 2 competition portal.

