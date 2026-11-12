"""Dark telemetry Plotly visualization builders for PRESSUREIQ v3."""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.dashboard.analytics import compute_eb_shrinkage_curve, compute_player_five_pillars
from src.dashboard.design_tokens import PALETTE, PLOTLY_SERIES

# Preserved exported constants for backwards compatibility with unit tests
RR_BLUE = PALETTE["accent_blue"]
RR_PINK = PALETTE["accent_violet"]
INK_DARK = PALETTE["text_primary"]
SLATE_MUTED = PALETTE["text_muted"]
EMERALD = PALETTE["positive"]
AMBER = PALETTE["warning"]
CRIMSON = PALETTE["danger"]
CYAN = PALETTE["accent_cyan"]

ARCHETYPE_COLORS = {
    "Clutch Climber": EMERALD,
    "Ice Cold Anchor": RR_BLUE,
    "Gradual Decliner": AMBER,
    "Pressure Fragile": CRIMSON,
    "Unclassified (Insufficient Evidence)": SLATE_MUTED,
}


def _apply_base_layout(fig: go.Figure, title: str, height: int = 400) -> go.Figure:
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color=PALETTE["text_primary"], family="Plus Jakarta Sans, Inter, sans-serif"), x=0.01),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=PALETTE["bg_surface"],
        height=height,
        margin=dict(l=52, r=24, t=54, b=48),
        font=dict(family="Plus Jakarta Sans, Inter, Segoe UI, sans-serif", size=12, color=PALETTE["text_secondary"]),
        hoverlabel=dict(
            bgcolor="#0B1120",
            bordercolor="#475569",
            font=dict(size=12, color="#F8FAFC", family="JetBrains Mono, monospace"),
        ),
        legend=dict(font=dict(color=PALETTE["text_secondary"], size=11), bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(
        gridcolor=PALETTE["plot_grid"],
        zerolinecolor="rgba(148, 163, 184, 0.24)",
        tickfont=dict(color=PALETTE["text_secondary"], size=11),
        title_font=dict(color=PALETTE["text_secondary"], size=12),
    )
    fig.update_yaxes(
        gridcolor=PALETTE["plot_grid"],
        zerolinecolor="rgba(148, 163, 184, 0.24)",
        tickfont=dict(color=PALETTE["text_secondary"], size=11),
        title_font=dict(color=PALETTE["text_secondary"], size=12),
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
                color="#E2E8F0",
                thickness=1.4,
                width=4,
            ),
            marker=dict(color=accent_color, line=dict(color="rgba(248,250,252,0.18)", width=1)),
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
            textfont=dict(size=10, color="#E2E8F0", family="JetBrains Mono, monospace"),
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
        opacity=0.88,
        labels={"reliability_score": "Reliability Score (0–100)", "prc_archetype": "PRC Class"},
    )
    med_val = float(work["reliability_score"].median())
    fig = _apply_base_layout(fig, title, height=390)
    if np.isfinite(med_val):
        fig.add_vline(
            x=med_val,
            line_dash="dash",
            line_color="#E2E8F0",
            annotation_text=f"Median: {med_val:.1f}",
            annotation_position="top left",
            annotation_font=dict(color="#F8FAFC", size=11),
        )
    fig.update_yaxes(title="Players Count")
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="center", x=0.5))
    return fig


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
                line=dict(color="rgba(148, 163, 184, 0.36)", width=6),
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
            marker=dict(color=RR_BLUE, size=10, symbol="diamond", line=dict(color="#F8FAFC", width=1)),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=med_vals,
            y=sub["player_name"],
            mode="markers",
            name="Bootstrap Median Rank (N=2,000)",
            marker=dict(color=RR_PINK, size=9, symbol="circle", line=dict(color="#F8FAFC", width=1)),
        )
    )
    max_x = max(15, int(ci_hi.max()) + 8) if np.isfinite(ci_hi.max()) else 155
    fig = _apply_base_layout(fig, title, height=max(420, top_n * 28))
    fig.update_xaxes(title="Rank Position (Lower is Better; Bar = 95% Bootstrap Interval)", autorange=False, range=[0, min(155, max_x)])
    fig.update_yaxes(title="")
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5))
    return fig


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

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=tier_df["tier"].astype(str),
            y=y_vals,
            marker_color=[SLATE_MUTED, RR_BLUE, RR_PINK, EMERALD],
            text=bar_text,
            textposition="outside",
            textfont=dict(color="#E2E8F0", size=11, family="JetBrains Mono, monospace"),
            name="Tier Mean Raw PAVA/ball",
        )
    )
    index_name = "BPI" if is_batting else "BoPI"
    fig = _apply_base_layout(fig, f"Pressure Response Profile — {player_name}", height=405)
    fig.add_hline(y=0.0, line_dash="dash", line_color="rgba(148,163,184,0.45)")
    max_y = max(y_vals) if y_vals else 0.1
    min_y = min(y_vals) if y_vals else 0.0
    fig.update_yaxes(title="Mean Raw PAVA (Runs / Ball)", range=[min(0.0, min_y) - 0.06, max(0.15, max_y * 1.22)])
    fig.update_xaxes(title=f"{index_name} Pressure Tier")
    fig.update_layout(margin=dict(l=64, r=28, t=60, b=52))
    return fig


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
            textfont=dict(color="#E2E8F0", size=11, family="JetBrains Mono, monospace"),
        )
    )
    fig = _apply_base_layout(fig, f"Phase-Wise Value Added — {player_name}", height=370)
    fig.add_hline(y=0.0, line_dash="dash", line_color="rgba(148,163,184,0.45)")
    fig.update_yaxes(title="Mean Raw PAVA (Runs/Ball)")
    fig.update_xaxes(title="Innings Phase")
    return fig


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
            fillcolor="rgba(59, 130, 246, 0.25)",
            name=player_name,
            line=dict(color=RR_BLUE, width=2.5),
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=peer_vals + [peer_vals[0]],
            theta=cats + [cats[0]],
            fill="toself",
            fillcolor="rgba(139, 92, 246, 0.16)",
            name=f"{role_label} Peer Mean",
            line=dict(color=RR_PINK, width=2, dash="dash"),
        )
    )
    res = _apply_base_layout(fig, f"Five-Pillar Decomposition vs {role_label} Peers", height=415)
    res.update_layout(
        polar=dict(
            bgcolor=PALETTE["bg_surface"],
            radialaxis=dict(visible=True, range=[0, 100], gridcolor=PALETTE["plot_grid"], tickfont=dict(color=SLATE_MUTED, size=10)),
            angularaxis=dict(gridcolor=PALETTE["plot_grid"], tickfont=dict(color="#E2E8F0", size=11)),
        ),
        margin=dict(l=95, r=95, t=68, b=56),
        legend=dict(orientation="h", yanchor="bottom", y=-0.20, xanchor="center", x=0.5),
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
    fig.update_traces(texttemplate="Avg %{text:.1f}", textposition="outside", textfont=dict(color="#E2E8F0", size=11))
    return _apply_base_layout(fig, "Rajasthan Royals 2026 Qualified Core Depth by Role (Model A Baseline)", height=390)


def fig_player_expected_vs_observed(player_delivs: pd.DataFrame, player_name: str, is_batting: bool = True) -> go.Figure:
    """Compare LightGBM pre-ball expected runs vs actual runs across pressure tiers for a player."""
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
    fig.add_trace(go.Bar(x=agg["tier"].astype(str), y=agg["exp"], name="Expected Runs / Ball (LightGBM)", marker_color="rgba(148,163,184,0.45)"))
    fig.add_trace(go.Bar(x=agg["tier"].astype(str), y=agg["obs"], name="Observed Runs / Ball", marker_color=EMERALD if is_batting else RR_PINK))
    fig = _apply_base_layout(fig, f"Expected vs Observed Runs / Ball — {player_name}", height=370)
    fig.update_layout(barmode="group", legend=dict(orientation="h", yanchor="bottom", y=-0.24, xanchor="center", x=0.5))
    fig.update_yaxes(title="Runs / Ball")
    return fig


def fig_multi_player_radar(selected_df: pd.DataFrame) -> go.Figure:
    """Overlaid 5-pillar comparative radar for 2–4 comparable players within the same discipline."""
    if selected_df.empty:
        return go.Figure()
    fig = go.Figure()
    for idx, (_, row) in enumerate(selected_df.iterrows()):
        pillars = compute_player_five_pillars(row)
        cats = list(pillars.keys())
        vals = list(pillars.values())
        col = PLOTLY_SERIES[idx % len(PLOTLY_SERIES)]
        fig.add_trace(
            go.Scatterpolar(
                r=vals + [vals[0]],
                theta=cats + [cats[0]],
                fill="toself",
                opacity=0.65,
                name=str(row["player_name"]),
                line=dict(color=col, width=2.4),
            )
        )
    fig = _apply_base_layout(fig, "Comparable Five-Pillar Profile Overlay (0–100 Scaled)", height=430)
    fig.update_layout(
        polar=dict(
            bgcolor=PALETTE["bg_surface"],
            radialaxis=dict(visible=True, range=[0, 100], gridcolor=PALETTE["plot_grid"], tickfont=dict(color=SLATE_MUTED, size=10)),
            angularaxis=dict(gridcolor=PALETTE["plot_grid"], tickfont=dict(color="#E2E8F0", size=11)),
        ),
        legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5),
    )
    return fig


