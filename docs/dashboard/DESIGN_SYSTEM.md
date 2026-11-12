# PRESSUREIQ — Visual Design System Specification (`v3.0`)

**Product:** PRESSUREIQ — Cricket Pressure Intelligence  
**Tagline:** *Beyond Performance. Measuring Composure Under Pressure.*  
**Mode:** `Operate` (High-density sports telemetry & franchise intelligence dashboard)  
**Target Stack:** Streamlit `1.56.0` + Plotly `6.6.0` + Custom CSS Design Tokens + Inline SVG Iconography

---

## 1. Color Tokens

| Token Name | Hex / Value | Usage | WCAG AA Contrast Check |
|---|---|---|---|
| `--bg-canvas` | `#080C18` | Primary deep-navy application canvas | Base background |
| `--bg-sidebar` | `#0C1222` | Persistent collapsible navigation rail | Separates cleanly from canvas |
| `--bg-surface` | `#11182C` | Primary panels, chart wrappers, KPI cards | Raised surface against `#080C18` |
| `--bg-surface-elevated` | `#17223B` | Hover states, table headers, interactive callouts | Distinct elevation step |
| `--bg-surface-subtle` | `#0F172A` | Nested summary strip / code/provenance strip | Subtle depth contrast |
| `--border-subtle` | `rgba(148, 163, 184, 0.16)` | 1px card/table hairlines | Non-distracting structural grid |
| `--border-strong` | `rgba(139, 92, 246, 0.42)` | Active focus, active nav pill, selected player tile | Clear focus/active state |
| `--text-primary` | `#F8FAFC` | Headings, primary metrics, player names | `> 15:1` on `#080C18` / `#11182C` |
| `--text-secondary` | `#CBD5E1` | Body prose, axis tick labels, secondary cells | `> 10:1` on `#11182C` |
| `--text-muted` | `#94A3B8` | Field captions, units, footnotes (never `< 12px` for critical copy) | `~ 5.9:1` on `#11182C` (`>= 4.5:1`) |
| `--accent-violet` | `#8B5CF6` | Primary brand telemetry highlight, active route pill, bowler series | Distinguishable telemetry anchor |
| `--accent-blue` | `#3B82F6` | Batter primary series, interactive control focus, links | Clear contrast with dark surfaces |
| `--accent-cyan` | `#22D3EE` | Expected baseline / secondary comparison trace | Distinct vs `#3B82F6` & `#8B5CF6` |
| `--status-positive` | `#14B8A6` (`#2DD4BF` text) | Positive PAVA, Clutch Climber, Confirmed Trade/Retained text | Readable positive signal without neon harshness |
| `--status-lime` | `#84CC16` | High reliability benchmark threshold marker (`>= 90` reference line) | Controlled telemetry accent |
| `--status-warning` | `#F59E0B` (`#FCD34D` text) | Pending Verification, cautious sample warning (`30–60` HP) | High-visibility amber pill |
| `--status-danger` | `#EF4444` (`#FCA5A5` text) | Negative PAVA, Pressure Fragile, Policy/Eligibility Review | Unmistakable risk state |

---

## 2. Typography Scale & 3. Font Families

- **Primary Sans (UI & Editorial):** `'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- **Telemetry Mono (Scores, Ranks, Hashes, Formulas):** `'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, monospace` (`font-variant-numeric: tabular-nums;`)

| Role | Size (`rem` / `px`) | Weight | Line Height | Tracking | Notes |
|---|---:|---:|---:|---:|---|
| Hero Masthead (`h1.p-hero-title`) | `2.0rem` (`32px`) | `700` | `1.15` | `-0.025em` | Restraint: crisp weight & size, no gradient text |
| Page Title (`h1`) | `1.65rem` (`26.4px`) | `700` | `1.2` | `-0.02em` | Clear single focal point |
| Section Header (`h2`) | `1.15rem` (`18.4px`) | `600` | `1.3` | `-0.01em` | More top margin (`24px`) than bottom (`8px`) |
| Card Title (`h3`) | `0.95rem` (`15.2px`) | `600` | `1.35` | `0` | Concise sentence case |
| KPI Hero Value | `1.65rem` (`26.4px`) | `700` | `1.1` | `-0.02em` | Always paired with `tabular-nums` |
| Body Copy | `0.94rem` (`15px`) | `400` | `1.55` | `0` | Constrained line measure (`<= 75ch`) |
| Micro / Caption / Badge | `0.78rem` (`12.5px`) | `500–600` | `1.4` | `+0.01em` | Never `< 12px` for readable prose |

