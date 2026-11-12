"""Global dark telemetry CSS system for PRESSUREIQ v3."""

from __future__ import annotations

import streamlit as st
from src.dashboard.design_tokens import PALETTE


def inject_global_styles() -> None:
    """Inject responsive, accessible dark telemetry CSS matching DESIGN_SYSTEM.md."""
    css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

:root {{
    --bg-canvas: {PALETTE['bg_canvas']};
    --bg-sidebar: {PALETTE['bg_sidebar']};
    --bg-surface: {PALETTE['bg_surface']};
    --bg-surface-elevated: {PALETTE['bg_surface_elevated']};
    --border-subtle: {PALETTE['border_subtle']};
    --border-strong: {PALETTE['border_strong']};
    --text-primary: {PALETTE['text_primary']};
    --text-secondary: {PALETTE['text_secondary']};
    --text-muted: {PALETTE['text_muted']};
    --accent-violet: {PALETTE['accent_violet']};
    --accent-blue: {PALETTE['accent_blue']};
    --accent-cyan: {PALETTE['accent_cyan']};
    --positive: {PALETTE['positive']};
    --warning: {PALETTE['warning']};
    --danger: {PALETTE['danger']};
}}

html, body, [class*="stAppViewContainer"] {{
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background-color: var(--bg-canvas);
    color: var(--text-primary);
    scroll-padding-top: 72px;
    overflow-x: hidden;
}}

[data-testid="stAppViewContainer"] {{
    background: radial-gradient(900px 420px at 92% -4%, rgba(139, 92, 246, 0.09), transparent 65%),
                radial-gradient(700px 380px at 15% 10%, rgba(59, 130, 246, 0.06), transparent 60%),
                var(--bg-canvas);
}}

[data-testid="stHeader"] {{
    background: rgba(8, 12, 24, 0.85);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid var(--border-subtle);
}}

section[data-testid="stSidebar"] {{
    background-color: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-subtle);
}}

.main .block-container {{
    padding-top: 1.1rem;
    padding-bottom: 2.5rem;
    padding-left: 1.75rem;
    padding-right: 1.75rem;
    max-width: 1440px;
}}

/* Custom scrollbars & selection */
::selection {{ background: rgba(139, 92, 246, 0.35); color: #F8FAFC; }}
::-webkit-scrollbar {{ width: 8px; height: 8px; }}
::-webkit-scrollbar-track {{ background: #0A0F1E; }}
::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 4px; }}
::-webkit-scrollbar-thumb:hover {{ background: #475569; }}

/* Accessible keyboard focus indicators */
button:focus-visible, a:focus-visible, input:focus-visible, select:focus-visible,
[role="tab"]:focus-visible, [data-baseweb="select"]:focus-within {{
    outline: 2px solid #A78BFA !important;
    outline-offset: 2px !important;
}}

/* Sidebar navigation buttons */
section[data-testid="stSidebar"] div[data-testid="stRadio"] > div {{
    gap: 4px;
}}
section[data-testid="stSidebar"] div[data-testid="stRadio"] label {{
    border-radius: 8px;
    padding: 7px 10px;
    border: 1px solid transparent;
    transition: background-color 150ms cubic-bezier(0.16, 1, 0.3, 1), border-color 150ms cubic-bezier(0.16, 1, 0.3, 1);
}}
section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {{
    background: rgba(139, 92, 246, 0.08);
    border-color: rgba(139, 92, 246, 0.25);
}}
section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"],
section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {{
    background: rgba(139, 92, 246, 0.16);
    border-color: rgba(139, 92, 246, 0.45);
}}

/* Typography */
h1, h2, h3, h4 {{
    color: var(--text-primary);
    letter-spacing: -0.02em;
}}
.main .block-container h1.piq-hero-title {{
    font-size: 1.78rem !important;
    font-weight: 700 !important;
    line-height: 1.18 !important;
    margin: 0 0 6px 0 !important;
}}
.piq-sec-head h2.piq-sec-title {{
    font-size: 1.12rem !important;
    font-weight: 600 !important;
    line-height: 1.3 !important;
    margin: 0 !important;
    padding: 0 !important;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.piq-mono, code {{
    font-family: 'JetBrains Mono', ui-monospace, monospace !important;
    font-variant-numeric: tabular-nums;
}}

/* Sticky telemetry header bar */
.piq-topbar {{
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 10px 16px;
    padding: 10px 16px;
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    margin-bottom: 16px;
}}
.piq-crumb {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-primary);
}}
.piq-crumb-muted {{
    color: var(--text-muted);
    font-weight: 500;
}}
.piq-meta-strip {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
}}

/* Hero masthead */
.piq-hero {{
    background: linear-gradient(135deg, #11182C 0%, #0F172A 72%, rgba(139, 92, 246, 0.12) 100%);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 22px 24px;
    margin-bottom: 18px;
}}
.piq-hero-top {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
    flex-wrap: wrap;
}}
.piq-hero-title {{
    font-size: 1.9rem;
    font-weight: 700;
    line-height: 1.15;
    margin: 0 0 6px 0;
    color: #F8FAFC;
    letter-spacing: -0.025em;
}}
.piq-hero-tagline {{
    font-size: 1.02rem;
    font-weight: 500;
    color: #C4B5FD;
    margin: 0 0 8px 0;
}}
.piq-hero-desc {{
    font-size: 0.92rem;
    line-height: 1.55;
    color: var(--text-secondary);
    max-width: 72ch;
    margin: 0;
}}

/* Responsive KPI grid */
.piq-kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(215px, 1fr));
    gap: 12px;
    margin-bottom: 18px;
}}
.piq-kpi {{
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-top: 2px solid var(--kpi-accent, #8B5CF6);
    border-radius: 10px;
    padding: 15px 17px;
    transition: border-color 160ms cubic-bezier(0.16, 1, 0.3, 1), transform 160ms cubic-bezier(0.16, 1, 0.3, 1);
}}
.piq-kpi:hover {{
    border-color: rgba(139, 92, 246, 0.42);
    transform: translateY(-1px);
}}
.piq-kpi-head {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text-muted);
}}
.piq-kpi-val {{
    font-size: 1.52rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-top: 6px;
    line-height: 1.18;
    font-variant-numeric: tabular-nums;
}}
.piq-kpi-sub {{
    font-size: 0.8rem;
    color: var(--text-secondary);
    margin-top: 5px;
    line-height: 1.38;
}}

