# PRESSUREIQ Dashboard — CodeRabbit Review & Remediation Audit Log

**Branch:** `dashboard-ui-v3`  
**Base Commit:** `82e77b262aa06802c791c792c1e59507824a15f1`  
**Frozen Baseline (`master`):** `fc0e622c10d49b4b484c6ddd0e6fdde4f76091c2`  
**CLI Tool:** CodeRabbit CLI `v0.9.5` (`cr review --committed`)  
**Audit Date:** 12 November 2026  

---

## 1. Review Summary & Pass History

| Pass | Target Range / Commits | Findings Reported | Critical | Major | Minor | Remediation Commit | Status |
|:---|:---|:---:|:---:|:---:|:---:|:---|:---:|
| **Pass 1** | `82e77b2..f199482` | **9** | 0 | 3 | 6 | `735287e` | **Resolved** |
| **Pass 2** | `f199482..735287e` | **1** | 0 | 0 | 1 | `462a37b` | **Resolved** |
| **Pass 3** | `735287e..462a37b` | **0** | 0 | 0 | 0 | `462a37b` | **Clean / Complete** |
| **Pass 4 (v4 Editorial)** | `dashboard-ui-v3..5117872` | **1** | 0 | 1 | 0 | `6fac083` | **Resolved** |
| **Pass 5 (v4 Editorial)** | `5117872..6fac083` | **2** | 0 | 0 | 2 | `04ad952` | **Resolved** |
| **Pass 6 (v4 Final)** | `dashboard-ui-v3..04ad952` | **0** | 0 | 0 | 0 | `04ad952` | **Clean / Complete** |
| **Pass 7 (Audit Polish)** | `04ad952..57c81f8` | **3** | 0 | 0 | 3 | `028e82c` | **Resolved** |
| **Pass 8 (Delta Verification)** | `57c81f8..028e82c` | **0** | 0 | 0 | 0 | `028e82c` | **Clean / Complete** |

---

## 2. Pass 1 Detailed Findings & Remediation Matrix (`82e77b2..f199482`)

### Finding 1: Include confirmed retentions and releases in the franchise status
- **File:** `src/dashboard/analytics.py:427`
- **Severity:** Minor
- **CodeRabbit Diagnostic:** If a team had confirmed retentions or confirmed releases but zero trades or pending entries, the expression defaulted to `Historical (2026 Roster)`.
- **Root Cause:** Conditional logic evaluated only `conf_trades_in > 0` and `pending_cnt > 0`.
- **Remediation Applied:** Extended branching to check `conf_ret` and `conf_rel`:
  ```python
  if conf_trades_in > 0:
      status_label = "Confirmed Trade Active"
  elif conf_ret > 0 and conf_rel > 0:
      status_label = "Confirmed Retained & Released"
  elif conf_ret > 0:
      status_label = "Confirmed Retention Active"
  elif conf_rel > 0:
      status_label = "Confirmed Release Active"
  elif pending_cnt > 0:
      status_label = "Pending Verification (Nov 17)"
  elif has_2026_coverage:
      status_label = "Historical (2026 Roster)"
  else:
      status_label = "Missing 2026 Coverage"
  ```
- **Verification:** Unit test `test_coderabbit_findings_remediation()` in `tests/test_dashboard_data.py` asserts CSK (`Confirmed Retention Active`), RCB (`Confirmed Release Active`), and KKR (`Confirmed Retained & Released`).

---

### Finding 2: Do not label an all-season fallback as the IPL 2026 roster
- **File:** `src/dashboard/analytics.py:401`
- **Severity:** Minor
- **CodeRabbit Diagnostic:** If a franchise lacked matching IPL 2026 rows, fallback pulled players across all historical seasons while labeling the column `IPL 2026 Dataset Roster`.
- **Root Cause:** `else: squad_ids = set(pl[pl["team_name"] == team_name]["player_id"].tolist())` was overly permissive.
- **Remediation Applied:** Removed the all-season fallback entirely. Added explicit `has_2026_coverage = bool(squad_ids)`. If absent, reports `0` squad size, `Missing IPL 2026 Rows`, and `N/A (No 2026 Roster)`.
- **Verification:** Tested in `test_coderabbit_findings_remediation()` with a dummy franchise having only 2024 records; confirms 0 roster count and `Missing IPL 2026 Rows` indicator.

