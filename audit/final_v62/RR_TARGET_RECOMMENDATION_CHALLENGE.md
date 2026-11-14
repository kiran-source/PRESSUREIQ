# RAJASTHAN ROYALS TARGET RECOMMENDATIONS CHALLENGE (CHECK 3)
## Adversarial Audit of the 33 Target Entries, Nationality Misclassifications, and Dual-Role Accounting

**Audit Protocol:** PRESSUREIQ V6.2 Final Evidence Challenge  
**Audit Directory:** `audit/final_v62/`  
**Reviewer Role:** Adversarial Cricket Analytics Auditor & Franchise Roster Compliance Lead  
**Audit Scope:** 33 Target Entries across `rr_model_b_target_batters.csv` and `rr_model_b_target_bowlers.csv`  
**Overall Finding:** **HIGH-SEVERITY DATA FINDING DETECTED (NATIONALITY MAPPING FALLBACK)**  
**Status:** **READY AFTER EVIDENCE CORRECTIONS**

---

### 1. Critical Finding: International Player Nationality Fallback Defect

#### The Evidence:
An inspection of `rr_model_b_target_batters.csv` and `rr_model_b_target_bowlers.csv` revealed that several prominent overseas international players are misclassified with `nationality = 'India'` and `is_overseas = False`:

```
[VERIFIED DEFECT IN TARGET CSV ARTIFACTS]
┌────────────────────────┬──────────────────────┬─────────────┬───────────────────────────┐
│ Player Name            │ Recorded Nationality │ Is Overseas │ Actual True Nationality   │
├────────────────────────┼──────────────────────┼─────────────┼───────────────────────────┤
│ Sikandar Raza          │ India (False)        │ False       │ Zimbabwe (Overseas)       │
│ Sherfane Rutherford    │ India (False)        │ False       │ West Indies (Overseas)    │
│ Moeen Ali              │ India (False)        │ False       │ England (Overseas)        │
│ Dasun Shanaka          │ India (False)        │ False       │ Sri Lanka (Overseas)      │
│ Glenn Phillips         │ India (False)        │ False       │ New Zealand (Overseas)    │
└────────────────────────┴──────────────────────┴─────────────┴───────────────────────────┘
```

#### Root Cause Analysis:
In `scripts/build_rr_recruitment_model_b.py`, line 146 & line 246:
```python
nat = KNOWN_NATIONALITIES.get(pname, "India" if latest_ipl != "None" else "International")
is_ov = (nat != "India")
```
When an overseas player played for an IPL franchise in previous seasons (e.g., Moeen Ali for CSK, Sikandar Raza for PBKS, Glenn Phillips for SRH, Sherfane Rutherford for KKR), `latest_ipl != 'None'` evaluated to `True`. Because these specific players were omitted from the initial `KNOWN_NATIONALITIES` dictionary in `build_rr_recruitment_model_b.py`, the fallback logic defaulted their nationality to `"India"`.

#### Regulatory & Franchise Roster Risk:
Under official BCCI/IPL roster regulations:
- Each franchise is permitted a maximum of **8 overseas players** in their total squad and **4 overseas players** in the Playing XI.
- If Rajasthan Royals' recruitment team drafted Moeen Ali or Sikandar Raza under the assumption that they do not consume an overseas roster slot (as indicated by `is_overseas == False`), RR would violate official squad composition rules.
- **Auditor Action:** This finding is logged as **FINDING-01 (HIGH SEVERITY)**. In accordance with audit rules, we do not silently modify the output; we document the exact proposed remediation.

---

### 2. Dual-Qualified All-Rounder Accounting (Avoiding Double-Counting)

