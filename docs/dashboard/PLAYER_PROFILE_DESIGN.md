# PRESSUREIQ v5.0 — Player Profile Design Architecture & Design System

## 1. Executive Summary & Design Vision

PRESSUREIQ v5.0 transforms cricket pressure analytics from a standard dense dashboard into an **award-winning, luxury editorial scouting intelligence platform**. Inspired by *Kinfolk*, *Cereal*, and high-end print editorial monographs, the platform presents high-stakes empirical sports science through a warm, human, and visually compelling lens.

Rather than relying on default SaaS dark modes or neon futuristic graphics, PRESSUREIQ adheres strictly to an organic, tactile aesthetic:
- **Warm Ivory Canvas:** `#F8F4EC` (soft, glare-free background with subtle paper grain texture)
- **Soft Cream Surfaces:** `#FAF6F0` (layered card and hero backgrounds with refined micro-borders `#D8CBBE`)
- **Terracotta Primary Accent:** `#BD6548` (signature brand tone evoking cricket leather and clay wickets)
- **Deep Ink Typography:** `#282321` (high-contrast, legible text replacing harsh pure black)
- **Muted Earth Accents:** Sage green (`#84927A`), Muted Gold (`#C5A46D`), Burnt Orange (`#A94F36`), and Muted Brown (`#77675D`)

---

## 2. Master Player Profile Hero Architecture

The **Master Player Profile Hero** (`render_player_profile_hero`) is the centerpiece of the player visual experience.

### 2.1 Desktop Two-Column Editorial Composition (1440px / 1366px)
- **Left Column (38% Width):**
  - **Portrait Frame (`.piq-player-hero-portrait-frame`):** Dimensions `200px × 200px` (or `220px × 220px` responsive), with a 14px border radius, subtle drop shadow (`0 8px 24px rgba(40, 35, 33, 0.10)`), and warm taupe border (`#D8CBBE`).
  - **Floating Rank Medallion (`.piq-player-hero-rank-medallion`):** Pinned to the top-left of the portrait (`top: 12px; left: 12px;`), featuring a deep ink pill (`#282321`) with a metallic gold `#C5A46D` or terracotta border and label (e.g., `#1 BATTER` or `#1 BOWLER`).
  - **Identity Provenance Tag:** Discreetly placed at the bottom-right of the image frame (`ID 6059 · MODEL A`), ensuring immediate transparency without visual clutter.
- **Right Column (62% Width):**
  - **Dossier Header Label:** Uppercase tracking label `PLAYER INTELLIGENCE DOSSIER · VERIFIED TELEMETRY` with subtle bullet separators.
  - **Hero Title (`.piq-player-hero-name`):** Rendered in high-contrast *Playfair Display* serif typography (`2.20rem`, `line-height: 1.15`).
  - **Status Badge Strip:** Pill badges denoting tactical role (`Top_Order`, `Middle_Order`, `Death_Specialist`), verified franchise (`Chennai Super Kings`, `Rajasthan Royals`), and audited market status (`Pending Verification (Pre-Nov 17)`).
  - **Integrated KPI Banner (`.piq-player-hero-kpi-banner`):** A 3-column micro-strip displaying:
    1. *Reliability Score:* High-contrast large mono numeral (`97.71`) with 95% bootstrap confidence interval (`[76.3, 99.1]`).
    2. *Top-10 Inclusion Probability:* Empirical percentage (`60.9%`) derived from 2,000 match-clustered bootstrap iterations.
    3. *Pressure Response Profile:* Empirical OLS PRC class (`Clutch Climber`, slope `+1.149`).
  - **Cohort Sub-strip:** High-pressure sample volume (`45 HP Balls`), career match count (`77 matches`), and verified cohort standing (`Rank #1 of 109 Qualified`).
  - **Subtle Watermark (`.piq-player-hero-watermark`):** An elegant large numeral watermark (`01`, `02`) placed in the bottom right corner with soft opacity (`0.05`), reinforcing editorial magazine layout traditions.

