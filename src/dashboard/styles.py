"""Global Editorial Luxury CSS system for PRESSUREIQ v4.

Warm Ivory (#F8F4EC) + Soft Cream (#F1E9DD) + Terracotta (#BD6548) + Deep Ink (#282321)
Kinfolk / Contemporary Luxury Editorial Magazine Aesthetics
"""

from __future__ import annotations

import streamlit as st
from src.dashboard.design_tokens import FONTS, PALETTE


def inject_global_styles() -> None:
    """Inject responsive, accessible warm editorial CSS matching Kinfolk luxury reference."""
    css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {{
    --bg-canvas: {PALETTE['bg_canvas']};
    --bg-sidebar: {PALETTE['bg_sidebar']};
    --bg-surface: {PALETTE['bg_surface']};
    --bg-surface-raised: {PALETTE['bg_surface_raised']};
    --bg-surface-subtle: {PALETTE['bg_surface_subtle']};
    --bg-deep: {PALETTE['bg_deep']};
    --border-subtle: {PALETTE['border_subtle']};
    --border-card: {PALETTE['border_card']};
    --border-strong: {PALETTE['border_strong']};
    --text-primary: {PALETTE['text_primary']};
    --text-secondary: {PALETTE['text_secondary']};
    --text-muted: {PALETTE['text_muted']};
    --text-inverse: {PALETTE['text_inverse']};
    --accent-terracotta: {PALETTE['accent_terracotta']};
    --accent-terracotta-hover: {PALETTE['accent_terracotta_hover']};
    --accent-gold: {PALETTE['accent_gold']};
    --accent-sage: {PALETTE['accent_sage']};
    --positive: {PALETTE['positive']};
    --warning: {PALETTE['warning']};
    --danger: {PALETTE['danger']};
    --font-serif: {FONTS['display']};
    --font-sans: {FONTS['body']};
    --font-mono: {FONTS['mono']};
}}

html, body, [class*="stAppViewContainer"] {{
    font-family: var(--font-sans);
    background-color: var(--bg-canvas);
    color: var(--text-primary);
    scroll-padding-top: 72px;
    overflow-x: hidden;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}}

[data-testid="stAppViewContainer"] {{
    background: radial-gradient(1200px 500px at 95% -5%, rgba(189, 101, 72, 0.05), transparent 70%),
                radial-gradient(900px 400px at 10% 15%, rgba(197, 164, 109, 0.06), transparent 60%),
                var(--bg-canvas);
}}

[data-testid="stHeader"] {{
    background: rgba(248, 244, 236, 0.92);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--border-subtle);
}}

section[data-testid="stSidebar"] {{
    background-color: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-card);
}}

section[data-testid="stSidebar"] hr {{
    border-color: var(--border-subtle) !important;
}}

.main .block-container {{
    padding-top: 1.25rem;
    padding-bottom: 3.2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1440px;
}}

/* Custom scrollbars & text selection in terracotta */
::selection {{
    background: rgba(189, 101, 72, 0.22);
    color: var(--text-primary);
}}
::-webkit-scrollbar {{
    width: 7px;
    height: 7px;
}}
::-webkit-scrollbar-track {{
    background: #F1E9DD;
}}
::-webkit-scrollbar-thumb {{
    background: #D8CBBE;
    border-radius: 4px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: #BD6548;
}}

/* Accessible keyboard focus states */
button:focus-visible, a:focus-visible, input:focus-visible, select:focus-visible,
[role="tab"]:focus-visible, [data-baseweb="select"]:focus-within {{
    outline: 2px solid var(--accent-terracotta) !important;
    outline-offset: 2px !important;
}}

/* Sidebar navigation styling: warm editorial pill items */
section[data-testid="stSidebar"] div[data-testid="stRadio"] > div {{
    gap: 4px;
}}
section[data-testid="stSidebar"] div[data-testid="stRadio"] label {{
    border-radius: 8px;
    padding: 8px 12px;
    border: 1px solid transparent;
    color: var(--text-secondary);
    font-size: 0.88rem;
    font-weight: 500;
    transition: all 140ms ease-out;
}}
section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {{
    background: #EAE1D5;
    color: var(--text-primary);
}}
section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"],
section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {{
    background: #FFFFFF !important;
    border-color: var(--border-card) !important;
    box-shadow: 0 1px 3px rgba(40, 35, 33, 0.05);
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    border-left: 3px solid var(--accent-terracotta) !important;
}}

