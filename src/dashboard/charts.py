"""Plotly visualization builders for PRESSUREIQ — Cricket Pressure Intelligence."""

from __future__ import annotations

from typing import Dict

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.dashboard.analytics import compute_player_five_pillars

RR_BLUE = "#004BA0"
RR_PINK = "#EA1B88"
INK_DARK = "#0F172A"
SLATE_MUTED = "#64748B"
EMERALD = "#059669"
AMBER = "#D97706"
CRIMSON = "#DC2626"

ARCHETYPE_COLORS = {
    "Clutch Climber": EMERALD,
    "Ice Cold Anchor": RR_BLUE,
    "Gradual Decliner": AMBER,
    "Pressure Fragile": CRIMSON,
    "Unclassified (Insufficient Evidence)": SLATE_MUTED,
}


def _apply_base_layout(fig: go.Figure, title: str, height: int = 400) -> go.Figure:
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color=INK_DARK)),
        template="plotly_white",
        height=height,
        margin=dict(l=48, r=24, t=52, b=48),
        font=dict(family="Inter, Segoe UI, sans-serif", size=12, color=INK_DARK),
        hoverlabel=dict(bgcolor="white", font_size=12),
    )
    return fig


def fig_top10_ci_bar(df: pd.DataFrame, title: str, accent_color: str = RR_BLUE) -> go.Figure:
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
                color=INK_DARK,
                thickness=1.4,
            ),
            marker_color=accent_color,
            customdata=np.stack([top10["rank"], hp_vals, top10_p, arch], axis=-1),
            name="Score & 95% CI",
            showlegend=False,
            hovertemplate=(
                "<b>%{x}</b> (Rank #%{customdata[0]})<br>"
                "Reliability Score: %{y:.2f}<br>"
                "HP Opportunities: %{customdata[1]}<br>"
                "Bootstrap Top-10 Prob: %{customdata[2]:.1f}%<br>"
                "PRC Archetype: %{customdata[3]}<extra></extra>"
            ),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=top10["player_name"],
            y=ci_hi + 2.5,
            mode="text",
            text=scores.round(1).astype(str),
            textfont=dict(size=10, color=INK_DARK),
            showlegend=False,
            hoverinfo="skip",
        )
    )
    min_y = max(0.0, float(ci_lo.min()) - 8.0) if not ci_lo.empty else 0.0
    fig.update_yaxes(range=[min_y, 108.0], title="Reliability Score (0–100)")
    fig.update_xaxes(title="", tickangle=-20)
    return _apply_base_layout(fig, title, height=410)


def fig_score_distribution(df: pd.DataFrame, title: str, accent_color: str = RR_BLUE) -> go.Figure:
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
        labels={"reliability_score": "Reliability Score (0–100)", "prc_archetype": "PRC Archetype"},
    )
    med_val = float(work["reliability_score"].median())
    if np.isfinite(med_val):
        fig.add_vline(
            x=med_val,
            line_dash="dash",
            line_color=INK_DARK,
            annotation_text=f"Median: {med_val:.1f}",
            annotation_position="top left",
        )
    fig.update_yaxes(title="Players Count")
    return _apply_base_layout(fig, title, height=390)


def fig_sample_vs_score(df: pd.DataFrame, is_batting: bool = True) -> go.Figure:
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
            "prc_archetype": "PRC Archetype",
        },
    )
    fig.add_vline(x=45, line_dash="dot", line_color=SLATE_MUTED, annotation_text="K_shrink = 45 HP balls")
    return _apply_base_layout(fig, f"Sample Size vs Reliability Score — {label}", height=430)


def fig_rank_uncertainty_intervals(df: pd.DataFrame, top_n: int = 15, title: str = "Bootstrap Rank Uncertainty") -> go.Figure:
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
                line=dict(color="#CBD5E1", width=6),
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
            marker=dict(color=RR_BLUE, size=10, symbol="diamond"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=med_vals,
            y=sub["player_name"],
            mode="markers",
            name="Bootstrap Median Rank (N=2,000)",
            marker=dict(color=RR_PINK, size=9, symbol="circle"),
        )
    )
    max_x = max(15, int(ci_hi.max()) + 8) if np.isfinite(ci_hi.max()) else 155
    fig.update_xaxes(title="Rank Position (Lower is Better; Range Shows 95% Rank Interval)", autorange=False, range=[0, min(155, max_x)])
    fig.update_yaxes(title="")
    return _apply_base_layout(fig, title, height=max(420, top_n * 28))


def fig_pressure_response_curve(player_delivs: pd.DataFrame, player_name: str, is_batting: bool = True) -> go.Figure:
    if player_delivs.empty:
        return go.Figure()
    ball_col = "is_batter_ball" if is_batting else "is_legal_ball"
    p_col = "bpi" if is_batting else "bopi"
    raw_col = "raw_bat_value" if is_batting else "raw_bowl_value"
    sub = player_delivs[player_delivs[ball_col] == 1].dropna(subset=[p_col, raw_col]).copy()
    if sub.empty:
        return go.Figure()

    bins = [0, 35, 65, 85, 100.1]
    labels = ["Low (<35)", "Medium [35-65)", "High [65-85)", "Extreme (>=85)"]
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

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=tier_df["tier"].astype(str),
            y=y_vals,
            marker_color=[SLATE_MUTED, RR_BLUE, RR_PINK, CRIMSON],
            text=bar_text,
            textposition="outside",
            name="Tier Mean Raw PAVA/ball",
        )
    )
    fig.add_hline(y=0.0, line_dash="dash", line_color=INK_DARK)
    index_name = "BPI" if is_batting else "BoPI"
    fig.update_yaxes(title="Raw PAVA (Runs / Ball)")
    fig.update_xaxes(title=f"{index_name} Pressure Tier")
    res = _apply_base_layout(fig, f"Pressure Response Profile — {player_name}", height=400)
    res.update_layout(margin=dict(l=64, r=28, t=64, b=48))
    return res


def fig_phase_performance(phase_df: pd.DataFrame, player_name: str, is_batting: bool = True) -> go.Figure:
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
        )
    )
    fig.add_hline(y=0.0, line_dash="dash", line_color=SLATE_MUTED)
    fig.update_yaxes(title="Mean Raw PAVA (Runs/Ball)")
    fig.update_xaxes(title="Innings Phase")
    return _apply_base_layout(fig, f"Phase-Wise Value Added — {player_name}", height=360)


def fig_five_pillar_radar(player_row: pd.Series, peer_means: Dict[str, float], player_name: str, role_label: str) -> go.Figure:
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
            name=player_name,
            line_color=RR_BLUE,
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=peer_vals + [peer_vals[0]],
            theta=cats + [cats[0]],
            fill="toself",
            name=f"{role_label} Peer Mean",
            line_color=RR_PINK,
            opacity=0.55,
        )
    )
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
    res = _apply_base_layout(fig, f"Five-Pillar Decomposition vs {role_label} Peers", height=410)
    res.update_layout(
        margin=dict(l=95, r=95, t=68, b=52),
        legend=dict(orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5),
    )
    return res


def fig_batter_vs_bowler_comparison(bat_df: pd.DataFrame, bowl_df: pd.DataFrame) -> go.Figure:
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
    fig.update_traces(texttemplate="Avg %{text:.1f}", textposition="outside")
    return _apply_base_layout(fig, "Rajasthan Royals 2026 Qualified Core Depth by Role (Model A Baseline)", height=380)