---

### Finding 3: Keep each player's color consistent across comparison charts
- **File:** `src/dashboard/charts.py:469`
- **Severity:** Minor
- **CodeRabbit Diagnostic:** `fig_multi_player_radar` assigned colors in selection order, while `fig_multi_player_ci_bars` sorted by reliability score before coloring, causing colors to swap when lower-scoring players were selected first.
- **Root Cause:** Color index was coupled to sorted bar positions rather than player identities.
- **Remediation Applied:** Introduced `build_player_color_map(player_names)` producing a deterministic `{player_name: color}` dictionary keyed by original selection order. Passed `color_map` consistently across `fig_multi_player_radar`, `fig_multi_player_ci_bars`, `fig_multi_player_prc_overlay`, and phase breakdown bar chart.
- **Verification:** Verified in `test_coderabbit_findings_remediation()` and visually checked in `04_player_comparison_desktop.png`.

---

### Finding 4: Keep the Featured Top 10 limit when the sort order changes
- **File:** `src/dashboard/views/overview_and_leaderboards.py:264`
- **Severity:** Minor
- **CodeRabbit Diagnostic:** If the user selected `Featured Top 10` and any non-default sort column, the full filtered cohort was displayed instead of 10 rows.
- **Root Cause:** Guard condition was `if scope_mode == "Featured Top 10" and sel_sort == "Official Model A Rank (Default)"`.
- **Remediation Applied:** Simplified condition to `display_df = filtered.head(10).copy() if scope_mode == "Featured Top 10" else filtered.copy()`.
- **Verification:** Manual check and Playwright E2E assertion confirmed 10 rows rendered under all sort configurations.

---

### Finding 5: Apply an empty season or format slice to the results
- **File:** `src/dashboard/views/overview_and_leaderboards.py:256`
- **Severity:** Major
- **CodeRabbit Diagnostic:** If a season/format combination returned no deliveries, `if not slice_df.empty:` skipped the merge, retaining all-season players instead of displaying the empty state.
- **Root Cause:** Silent fallback to all-season cohort when slice returned 0 matching rows.
- **Remediation Applied:** Wrapped slice query in explicit exception handling and file existence checks. When `slice_df.empty`, sets `filtered = filtered.iloc[0:0].copy()`, cleanly triggering `render_empty_state()`.
- **Verification:** Validated via unit test and Playwright browser check.

---

### Finding 6: Compare the market snapshot checksum before reporting verification
- **File:** `src/dashboard/views/methodology_and_provenance.py:134`
- **Severity:** Major
- **CodeRabbit Diagnostic:** The pinned market snapshot table row always reported `VERIFIED` regardless of whether the observed checksum matched the expected value or was missing.
- **Root Cause:** Hardcoded `"Status": "VERIFIED"` in the provenance row dictionary.
- **Remediation Applied:** Evaluated observed SHA-256 against `FROZEN_MARKET_SNAPSHOT_SHA256`:
  ```python
  if snap_observed == "MISSING" or not snap_observed:
      snap_status = "MISSING"
  elif snap_observed == snap_expected:
      snap_status = "EXACT MATCH"
  else:
      snap_status = "MISMATCH"
  ```
  Exported `FROZEN_MARKET_SNAPSHOT_SHA256` in `src/dashboard/data_loader.py` and recorded `market_snapshot_match` in `integrity_status`.
- **Verification:** Verified runtime reporting in `10_provenance_desktop.png` shows `EXACT MATCH`.

---