/* Editorial Typography */
h1, h2, h3, h4 {{
    font-family: var(--font-serif);
    color: var(--text-primary);
    letter-spacing: -0.015em;
    font-weight: 600;
}}

.main .block-container h1 {{
    font-family: var(--font-serif) !important;
    font-size: 2.1rem !important;
    font-weight: 600 !important;
    line-height: 1.2 !important;
    color: var(--text-primary) !important;
    margin-bottom: 0.4rem !important;
}}

.piq-serif {{
    font-family: var(--font-serif) !important;
}}

.piq-mono, code {{
    font-family: var(--font-mono) !important;
    font-variant-numeric: tabular-nums;
}}

/* Streamlit Native Select, Input, Slider styling in warm cream */
div[data-baseweb="select"] > div {{
    background-color: #FFFFFF !important;
    border-color: var(--border-card) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
}}
input[type="text"] {{
    background-color: #FFFFFF !important;
    border-color: var(--border-card) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
}}

/* Top Navigation / Breadcrumb Header Strip (Deep Ink or Warm Cream) */
.piq-topbar {{
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 12px 18px;
    padding: 10px 18px;
    background: #282321;
    border-radius: 10px;
    margin-bottom: 18px;
    box-shadow: 0 2px 6px rgba(40, 35, 33, 0.08);
}}
.piq-crumb {{
    display: inline-flex;
    align-items: center;
    gap: 10px;
    font-size: 0.88rem;
    font-weight: 500;
    color: #F8F4EC;
    letter-spacing: 0.02em;
}}
.piq-crumb-muted {{
    color: #D8CBBE;
    font-weight: 400;
}}
.piq-meta-strip {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
}}

/* Hero Section (Kinfolk Editorial Style) */
.piq-hero {{
    background: #FFFFFF;
    border: 1px solid var(--border-card);
    border-radius: 14px;
    padding: 28px 32px;
    margin-bottom: 22px;
    box-shadow: 0 3px 12px rgba(40, 35, 33, 0.03);
    position: relative;
    overflow: hidden;
}}
.piq-hero::after {{
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    width: 220px;
    height: 100%;
    background: radial-gradient(circle at 100% 0%, rgba(189, 101, 72, 0.07), transparent 70%);
    pointer-events: none;
}}
.piq-hero-eyebrow {{
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent-terracotta);
    margin-bottom: 8px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}}
.piq-hero-title {{
    font-family: var(--font-serif);
    font-size: 2.35rem;
    font-weight: 600;
    line-height: 1.15;
    margin: 0 0 6px 0;
    color: var(--text-primary);
    letter-spacing: -0.02em;
}}
.piq-hero-tagline {{
    font-family: var(--font-serif);
    font-style: italic;
    font-size: 1.25rem;
    color: #77675D;
    margin: 0 0 12px 0;
    font-weight: 400;
}}
.piq-hero-desc {{
    font-size: 0.95rem;
    line-height: 1.6;
    color: var(--text-secondary);
    max-width: 76ch;
    margin: 0 0 18px 0;
}}
.piq-hero-stats {{
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    padding-top: 14px;
    border-top: 1px solid var(--border-subtle);
}}

/* Responsive Editorial KPI Cards */
.piq-kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(215px, 1fr));
    gap: 14px;
    margin-bottom: 22px;
}}
.piq-kpi {{
    background: #FFFFFF;
    border: 1px solid var(--border-card);
    border-top: 3px solid var(--kpi-accent, #BD6548);
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 2px 6px rgba(40, 35, 33, 0.03);
    transition: all 160ms ease-out;
}}
.piq-kpi:hover {{
    border-color: var(--border-strong);
    box-shadow: 0 4px 12px rgba(189, 101, 72, 0.08);
    transform: translateY(-1px);
}}
.piq-kpi-head {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
}}
.piq-kpi-val {{
    font-family: var(--font-serif);
    font-size: 1.85rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-top: 8px;
    line-height: 1.15;
    font-variant-numeric: tabular-nums;
}}
.piq-kpi-sub {{
    font-size: 0.82rem;
    color: var(--text-secondary);
    margin-top: 6px;
    line-height: 1.4;
}}

