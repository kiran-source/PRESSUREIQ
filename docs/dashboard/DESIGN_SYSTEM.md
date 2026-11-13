# PRESSUREIQ — Visual Design System Specification (`v4.0 Editorial`)

**Product:** PRESSUREIQ — Cricket Pressure Intelligence  
**Tagline:** *Beyond Performance. Measuring Composure Under Pressure.*  
**Design Direction:** **Contemporary Luxury Editorial & Kinfolk Magazine Aesthetic**  
**Core Palette:** Warm Ivory (`#F8F4EC`), Soft Cream (`#F1E9DD`), Terracotta (`#BD6548`), Deep Ink (`#282321`)  
**Typography:** Playfair Display (Editorial Serifs), Inter (Body & Microcopy), JetBrains Mono (Telemetry Numbers)  
**Target Stack:** Streamlit `1.56.0` + Plotly `6.6.0` (`plotly_white` editorial theme) + Custom CSS Design Tokens + Inline Accessible Vector Primitives  

---

## 1. Visual Philosophy & Inspiration

Inspired directly by contemporary luxury editorial print publications (Kinfolk, Cereal, architectural journals):
1. **Quiet Luxury:** Restraint, generous whitespace, warm natural paper tones, and sophisticated contrast.
2. **Never Generic Dark SaaS:** Zero harsh pitch-black backgrounds, neon glow boxes, or generic blue-purple AI gradients.
3. **Typography-First:** Elegant high-contrast serif headlines paired with crisp, functional humanist sans-serif body copy and tabular monospace numerals.
4. **Natural Textures & Tones:** Terracotta cricket seam motifs, warm cream cards with subtle 1px oatmeal hairlines, and soft burnt-earth accents.

---

## 2. Color Tokens

| Token Name | Hex / Value | Usage | WCAG AA Contrast Check |
|---|---|---|---|
| `--bg-canvas` | `#F8F4EC` | Master warm ivory page canvas | Base background |
| `--bg-sidebar` | `#F1E9DD` | Soft cream persistent navigation rail | Clean natural separation |
| `--bg-surface` | `#FFFFFF` | Editorial cards, chart containers, data panels | Pure white elevated surface |
| `--bg-surface-elevated` | `#FAF6F0` | Hero feature cards, hovered rows, elevated widgets | Subtle parchment tint |
| `--bg-surface-subtle` | `#EFE8DE` | Nested summary strips, metadata pill backgrounds | Neutral earthy contrast |
| `--border-card` | `#D8CBBE` | 1px refined oatmeal card border | Crisp structural definition |
| `--border-subtle` | `#E8DFD5` | Table row dividers, subtle separator rules | Hairline organic division |
| `--text-primary` | `#282321` | Headings, primary metrics, player titles | `> 14:1` on `#F8F4EC` / `#FFFFFF` |
| `--text-secondary` | `#77675D` | Body prose, captions, axis tick labels | `> 4.8:1` on `#F8F4EC` (`>= 4.5:1`) |
| `--text-muted` | `#9E9086` | Footnotes, secondary metadata, unit labels | Supplemental contrast |
| `--accent-terracotta` | `#BD6548` | Primary editorial accent, batter series, brand seam | Warm terracotta luxury anchor |
| `--accent-burnt` | `#A94F36` | Active hover accent, urgent emphasis | Deep warm burnt orange |
| `--accent-gold` | `#C5A46D` | Bowler series, secondary metric trace, featured awards | Warm muted gold |
| `--accent-sage` | `#84927A` | Positive PAVA, clutch climber, verified status | Natural earthy sage |
| `--status-warning` | `#D99443` | Pending verification, sample size notices | Warm amber-wheat |
| `--status-danger` | `#B84A39` | Fragile performance, negative delta | Muted red clay |

---

## 3. Typography Scale & Font Hierarchy

