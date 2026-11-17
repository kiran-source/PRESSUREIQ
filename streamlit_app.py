"""PRESSUREIQ V7.0 — Root Streamlit Entry Point.

This file is the Streamlit Cloud deployment entrypoint.
It resolves the repository root onto sys.path and delegates
to the main dashboard application.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure repo root is importable from any working directory
_REPO_ROOT = Path(__file__).resolve().parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.dashboard.app import main  # noqa: E402

main()