### Finding 7: Do not display a missing franchise as `nan`
- **File:** `src/dashboard/views/player_views.py:118-119`
- **Severity:** Minor
- **CodeRabbit Diagnostic:** In player profiles, `if m_row.get("current_verified_franchise"):` evaluated truthy on pandas `float("nan")`, converting missing franchises into the string `"nan"`.
- **Root Cause:** Untyped dictionary lookup on pandas DataFrame row.
- **Remediation Applied:** Checked `pd.notna(raw_curr_team) and str(raw_curr_team).strip() != ""` before updating `mkt_team`.
- **Verification:** Unit test validated that players without a tracked franchise retain `"International / Non-IPL"` or their dataset squad.

---

### Finding 8: Derive the release claim from the loaded watchlist
- **File:** `src/dashboard/views/rr_and_market.py:33-34`
- **Severity:** Major
- **CodeRabbit Diagnostic:** Callout text claimed `0 external watchlist targets are confirmed released` statically, which could contradict the `confirmed_rel_cnt` KPI if the candidate watchlist changed.
- **Root Cause:** Hardcoded `"0"` in callout markdown.
- **Remediation Applied:** Replaced static string with dynamic template:
  ```python
  rel_noun = "target is" if confirmed_rel_cnt == 1 else "targets are"
  render_callout(
      f"... ahead of the 17 November 2026 IPL retention deadline, "
      f"{confirmed_rel_cnt} external watchlist {rel_noun} confirmed released.",
      accent=PALETTE["accent_violet"],
  )
  ```
- **Verification:** Verified dynamic string formatting in `07_rr_intelligence_desktop.png`.

---

### Finding 9: Make the empty-state guidance match the active filters
- **File:** `src/dashboard/views/rr_and_market.py:105-109`
- **Severity:** Minor
- **CodeRabbit Diagnostic:** Empty state always blamed the `Confirmed Released` filter even when `only_rel` was false, telling users to uncheck a box that was already unchecked.
- **Root Cause:** Single generic empty state message regardless of active filter state.
- **Remediation Applied:** Branching logic tailoring title and description depending on whether `only_rel`, an empty `sel_stats`, or a discipline filter caused 0 rows to match.
- **Verification:** Verified via Playwright automated interaction test `rr_empty_state_ok`.

---

## 3. Pass 2 Detailed Findings & Remediation Matrix (`f199482..735287e`)

### Finding 10: Report an empty Market Status selection first
- **File:** `src/dashboard/views/rr_and_market.py:109`
- **Severity:** Minor
- **CodeRabbit Diagnostic:** When a user cleared `sel_stats` and enabled `only_rel`, the empty `sel_stats` cleared `view_t`, but the code reported the `only_rel` message first.
- **Root Cause:** `if only_rel:` preceded `elif not sel_stats:`.
- **Remediation Applied:** Reordered conditionals to evaluate `if not sel_stats:` first:
  ```python
  if view_t.empty:
      if not sel_stats:
          empty_title = "No Market Status selected"
          empty_desc = "Select at least one Market Status value in the filter above to inspect watchlist candidates."
      elif only_rel:
          empty_title = "0 candidates currently satisfy Confirmed Released filter"
          empty_desc = "Expected pre-Nov 17 state: official IPL 2027 release lists have not been submitted yet..."
      else:
          empty_title = "No candidates match the active discipline and market-status filters"
          ...
  ```
- **Verification Commit:** `462a37b`.

---

## 4. Pass 3 Delta Review Verification

- **Command Executed:** `cr review --committed --base 735287e --agent`
- **Base Commit:** `735287e`
- **HEAD Commit:** `462a37b`
- **Findings Reported:** **0 Critical, 0 Major, 0 Minor**
- **Outcome:** Clean review completion. All identified issues across the dashboard architecture are fully remediated and verified.

---

## 5. Pass 4 Kinfolk Luxury Editorial Review (`dashboard-ui-v3..5117872`)