/* Section Headers */
.piq-sec-head {{
    margin-top: 20px;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid var(--border-subtle);
}}
.piq-sec-title {{
    font-size: 1.12rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.piq-sec-sub {{
    font-size: 0.85rem;
    color: var(--text-muted);
    margin: 3px 0 0 0;
}}

/* Callouts & States */
.piq-callout {{
    background: #101930;
    border: 1px solid var(--border-subtle);
    border-left: 3px solid var(--callout-accent, #3B82F6);
    border-radius: 8px;
    padding: 12px 15px;
    font-size: 0.88rem;
    line-height: 1.5;
    color: var(--text-secondary);
    margin-bottom: 14px;
}}
.piq-empty {{
    background: var(--bg-surface);
    border: 1px dashed rgba(148, 163, 184, 0.32);
    border-radius: 10px;
    padding: 24px 20px;
    text-align: center;
    color: var(--text-secondary);
    margin: 12px 0;
}}

/* Badges & Pills */
.piq-badge {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 9px;
    border-radius: 999px;
    font-size: 0.76rem;
    font-weight: 600;
    line-height: 1.3;
    white-space: nowrap;
}}

/* Team grid cards */
.piq-team-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 10px;
    margin-bottom: 16px;
}}
.piq-team-card {{
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 13px 15px;
}}

/* Dark styled HTML tables */
.piq-table-wrap {{
    width: 100%;
    overflow-x: auto;
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    background: var(--bg-surface);
    margin-bottom: 14px;
}}
.piq-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.84rem;
    color: var(--text-secondary);
    font-variant-numeric: tabular-nums;
}}
.piq-table th {{
    background: #162038;
    color: #F8FAFC;
    font-weight: 600;
    text-align: left;
    padding: 9px 11px;
    border-bottom: 1px solid var(--border-subtle);
    white-space: nowrap;
}}
.piq-table td {{
    padding: 8px 11px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.10);
    vertical-align: top;
}}
.piq-table tr:hover td {{
    background: rgba(59, 130, 246, 0.07);
}}

/* Buttons */
div.stButton > button, div.stDownloadButton > button {{
    min-height: 40px;
    border-radius: 8px;
    border: 1px solid rgba(148, 163, 184, 0.25);
    background: #162038;
    color: #F8FAFC;
    font-weight: 600;
    transition: background-color 140ms ease-out, border-color 140ms ease-out, transform 100ms ease-out;
}}
div.stButton > button:hover, div.stDownloadButton > button:hover {{
    background: #1E2C4D;
    border-color: #8B5CF6;
}}
div.stButton > button:active, div.stDownloadButton > button:active {{
    transform: scale(0.985);
}}

/* Tabs */
button[data-baseweb="tab"] {{
    min-height: 40px;
    font-weight: 600;
    color: var(--text-muted);
}}
button[data-baseweb="tab"][aria-selected="true"] {{
    color: #F8FAFC;
}}

/* Footer */
.piq-footer {{
    margin-top: 32px;
    padding-top: 14px;
    border-top: 1px solid var(--border-subtle);
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 8px 16px;
    font-size: 0.79rem;
    color: var(--text-muted);
}}

/* Responsive adjustments */
@media (max-width: 1024px) {{
    .main .block-container {{
        padding-left: 1.1rem;
        padding-right: 1.1rem;
    }}
}}
@media (max-width: 767px) {{
    .main .block-container {{
        padding-left: 0.75rem;
        padding-right: 0.75rem;
    }}
    .piq-hero {{ padding: 16px; }}
    .main .block-container h1.piq-hero-title {{ font-size: 1.36rem !important; }}
    .piq-kpi-grid {{ grid-template-columns: 1fr; }}
}}

/* Strict reduced motion support */
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