- **Editorial Serif (Headings & Hero):** `'Playfair Display', Georgia, 'Times New Roman', serif`
- **Body & Controls:** `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- **Telemetry Numbers & Hashes:** `'JetBrains Mono', 'Fira Code', ui-monospace, monospace` (`font-variant-numeric: tabular-nums;`)

| Role | Size (`rem` / `px`) | Weight | Font Family | Notes |
|---|---:|---:|---|---|
| Hero Masthead (`.piq-hero-title`) | `2.6rem` (`41.6px`) | `700` | Playfair Display | High editorial impact |
| Hero Tagline (`.piq-hero-tagline`) | `1.15rem` (`18.4px`) | `400` | Playfair Display (Italic) | Poetic subtitle |
| Page / Section Header (`h2.piq-sec-title`) | `1.35rem` (`21.6px`) | `600` | Playfair Display | Terracotta icon paired |
| Subtitle / Description | `0.88rem` (`14px`) | `400` | Inter | Muted brown `#77675D` |
| KPI Hero Value | `1.65rem` (`26.4px`) | `700` | Playfair Display | Tabular numerals |
| Table Headers | `0.74rem` (`11.8px`) | `700` | Inter | Uppercase tracking `0.08em` |
| Badges & Status Pills | `0.72rem` (`11.5px`) | `600` | Inter | Rounded `4px`, 1px border |

---

## 4. Layout, Spacing & Breakpoints

- **Canvas Container:** Maximum width `1400px` centered with generous breathing room (`padding: 1.5rem 2rem` on desktop).
- **Component Radius:** Refined `8px–12px` for cards, `6px` for buttons, `4px` for status pills.
- **Card Styling (`.piq-card`, `.piq-kpi`):** Crisp `#FFFFFF` surface with `1px solid #D8CBBE` border, subtle `0 2px 8px rgba(40,35,33,0.04)` elevation shadow, zero harsh drop shadows.
- **Navigation Sidebar (v4.1 Redesign):** Fixed `270–290px` width desktop sidebar on soft cream `#F1E9DD` with custom vector brand emblem, compact `PLAYER LOOKUP` with search icon and collapsed selectbox, and 4 editorial groups:
  - `DISCOVER`: Overview, Pressure Leaderboards, Emerging Talent
  - `PLAYER ANALYTICS`: Player Intelligence, Player Comparison, Pressure Analytics
  - `FRANCHISE INTELLIGENCE`: Rajasthan Royals Intelligence, IPL 2027 Market Intelligence
  - `RESEARCH`: Methodology & Validation, Data Sources & Provenance
  - **Active State:** Terracotta left indicator (`border-left: 3px solid #BD6548`), gradient ivory surface (`#FFFFFF` to `#FAF6F0`), terracotta Lucide line icon, and dark emphasized label.
  - **Bottom Status Area:** Restrained divider, live Model A verification dot (`#5B7B5A`), competition snapshot (`2026-11-11`), retention filing deadline (`2026-11-17`), and version telemetry (`PRESSUREIQ v4.1`).
- **Breakpoints Tested:**
  - **Desktop (`>= 1280px`):** Side-by-side hero layout with featured player cards, 4-column KPI grids, side-by-side Plotly charts.
  - **Tablet (`768px`):** 2-column KPI grid, stacked chart panels, zero overflow.
  - **Mobile (`375px`):** Clean single-column vertical flow, flex-shrink columns, 0 horizontal scroll.

---

## 5. Visualizations & Plotly Styling

- **Base Template:** `plotly_white` modified with transparent paper and plot backgrounds.
- **Palette Implementation:**
  - Primary Series / Batters: Terracotta `#BD6548`
  - Secondary Series / Bowlers: Muted Gold `#C5A46D`
  - Positive Performance / Surpluses: Sage Green `#5B7B5A`
  - Reference Lines & Grid: Hairline `#EAE1D5`
- **Tooltips:** Cream `#FAF6F0` surface with `1px solid #D8CBBE` border and Deep Ink `#282321` typography.

---

## 6. CodeRabbit Review & Compliance

- **Current Status:** Clean Pass (**0 findings**) across all 12 dashboard source files.
- **Integrity Guarantee:** Zero modification to frozen Model A ranking CSVs (`final_batter_rankings.csv`, `final_bowler_rankings.csv`), zero modification to `PRESSUREIQ_Final_Submission.zip`, and 100% test pass rate (91/91 tests).