---

## 4. Spacing Scale, 5. Layout Grid & 6. Responsive Breakpoints

- **Base Unit:** `4px` (`0.25rem`). Token steps: `4, 8, 12, 16, 24, 32, 48px`.
- **Container Max Width:** `1440px` (`padding: 1.25rem 1.75rem` desktop).
- **Grid Columns:** Fluid CSS Grid (`grid-template-columns: repeat(auto-fit, minmax(220px, 1fr))`) for KPI tiles + Streamlit columns that stack cleanly at mobile width.
- **Breakpoints Verified via Playwright:**
  - **Desktop (`>= 1280px` / `1440x900`):** Expanded sidebar + 2-column / 4-column metric rows + side-by-side Plotly visualizations.
  - **Laptop (`1024px–1279px`):** Compact margins (`1rem`), clean chart auto-sizing, scrollable wide tables with sticky headers.
  - **Tablet (`768px–1023px`):** 2-column KPI grid, collapsible sidebar drawer, charts stack vertically if narrow.
  - **Mobile (`375px–767px`):** Single-column KPI stack, zero horizontal page overflow (`overflow-x: hidden`), `44px` minimum touch targets on interactive controls.

---

## 7. Card Variants & 8. Button Variants

- **KPI Metric Tile (`.piq-kpi`):** `#11182C` fill, `1px solid rgba(148,163,184,0.16)`, `10px` radius, `16px 18px` padding, restrained top-edge `2px` accent rule (`--accent-violet` / `--accent-blue` / `--status-positive`), subtle `180ms ease-out` border lighten on hover. Never uses neon glow boxes.
- **Hero Surface (`.piq-hero`):** `#11182C` -> `#0F172A` subtle directional wash (`<= 1` soft radial wash at top-right `< 12%` opacity), crisp inline SVG telemetry emblem, tagline, live frozen integrity chip, snapshot date chip.
- **Notice / Context Panel (`.piq-callout`):** Soft `#131D36` surface, semantic tone border (`1px solid` + clean `3px` accent bar ONLY for distinct status notices, never nested cards).
- **Buttons (`st.button`, `st.download_button`):** Minimum `40–44px` height, `#1E293B` secondary fill with `#8B5CF6` focus outline, active feedback `transform: scale(0.985)` within `120ms`. Primary action fills `#6D28D9` -> hover `#7C3AED` (`#FFFFFF` text `> 5.5:1` contrast).

---

## 9. Table Styles & 10. Chart Styles & 11. Tooltip Styles

- **Dataframes / HTML Data Grids:** Dark slate surface `#0F172A`, sticky uppercase-free `600`-weight column header `#162038`, subtle `1px` row dividers, `tabular-nums` right-aligned numeric columns, hover row tint `rgba(59, 130, 246, 0.08)`, zero dense wall-of-text columns (compact badges + expandable details).
- **Plotly Dark Telemetry Template (`plotly_dark` custom base):**
  - Transparent paper & plot backgrounds (`rgba(0,0,0,0)` inside styled panel containers or `#11182C` explicit fill).
  - Subtle dashed horizontal gridlines `rgba(148, 163, 184, 0.12)`, zero heavy zero-line clutter.
  - Accessible dual-encoding: distinct hues (`#3B82F6` Cobalt, `#8B5CF6` Violet, `#14B8A6` Teal, `#F59E0B` Amber, `#F43F5E` Coral) + distinct line dashes/marker symbols + direct numeric labels.
- **Tooltips (`hoverlabel`):** Deep slate `#0B1120`, border `#475569`, `#F8FAFC` `12.5px` Inter/JetBrains Mono text, explicit units (`runs/ball`, `%`, `balls`, `pts`), `hovermode="closest"` / `"x unified"`.

---

## 12. Navigation Styles