### Finding 11: Do not substitute fixed rankings when ranking data is unavailable
- **File:** `src/dashboard/views/overview_and_leaderboards.py:56-61`
- **Severity:** Major
- **CodeRabbit Diagnostic:** If either ranking frame is empty, fallback defaults passed a named player ("Ruturaj Gaikwad", "Liam Dawson"), score, and confidence interval to `render_editorial_hero` without supporting ranking data while KPI reported "Frozen ranking unavailable."
- **Root Cause:** Hardcoded strings in default fallback variables.
- **Remediation Applied:**
  - Updated `render_editorial_hero()` in `src/dashboard/components.py` to accept `Optional[str]` and `Optional[float]`.
  - When ranking data is empty, renders an honest "Data Unavailable" card with neutral border and "No verified Model A data loaded" description. Never substitutes mock player names or numbers.
  - Updated `overview_and_leaderboards.py` to pass `None` when dataframes are empty.
  - Added unit test in `tests/test_dashboard_data.py`.
- **Remediation Commit:** `6fac083`.

---

## 6. Pass 5 Kinfolk Polish & Responsiveness Review (`5117872..6fac083`)

### Finding 12: Allow the hero columns to shrink on narrow screens
- **File:** `src/dashboard/components.py:168`
- **Severity:** Minor
- **CodeRabbit Diagnostic:** Columns had fixed `min-width: 280px` and `min-width: 270px` which could cause clipping or overflow on screens narrower than 280px (e.g. 320px).
- **Remediation Applied:** Changed hero column flex rules to `flex: 1 1 540px; min-width: 0; max-width: 100%;` and `flex: 1 1 380px; min-width: 0; max-width: 100%;`.

### Finding 13: Derive featured role badges from the selected players
- **File:** `src/dashboard/components.py:118`
- **Severity:** Minor
- **CodeRabbit Diagnostic:** Batter was hardcoded to "Top Order" and bowler to "Slow Orthodox" badges.
- **Remediation Applied:** Parameterized `featured_bat_role` and `featured_bowl_role` in `render_editorial_hero()`. Extracted dynamic `role` (formatted as Title Case) from `top_bat` and `bowling_type` / `pace_or_spin` from `top_bowl`. Omitted badge when data is unavailable.
- **Remediation Commit:** `04ad952`.

---

## 7. Pass 6 Final Verification Review (`dashboard-ui-v3..04ad952`)

- **Command Executed:** `cr review --committed --base dashboard-ui-v3 --agent`
- **Base Commit:** `dashboard-ui-v3`
- **HEAD Commit:** `04ad952`
- **Reviewed Files:** 12 files (`.streamlit/config.toml`, `src/dashboard/*.py`, `tests/test_dashboard_data.py`)
- **Findings Reported:** **0 Critical, 0 Major, 0 Minor**
- **Outcome:** Complete clean pass. Zero outstanding findings.

---

## 8. Pass 7 Visual Excellence Audit Review (`04ad952..57c81f8`)

### Finding 14: Encode the ampersand in both page query values
- **File:** `docs/dashboard/DASHBOARD_HANDOVER.md:137, 142`
- **Severity:** Minor
- **CodeRabbit Diagnostic:** In `?page=Methodology+&+Validation` and `?page=Data+Sources+&+Provenance`, the unencoded ampersand acts as a query parameter separator, causing Streamlit's query parameter parser to truncate the value and fall back to Overview.
- **Remediation Applied:** Replaced documentation examples with `?page=Methodology+%26+Validation` and `?page=Data+Sources+%26+Provenance`.

### Finding 15: Do not claim clutch amplification from a single-band value
- **File:** `src/dashboard/views/player_views.py:187`
- **Severity:** Minor
- **CodeRabbit Diagnostic:** Caption asserted that positive surplus in High and Extreme bands indicates clutch amplification, whereas single-band positive surplus indicates above-expectation execution only; establishing amplification requires comparison with lower tiers.
- **Remediation Applied:** Reworded caption: `"Mean delivery PAVA surplus across pressure tiers. Positive values in High [65–85) and Extreme (>=85) bands reflect above-expectation execution in those tiers; upward tier-over-tier slope indicates clutch amplification."`

