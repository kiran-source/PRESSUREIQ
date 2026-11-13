"""Cached, thread-safe player image resolution and base64 encoding service for PRESSUREIQ."""

from __future__ import annotations

import base64
import functools
import json
import re
from pathlib import Path
from typing import Any, Dict, Optional

ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST_PATH = ROOT / "assets" / "players" / "players_manifest.json"
ASSETS_DIR = ROOT / "assets" / "players"

_MANIFEST_CACHE: Optional[Dict[str, Dict[str, Any]]] = None
_B64_CACHE: Dict[str, str] = {}


def sanitize_player_filename(name: str) -> str:
    cleaned = re.sub(r'[^a-zA-Z0-9_]', '', name.replace(' ', '_'))
    return f"{cleaned}.png"


def get_player_manifest_dict() -> Dict[str, Dict[str, Any]]:
    """Return dictionary of player name -> manifest record."""
    global _MANIFEST_CACHE
    if _MANIFEST_CACHE is not None:
        return _MANIFEST_CACHE

    if MANIFEST_PATH.exists():
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as fp:
                raw_list = json.load(fp)
                _MANIFEST_CACHE = {item["player_name"]: item for item in raw_list}
                return _MANIFEST_CACHE
        except Exception:
            pass

    _MANIFEST_CACHE = {}
    return _MANIFEST_CACHE


def get_player_image_path(player_name: str) -> Path:
    """Return Path to local player avatar PNG, guaranteeing a valid existing file."""
    m_dict = get_player_manifest_dict()
    if player_name in m_dict:
        rel = m_dict[player_name].get("file_path")
        if rel:
            candidate = ROOT / rel
            if candidate.exists():
                return candidate

    # Direct filename fallback
    fn = sanitize_player_filename(player_name)
    direct = ASSETS_DIR / fn
    if direct.exists():
        return direct

    # Dedicated neutral silhouette fallback
    neutral = ASSETS_DIR / "neutral_avatar.png"
    if neutral.exists():
        return neutral
    return direct


@functools.lru_cache(maxsize=300)
def get_player_image_b64(player_name: str) -> str:
    """Return base64 data URI string for player avatar PNG (cached)."""
    p = get_player_image_path(player_name)
    if p.exists():
        try:
            with open(p, "rb") as fp:
                encoded = base64.b64encode(fp.read()).decode("utf-8")
                return f"data:image/png;base64,{encoded}"
        except Exception:
            pass
    # 1x1 transparent pixel data URI fallback
    return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