- **Collapsible Left Rail:** `268px` width, crisp PRESSUREIQ SVG wordmark & emblem, version & frozen-integrity summary footer (`v3.0 | 867 matches | Nov 11 Snapshot`).
- **10 Numbered Functional Routes:** Clean radio/button navigation items with inline `16x16` Lucide-style SVG icons, active electric-violet tint `rgba(139, 92, 246, 0.16)` with `#C4B5FD` text and `2px` accent marker.
- **Top Sticky Application Bar:** Current route breadcrumb, frozen SHA-256 verification status pill (`VERIFIED`), Market Snapshot anchor (`2026-11-11`), and quick global player jump selector / search.

---

## 13. Status Indicators

Every market classification maps strictly to a distinct badge shape/icon + color pair:

| Status Label | Fill | Border | Text | Meaning |
|---|---|---|---|---|
| `Confirmed Retained` / `Confirmed` | `rgba(20, 184, 166, 0.16)` | `rgba(45, 212, 191, 0.45)` | `#5EEAD4` | Verified official IPL retention filing |
| `Confirmed Released` | `rgba(59, 130, 246, 0.16)` | `rgba(96, 165, 250, 0.45)` | `#93C5FD` | Verified official release into auction pool |
| `Confirmed Trade` | `rgba(139, 92, 246, 0.18)` | `rgba(167, 139, 250, 0.48)` | `#DDD6FE` | Verified franchise-to-franchise trade (`Nathan Ellis: CSK -> SRH`) |
| `Reported` | `rgba(34, 211, 238, 0.15)` | `rgba(34, 211, 238, 0.42)` | `#67E8F9` | Attributed media report pending official IPL filing |
| `Pending Verification` | `rgba(245, 158, 11, 0.16)` | `rgba(251, 191, 36, 0.45)` | `#FDE68A` | Unconfirmed ahead of 17 Nov 2026 retention lists |
| `Rumour` | `rgba(148, 163, 184, 0.15)` | `rgba(148, 163, 184, 0.38)` | `#CBD5E1` | Unverified report; never treated as confirmed |
| `Policy/Eligibility Review` | `rgba(244, 63, 94, 0.16)` | `rgba(251, 113, 133, 0.45)` | `#FDA4AF` | Subject to historical BCCI/IPL policy verification |
| `Historical` | `rgba(100, 116, 139, 0.18)` | `rgba(100, 116, 139, 0.40)` | `#94A3B8` | Historical 2022–2026 squad / pre-Nov 17 baseline snapshot |

---

## 14. Loading, 15. Empty & 16. Error States

- **Loading States:** `show_spinner=False` on cached DuckDB queries paired with styled compact telemetry skeleton bar (`.piq-skeleton` subtle shimmer only when motion enabled) so initial render is smooth and non-jarring.
- **Empty States:** Custom bordered panel with clear action prompt (e.g., `"0 players match the active filters — lower Min HP Opportunities or reset team/role selection"`), never a blank screen.
- **Error / Integrity Failure States:** Explicit crimson alert panel surfacing missing Parquet/CSV paths or frozen SHA-256 mismatch with exact expected vs observed digest and CLI recovery instruction.

---

## 17. Accessibility Standards (WCAG 2.2 AA)

- All body text `>= 4.5:1` contrast, large headings `>= 3:1` contrast.
- Custom visible `:focus-visible` ring (`outline: 2px solid #A78BFA; outline-offset: 2px;`) across buttons, inputs, tabs, and sidebar links; sticky top header offsets scroll padding (`scroll-padding-top: 72px`) so focus is never obscured.
- Zero emoji stand-ins for UI icons (`stroke="currentColor"`, `aria-hidden="true"` inline SVGs).
- Never rely on color alone: pair colors with explicit status text, symbols (`+`/`-`/markers), and tabular numerical columns.

---

## 18. Animation & Transition Rules (`emil-design-eng`)

- **No animation on high-frequency interactions:** Tab switches, sidebar route clicks, search input typing, and filter updates respond immediately (`0ms` delay) with zero sluggish entrance replays.
- **Authoritative Subtle Micro-interactions:**
  - Hover border/surface tint transition: `160ms cubic-bezier(0.16, 1, 0.3, 1)` (color/border/transform only — never `transition: all`).
  - Button `:active` tactile press: `transform: scale(0.985)` over `100ms`.
  - Optional initial hero KPI reveal (`fade-in` `220ms ease-out`) without delaying data visibility.
- **Reduced Motion:** Global `@media (prefers-reduced-motion: reduce)` rule disables all keyframes, transitions, and smooth-scrolling animations cleanly.

