"""Unit tests for PRESSUREIQ v5.0 Player Visual Intelligence."""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from src.dashboard.data_loader import load_dashboard_bundle_uncached
from src.dashboard.player_images import (
    ASSETS_DIR,
    MANIFEST_PATH,
    get_player_image_b64,
    get_player_image_path,
    get_player_manifest_dict,
)
from src.dashboard.views.player_directory import _build_unified_directory


def test_player_image_manifest_exists_and_complete():
    """Verify manifest is loaded and covers all 227 qualified athletes."""
    manifest = get_player_manifest_dict()
    assert len(manifest) >= 227, f"Expected at least 227 players in manifest, got {len(manifest)}"

    # Check known players
    assert "Ruturaj Gaikwad" in manifest
    assert "Liam Dawson" in manifest
    assert "Naman Dhir" in manifest

    for pname, item in manifest.items():
        assert "file_path" in item
        img_file = ASSETS_DIR.parent.parent / item["file_path"]
        assert img_file.exists(), f"Image file missing for {pname}: {img_file}"
        assert img_file.stat().st_size > 0, f"Image file empty for {pname}: {img_file}"


def test_get_player_image_path():
    """Verify player path lookup and fallback resolution."""
    # Known player
    p_path = get_player_image_path("Ruturaj Gaikwad")
    assert p_path.exists()
    assert p_path.suffix == ".png"

    # Unknown player fallback
    p_fallback = get_player_image_path("Nonexistent Player 999")
    assert p_fallback.exists()
    assert p_fallback.suffix == ".png"


def test_get_player_image_b64():
    """Verify base64 data URI generation and caching."""
    b64_str = get_player_image_b64("Ruturaj Gaikwad")
    assert b64_str.startswith("data:image/png;base64,")
    assert len(b64_str) > 500

    # Ensure caching works and returns identical string
    b64_str_2 = get_player_image_b64("Ruturaj Gaikwad")
    assert b64_str == b64_str_2


def test_unified_directory_builder():
    """Verify player directory combines qualified batters and bowlers correctly."""
    bundle = load_dashboard_bundle_uncached()
    df_dir = _build_unified_directory(bundle)

    assert not df_dir.empty
    assert len(df_dir) == len(bundle.bat_df) + len(bundle.bowl_df)

    unique_names = set(df_dir["player_name"])
    assert len(unique_names) == 227, f"Expected exactly 227 unique athletes, got {len(unique_names)}"

    # Check columns
    required_cols = {"player_id", "player_name", "discipline", "rank", "reliability_score", "hp_balls"}
    assert required_cols.issubset(df_dir.columns)