### 2.2 Mobile Responsive Architecture (768px / 375px)
- **Single-Column Fluid Stack:** The grid collapses gracefully into a vertical layout (`flex-direction: column`).
- **Centered Portrait:** The avatar centers horizontally with consistent circular or rounded geometry.
- **Adapted Heading:** Typography scales dynamically (`1.70rem` on mobile) to prevent text clipping while retaining full legibility.
- **Balanced Metric Banner:** The KPI banner transitions into a single-column or 2-column mobile layout.
- **Hidden Watermark:** The background watermark is hidden on small viewports to maintain vertical whitespace discipline and eliminate horizontal scrolling.

---

## 3. Seven-Section Player Dossier Flow

Every qualified player profile follows a strict 7-section analytical progression:

1. **Section 1: Master Profile Hero (`render_player_profile_hero`)**
   Visual authority, verified identity tags, cohort percentile, and core reliability score with bootstrap 95% CI.
2. **Section 2: Structured Metric Cards (`render_kpi_grid`)**
   Four primary metric cards highlighting Frozen Model A Rank, Reliability Score & CI, High-Pressure Deliveries (with Kish ESS and raw HP PAVA), and Shrunk HP PAVA with Empirical Bayes shrinkage weight ($w = n / (n + 45)$).
3. **Section 3: Career Aggregates & PAVA Telemetry Strip**
   Empirical career counts: valid deliveries, total runs/wickets, career rate statistics (SR/Econ), raw HP PAVA surplus, and retention delta.
4. **Section 4: Five-Pillar Composite Radar Benchmark (`fig_five_pillar_radar`)**
   Comparative radar chart plotting the player's 5 component scores against the median benchmark of their specific role peers (e.g., Top Order Batters, Middle Order, or Pace/Spin Bowlers).
5. **Section 5: Continuous Leverage Exposure Histogram & Pressure Response Curve**
   Distribution of ball-by-ball leverage exposure ($P \in [0, 100]$) alongside the player's empirical OLS slope across pressure deciles.
6. **Section 6: Match-Phase Summary Table (`compute_player_phase_summary`)**
   Exact ball counts, runs, wickets, dot percentage, boundary percentage, and average PAVA across Powerplay (overs 1–6), Middle (overs 7–15), and Death (overs 16–20).
7. **Section 7: Methodological Guardrails & Match-Level DuckDB Telemetry**
   Explicit analytical strengths and sample limitations callout, followed by DuckDB-queried chronological innings/spells.

---

## 4. Typography & Visual System Hierarchy

| Element | Typeface | Size | Weight | Line Height | Color |
|---|---|---|---|---|---|
| Page Titles | Playfair Display | 2.25rem (36px) | 700 Bold | 1.15 | Deep Ink (`#282321`) |
| Hero Player Name | Playfair Display | 2.20rem (35px) | 700 Bold | 1.15 | Deep Ink (`#282321`) |
| Section Headings | Playfair Display | 1.25rem (20px) | 600 SemiBold | 1.30 | Deep Ink (`#282321`) |
| Upper Section Labels | Inter | 0.72rem (11.5px) | 700 Bold | 1.00 | Terracotta (`#BD6548`) |
| KPI / Metric Numerals | JetBrains Mono | 1.75rem – 2.00rem | 700 Bold | 1.05 | Ink / Terracotta / Gold |
| Navigation Items | Inter | 0.84rem (13.5px) | 500 Medium / 600 Bold | 1.20 | Deep Ink (`#282321`) |
| Body & Callouts | Inter | 0.88rem – 0.92rem | 400 Regular / 600 SemiBold | 1.50 | Deep Ink (`#282321`) |
| Captions & Metadata | Inter | 0.75rem (12px) | 400 Regular | 1.40 | Muted Brown (`#77675D`) |

---

## 5. Verification & Governance Guardrails

1. **Immutability of Frozen Rankings:** All player cards, hero banners, and leaderboards display frozen Model A rankings directly from verified CSVs without runtime recomputation.
2. **Zero Synthetic Imagery:** Every player portrait is drawn directly from verified local image assets (`assets/players/`), verified against `players_manifest.json`.
3. **No Psychological Claims:** Pressure Response Curves (PRC) and retention metrics are explicitly labeled as empirical regression slopes describing historical co-variation, never psychological traits.