def fig_multi_player_ci_bars(selected_df: pd.DataFrame) -> go.Figure:
    """Compare Reliability Score and 95% Bootstrap CIs across 2–4 selected players."""
    if selected_df.empty:
        return go.Figure()
    sub = selected_df.sort_values("reliability_score", ascending=False).copy()
    scores = pd.to_numeric(sub["reliability_score"], errors="coerce").fillna(0.0)
    lo = pd.to_numeric(sub["ci_lower_95"], errors="coerce").fillna(scores)
    hi = pd.to_numeric(sub["ci_upper_95"], errors="coerce").fillna(scores)
    fig = go.Figure(
        go.Bar(
            x=sub["player_name"],
            y=scores,
            error_y=dict(type="data", symmetric=False, array=(hi - scores).clip(lower=0), arrayminus=(scores - lo).clip(lower=0), color="#F8FAFC", thickness=1.5),
            marker_color=PLOTLY_SERIES[: len(sub)],
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=sub["player_name"],
            y=hi + 3.0,
            mode="text",
            text=scores.apply(lambda v: f"{v:.2f}"),
            textfont=dict(color="#F8FAFC", size=11, family="JetBrains Mono, monospace"),
            showlegend=False,
            hoverinfo="skip",
        )
    )
    fig = _apply_base_layout(fig, "Reliability Score & 95% Match-Clustered Bootstrap CI", height=390)
    fig.update_yaxes(range=[0, 110], title="Reliability Score (0–100)")
    return fig


