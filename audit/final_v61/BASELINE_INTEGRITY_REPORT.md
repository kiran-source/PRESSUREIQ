# BASELINE INTEGRITY AUDIT REPORT
## Verification of Frozen Baseline Hashes, Git Lineage, and Immutability Safeguards

**Audit Protocol:** PRESSUREIQ V6.1 Independent Certification  
**Audit Timestamp:** 2026-11-14T21:45:00+05:30  
**Auditor:** Independent Quantitative Review & Baseline Certification Lead  
**Audit Directory:** `audit/final_v61/`  
**Verdict:** **PASS — 100% BIT-FOR-BIT INVARIANCE (0.00 DRIFT)**

---

### 1. Git Repository & Working Tree State

| Parameter | Recorded Value | Verification Status |
|---|---|---|
| **Active Working Branch** | `redesign-editorial-v4` | Verified (`git branch -v`) |
| **Active Branch HEAD Commit** | `ff0a25bf838e18b906a11bae660cf0eac8d34165` | Cleanly committed |
| **Implementation Commit** | `f7e046457c49aeef136d8108b7f70bfda5600f78` | Verified (`git show f7e0464`) |
| **Path Resolution Hotfix Commit** | `ff0a25bf838e18b906a11bae660cf0eac8d34165` | Verified (`sys.path` injection) |
| **Remote Synchronization** | Up to date with `origin/redesign-editorial-v4` | Verified (`git status`) |
| **Git Working Tree Status** | Clean (no uncommitted or untracked modifications) | Verified (`nothing to commit`) |
| **Frozen Master Branch HEAD** | `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2` | **100% EXACT MATCH** |

---

### 2. Cryptographic SHA-256 Hash Verification

To guarantee that the Model B recruitment intelligence implementation has not modified, corrupted, or drifted from the canonical Model A competition deliverables, SHA-256 checksums were independently computed from raw bytes and verified against the certified baseline hashes:

```
[AUDIT VERIFICATION CMD]
python -c "import hashlib
def h(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
print('Batters:', h('data/processed/final_batter_rankings.csv'))
print('Bowlers:', h('data/processed/final_bowler_rankings.csv'))
print('Archive:', h('PRESSUREIQ_Final_Submission.zip'))"
```

| Canonical Deliverable File | Expected Certified SHA-256 Hash | Independently Computed Live Hash | Audit Status | Drift |
|---|---|---|---|---|
| `data/processed/final_batter_rankings.csv` | `887f0c104047eb7b5c7d662b83600bacaf6263fa7162fc343b27800760b99b87` | `887f0c104047eb7b5c7d662b83600bacaf6263fa7162fc343b27800760b99b87` | **MATCH** | **0.000%** |
| `data/processed/final_bowler_rankings.csv` | `344d63c55cecc7bce9de3cd06d82b6ac8217fcd448bb3f2e93d55da314f1e7bb` | `344d63c55cecc7bce9de3cd06d82b6ac8217fcd448bb3f2e93d55da314f1e7bb` | **MATCH** | **0.000%** |
| `PRESSUREIQ_Final_Submission.zip` | `76059a8f5f8b8de5126a5ed8b2a9378fb6664016989f3125df7ca4bbbe9696db` | `76059a8f5f8b8de5126a5ed8b2a9378fb6664016989f3125df7ca4bbbe9696db` | **MATCH** | **0.000%** |

---

### 3. Model A Official Ranking Preservation Audit

The top-10 official rankings from Model A were independently checked to ensure zero modification:

#### Official Model A Batters (Top 10 Immutable Global Rankings)
| Rank | Player Name | Reliability Score | PRC Archetype | 95% CI | Model A Integrity |
|---|---|---|---|---|---|
| **1** | Ruturaj Gaikwad | 91.82 | Ice Cold Anchor | [87.52 – 93.63] | **UNTOUCHED** |
| **2** | Rohit Sharma | 91.43 | Clutch Climber | [86.99 – 93.30] | **UNTOUCHED** |
| **3** | Suryakumar Yadav | 91.07 | Clutch Climber | [86.13 – 92.74] | **UNTOUCHED** |
| **4** | Nicholas Pooran | 90.72 | Clutch Climber | [84.95 – 92.35] | **UNTOUCHED** |
| **5** | Heinrich Klaasen | 90.58 | Clutch Climber | [85.50 – 92.20] | **UNTOUCHED** |
| **6** | Sanju Samson | 89.96 | Clutch Climber | [84.77 – 91.95] | **UNTOUCHED** |
| **7** | Shivam Dube | 89.28 | Clutch Climber | [82.52 – 90.87] | **UNTOUCHED** |
| **8** | Yashasvi Jaiswal | 88.59 | Clutch Climber | [82.90 – 90.95] | **UNTOUCHED** |
| **9** | Riyan Parag | 88.58 | Ice Cold Anchor | [82.54 – 90.74] | **UNTOUCHED** |
| **10** | Hardik Pandya | 88.24 | Ice Cold Anchor | [82.02 – 90.35] | **UNTOUCHED** |

#### Official Model A Bowlers (Top 10 Immutable Global Rankings)
| Rank | Player Name | Reliability Score | PRC Archetype | 95% CI | Model A Integrity |
|---|---|---|---|---|---|
| **1** | Liam Dawson | 95.40 | Clutch Climber | [74.17 – 98.08] | **UNTOUCHED** |
| **2** | Prince Yadav | 92.93 | Clutch Climber | [73.57 – 96.79] | **UNTOUCHED** |
| **3** | Shoriful Islam | 91.82 | Clutch Climber | [70.52 – 96.22] | **UNTOUCHED** |
| **4** | Tim Southee | 91.44 | Clutch Climber | [73.55 – 95.74] | **UNTOUCHED** |
| **5** | Jason Holder | 91.29 | Clutch Climber | [72.24 – 95.79] | **UNTOUCHED** |
| **6** | Dasun Shanaka | 91.13 | Clutch Climber | [72.33 – 95.66] | **UNTOUCHED** |
| **7** | Mohammad Nabi | 91.06 | Clutch Climber | [71.49 – 95.64] | **UNTOUCHED** |
| **8** | Lungi Ngidi | 90.64 | Clutch Climber | [72.48 – 95.34] | **UNTOUCHED** |
| **9** | Jasprit Bumrah | 90.43 | Ice Cold Anchor | [84.14 – 92.95] | **UNTOUCHED** |
| **10** | Sikandar Raza | 90.04 | Clutch Climber | [71.74 – 95.03] | **UNTOUCHED** |

---

### 4. Git History & Isolation Verification

Inspection of commits `f7e0464` and `ff0a25b`:
- **Files Modified in `f7e0464`:** 38 files added/modified.
- **Files Modified in `ff0a25b`:** 1 file modified (`src/dashboard/app.py`).
- **Model A Files Touched:** **0 (None)**.
- **Master Branch:** Local `master` branch is preserved at `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2` with 0 uncommitted changes.
- **Automated Baseline Test:** `tests/test_audit_remediation.py::test_frozen_baseline_integrity` executed and **PASSED**.

**Conclusion:** The baseline integrity audit is completely satisfied. The Model A competition deliverables remain immutable, reproducible, and verifiable.
