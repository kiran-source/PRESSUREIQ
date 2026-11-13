"""Centralized Warm Editorial Design Tokens & Navigation Map for PRESSUREIQ v4.

Aesthetic: Contemporary Luxury Magazine / Editorial Telemetry (Kinfolk & Monocle aesthetic)
Warm Ivory (#F8F4EC) + Soft Cream (#F1E9DD) + Terracotta (#BD6548) + Deep Ink (#282321)
"""

from __future__ import annotations

PRODUCT_NAME = "PRESSUREIQ"
PRODUCT_TAGLINE = "Beyond Performance. Measuring Composure Under Pressure."
PRODUCT_SUBTITLE = "An advanced cricket intelligence platform identifying players who deliver when the game is on the line."
PRODUCT_VERSION = "v5.0 Visual Intelligence"
COMPETITION_TITLE = "Rajasthan Royals SupeRR Selector Season 2"
SNAPSHOT_ANCHOR_DATE = "2026-11-11"
RETENTION_DEADLINE_DATE = "2026-11-17"

PALETTE = {
    # Canvas & Surface Tokens (Warm Ivory & Soft Cream)
    "bg_canvas": "#F8F4EC",         # Primary canvas ivory
    "bg_sidebar": "#F1E9DD",        # Soft cream sidebar
    "bg_surface": "#FFFFFF",        # Crisp white card surface
    "bg_surface_raised": "#FAF6F0", # Elevated card warm cream
    "bg_surface_subtle": "#F1E9DD", # Soft cream container
    "bg_deep": "#282321",           # Deep ink contrast header
    "bg_card_contrast": "#EFE6D8",  # Slightly deeper cream for emphasis

    # Borders & Dividers
    "border_subtle": "#E8DFD5",     # Fine separator line
    "border_card": "#D8CBBE",       # Refined card perimeter border
    "border_strong": "#BD6548",     # Terracotta active accent border
    "border_focus": "#BD6548",      # Accessible focus border

    # Typography Colors
    "text_primary": "#282321",      # Deep ink headline & body
    "text_secondary": "#77675D",    # Muted brown metadata & subtitles
    "text_muted": "#9B8B80",        # Warm taupe-gray secondary captions
    "text_inverse": "#F8F4EC",      # Warm ivory on dark cards

    # Editorial Accents
    "accent_terracotta": "#BD6548", # Signature brand terracotta
    "accent_terracotta_hover": "#A94F36", # Burnt orange hover state
    "accent_burnt_orange": "#A94F36",
    "accent_gold": "#C5A46D",       # Muted gold highlight
    "accent_sage": "#84927A",       # Sage green (positive)
    "accent_slate": "#5C6B57",      # Olive slate

    # Semantic Indicators
    "positive": "#5B7B5A",          # Refined sage green
    "positive_text": "#2B472A",
    "warning": "#C58B38",           # Warm amber gold
    "warning_text": "#75460E",
    "danger": "#B84A39",            # Clay red
    "danger_text": "#6D1F13",

    # Chart Specific
    "plot_bg": "#FFFFFF",
    "plot_grid": "#EAE1D5",
    "plot_line": "#D8CBBE",
}

# Typography Families
FONTS = {
    "display": "'Playfair Display', 'DM Serif Display', Georgia, serif",
    "body": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "mono": "'JetBrains Mono', 'SF Mono', Consolas, monospace",
}

# Primary Editorial Plotly Series (Warm Terracotta, Muted Gold, Brown, Sage, Burnt Orange)
PLOTLY_SERIES = [
    "#BD6548",  # Terracotta (Primary)
    "#C5A46D",  # Muted Gold
    "#77675D",  # Muted Brown
    "#84927A",  # Sage Green
    "#A94F36",  # Burnt Orange
    "#5C6B57",  # Olive Sage
    "#A68050",  # Clay Tan
    "#282321",  # Deep Ink
]

