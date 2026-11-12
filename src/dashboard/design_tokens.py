"""Centralized Dark Sports Telemetry Design Tokens & Navigation Map for PRESSUREIQ v3."""

from __future__ import annotations

PRODUCT_NAME = "PRESSUREIQ"
PRODUCT_TAGLINE = "Beyond Performance. Measuring Composure Under Pressure."
PRODUCT_VERSION = "v3.0"
COMPETITION_TITLE = "Rajasthan Royals SupeRR Selector Season 2"
SNAPSHOT_ANCHOR_DATE = "2026-11-11"
RETENTION_DEADLINE_DATE = "2026-11-17"

PALETTE = {
    "bg_canvas": "#080C18",
    "bg_sidebar": "#0C1222",
    "bg_surface": "#11182C",
    "bg_surface_elevated": "#17223B",
    "bg_surface_subtle": "#0F172A",
    "border_subtle": "rgba(148, 163, 184, 0.16)",
    "border_strong": "rgba(139, 92, 246, 0.45)",
    "text_primary": "#F8FAFC",
    "text_secondary": "#CBD5E1",
    "text_muted": "#94A3B8",
    "accent_violet": "#8B5CF6",
    "accent_violet_soft": "#C4B5FD",
    "accent_blue": "#3B82F6",
    "accent_cyan": "#22D3EE",
    "positive": "#14B8A6",
    "positive_text": "#5EEAD4",
    "lime": "#84CC16",
    "warning": "#F59E0B",
    "warning_text": "#FDE68A",
    "danger": "#EF4444",
    "danger_text": "#FDA4AF",
    "plot_grid": "rgba(148, 163, 184, 0.12)",
}

PLOTLY_SERIES = ["#3B82F6", "#8B5CF6", "#14B8A6", "#F59E0B", "#22D3EE", "#F43F5E"]

NAV_ITEMS = [
    {"id": "Overview", "label": "Overview", "icon": "overview", "subtitle": "Executive intelligence & Model A summary"},
    {"id": "Pressure Leaderboards", "label": "Pressure Leaderboards", "icon": "trophy", "subtitle": "Frozen Batters (109) & Bowlers (147) cohorts"},
    {"id": "Player Intelligence", "label": "Player Intelligence", "icon": "user", "subtitle": "Individual pressure profile & match evidence"},
    {"id": "Player Comparison", "label": "Player Comparison", "icon": "compare", "subtitle": "Head-to-head multi-player telemetry comparator"},
    {"id": "Pressure Analytics", "label": "Pressure Analytics", "icon": "activity", "subtitle": "BPI, BoPI, PAVA & expected-outcome physics"},
    {"id": "Emerging Talent", "label": "Emerging Talent", "icon": "sparkles", "subtitle": "Opportunity-aware uncapped & prospect scouting"},
    {"id": "Rajasthan Royals Intelligence", "label": "Rajasthan Royals Intelligence", "icon": "shield", "subtitle": "SMS Jaipur tactical fit vs verified availability"},
    {"id": "IPL 2027 Market Intelligence", "label": "IPL 2027 Market Intelligence", "icon": "briefcase", "subtitle": "All 10 franchises, retentions, trades & sources"},
    {"id": "Methodology & Validation", "label": "Methodology & Validation", "icon": "book", "subtitle": "Formulas, LightGBM calibration & bootstrap audit"},
    {"id": "Data Sources & Provenance", "label": "Data Sources & Provenance", "icon": "database", "subtitle": "Lineage, checksums, missingness & change log"},
]

NAV_LABELS = [item["label"] for item in NAV_ITEMS]
NAV_META = {item["label"]: item for item in NAV_ITEMS}

IPL_FRANCHISES = [
    ("RR", "Rajasthan Royals", "#8B5CF6"),
    ("CSK", "Chennai Super Kings", "#FACC15"),
    ("MI", "Mumbai Indians", "#3B82F6"),
    ("KKR", "Kolkata Knight Riders", "#A855F7"),
    ("RCB", "Royal Challengers Bengaluru", "#EF4444"),
    ("SRH", "Sunrisers Hyderabad", "#F97316"),
    ("DC", "Delhi Capitals", "#2563EB"),
    ("PBKS", "Punjab Kings", "#F43F5E"),
    ("GT", "Gujarat Titans", "#38BDF8"),
    ("LSG", "Lucknow Super Giants", "#14B8A6"),
]

STATUS_TONES = {
    "Confirmed": ("rgba(20, 184, 166, 0.16)", "rgba(45, 212, 191, 0.45)", "#5EEAD4"),
    "Confirmed Retained": ("rgba(20, 184, 166, 0.16)", "rgba(45, 212, 191, 0.45)", "#5EEAD4"),
    "Confirmed Released": ("rgba(59, 130, 246, 0.16)", "rgba(96, 165, 250, 0.45)", "#93C5FD"),
    "Confirmed Trade": ("rgba(139, 92, 246, 0.18)", "rgba(167, 139, 250, 0.48)", "#DDD6FE"),
    "Reported": ("rgba(34, 211, 238, 0.15)", "rgba(34, 211, 238, 0.42)", "#67E8F9"),
    "Pending Verification": ("rgba(245, 158, 11, 0.16)", "rgba(251, 191, 36, 0.45)", "#FDE68A"),
    "Rumour": ("rgba(148, 163, 184, 0.15)", "rgba(148, 163, 184, 0.38)", "#CBD5E1"),
    "Policy/Eligibility Review": ("rgba(244, 63, 94, 0.16)", "rgba(251, 113, 133, 0.45)", "#FDA4AF"),
    "Historical": ("rgba(100, 116, 139, 0.18)", "rgba(100, 116, 139, 0.40)", "#94A3B8"),
}

