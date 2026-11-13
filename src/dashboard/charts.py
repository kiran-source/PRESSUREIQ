"""Warm editorial Plotly visualization builders for PRESSUREIQ v4.

Aesthetics: Contemporary Luxury Magazine (Kinfolk & Monocle style)
Warm Ivory (#F8F4EC) + Soft Cream (#F1E9DD) + Terracotta (#BD6548) + Muted Gold (#C5A46D) + Sage (#84927A)
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.dashboard.analytics import compute_eb_shrinkage_curve, compute_player_five_pillars
from src.dashboard.design_tokens import FONTS, PALETTE, PLOTLY_SERIES

# Preserved exported constants for backwards compatibility with tests & views
RR_BLUE = PALETTE["accent_terracotta"]       # Terracotta (#BD6548)
RR_PINK = PALETTE["accent_gold"]             # Muted Gold (#C5A46D)
INK_DARK = PALETTE["text_primary"]           # Deep Ink (#282321)
SLATE_MUTED = PALETTE["text_secondary"]      # Muted Brown (#77675D)
EMERALD = PALETTE["positive"]                # Sage Green (#5B7B5A)
AMBER = PALETTE["warning"]                   # Amber Gold (#C58B38)
CRIMSON = PALETTE["danger"]                  # Clay Red (#B84A39)
CYAN = PALETTE["accent_sage"]                # Olive Sage (#84927A)

ARCHETYPE_COLORS = {
    "Clutch Climber": EMERALD,
    "Ice Cold Anchor": RR_BLUE,
    "Gradual Decliner": AMBER,
    "Pressure Fragile": CRIMSON,
    "Unclassified (Insufficient Evidence)": PALETTE["text_muted"],
}


def _apply_base_layout(fig: go.Figure, title: str, height: int = 400) -> go.Figure:
    """Apply consistent warm editorial styling across all Plotly charts."""
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=14, color=PALETTE["text_primary"], family="Playfair Display, serif"),
            x=0.01,
        ),
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        height=height,
        margin=dict(l=54, r=24, t=54, b=50),
        font=dict(family="Inter, -apple-system, sans-serif", size=11.5, color=PALETTE["text_secondary"]),
        hoverlabel=dict(
            bgcolor="#FAF6F0",
            bordercolor="#D8CBBE",
            font=dict(size=11.5, color="#282321", family="JetBrains Mono, monospace"),
        ),
        legend=dict(
            font=dict(color=PALETTE["text_secondary"], size=10.5),
            bgcolor="rgba(0,0,0,0)",
        ),
    )
    fig.update_xaxes(
        gridcolor="#EAE1D5",
        zerolinecolor="#D8CBBE",
        tickfont=dict(color=PALETTE["text_secondary"], size=10.5),
        title_font=dict(color=PALETTE["text_primary"], size=11.5, family="Inter, sans-serif"),
    )
    fig.update_yaxes(
        gridcolor="#EAE1D5",
        zerolinecolor="#D8CBBE",
        tickfont=dict(color=PALETTE["text_secondary"], size=10.5),
        title_font=dict(color=PALETTE["text_primary"], size=11.5, family="Inter, sans-serif"),
    )
    return fig


def fig_top10_ci_bar(df: pd.DataFrame, title: str, accent_color: str = RR_BLUE) -> go.Figure:
    """Top 10 players bar chart with 95% bootstrap error bars in warm editorial styling."""
    if df.empty or "rank" not in df.columns:
        return go.Figure()
    top10 = df.sort_values("rank", ascending=True).head(10).copy()
    if top10.empty:
        return go.Figure()

    scores = pd.to_numeric(top10.get("reliability_score"), errors="coerce").fillna(0.0)
    ci_lo = pd.to_numeric(top10.get("ci_lower_95"), errors="coerce").fillna(scores)
    ci_hi = pd.to_numeric(top10.get("ci_upper_95"), errors="coerce").fillna(scores)
    hp_vals = pd.to_numeric(top10.get("hp_balls"), errors="coerce").fillna(0).astype(int)
    top10_p = pd.to_numeric(top10.get("top10_inclusion_prob"), errors="coerce").fillna(0.0) * 100.0
    arch = top10.get("prc_archetype", pd.Series(["N/A"] * len(top10))).fillna("N/A")

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=top10["player_name"],
            y=scores,
            error_y=dict(
                type="data",
                symmetric=False,
                array=(ci_hi - scores).clip(lower=0.0),
                arrayminus=(scores - ci_lo).clip(lower=0.0),
                color="#77675D",
                thickness=1.5,
                width=4,
            ),
            marker=dict(
                color=accent_color,
                line=dict(color="#D8CBBE", width=1),
            ),
            customdata=np.stack([top10["rank"], hp_vals, top10_p, arch], axis=-1),
            name="Score & 95% CI",
            showlegend=False,
            hovertemplate=(
                "<b>%{x}</b> (Rank #%{customdata[0]})<br>"
                "Reliability Score: %{y:.2f} (norm-CDF index)<br>"
                "HP Opportunities: %{customdata[1]} balls<br>"
                "Bootstrap Top-10 Prob: %{customdata[2]:.1f}%<br>"
                "PRC Class: %{customdata[3]}<extra></extra>"
            ),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=top10["player_name"],
            y=ci_hi + 2.8,
            mode="text",
            text=scores.round(1).astype(str),
            textfont=dict(size=10.5, color="#282321", family="JetBrains Mono, monospace"),
            showlegend=False,
            hoverinfo="skip",
        )
    )
    min_y = max(0.0, float(ci_lo.min()) - 8.0) if not ci_lo.empty else 0.0
    fig = _apply_base_layout(fig, title, height=410)
    fig.update_yaxes(range=[min_y, 108.0], title="Reliability Score (0–100)")
    fig.update_xaxes(title="", tickangle=-22)
    return fig


def fig_score_distribution(df: pd.DataFrame, title: str, accent_color: str = RR_BLUE) -> go.Figure:
    """Plot league-wide reliability score distribution."""
    if df.empty or "reliability_score" not in df.columns:
        return go.Figure()
    work = df.dropna(subset=["reliability_score"]).copy()
    if work.empty:
        return go.Figure()
    fig = px.histogram(
        work,
        x="reliability_score",
        nbins=22,
        color="prc_archetype" if "prc_archetype" in work.columns else None,
        color_discrete_map=ARCHETYPE_COLORS,
        opacity=0.85,
        labels={"reliability_score": "Reliability Score (0–100)", "prc_archetype": "PRC Class"},
    )
    med_val = float(work["reliability_score"].median())
    fig = _apply_base_layout(fig, title, height=390)
    if np.isfinite(med_val):
        fig.add_vline(
            x=med_val,
            line_dash="dash",
            line_color="#77675D",
            annotation_text=f"Median: {med_val:.1f}",
            annotation_position="top left",
            annotation_font=dict(color="#282321", size=11),
        )
    fig.update_yaxes(title="Players Count")
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="center", x=0.5))
    return fig


def fig_sample_vs_score(df: pd.DataFrame, is_batting: bool = True) -> go.Figure:
    """Scatter plot of sample exposure vs reliability score."""
    if df.empty or "hp_balls" not in df.columns or "reliability_score" not in df.columns:
        return go.Figure()
    work = df.dropna(subset=["hp_balls", "reliability_score"]).copy()
    if work.empty:
        return go.Figure()
    work["_scatter_size"] = pd.to_numeric(work.get("matches", 1), errors="coerce").fillna(1).clip(lower=1)
    label = f"{'Batters' if is_batting else 'Bowlers'} ({len(work)} Qualified)"
    fig = px.scatter(
        work,
        x="hp_balls",
        y="reliability_score",
        size="_scatter_size",
        color="prc_archetype" if "prc_archetype" in work.columns else None,
        color_discrete_map=ARCHETYPE_COLORS,
        hover_name="player_name",
        hover_data={
            "rank": True,
            "hp_balls": True,
            "matches": True,
            "top10_inclusion_prob": ":.3f",
            "prc_archetype": True,
            "_scatter_size": False,
        },
        labels={
            "hp_balls": "High-Pressure Opportunities (P >= 50.0 Balls)",
            "reliability_score": "Reliability Score (0–100)",
            "prc_archetype": "PRC Class",
        },
    )
    fig = _apply_base_layout(fig, f"Sample Exposure vs Reliability Score — {label}", height=430)
    fig.add_vline(
        x=45,
        line_dash="dot",
        line_color=PALETTE["warning"],
        annotation_text="K_shrink = 45 HP",
        annotation_font=dict(color=PALETTE["warning_text"], size=11),
    )
    return fig


def fig_rank_uncertainty_intervals(df: pd.DataFrame, top_n: int = 15, title: str = "Bootstrap Rank Uncertainty") -> go.Figure:
    """Plot 2,000-bootstrap rank uncertainty intervals."""
    if df.empty or "rank" not in df.columns:
        return go.Figure()
    sub = df.sort_values("rank", ascending=True).head(top_n).copy().iloc[::-1]
    if sub.empty:
        return go.Figure()

    ci_lo = pd.to_numeric(sub.get("boot_rank_ci_lower_95"), errors="coerce").fillna(sub["rank"])
    ci_hi = pd.to_numeric(sub.get("boot_rank_ci_upper_95"), errors="coerce").fillna(sub["rank"])
    med_col = "boot_median_rank" if "boot_median_rank" in sub.columns else "boot_mean_rank"
    med_vals = pd.to_numeric(sub.get(med_col, sub["rank"]), errors="coerce").fillna(sub["rank"])

    fig = go.Figure()
    for name, lo, hi in zip(sub["player_name"], ci_lo, ci_hi):
        fig.add_trace(
            go.Scatter(
                x=[lo, hi],
                y=[name, name],
                mode="lines",
                line=dict(color="#D8CBBE", width=6),
                showlegend=False,
                hoverinfo="skip",
            )
        )
    fig.add_trace(
        go.Scatter(
            x=sub["rank"],
            y=sub["player_name"],
            mode="markers",
            name="Frozen Model A Rank",
            marker=dict(color=RR_BLUE, size=10, symbol="diamond", line=dict(color="#282321", width=1)),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=med_vals,
            y=sub["player_name"],
            mode="markers",
            name="Bootstrap Median Rank (N=2,000)",
            marker=dict(color=RR_PINK, size=9, symbol="circle", line=dict(color="#282321", width=1)),
        )
    )
    max_x = max(15, int(ci_hi.max()) + 8) if np.isfinite(ci_hi.max()) else 155
    fig = _apply_base_layout(fig, title, height=max(420, top_n * 28))
    fig.update_xaxes(title="Rank Position (Lower is Better; Bar = 95% Bootstrap Interval)", autorange=False, range=[0, min(155, max_x)])
    fig.update_yaxes(title="")
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5))
    return fig


def fig_pressure_response_curve(player_delivs: pd.DataFrame, player_name: str, is_batting: bool = True) -> go.Figure:
    """Render player empirical pressure response bar breakdown across leverage tiers."""
    if player_delivs.empty:
        return go.Figure()
    ball_col = "is_batter_ball" if is_batting else "is_legal_ball"
    p_col = "bpi" if is_batting else "bopi"
    raw_col = "raw_bat_value" if is_batting else "raw_bowl_value"
    sub = player_delivs[player_delivs[ball_col] == 1].dropna(subset=[p_col, raw_col]).copy()
    if sub.empty:
        return go.Figure()

    bins = [0, 35, 65, 85, 100.1]
    labels = ["Low (<35)", "Medium [35–65)", "High [65–85)", "Extreme (>=85)"]
    sub["tier"] = pd.cut(sub[p_col], bins=bins, labels=labels, right=False)
    tier_df = sub.groupby("tier", observed=False).agg(
        mean_raw=(raw_col, "mean"),
        n_balls=(raw_col, "count"),
        mean_p=(p_col, "mean"),
    ).reset_index()

    y_vals = [0.0 if (pd.isna(v) or n == 0) else float(v) for v, n in zip(tier_df["mean_raw"], tier_df["n_balls"])]
    bar_text = [
        "No balls (n=0)" if (pd.isna(v) or n == 0) else f"{float(v):+.3f} (n={int(n)})"
        for v, n in zip(tier_df["mean_raw"], tier_df["n_balls"])
    ]

    tier_palette = ["#D8CBBE", "#C5A46D", "#BD6548", "#5B7B5A"]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=tier_df["tier"].astype(str),
            y=y_vals,
            marker_color=tier_palette,
            text=bar_text,
            textposition="outside",
            textfont=dict(color="#282321", size=10.5, family="JetBrains Mono, monospace"),
            name="Tier Mean Raw PAVA/ball",
        )
    )
    index_name = "BPI" if is_batting else "BoPI"
    fig = _apply_base_layout(fig, f"Pressure Response Profile — {player_name}", height=405)
    fig.add_hline(y=0.0, line_dash="dash", line_color="#D8CBBE")
    max_y = max(y_vals) if y_vals else 0.1
    min_y = min(y_vals) if y_vals else 0.0
    fig.update_yaxes(title="Mean Raw PAVA (Runs / Ball)", range=[min(0.0, min_y) - 0.06, max(0.15, max_y * 1.25)])
    fig.update_xaxes(title=f"{index_name} Pressure Tier")
    fig.update_layout(margin=dict(l=64, r=28, t=60, b=52))
    return fig


def fig_phase_performance(phase_df: pd.DataFrame, player_name: str, is_batting: bool = True) -> go.Figure:
    """Render phase-wise value added bar breakdown."""
    if phase_df.empty or "Raw PAVA / Ball" not in phase_df.columns:
        return go.Figure()
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=phase_df["Phase"],
            y=phase_df["Raw PAVA / Ball"],
            name="Raw PAVA / Ball",
            marker_color=RR_BLUE if is_batting else RR_PINK,
            text=phase_df["Raw PAVA / Ball"].apply(lambda v: f"{v:+.3f}"),
            textposition="outside",
            textfont=dict(color="#282321", size=10.5, family="JetBrains Mono, monospace"),
        )
    )
    fig = _apply_base_layout(fig, f"Phase-Wise Value Added — {player_name}", height=370)
    fig.add_hline(y=0.0, line_dash="dash", line_color="#D8CBBE")
    fig.update_yaxes(title="Mean Raw PAVA (Runs/Ball)")
    fig.update_xaxes(title="Innings Phase")
    return fig


def fig_five_pillar_radar(player_row: pd.Series, peer_means: Dict[str, float], player_name: str, role_label: str) -> go.Figure:
    """5-Pillar Spider Radar with warm cream polar background and terracotta polygon."""
    if player_row.empty:
        return go.Figure()
    pillars = compute_player_five_pillars(player_row)
    cats = list(pillars.keys())
    vals = list(pillars.values())
    peer_vals = [peer_means.get(c, 50.0) for c in cats]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=vals + [vals[0]],
            theta=cats + [cats[0]],
            fill="toself",
            fillcolor="rgba(189, 101, 72, 0.22)",
            name=player_name,
            line=dict(color=RR_BLUE, width=2.4),
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=peer_vals + [peer_vals[0]],
            theta=cats + [cats[0]],
            fill="toself",
            fillcolor="rgba(197, 164, 109, 0.16)",
            name=f"{role_label} Peer Mean",
            line=dict(color=RR_PINK, width=2, dash="dash"),
        )
    )
    res = _apply_base_layout(fig, f"Five-Pillar Profile vs {role_label} Peers (0–100 Scaled)", height=415)
    res.update_layout(
        polar=dict(
            bgcolor="#FAF6F0",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="#EAE1D5", tickfont=dict(color="#77675D", size=9.5)),
            angularaxis=dict(gridcolor="#EAE1D5", tickfont=dict(color="#282321", size=10.5, family="Inter, sans-serif")),
        ),
        margin=dict(l=90, r=90, t=64, b=54),
        legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5),
    )
    return res


def fig_batter_vs_bowler_comparison(bat_df: pd.DataFrame, bowl_df: pd.DataFrame) -> go.Figure:
    """Compare score distributions between qualified Batters and Bowlers."""
    if bat_df.empty or bowl_df.empty:
        return go.Figure()
    bat_lbl = f"Batters ({len(bat_df)})"
    bowl_lbl = f"Bowlers ({len(bowl_df)})"
    b1 = bat_df[["player_name", "reliability_score", "hp_balls", "prc_archetype"]].copy()
    b1["Discipline"] = bat_lbl
    b2 = bowl_df[["player_name", "reliability_score", "hp_balls", "prc_archetype"]].copy()
    b2["Discipline"] = bowl_lbl
    comb = pd.concat([b1, b2], ignore_index=True)

    fig = px.box(
        comb,
        x="Discipline",
        y="reliability_score",
        color="Discipline",
        points="all",
        hover_name="player_name",
        color_discrete_map={bat_lbl: RR_BLUE, bowl_lbl: RR_PINK},
        labels={"reliability_score": "Reliability Score (0–100)", "Discipline": ""},
    )
    return _apply_base_layout(fig, "Score Distribution Comparison: Qualified Batters vs Bowlers", height=400)


def fig_rr_role_depth(role_depth_df: pd.DataFrame) -> go.Figure:
    """Visualize Rajasthan Royals squad core depth by role."""
    if role_depth_df.empty:
        return go.Figure()
    fig = px.bar(
        role_depth_df,
        x="role",
        y="Players",
        color="discipline",
        text="Avg_Reliability",
        color_discrete_map={"Batter": RR_BLUE, "Bowler": RR_PINK},
        labels={"role": "Squad Role", "Players": "Qualified Core Players", "discipline": "Discipline"},
    )
    fig.update_traces(texttemplate="Avg %{text:.1f}", textposition="outside", textfont=dict(color="#282321", size=10.5))
    return _apply_base_layout(fig, "Rajasthan Royals 2026 Qualified Core Depth by Role", height=390)


def fig_player_expected_vs_observed(player_delivs: pd.DataFrame, player_name: str, is_batting: bool = True) -> go.Figure:
    """Compare LightGBM pre-ball expected runs vs actual runs across pressure tiers."""
    if player_delivs.empty:
        return go.Figure()
    ball_col = "is_batter_ball" if is_batting else "is_legal_ball"
    p_col = "bpi" if is_batting else "bopi"
    obs_col = "batter_runs" if is_batting else "bowler_runs_conceded"
    exp_col = "exp_batter_runs" if is_batting else "exp_bowler_runs"
    if exp_col not in player_delivs.columns or obs_col not in player_delivs.columns:
        return go.Figure()

    sub = player_delivs[player_delivs[ball_col] == 1].dropna(subset=[p_col, obs_col, exp_col]).copy()
    if sub.empty:
        return go.Figure()
    sub["tier"] = pd.cut(sub[p_col], bins=[0, 35, 65, 85, 100.1], labels=["Low (<35)", "Medium [35–65)", "High [65–85)", "Extreme (>=85)"], right=False)
    agg = sub.groupby("tier", observed=False).agg(obs=(obs_col, "mean"), exp=(exp_col, "mean"), n=(obs_col, "count")).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(x=agg["tier"].astype(str), y=agg["exp"], name="Expected Runs / Ball (LightGBM)", marker_color="#D8CBBE"))
    fig.add_trace(go.Bar(x=agg["tier"].astype(str), y=agg["obs"], name="Observed Runs / Ball", marker_color=EMERALD if is_batting else RR_PINK))
    fig = _apply_base_layout(fig, f"Expected vs Observed Runs / Ball — {player_name}", height=370)
    fig.update_layout(barmode="group", legend=dict(orientation="h", yanchor="bottom", y=-0.24, xanchor="center", x=0.5))
    fig.update_yaxes(title="Runs / Ball")
    return fig


def build_player_color_map(player_names: Any) -> Dict[str, str]:
    """Build a deterministic player-to-color mapping preserving original selection order."""
    mapping: Dict[str, str] = {}
    for name in player_names:
        key = str(name)
        if key not in mapping:
            mapping[key] = PLOTLY_SERIES[len(mapping) % len(PLOTLY_SERIES)]
    return mapping


def fig_multi_player_radar(selected_df: pd.DataFrame, color_map: Optional[Dict[str, str]] = None) -> go.Figure:
    """Overlaid 5-pillar comparative radar for 2–4 comparable players."""
    if selected_df.empty:
        return go.Figure()
    cmap = color_map or build_player_color_map(selected_df["player_name"].tolist())
    fig = go.Figure()
    for idx, (_, row) in enumerate(selected_df.iterrows()):
        pillars = compute_player_five_pillars(row)
        cats = list(pillars.keys())
        vals = list(pillars.values())
        pname = str(row["player_name"])
        col = cmap.get(pname, PLOTLY_SERIES[idx % len(PLOTLY_SERIES)])
        fig.add_trace(
            go.Scatterpolar(
                r=vals + [vals[0]],
                theta=cats + [cats[0]],
                fill="toself",
                opacity=0.45,
                name=pname,
                line=dict(color=col, width=2.2),
            )
        )
    fig = _apply_base_layout(fig, "Comparable Five-Pillar Profile Overlay (0–100 Scaled)", height=430)
    fig.update_layout(
        polar=dict(
            bgcolor="#FAF6F0",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="#EAE1D5", tickfont=dict(color="#77675D", size=9.5)),
            angularaxis=dict(gridcolor="#EAE1D5", tickfont=dict(color="#282321", size=10.5, family="Inter, sans-serif")),
        ),
        legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5),
    )
    return fig


def fig_multi_player_ci_bars(selected_df: pd.DataFrame, color_map: Optional[Dict[str, str]] = None) -> go.Figure:
    """Compare Reliability Score and 95% Bootstrap CIs across selected players."""
    if selected_df.empty:
        return go.Figure()
    cmap = color_map or build_player_color_map(selected_df["player_name"].tolist())
    sub = selected_df.sort_values("reliability_score", ascending=False).copy()
    scores = pd.to_numeric(sub["reliability_score"], errors="coerce").fillna(0.0)
    lo = pd.to_numeric(sub["ci_lower_95"], errors="coerce").fillna(scores)
    hi = pd.to_numeric(sub["ci_upper_95"], errors="coerce").fillna(scores)
    bar_colors = [cmap.get(str(n), PLOTLY_SERIES[i % len(PLOTLY_SERIES)]) for i, n in enumerate(sub["player_name"])]
    fig = go.Figure(
        go.Bar(
            x=sub["player_name"],
            y=scores,
            error_y=dict(type="data", symmetric=False, array=(hi - scores).clip(lower=0), arrayminus=(scores - lo).clip(lower=0), color="#77675D", thickness=1.5),
            marker_color=bar_colors,
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=sub["player_name"],
            y=hi + 3.0,
            mode="text",
            text=scores.apply(lambda v: f"{v:.2f}"),
            textfont=dict(color="#282321", size=10.5, family="JetBrains Mono, monospace"),
            showlegend=False,
            hoverinfo="skip",
        )
    )
    fig = _apply_base_layout(fig, "Reliability Score & 95% Match-Clustered Bootstrap CI", height=390)
    fig.update_yaxes(range=[0, 110], title="Reliability Score (0–100)")
    return fig


def fig_multi_player_prc_overlay(
    deliv_map: Dict[str, pd.DataFrame],
    is_batting: bool = True,
    color_map: Optional[Dict[str, str]] = None,
) -> go.Figure:
    """Overlay tier-wise Mean Raw PAVA curves for comparable players."""
    if not deliv_map:
        return go.Figure()
    cmap = color_map or build_player_color_map(deliv_map.keys())
    ball_col = "is_batter_ball" if is_batting else "is_legal_ball"
    p_col = "bpi" if is_batting else "bopi"
    raw_col = "raw_bat_value" if is_batting else "raw_bowl_value"
    labels = ["Low (<35)", "Medium [35–65)", "High [65–85)", "Extreme (>=85)"]
    dash_styles = ["solid", "dash", "dot", "dashdot"]
    symbols = ["circle", "diamond", "square", "triangle-up"]

    fig = go.Figure()
    for idx, (pname, pdf) in enumerate(deliv_map.items()):
        if pdf.empty:
            continue
        sub = pdf[pdf[ball_col] == 1].dropna(subset=[p_col, raw_col]).copy()
        if sub.empty:
            continue
        sub["tier"] = pd.cut(sub[p_col], bins=[0, 35, 65, 85, 100.1], labels=labels, right=False)
        agg = sub.groupby("tier", observed=False).agg(mean_raw=(raw_col, "mean"), n=(raw_col, "count")).reset_index()
        col = cmap.get(str(pname), PLOTLY_SERIES[idx % len(PLOTLY_SERIES)])
        fig.add_trace(
            go.Scatter(
                x=agg["tier"].astype(str),
                y=agg["mean_raw"],
                mode="lines+markers",
                name=pname,
                customdata=agg["n"],
                line=dict(color=col, width=2.4, dash=dash_styles[idx % len(dash_styles)]),
                marker=dict(size=8, symbol=symbols[idx % len(symbols)]),
                hovertemplate=f"<b>{pname}</b><br>%{{x}}: %{{y:+.3f}} PAVA/ball (n=%{{customdata}})<extra></extra>",
            )
        )
    fig = _apply_base_layout(fig, "Pressure-Response Trajectory Overlay by Leverage Band", height=390)
    fig.add_hline(y=0.0, line_dash="dot", line_color="#D8CBBE")
    fig.update_yaxes(title="Mean Raw PAVA (Runs / Ball)")
    fig.update_xaxes(title="Pressure Index Band")
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.24, xanchor="center", x=0.5))
    return fig


def fig_bpi_bopi_distribution(hist_df: pd.DataFrame) -> go.Figure:
    """Plot 10-point BPI & BoPI delivery frequency distributions across 200,961 deliveries."""
    if hist_df.empty:
        return go.Figure()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=hist_df["bin_label"], y=hist_df["bat_deliveries"], name="Batting Deliveries (BPI)", marker_color=RR_BLUE))
    fig.add_trace(go.Bar(x=hist_df["bin_label"], y=hist_df["bowl_deliveries"], name="Legal Bowling Deliveries (BoPI)", marker_color=RR_PINK))
    fig = _apply_base_layout(fig, "League-Wide BPI vs BoPI Delivery Distribution (200,961 Balls)", height=405)
    fig.update_layout(barmode="group", margin=dict(l=52, r=24, t=54, b=82), legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5))
    fig.update_xaxes(title="Continuous Pressure Index Bin [0–100]")
    fig.update_yaxes(title="Deliveries Count")
    return fig


def fig_expected_vs_observed_tiers(tiers_df: pd.DataFrame) -> go.Figure:
    """Show league-wide Expected vs Observed batter runs/ball across BPI tiers."""
    if tiers_df.empty:
        return go.Figure()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=tiers_df["pressure_tier"], y=tiers_df["exp_bat_runs"], name="Expected Runs / Ball (LightGBM)", marker_color="#D8CBBE"))
    fig.add_trace(go.Bar(x=tiers_df["pressure_tier"], y=tiers_df["obs_bat_runs"], name="Observed Runs / Ball", marker_color=EMERALD))
    fig = _apply_base_layout(fig, "Expected vs Observed Batting Scoring Rate by BPI Pressure Tier", height=380)
    fig.update_layout(barmode="group", legend=dict(orientation="h", yanchor="bottom", y=-0.24, xanchor="center", x=0.5))
    fig.update_yaxes(title="Runs / Ball")
    return fig


def fig_shrinkage_curve(k_shrink: float = 45.0) -> go.Figure:
    """Plot Empirical Bayes shrinkage weight progression against HP delivery exposure."""
    curve_df = compute_eb_shrinkage_curve(k_shrink=k_shrink)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=curve_df["hp_balls"],
            y=curve_df["shrinkage_weight"] * 100.0,
            mode="lines+markers",
            name="Empirical Data Weight w = n / (n + 45)",
            line=dict(color=RR_BLUE, width=2.4),
            marker=dict(size=6),
        )
    )
    fig = _apply_base_layout(fig, f"Empirical Bayes Shrinkage Weight Curve (K = {int(k_shrink)} Pseudo-Deliveries)", height=360)
    fig.add_vline(x=k_shrink, line_dash="dash", line_color=AMBER, annotation_text="50% Weight at n = 45 HP", annotation_font=dict(color="#282321"))
    fig.update_xaxes(title="High-Pressure Deliveries (n_HP)")
    fig.update_yaxes(title="Empirical Weight Retained (%)", range=[0, 102])
    return fig


def fig_emerging_opportunity_matrix(em_df: pd.DataFrame) -> go.Figure:
    """Visualize total dataset exposure vs HP opportunities across the Emerging Talent Watchlist."""
    if em_df.empty:
        return go.Figure()
    work = em_df.copy()
    work["total_balls_dataset"] = pd.to_numeric(work["total_balls_dataset"], errors="coerce").fillna(0)
    work["hp_balls_dataset"] = pd.to_numeric(work["hp_balls_dataset"], errors="coerce").fillna(0)
    work["short_tier"] = work["category"].astype(str).apply(lambda s: s.split(":")[0])
    fig = px.scatter(
        work,
        x="total_balls_dataset",
        y="hp_balls_dataset",
        color="short_tier",
        text="player_name",
        hover_data=["age", "role", "franchise", "pressure_reliability_score"],
        color_discrete_map={"Tier A": EMERALD, "Tier B": RR_BLUE, "Tier C": AMBER},
        labels={"total_balls_dataset": "Total Dataset Balls", "hp_balls_dataset": "High-Pressure Balls (P >= 50)", "short_tier": "Evaluation Tier"},
    )
    fig.update_traces(textposition="top center", marker=dict(size=11, line=dict(color="#282321", width=1)), textfont=dict(color="#282321", size=10))
    fig = _apply_base_layout(fig, "Emerging Talent: Total Opportunity vs High-Pressure Eligibility Cutoffs", height=420)
    fig.add_hline(y=30, line_dash="dash", line_color=CRIMSON, annotation_text="Min 30 HP Cutoff", annotation_font=dict(color="#6D1F13"))
    fig.add_vline(x=400, line_dash="dash", line_color=AMBER, annotation_text="Min 400 Total Balls Cutoff", annotation_font=dict(color="#75460E"))
    return fig


def fig_market_team_matrix(teams_df: pd.DataFrame) -> go.Figure:
    """Visualize all 10 IPL franchises by 2026 Dataset Roster & Pending/Confirmed 2027 Market Status."""
    if teams_df.empty:
        return go.Figure()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=teams_df["Code"], y=teams_df["IPL 2026 Dataset Roster"], name="IPL 2026 Dataset Roster", marker_color=RR_BLUE))
    fig.add_trace(go.Bar(x=teams_df["Code"], y=teams_df["Pending Verification"], name="Pending 2027 Verification", marker_color=RR_PINK))
    fig.add_trace(go.Bar(x=teams_df["Code"], y=teams_df["Confirmed Trades In"], name="Confirmed Trades In", marker_color=EMERALD))
    fig = _apply_base_layout(fig, "All 10 IPL Franchises — 2026 Roster Depth vs Audited 2027 Status", height=370)
    fig.update_layout(barmode="group", legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5))
    fig.update_yaxes(title="Players Count")
    return fig