/* Section Headers: Editorial Subheaders */
.piq-sec-head {{
    margin-top: 26px;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border-card);
}}
.piq-sec-title {{
    font-family: var(--font-serif);
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.piq-sec-sub {{
    font-size: 0.84rem;
    color: var(--text-secondary);
    margin: 4px 0 0 0;
}}

/* Callouts & Info Containers */
.piq-callout {{
    background: #FAF6F0;
    border: 1px solid var(--border-card);
    border-left: 3px solid var(--callout-accent, #BD6548);
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.88rem;
    line-height: 1.55;
    color: var(--text-primary);
    margin-bottom: 16px;
}}
.piq-empty {{
    background: #FFFFFF;
    border: 1px dashed var(--border-card);
    border-radius: 12px;
    padding: 28px 22px;
    text-align: center;
    color: var(--text-secondary);
    margin: 14px 0;
}}

/* Refined Editorial Badges & Status Pills */
.piq-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    line-height: 1.3;
    white-space: nowrap;
}}

/* Editorial Table Wrapper */
.piq-table-wrap {{
    width: 100%;
    overflow-x: auto;
    border: 1px solid var(--border-card);
    border-radius: 12px;
    background: #FFFFFF;
    margin-bottom: 16px;
    box-shadow: 0 1px 4px rgba(40, 35, 33, 0.03);
}}
.piq-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
    color: var(--text-primary);
    font-variant-numeric: tabular-nums;
}}
.piq-table th {{
    background: #F1E9DD;
    color: #282321;
    font-family: var(--font-sans);
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    text-align: left;
    padding: 10px 14px;
    border-bottom: 1px solid var(--border-card);
    white-space: nowrap;
}}
.piq-table td {{
    padding: 9px 14px;
    border-bottom: 1px solid var(--border-subtle);
    vertical-align: top;
}}
.piq-table tr:hover td {{
    background: #FAF6F0;
}}

/* Streamlit Tabs */
button[data-baseweb="tab"] {{
    min-height: 42px;
    font-weight: 600;
    color: var(--text-secondary);
    font-size: 0.92rem;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
    color: var(--accent-terracotta) !important;
    border-bottom-color: var(--accent-terracotta) !important;
}}

/* Streamlit Action Buttons in Warm Editorial Palette */
div.stButton > button, div.stDownloadButton > button {{
    min-height: 38px;
    border-radius: 8px;
    border: 1px solid var(--border-card);
    background: #FFFFFF;
    color: var(--text-primary);
    font-weight: 600;
    font-size: 0.86rem;
    transition: all 140ms ease-out;
}}
div.stButton > button:hover, div.stDownloadButton > button:hover {{
    background: var(--accent-terracotta);
    border-color: var(--accent-terracotta);
    color: #FFFFFF !important;
}}

/* Subtle Tape Badge Accent from Reference Image 4 */
.piq-tape-tag {{
    display: inline-block;
    padding: 3px 8px;
    background: #C5A46D;
    color: #282321;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border-radius: 2px;
}}

/* Footer */
.piq-footer {{
    margin-top: 36px;
    padding-top: 16px;
    border-top: 1px solid var(--border-card);
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 8px 16px;
    font-size: 0.8rem;
    color: var(--text-muted);
}}

/* Responsive adjustments */
@media (max-width: 1024px) {{
    .main .block-container {{
        padding-left: 1.25rem;
        padding-right: 1.25rem;
    }}
}}
@media (max-width: 767px) {{
    .main .block-container {{
        padding-left: 0.85rem;
        padding-right: 0.85rem;
    }}
    .piq-hero {{ padding: 18px; }}
    .piq-hero-title {{ font-size: 1.6rem !important; }}
    .piq-hero-tagline {{ font-size: 1.05rem !important; }}
    .piq-kpi-grid {{ grid-template-columns: 1fr; }}
}}

/* Reduced motion preference */
@media (prefers-reduced-motion: reduce) {{
    *, *::before, *::after {{
        animation-duration: 0.001ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.001ms !important;
        scroll-behavior: auto !important;
    }}
}}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)