#### The Overlap:
The target boards present 14 target batters and 19 target bowlers. A set-theoretic intersection reveals **5 dual-qualified all-rounders**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                      33 Total Role Entries (28 Unique Athletes)                         │
├────────────────────────┬───────────────────────────────┬───────────────────────────────┤
│ Player Name            │ Batting Target Board Position │ Bowling Target Board Position │
├────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ Sikandar Raza          │ Rank 4 Target Batter (78.80)  │ Rank 5 Target Bowler (88.92)  │
│ Moeen Ali              │ Rank 6 Target Batter (78.24)  │ Rank 9 Target Bowler (85.14)  │
│ Mohammad Nabi          │ Rank 7 Target Batter (77.68)  │ Rank 16 Target Bowler (73.95) │
│ Dasun Shanaka          │ Rank 9 Target Batter (76.15)  │ Rank 13 Target Bowler (78.54) │
│ Jason Holder           │ Rank 10 Target Batter (76.10) │ Rank 10 Target Bowler (82.08) │
└────────────────────────┴───────────────────────────────┴───────────────────────────────┘
```

#### Analytical Justification & Safeguards:
1. **Legitimate Dual Evaluation:** In modern franchise cricket, genuine all-rounders provide two distinct tactical utility streams. Evaluating them independently against batting needs (middle-overs finishing) and bowling needs (spin/seam control) is sound decision science.
2. **Double-Counting Prevention:**
   - In executive budget allocation, drafting one of these players consumes **1 squad slot**, not 2.
   - The total actionable talent pool consists of **28 unique athletes**, not 33.
   - The submission presentation must explicitly highlight: *"28 unique auction targets offering 33 role-execution options, featuring 5 high-utility all-rounders."*

---

### 3. Sample-Size Sufficiency & Extreme-Low Evidence Cases

The audit examined high-pressure delivery counts ($N_{hp}$) across all 33 targets:

| Target Player | Target Discipline | High-Pressure Deliveries ($N_{hp}$) | Evidence Tier | Analytical Risk & Assessment |
|---|---|---|---|---|
| **Liam Dawson** | Bowler | 83 balls | High Empirical Evidence | Top global rating backed by first-class and international evidence. |
| **Ashutosh Sharma** | Batter | 369 balls (245 death balls) | High Empirical Evidence | Exceptional death-overs sample ($SR = 175.5$). Solid statistical backing. |
| **Spencer Johnson** | Bowler | 136 balls | High Empirical Evidence | Verified express pace sample. |
| **Jamie Smith** | Batter | 68 balls | Medium Sample | Explosive metrics ($SR = 191.2$), but smaller tournament sample. |
| **Tanush Kotian** | Bowler | **0 balls** | **Low In-Dataset Evidence** | Did not bowl in the tournament delivery dataset. Score relies heavily on domestic Ranji/SMAT heuristic and squad-fit prior. |
| **Darwish Rasooli** | Batter | **38 balls** | **Low In-Dataset Evidence** | Small sample in high-pressure tiers ($N < 40$). Should be flagged for visual scouting. |

---

### 4. Squad-Fit & Alternative Comparability Verification

1. **Liam Dawson vs. Allah Ghazanfar / Tanush Kotian:**
   - *Fit Claim:* Defensive finger-spin control on 78m Jaipur boundary ropes.
   - *Audit Verdict:* **VALID.** Dawson's 6.8 rpo middle-overs economy directly matches the tactical requirement. Ghazanfar is an appropriate alternative (mystery spin fallback).
2. **Spencer Johnson vs. FazalHaq Farooqi:**
   - *Fit Claim:* Overseas express left-arm death pace.
   - *Audit Verdict:* **VALID.** Johnson's 145kph+ trajectory is an authentic point of difference from Sandeep Sharma's 125kph medium-pace. Farooqi provides swing security as fallback.
3. **Ashutosh Sharma vs. Jamie Smith / Nehal Wadhera:**
   - *Fit Claim:* No. 7 pace-hitting crisis finisher.
   - *Audit Verdict:* **VALID.** Ashutosh provides domestic Indian slot efficiency, preserving RR's 4-overseas limit.

---

### 5. Summary & Remediation Requirement
All 33 targets pass eligibility and availability gating. However, **FINDING-01** (nationality misclassification of Raza, Rutherford, Moeen, Shanaka, and Phillips) must be remediated in `scripts/build_rr_recruitment_model_b.py` before final competition submission.