def fig_multi_player_prc_overlay(deliv_map: Dict[str, pd.DataFrame], is_batting: bool = True) -> go.Figure:
    """Overlay tier-wise Mean Raw PAVA curves for 2–4 selected players."""
    if not deliv_map:
        return go.Figure()
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
        fig.add_trace(
            go.Scatter(
                x=agg["tier"].astype(str),
                y=agg["mean_raw"],
                mode="lines+markers",
                name=pname,
                customdata=agg["n"],
                line=dict(color=PLOTLY_SERIES[idx % len(PLOTLY_SERIES)], width=2.5, dash=dash_styles[idx % len(dash_styles)]),
                marker=dict(size=8, symbol=symbols[idx % len(symbols)]),
                hovertemplate=f"<b>{pname}</b><br>%{{x}}: %{{y:+.3f}} PAVA/ball (n=%{{customdata}})<extra></extra>",
            )
        )
    fig = _apply_base_layout(fig, "Pressure-Response Trajectory Overlay by Leverage Band", height=390)
    fig.add_hline(y=0.0, line_dash="dot", line_color="rgba(148,163,184,0.4)")
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
    fig.add_trace(go.Bar(x=tiers_df["pressure_tier"], y=tiers_df["exp_bat_runs"], name="Expected Runs / Ball (LightGBM)", marker_color="rgba(148,163,184,0.45)"))
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
            line=dict(color=CYAN, width=2.5),
            marker=dict(size=7),
        )
    )
    fig = _apply_base_layout(fig, f"Empirical Bayes Shrinkage Weight Curve (K = {int(k_shrink)} Pseudo-Deliveries)", height=360)
    fig.add_vline(x=k_shrink, line_dash="dash", line_color=AMBER, annotation_text="50% Weight at n = 45 HP", annotation_font=dict(color="#FDE68A"))
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
    fig.update_traces(textposition="top center", marker=dict(size=12, line=dict(color="#F8FAFC", width=1)), textfont=dict(color="#E2E8F0", size=10))
    fig = _apply_base_layout(fig, "Emerging Talent: Total Opportunity vs High-Pressure Eligibility Cutoffs", height=420)
    fig.add_hline(y=30, line_dash="dash", line_color=CRIMSON, annotation_text="Min 30 HP Cutoff", annotation_font=dict(color="#FDA4AF"))
    fig.add_vline(x=400, line_dash="dash", line_color=AMBER, annotation_text="Min 400 Total Balls Cutoff", annotation_font=dict(color="#FDE68A"))
    return fig


def fig_market_team_matrix(teams_df: pd.DataFrame) -> go.Figure:
    """Visualize all 10 IPL franchises by 2026 Dataset Roster & Pending/Confirmed 2027 Market Status."""
    if teams_df.empty:
        return go.Figure()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=teams_df["Code"], y=teams_df["IPL 2026 Dataset Roster"], name="IPL 2026 Dataset Roster", marker_color=RR_BLUE))
    fig.add_trace(go.Bar(x=teams_df["Code"], y=teams_df["Pending Verification"], name="Pending 2027 Verification", marker_color=AMBER))
    fig.add_trace(go.Bar(x=teams_df["Code"], y=teams_df["Confirmed Trades In"], name="Confirmed Trades In", marker_color=RR_PINK))
    fig = _apply_base_layout(fig, "All 10 IPL Franchises — 2026 Roster Depth vs Audited 2027 Status", height=370)
    fig.update_layout(barmode="group", legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5))
    fig.update_yaxes(title="Players Count")
    return fig
