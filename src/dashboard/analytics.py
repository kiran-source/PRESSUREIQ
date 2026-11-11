"""Pure analytical transformations and market-status safeguards for PRESSUREIQ Dashboard."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

K_SHRINK_CANONICAL = 45.0

STRICT_MARKET_STATUSES = [
    "Confirmed Trade",
    "Confirmed Retained",
    "Confirmed Released",
    "Pending Verification",
    "Rumour",
    "Policy/Eligibility Review",
]

_FORBIDDEN_AVAILABILITY_RE = re.compile(
    r"(confirmed\s+available|confirmed\s+released|officially\s+available|"
    r"officially\s+released|confirmed\s+target|released\s+for\s+auction)",
    re.IGNORECASE,
)


def _safe_float(val: Any, default: float = 0.0) -> float:
    if val is None or pd.isna(val):
        return default
    try:
        return float(val)
    except (TypeError, ValueError):
        return default


def extract_unique_teams(df: pd.DataFrame) -> List[str]:
    """Extract sorted unique team labels from mapped teams_list column."""
    if df.empty or "teams_list" not in df.columns:
        return []
    return sorted(
        {
            t.strip()
            for s in df["teams_list"].dropna()
            for t in str(s).split(",")
            if t.strip()
        }
    )


def add_effective_sample_columns(df: pd.DataFrame, k_shrink: float = K_SHRINK_CANONICAL) -> pd.DataFrame:
    """Distinguish raw high-pressure opportunities from EB shrinkage weight and effective sample sizes."""
    if df.empty:
        return df
    out = df.copy()
    hp = pd.to_numeric(out.get("hp_balls", 0), errors="coerce").fillna(0.0)
    weight = hp / (hp + float(k_shrink))
    out["eb_shrinkage_weight"] = np.round(weight, 3)
    out["eb_effective_hp_balls"] = np.round(hp * weight, 1)
    if "kish_match_ess" not in out.columns:
        out["kish_match_ess"] = np.nan
    return out


def prepare_leaderboard_table(df: pd.DataFrame, is_batting: bool = True) -> pd.DataFrame:
    """Format official frozen leaderboard with sample-size distinction and bootstrap uncertainty."""
    if df.empty or "rank" not in df.columns:
        return df
    work = add_effective_sample_columns(df).sort_values("rank", ascending=True).copy()

    work["score_ci_95"] = work.apply(
        lambda r: f"[{_safe_float(r.get('ci_lower_95')):.1f}, {_safe_float(r.get('ci_upper_95')):.1f}]"
        if pd.notna(r.get("ci_lower_95")) and pd.notna(r.get("ci_upper_95"))
        else "N/A",
        axis=1,
    )
    work["rank_ci_95"] = work.apply(
        lambda r: f"[#{int(round(_safe_float(r.get('boot_rank_ci_lower_95'))))}, #{int(round(_safe_float(r.get('boot_rank_ci_upper_95'))))}]"
        if pd.notna(r.get("boot_rank_ci_lower_95")) and pd.notna(r.get("boot_rank_ci_upper_95"))
        else "N/A",
        axis=1,
    )
    work["top10_prob_pct"] = np.round(pd.to_numeric(work.get("top10_inclusion_prob", 0.0), errors="coerce").fillna(0.0) * 100.0, 1)
    work["boot_median_rank_int"] = pd.to_numeric(work.get("boot_median_rank", work.get("boot_mean_rank")), errors="coerce").round(0)

    if is_batting:
        work["total_sample_balls"] = pd.to_numeric(work.get("total_balls", 0), errors="coerce").fillna(0)
        work["primary_rate_label"] = pd.to_numeric(work.get("career_sr", 0.0), errors="coerce").round(1)
    else:
        work["total_sample_balls"] = pd.to_numeric(work.get("legal_balls", 0), errors="coerce").fillna(0)
        work["primary_rate_label"] = pd.to_numeric(work.get("career_economy", 0.0), errors="coerce").round(2)

    return work


def filter_leaderboard(
    df: pd.DataFrame,
    roles: Optional[List[str]] = None,
    role_col: str = "role",
    team_filter: str = "All Teams",
    min_hp_balls: int = 0,
    min_matches: int = 0,
    search_query: str = "",
) -> pd.DataFrame:
    """Filter leaderboard without changing frozen Official Model A career rank numbers."""
    if df.empty or "rank" not in df.columns:
        return df
    out = df.copy()
    if roles is not None and role_col in out.columns:
        out = out[out[role_col].isin(roles)]
    if team_filter and team_filter != "All Teams" and "teams_list" in out.columns:
        out = out[out["teams_list"].str.contains(team_filter, case=False, na=False, regex=False)]
    if min_hp_balls > 0 and "hp_balls" in out.columns:
        out = out[pd.to_numeric(out["hp_balls"], errors="coerce").fillna(0) >= int(min_hp_balls)]
    if min_matches > 0 and "matches" in out.columns:
        out = out[pd.to_numeric(out["matches"], errors="coerce").fillna(0) >= int(min_matches)]
    if search_query and search_query.strip() and "player_name" in out.columns:
        out = out[out["player_name"].str.contains(search_query.strip(), case=False, na=False, regex=False)]
    return out.sort_values("rank", ascending=True)


def compute_player_phase_summary(player_delivs: pd.DataFrame, is_batting: bool = True) -> pd.DataFrame:
    """Compute Powerplay / Middle / Death metrics from actual player deliveries."""
    if player_delivs.empty:
        return pd.DataFrame()

    p_col = "bpi" if is_batting else "bopi"
    raw_col = "raw_bat_value" if is_batting else "raw_bowl_value"

    rows = []
    for ph in ["Powerplay", "Middle", "Death"]:
        ph_all = player_delivs[player_delivs["phase"] == ph]
        if ph_all.empty:
            continue
        if is_batting:
            ph_df = ph_all[ph_all["is_batter_ball"] == 1]
            if ph_df.empty:
                continue
            balls = int(len(ph_df))
            hp_balls = int((ph_df[p_col] >= 50.0).sum())
            mean_p = _safe_float(ph_df[p_col].mean(), 0.0)
            mean_raw_pava = _safe_float(ph_df[raw_col].mean(), 0.0)
            runs = int(ph_df["batter_runs"].sum())
            rate_val = round(runs * 100.0 / balls, 1) if balls > 0 else 0.0
            events = int(ph_df["is_boundary"].sum()) if "is_boundary" in ph_df.columns else 0
            rows.append({
                "Phase": ph,
                "Balls": balls,
                "HP Balls (P>=50)": hp_balls,
                "Runs": runs,
                "Strike Rate": rate_val,
                "Boundaries": events,
                "Avg BPI": round(mean_p, 1),
                "Raw PAVA / Ball": round(mean_raw_pava, 4),
            })
        else:
            # MCC-compliant economy: include wide/no-ball runs from all deliveries,
            # while legal deliveries serve as the ball denominator and BoPI>=50 pool.
            ph_legal = ph_all[ph_all["is_legal_ball"] == 1]
            balls = int(len(ph_legal))
            hp_balls = int((ph_legal[p_col] >= 50.0).sum()) if not ph_legal.empty else 0
            mean_p = _safe_float(ph_legal[p_col].mean(), 0.0) if not ph_legal.empty else 0.0
            mean_raw_pava = _safe_float(ph_legal[raw_col].mean(), 0.0) if not ph_legal.empty else 0.0
            runs_c = int(ph_all["bowler_runs_conceded"].sum())
            rate_val = round(runs_c * 6.0 / balls, 2) if balls > 0 else 0.0
            wkts = int(ph_all["is_bowler_wicket"].sum()) if "is_bowler_wicket" in ph_all.columns else 0
            rows.append({
                "Phase": ph,
                "Legal Balls": balls,
                "HP Balls (BoPI>=50)": hp_balls,
                "Runs Conceded": runs_c,
                "Economy": rate_val,
                "Wickets": wkts,
                "Avg BoPI": round(mean_p, 1),
                "Raw PAVA / Ball": round(mean_raw_pava, 4),
            })
    return pd.DataFrame(rows)


def compute_player_five_pillars(player_row: pd.Series) -> Dict[str, float]:
    """Compute normalized 0-100 Five-Pillar scores cleanly handling NaN/None inputs."""
    p1 = float(np.clip(_safe_float(player_row.get("shrunk_hp_pava_per_ball"), 0.0) * 80.0 + 50.0, 10.0, 100.0))
    p2 = float(np.clip(_safe_float(player_row.get("retention_delta"), 0.0) * 40.0 + 50.0, 10.0, 100.0))
    p3 = float(np.clip(_safe_float(player_row.get("consistency_score"), 30.0), 0.0, 100.0))
    p4 = float(np.clip(_safe_float(player_row.get("adaptability_score"), 60.0), 0.0, 100.0))
    p5 = float(np.clip(_safe_float(player_row.get("evidence_weight"), 0.5) * 100.0, 0.0, 100.0))
    return {
        "Shrunk HP PAVA": round(p1, 1),
        "Baseline Retention": round(p2, 1),
        "Match Consistency": round(p3, 1),
        "Context Adaptability": round(p4, 1),
        "Evidence Weight": round(p5, 1),
    }


def compute_peer_comparison(
    rankings_df: pd.DataFrame,
    player_id: int,
    role_col: str,
) -> Tuple[pd.Series, Dict[str, float], int, int]:
    """Return selected player row, role-peer five-pillar means, rank within role, and role cohort size."""
    if rankings_df.empty or "player_id" not in rankings_df.columns:
        return pd.Series(dtype=object), {}, 0, 0
    matched = rankings_df[rankings_df["player_id"] == player_id]
    if matched.empty:
        return pd.Series(dtype=object), {}, 0, 0

    sel = matched.iloc[0]
    peers = rankings_df[rankings_df[role_col] == sel[role_col]].sort_values("rank", ascending=True)
    role_rank = int((peers["player_id"].values == player_id).nonzero()[0][0]) + 1

    peer_pillars_list = [compute_player_five_pillars(r) for _, r in peers.iterrows()]
    peer_df = pd.DataFrame(peer_pillars_list)
    peer_means = peer_df.mean().round(1).to_dict() if not peer_df.empty else {}
    return sel, peer_means, role_rank, len(peers)


def sanitize_availability_label(market_status: Any, raw_availability: Any) -> str:
    """Case-insensitive safeguard: non-released records must never read Confirmed Available."""
    status = "" if (market_status is None or pd.isna(market_status)) else str(market_status).strip()
    text = "" if (raw_availability is None or pd.isna(raw_availability)) else str(raw_availability).strip()

    if status != "Confirmed Released":
        if not text or _FORBIDDEN_AVAILABILITY_RE.search(text):
            if status in {"Confirmed Trade", "Confirmed Retained"}:
                return f"{status} — Unavailable for Open Auction"
            return f"{status or 'Pending Verification'} — Availability Unverified (Awaiting Nov 17 Official Filing)"
    return text


def prepare_market_display(market_df: pd.DataFrame, selected_statuses: Optional[List[str]] = None) -> pd.DataFrame:
    """Filter and sanitize all displayed availability/status fields in market ledger."""
    if market_df.empty:
        return market_df
    work = market_df.copy()
    if selected_statuses is not None and "official_retention_status" in work.columns:
        work = work[work["official_retention_status"].isin(selected_statuses)].copy()
    if work.empty:
        return work
    for col in ("official_release_status", "auction_availability"):
        if col in work.columns:
            work[col] = work.apply(
                lambda r: sanitize_availability_label(r.get("official_retention_status"), r.get(col)),
                axis=1,
            )
    return work


def enrich_emerging_watchlist(emerging_df: pd.DataFrame, market_df: pd.DataFrame) -> pd.DataFrame:
    """Attach live audited market status to watchlist entries."""
    if emerging_df.empty:
        return emerging_df
    out = emerging_df.copy()
    mkt_map = (
        market_df.set_index("player_name")["official_retention_status"].to_dict()
        if (not market_df.empty and "player_name" in market_df.columns and "official_retention_status" in market_df.columns)
        else {}
    )
    out["audited_market_status"] = out["player_name"].map(lambda n: mkt_map.get(n, "Pending Verification (Pre-Nov 17)"))
    return out


def build_benchmark_rows(bm: Dict[str, Any]) -> pd.DataFrame:
    """Shape MODEL_BENCHMARK_REPORT.json into structured DataFrame rows."""
    if not bm:
        return pd.DataFrame()
    rows = [
        {
            "Model Target": "Batting Expected Runs (RMSE)",
            "Val 2025": bm.get("batting_expected_runs", {}).get("validation_2025", {}).get("LightGBM", {}).get("RMSE"),
            "Test 2026": bm.get("batting_expected_runs", {}).get("untouched_test_2026", {}).get("LightGBM", {}).get("RMSE"),
        },
        {
            "Model Target": "Batting Dismissal Prob (Brier / ECE)",
            "Val 2025": f"{bm.get('batting_dismissal_prob', {}).get('validation_2025', {}).get('Brier_Score')} / {bm.get('batting_dismissal_prob', {}).get('validation_2025', {}).get('ECE')}",
            "Test 2026": f"{bm.get('batting_dismissal_prob', {}).get('untouched_test_2026', {}).get('Brier_Score')} / {bm.get('batting_dismissal_prob', {}).get('untouched_test_2026', {}).get('ECE')}",
        },
        {
            "Model Target": "Bowling Expected Runs (RMSE)",
            "Val 2025": bm.get("bowling_expected_runs", {}).get("validation_2025", {}).get("LightGBM_RMSE"),
            "Test 2026": bm.get("bowling_expected_runs", {}).get("untouched_test_2026", {}).get("LightGBM_RMSE"),
        },
        {
            "Model Target": "Bowling Wicket Prob (Brier / ECE)",
            "Val 2025": f"{bm.get('bowling_wicket_prob', {}).get('validation_2025', {}).get('Brier_Score')} / {bm.get('bowling_wicket_prob', {}).get('validation_2025', {}).get('ECE')}",
            "Test 2026": f"{bm.get('bowling_wicket_prob', {}).get('untouched_test_2026', {}).get('Brier_Score')} / {bm.get('bowling_wicket_prob', {}).get('untouched_test_2026', {}).get('ECE')}",
        },
    ]
    return pd.DataFrame(rows)


def build_ablation_rows(val_json: Dict[str, Any]) -> pd.DataFrame:
    """Shape VALIDATION_REPORT.json ablations into structured DataFrame rows."""
    abls = val_json.get("ablations", {}) if val_json else {}
    if not abls:
        return pd.DataFrame()
    return pd.DataFrame(
        [
            {
                "Ablation Variant": k.replace("_", " ").title(),
                "Top-10 Overlap (out of 10)": v.get("top10_overlap_with_full"),
                "Jaccard Similarity": v.get("jaccard_similarity"),
            }
            for k, v in abls.items()
        ]
    )


def summarize_rr_squad_intelligence(
    audit_df: pd.DataFrame,
    candidates_df: pd.DataFrame,
) -> Dict[str, pd.DataFrame]:
    """Build RR 2026 core profile and recruitment fit tables separating fit from market availability."""
    if audit_df.empty or candidates_df.empty:
        return {"rr_core": pd.DataFrame(), "role_depth": pd.DataFrame(), "targets": pd.DataFrame()}

    rr_core = audit_df[audit_df["eligibility_class"] == "A"].sort_values("reliability_score", ascending=False).copy()
    rr_core["market_status_verified"] = rr_core["market_status"].astype(str)

    role_depth = (
        rr_core.groupby(["discipline", "role"], as_index=False)
        .agg(
            Players=("player_name", "count"),
            Avg_Reliability=("reliability_score", "mean"),
            Total_HP_Balls=("hp_balls", "sum"),
        )
    )
    role_depth["Avg_Reliability"] = role_depth["Avg_Reliability"].round(2)

    targets = candidates_df[candidates_df["eligibility_class"] != "A"].copy()
    targets["auction_availability"] = targets.apply(
        lambda r: sanitize_availability_label(r.get("market_status", "Pending Verification"), r.get("auction_availability", "")),
        axis=1,
    )
    targets["market_verified_available"] = targets["market_status"].isin(["Confirmed Released"])
    return {"rr_core": rr_core, "role_depth": role_depth, "targets": targets}


def summarize_market_counts(market_df: pd.DataFrame) -> Dict[str, int]:
    """Return exact counts across the strict 6-status taxonomy."""
    counts = {s: 0 for s in STRICT_MARKET_STATUSES}
    if market_df.empty or "official_retention_status" not in market_df.columns:
        return counts
    vc = market_df["official_retention_status"].value_counts().to_dict()
    for s in STRICT_MARKET_STATUSES:
        counts[s] = int(vc.get(s, 0))
    return counts