### Finding 16: Do not read overlapping intervals as equal scores
- **File:** `src/dashboard/views/player_views.py:305`
- **Severity:** Minor
- **CodeRabbit Diagnostic:** Caption asserted that overlapping 95% bootstrap confidence intervals indicate indistinguishable statistical difference, which is statistically inaccurate (two 95% CIs can overlap even when difference is significant).
- **Remediation Applied:** Reworded caption: `"Reliability Scores with 95% bootstrap confidence intervals representing estimation uncertainty given historical sample size and variance."`
- **Remediation Commit:** `028e82c`.

---

## 9. Pass 8 Final Delta Review (`57c81f8..028e82c`)

- **Command Executed:** `cr review --committed --base 57c81f8 --agent`
- **Base Commit:** `57c81f8`
- **HEAD Commit:** `028e82c`
- **Reviewed Files:** 3 files (`docs/dashboard/CODERABBIT_REVIEW_LOG.md`, `docs/dashboard/DASHBOARD_HANDOVER.md`, `src/dashboard/views/player_views.py`)
- **Findings Reported:** **0 Critical, 0 Major, 0 Minor**
- **Outcome:** Complete clean pass. All minor audit observations resolved with 100% precision. Zero outstanding issues.

---

## 10. Pass 9 Premium Sidebar Redesign Review (`8df01e4..fcda3f3`)

- **Command Executed:** `cr review --committed --base 8df01e4 --agent`
- **Base Commit:** `8df01e4`
- **HEAD Commit:** `fcda3f3`
- **Reviewed Files:** `src/dashboard/components.py`, `src/dashboard/design_tokens.py`, `src/dashboard/styles.py`

### Finding 17: Scope sidebar dimensions to aria-expanded
- **File:** `src/dashboard/styles.py:410-435`
- **Severity:** Major
- **CodeRabbit Diagnostic:** Unconditional width (`width: 280px !important`) applied to `section[data-testid="stSidebar"]` overrode Streamlit's collapsed zero-width state, preventing the sidebar from collapsing properly.
- **Remediation Applied:** Scoped desktop and tablet sidebar width and padding declarations strictly to `section[data-testid="stSidebar"][aria-expanded="true"]`.
- **Verification:** Verified in Playwright audit `05_overview_mobile_closed_375.png` and `06_overview_mobile_drawer_375.png`.

### Finding 18: Preserve Streamlit session state during sidebar navigation
- **File:** `src/dashboard/components.py:347-368`
- **Severity:** Major
- **CodeRabbit Diagnostic:** Navigation was rendered using raw HTML anchor links (`<a href="?page=..." target="_self">`), triggering full page reloads that reset in-memory Streamlit session state.
- **Remediation Applied:** Replaced anchor links with native Streamlit buttons (`st.sidebar.button`) with custom primary/secondary pill styling, Material Symbols (`:material/...:`), and an `on_click=_on_nav_item_click` callback that preserves session state and updates query params cleanly.
- **Remediation Commit:** `6aa231a`.

---

## 11. Pass 10 Launcher Selector Verification Review (`6aa231a..7ef410b`)

- **Command Executed:** `cr review --committed --base 6aa231a --agent`
- **Base Commit:** `6aa231a`
- **HEAD Commit:** `7ef410b`
- **Reviewed Files:** `src/dashboard/styles.py`

### Finding 19: Replace invalid :contains() selector with valid container class
- **File:** `src/dashboard/styles.py:313-334`
- **Severity:** Minor
- **CodeRabbit Diagnostic:** CSS does not support `:contains()`. Including it invalidated the entire comma-separated selector block, causing the "Open Player Profile →" launcher button to lose its distinct terracotta styling.
- **Remediation Applied:** Replaced invalid selector with W3C-standard `section[data-testid="stSidebar"] div.st-key-global_jump_btn button`, targeting Streamlit's native `.st-key-global_jump_btn` container class.
- **Verification:** Verified computed CSS with Playwright (`rgb(189, 101, 72)` background, `rgb(255, 255, 255)` text). Re-reviewed with CodeRabbit CLI: **0 findings reported**. Complete clean pass.





