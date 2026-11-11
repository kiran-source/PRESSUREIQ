"""PRESSUREIQ — Streamlit & Plotly Analytical Dashboard.

Context-Aware Cricket Performance and Reliability Intelligence Framework.
"""

import json
from pathlib import Path
import duckdb
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Paths
ROOT = Path(__file__).resolve().parent.parent.parent
PROCESSED_DATA_DIR = ROOT / "data" / "processed"
DOCS_DIR = ROOT / "docs"

BATTER_RANKINGS_PATH = PROCESSED_DATA_DIR / "final_batter_rankings.parquet"
BOWLER_RANKINGS_PATH = PROCESSED_DATA_DIR / "final_bowler_rankings.parquet"
DELIVERIES_PAVA_PATH = PROCESSED_DATA_DIR / "deliveries_with_pava.parquet"
BENCHMARK_PATH = DOCS_DIR / "MODEL_BENCHMARK_REPORT.json"
VALIDATION_PATH = DOCS_DIR / "VALIDATION_REPORT.json"
PROVENANCE_PATH = DOCS_DIR / "PROVENANCE.json"

st.set_page_config(
    page_title="PRESSUREIQ | Cricket Reliability Intelligence",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 16px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 12px;
    }
    .badge-climber {
        background-color: #28a745;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    bat_df = pd.read_parquet(BATTER_RANKINGS_PATH)
    bowl_df = pd.read_parquet(BOWLER_RANKINGS_PATH)
    
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        benchmark = json.load(f)
    with open(VALIDATION_PATH, "r", encoding="utf-8") as f:
        validation = json.load(f)
    with open(PROVENANCE_PATH, "r", encoding="utf-8") as f:
        provenance = json.load(f)
        
    return bat_df, bowl_df, benchmark, validation, provenance


bat_df, bowl_df, benchmark, validation, provenance = load_data()

# Sidebar Navigation
st.sidebar.title("🏏 PRESSUREIQ")
st.sidebar.markdown("**Context-Aware Reliability Intelligence**")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏆 Top 10 Leaderboards",
        "📈 Pressure Response Curves (PRC)",
        "🎴 Player Decision Cards",
        "🔬 Five-Pillar Methodology",
        "🧪 Validation & Ablation Studies",
        "📁 Data Inventory & Provenance"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("IPL & T20I (2022–2026) | 200,999 Deliveries | 867 Matches")

# ==========================================
# PAGE 1: LEADERBOARDS
# ==========================================
if page == "🏆 Top 10 Leaderboards":
    st.title("🏆 Most Reliable Players Under Pressure (2022–2026)")
    st.markdown(
        "Ranked using the **Five-Pillar Reliability Score (0–100)** incorporating "
        "Pressure-Adjusted Value Added (PAVA), Baseline Retention Delta, Match Consistency, "
        "and Empirical Bayes Shrinkage with **2,000 match-clustered bootstrap confidence intervals**."
    )
    
    tab_bat, tab_bowl = st.tabs(["🏏 Top 10 Batters", "🎯 Top 10 Bowlers"])
    
    with tab_bat:
        st.subheader("Official Top 10 Most Reliable Batters")
        top10_bat = bat_df.head(10).copy()
        
        display_bat = top10_bat[[
            "rank", "player_name", "role", "reliability_score", "ci_lower_95", "ci_upper_95",
            "top10_inclusion_prob", "hp_balls", "shrunk_hp_pava_per_ball", "retention_delta", "prc_archetype"
        ]].rename(columns={
            "rank": "Rank", "player_name": "Player", "role": "Role",
            "reliability_score": "Reliability Score", "ci_lower_95": "95% CI Lower",
            "ci_upper_95": "95% CI Upper", "top10_inclusion_prob": "Top-10 Prob",
            "hp_balls": "HP Balls", "shrunk_hp_pava_per_ball": "Shrunk PAVA/Ball",
            "retention_delta": "Retention Delta", "prc_archetype": "PRC Archetype"
        })
        st.dataframe(display_bat, use_container_width=True, hide_index=True)
        
        fig_bat = go.Figure()
        fig_bat.add_trace(go.Bar(
            x=top10_bat["player_name"],
            y=top10_bat["reliability_score"],
            error_y=dict(
                type="data",
                symmetric=False,
                array=top10_bat["ci_upper_95"] - top10_bat["reliability_score"],
                arrayminus=top10_bat["reliability_score"] - top10_bat["ci_lower_95"]
            ),
            marker_color="#1f77b4",
            text=top10_bat["reliability_score"].astype(str),
            textposition="auto"
        ))
        fig_bat.update_layout(
            title="Top 10 Batters Reliability Score with 95% Match-Clustered Bootstrap CIs",
            xaxis_title="Batter",
            yaxis_title="Reliability Score (0-100)",
            yaxis=dict(range=[50, 102]),
            height=450
        )
        st.plotly_chart(fig_bat, use_container_width=True)
        
    with tab_bowl:
        st.subheader("Official Top 10 Most Reliable Bowlers")
        top10_bowl = bowl_df.head(10).copy()
        
        display_bowl = top10_bowl[[
            "rank", "player_name", "pace_or_spin", "bowling_type", "reliability_score",
            "ci_lower_95", "ci_upper_95", "top10_inclusion_prob", "hp_balls", "career_economy",
            "shrunk_hp_pava_per_ball", "retention_delta", "prc_archetype"
        ]].rename(columns={
            "rank": "Rank", "player_name": "Player", "pace_or_spin": "Type",
            "bowling_type": "Style", "reliability_score": "Reliability Score",
            "ci_lower_95": "95% CI Lower", "ci_upper_95": "95% CI Upper",
            "top10_inclusion_prob": "Top-10 Prob", "hp_balls": "HP Balls",
            "career_economy": "Economy", "shrunk_hp_pava_per_ball": "Shrunk PAVA/Ball",
            "retention_delta": "Retention Delta", "prc_archetype": "PRC Archetype"
        })
        st.dataframe(display_bowl, use_container_width=True, hide_index=True)
        
        fig_bowl = go.Figure()
        fig_bowl.add_trace(go.Bar(
            x=top10_bowl["player_name"],
            y=top10_bowl["reliability_score"],
            error_y=dict(
                type="data",
                symmetric=False,
                array=top10_bowl["ci_upper_95"] - top10_bowl["reliability_score"],
                arrayminus=top10_bowl["reliability_score"] - top10_bowl["ci_lower_95"]
            ),
            marker_color="#2ca02c",
            text=top10_bowl["reliability_score"].astype(str),
            textposition="auto"
        ))
        fig_bowl.update_layout(
            title="Top 10 Bowlers Reliability Score with 95% Match-Clustered Bootstrap CIs",
            xaxis_title="Bowler",
            yaxis_title="Reliability Score (0-100)",
            yaxis=dict(range=[50, 102]),
            height=450
        )
        st.plotly_chart(fig_bowl, use_container_width=True)

# ==========================================
# PAGE 2: PRESSURE RESPONSE CURVES
# ==========================================
elif page == "📈 Pressure Response Curves (PRC)":
    st.title("📈 Pressure Response Curves (PRC)")
    st.markdown(
        "A player's Pressure Response Curve maps their performance above expectation "
        "as a function of pressure, revealing whether they elevate, anchor, or decline when stakes peak. "
        "Displays **actual observed binned performance** alongside the fitted trend (P1-7)."
    )
    
    role_choice = st.radio("Select Discipline:", ["Batters", "Bowlers"], horizontal=True)
    df_pool = bat_df[bat_df["is_eligible"]] if role_choice == "Batters" else bowl_df[bowl_df["is_eligible"]]
    
    player_choice = st.selectbox("Select Player:", df_pool["player_name"].tolist())
    p_row = df_pool[df_pool["player_name"] == player_choice].iloc[0]
    pid = p_row["player_id"]
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Reliability Score", f"{p_row['reliability_score']:.1f}")
    col2.metric("PRC Archetype", p_row["prc_archetype"])
    col3.metric("PRC Slope (β)", f"{p_row['prc_slope']:+.3f}")
    col4.metric("Retention Delta", f"{p_row['retention_delta']:+.3f}")
    col5.metric("Top-10 Prob (Bootstrap)", f"{p_row.get('top10_inclusion_prob', 0.0)*100:.1f}%")
    
    # Query actual deliveries for selected player via duckdb for instant response
    is_bat = (role_choice == "Batters")
    filter_col = "striker_id" if is_bat else "bowler_id"
    p_col = "bpi" if is_bat else "bopi"
    val_col = "raw_bat_value" if is_bat else "raw_bowl_value"
    
    conn = duckdb.connect()
    p_delivs = conn.execute(f"""
        SELECT {p_col} as pressure, {val_col} as raw_val
        FROM parquet_scan('{str(DELIVERIES_PAVA_PATH).replace('\\', '/')}')
        WHERE {filter_col} = {pid} AND {'is_batter_ball' if is_bat else 'bowler_id IS NOT NULL'}
    """).df()
    conn.close()
    
    fig = go.Figure()
    
    if len(p_delivs) > 0:
        # Bin deliveries into pressure intervals
        bins = [0, 30, 45, 60, 75, 90, 100]
        labels = [15, 37.5, 52.5, 67.5, 82.5, 95]
        p_delivs["bin"] = pd.cut(p_delivs["pressure"], bins=bins, labels=labels)
        
        binned = p_delivs.groupby("bin", observed=False).agg(
            mean_val=("raw_val", "mean"),
            count=("raw_val", "count"),
            std_val=("raw_val", "std")
        ).reset_index()
        
        binned["se_val"] = binned["std_val"] / np.sqrt(np.maximum(binned["count"], 1))
        binned_valid = binned[binned["count"] >= 3].copy()
        
        # Add actual observed points with error bars (±1 SE)
        fig.add_trace(go.Scatter(
            x=binned_valid["bin"],
            y=binned_valid["mean_val"],
            error_y=dict(type="data", array=binned_valid["se_val"], visible=True),
            mode="markers",
            marker=dict(size=10, color="#1f77b4"),
            name="Actual Observed Bins (±1 SE)"
        ))
        
        # Fitted linear response trend line
        x_trend = np.linspace(15, 95, 30)
        y_trend = (p_row["prc_slope"] * (x_trend / 100.0)) + (binned_valid["mean_val"].mean() - p_row["prc_slope"] * (binned_valid["bin"].astype(float).mean() / 100.0))
        
        fig.add_trace(go.Scatter(
            x=x_trend,
            y=y_trend,
            mode="lines",
            line=dict(color="#d62728" if p_row["prc_slope"] > 0 else "#2ca02c", width=3),
            name=f"Fitted Trend (β={p_row['prc_slope']:+.3f})"
        ))
        
    fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="League Neutral Expectation")
    fig.update_layout(
        title=f"Observed Performance & Fitted PRC Trend for {player_choice} ({p_row['prc_archetype']})",
        xaxis_title="Pressure Index (0–100)",
        yaxis_title="Runs Added Above Expectation per Ball",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# PAGE 3: PLAYER DECISION CARDS
# ==========================================
elif page == "🎴 Player Decision Cards":
    st.title("🎴 Five-Pillar Player Decision Cards")
    st.markdown("Detailed quantitative breakdown across all 5 reliability dimensions.")
    
    role_choice = st.radio("Select Discipline:", ["Batters", "Bowlers"], horizontal=True, key="card_role")
    df_pool = bat_df.head(20) if role_choice == "Batters" else bowl_df.head(20)
    
    player_choice = st.selectbox("Select Player:", df_pool["player_name"].tolist(), key="card_player")
    p_row = df_pool[df_pool["player_name"] == player_choice].iloc[0]
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.markdown(f"### {p_row['player_name']}")
        st.markdown(f"**Rank**: #{p_row.get('rank', 'N/A')}")
        st.markdown(f"**Discipline**: {role_choice[:-1]}")
        st.markdown(f"**Archetype**: `{p_row['prc_archetype']}`")
        st.markdown(f"**Reliability Score**: **{p_row['reliability_score']:.2f} / 100**")
        st.markdown(f"**95% Score CI**: [{p_row['ci_lower_95']:.1f}, {p_row['ci_upper_95']:.1f}]")
        st.markdown(f"**Top-10 Inclusion Prob**: **{p_row.get('top10_inclusion_prob', 0.0)*100:.1f}%**")
        st.markdown(f"**95% Rank CI**: [{p_row.get('boot_rank_ci_lower_95', 'N/A')}, {p_row.get('boot_rank_ci_upper_95', 'N/A')}]")
        st.markdown(f"**High-Pressure Exposure**: {p_row['hp_balls']} legal balls")
        st.markdown(f"**Total Exposure**: {p_row['total_balls']} balls across {p_row['matches']} matches")
        
    with c2:
        categories = [
            "Pressure PAVA",
            "Baseline Retention",
            "Match Consistency",
            "Adaptability",
            "Evidence Strength"
        ]
        
        p1 = float(np.clip(p_row["shrunk_hp_pava_per_ball"] * 80.0 + 50.0, 10.0, 100.0))
        p2 = float(np.clip(p_row["retention_delta"] * 40.0 + 50.0, 10.0, 100.0))
        p3 = float(p_row["consistency_score"])
        p4 = float(p_row["adaptability_score"])
        p5 = float(p_row["evidence_weight"] * 100.0)
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=[p1, p2, p3, p4, p5, p1],
            theta=categories + [categories[0]],
            fill='toself',
            name=player_choice,
            line=dict(color="#1f77b4")
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            title="Five-Pillar Quantitative Evaluation Radar",
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# PAGE 4: METHODOLOGY
# ==========================================
elif page == "🔬 Five-Pillar Methodology":
    st.title("🔬 PRESSUREIQ Methodology Architecture")
    
    st.markdown(r"""
    ### 1. Conceptual Definition of Pressure
    Pressure is defined strictly as **contextual match difficulty**, NOT player success or failure.
    Every delivery receives a calibrated continuous **0–100 score**:
    - **Batting Pressure Index (BPI)**: Combines Scoring Demand (RRR in chase / Par Deficit in 1st inn), Resource Scarcity (wickets lost), Temporal Climax (balls remaining), and Knockout Match Stakes.
    - **Bowling Pressure Index (BoPI)**: Combines Target Defense Urgency (chasing team cruise rate / par surplus), Batting Resources in Hand, Death Overs Exposure, and Close-Finish Volatility.
    
    ### 2. Expected Performance Models (P0-2 Walk-Forward OOF)
    Historical deliveries used in PAVA are scored via **strictly chronological walk-forward out-of-fold estimation**:
    - 2022: 5-fold match-grouped out-of-fold cross-validation.
    - 2023–2026: Models trained strictly on prior years ($<= \text{year}-1$, no future leakage).
    
    ### 3. Pressure-Adjusted Value Added (PAVA)
    $$\text{PAVA}_{\text{delivery}} = (\text{Actual Runs} - E[\text{Runs}]) + \lambda_{\text{wkt}} \cdot (P(\text{Dismissal}) - \text{Dismissal}) + \lambda_{\text{bnd}} \cdot (\text{Boundary} - P(\text{Boundary}))$$
    *Note: Expected outcome models $E[\cdot]$ are already conditioned on match pressure (BPI/BoPI). PAVA measures pure above-expectation execution surplus (in runs/ball). Leverage-weighted impact ($L(P) = \text{PAVA} \times (1 + \text{Pressure}/50)$) is reported separately to prevent double-counting pressure in retention deltas.*
    
    ### 4. The Five Pillars of Reliability
    1. **Absolute Pressure Performance**: Mean PAVA in high-pressure match situations ($>= 50$ BPI/BoPI).
    2. **Baseline Retention Delta**: Performance under pressure minus performance in low pressure with Bayesian shrinkage towards career mean.
    3. **Opportunity-Adjusted Consistency**: Inverse inter-match rate variance across independent innings/spells.
    4. **Context Adaptability**: Cross-competition stability between IPL and T20 Internationals.
    5. **Empirical Bayes Shrinkage**: Calibrated shrinkage ($K=45$) based on between-player and within-player variance ratios.
    """)

# ==========================================
# PAGE 5: VALIDATION & ABLATION
# ==========================================
elif page == "🧪 Validation & Ablation Studies":
    st.title("🧪 Model Validation, Calibration & Ablation Studies")
    
    st.subheader("1. Expected Performance Model Out-of-Sample Benchmark (2025 Val & 2026 Test)")
    
    val_runs = benchmark["batting_expected_runs"]["validation_2025"]
    test_runs = benchmark["batting_expected_runs"]["untouched_test_2026"]
    
    b_df = pd.DataFrame([
        {"Target": "Batting Runs (2025 Val RMSE)", "Baseline": val_runs["Baseline"]["RMSE"], "LightGBM": val_runs["LightGBM"]["RMSE"], "XGBoost": val_runs["XGBoost"]["RMSE"], "CatBoost": val_runs["CatBoost"]["RMSE"]},
        {"Target": "Batting Runs (2026 Test RMSE)", "Baseline": test_runs["Baseline"]["RMSE"], "LightGBM": test_runs["LightGBM"]["RMSE"], "XGBoost": test_runs["XGBoost"]["RMSE"], "CatBoost": test_runs["CatBoost"]["RMSE"]},
        {"Target": "Batting Dismissal Prob (2025 Val Brier / ECE)", "Baseline": "0.0549", "LightGBM": f"{benchmark['batting_dismissal_prob']['validation_2025']['Brier_Score']} (ECE: {benchmark['batting_dismissal_prob']['validation_2025']['ECE']})", "XGBoost": "—", "CatBoost": "—"},
        {"Target": "Batting Dismissal Prob (2026 Test Brier / ECE)", "Baseline": "0.0549", "LightGBM": f"{benchmark['batting_dismissal_prob']['untouched_test_2026']['Brier_Score']} (ECE: {benchmark['batting_dismissal_prob']['untouched_test_2026']['ECE']})", "XGBoost": "—", "CatBoost": "—"},
        {"Target": "Bowling Expected Runs (2025 Val RMSE)", "Baseline": "1.7180", "LightGBM": benchmark["bowling_expected_runs"]["validation_2025"]["LightGBM_RMSE"], "XGBoost": "—", "CatBoost": "—"},
        {"Target": "Bowling Expected Runs (2026 Test RMSE)", "Baseline": "1.7180", "LightGBM": benchmark["bowling_expected_runs"]["untouched_test_2026"]["LightGBM_RMSE"], "XGBoost": "—", "CatBoost": "—"}
    ])
    st.table(b_df)
    
    st.subheader("2. Ablation Study: What Powers Reliable Rankings?")
    st.markdown(r"""
    | Framework Configuration | Top-10 Overlap with Full Model | Key Methodological Impact |
    |---|---|---|
    | **Full Five-Pillar Model** | **10 / 10 (100%)** | Benchmark standard |
    | **Raw Career Strike Rate Only** | **1 / 10 (10%)** | **Completely fails**: rewards stat-padding in low-pressure situations |
    | **No Empirical Bayes Shrinkage** | **7 / 10 (70%)** | Distorted by small-sample extreme spikes |
    | **No Retention Delta** | **7 / 10 (70%)** | Fails to penalize players who collapse under pressure |
    """)

# ==========================================
# PAGE 6: DATA INVENTORY & PROVENANCE
# ==========================================
elif page == "📁 Data Inventory & Provenance":
    st.title("📁 Data Lineage & Provenance Log")
    st.json(provenance)