NAV_ITEMS = [
    # DISCOVER Group
    {"id": "Overview", "label": "Overview", "icon": "layout-dashboard", "mat_icon": ":material/dashboard:", "group": "DISCOVER", "subtitle": "Executive intelligence & Model A summary"},
    {"id": "Pressure Leaderboards", "label": "Pressure Leaderboards", "icon": "trophy", "mat_icon": ":material/emoji_events:", "group": "DISCOVER", "subtitle": "Frozen Batters (109) & Bowlers (147) cohorts"},
    {"id": "Emerging Talent", "label": "Emerging Talent", "icon": "trending-up", "mat_icon": ":material/trending_up:", "group": "DISCOVER", "subtitle": "Opportunity-aware uncapped & prospect scouting"},

    # PLAYER ANALYTICS Group
    {"id": "Player Intelligence", "label": "Player Intelligence", "icon": "user-round-search", "mat_icon": ":material/person_search:", "group": "PLAYER ANALYTICS", "subtitle": "Individual pressure profile & match evidence"},
    {"id": "Player Comparison", "label": "Player Comparison", "icon": "users", "mat_icon": ":material/group:", "group": "PLAYER ANALYTICS", "subtitle": "Head-to-head multi-player telemetry comparator"},
    {"id": "Player Directory", "label": "Player Directory", "icon": "user", "mat_icon": ":material/badge:", "group": "PLAYER ANALYTICS", "subtitle": "Visual scouting catalog of 227 qualified athletes"},
    {"id": "Pressure Analytics", "label": "Pressure Analytics", "icon": "chart-no-axes-combined", "mat_icon": ":material/insights:", "group": "PLAYER ANALYTICS", "subtitle": "BPI, BoPI, PAVA & expected-outcome physics"},

    # FRANCHISE INTELLIGENCE Group
    {"id": "Rajasthan Royals Intelligence", "label": "Rajasthan Royals Intelligence", "icon": "shield", "mat_icon": ":material/shield:", "group": "FRANCHISE INTELLIGENCE", "subtitle": "SMS Jaipur tactical fit vs verified availability"},
    {"id": "IPL 2027 Market Intelligence", "label": "IPL 2027 Market Intelligence", "icon": "activity", "mat_icon": ":material/storefront:", "group": "FRANCHISE INTELLIGENCE", "subtitle": "All 10 franchises, retentions, trades & sources"},

    # RESEARCH Group
    {"id": "Methodology & Validation", "label": "Methodology & Validation", "icon": "flask-conical", "mat_icon": ":material/science:", "group": "RESEARCH", "subtitle": "Formulas, LightGBM calibration & bootstrap audit"},
    {"id": "Data Sources & Provenance", "label": "Data Sources & Provenance", "icon": "database", "mat_icon": ":material/database:", "group": "RESEARCH", "subtitle": "Lineage, checksums, missingness & change log"},
]

NAV_LABELS = [item["label"] for item in NAV_ITEMS]
NAV_META = {item["label"]: item for item in NAV_ITEMS}

NAV_GROUPS = [
    {
        "group": "DISCOVER",
        "items": [item for item in NAV_ITEMS if item["group"] == "DISCOVER"],
    },
    {
        "group": "PLAYER ANALYTICS",
        "items": [item for item in NAV_ITEMS if item["group"] == "PLAYER ANALYTICS"],
    },
    {
        "group": "FRANCHISE INTELLIGENCE",
        "items": [item for item in NAV_ITEMS if item["group"] == "FRANCHISE INTELLIGENCE"],
    },
    {
        "group": "RESEARCH",
        "items": [item for item in NAV_ITEMS if item["group"] == "RESEARCH"],
    },
]

IPL_FRANCHISES = [
    ("RR", "Rajasthan Royals", "#BD6548"),
    ("CSK", "Chennai Super Kings", "#C5A46D"),
    ("MI", "Mumbai Indians", "#3B5C7D"),
    ("KKR", "Kolkata Knight Riders", "#694C7D"),
    ("RCB", "Royal Challengers Bengaluru", "#B84A39"),
    ("SRH", "Sunrisers Hyderabad", "#C86733"),
    ("DC", "Delhi Capitals", "#346187"),
    ("PBKS", "Punjab Kings", "#A83E44"),
    ("GT", "Gujarat Titans", "#3D7A84"),
    ("LSG", "Lucknow Super Giants", "#5B7B5A"),
]

# Editorial Status Badge Styling (bg, border, text)
STATUS_TONES = {
    "Confirmed": ("rgba(132, 146, 122, 0.16)", "#84927A", "#2B472A"),
    "Confirmed Retained": ("rgba(132, 146, 122, 0.16)", "#84927A", "#2B472A"),
    "Confirmed Released": ("rgba(189, 101, 72, 0.12)", "#D8CBBE", "#77675D"),
    "Confirmed Trade": ("rgba(189, 101, 72, 0.16)", "#BD6548", "#822F19"),
    "Reported": ("rgba(197, 164, 109, 0.20)", "#C5A46D", "#694E1E"),
    "Pending Verification": ("rgba(197, 164, 109, 0.18)", "#C5A46D", "#694E1E"),
    "Rumour": ("rgba(216, 203, 190, 0.35)", "#D8CBBE", "#77675D"),
    "Policy/Eligibility Review": ("rgba(184, 74, 57, 0.14)", "#B84A39", "#6D1F13"),
    "Historical": ("rgba(119, 103, 93, 0.12)", "#D8CBBE", "#77675D"),
}
