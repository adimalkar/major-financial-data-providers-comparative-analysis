from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
DOCS = ROOT / "docs"
PROVIDER_COLORS = {
    "Yahoo": "#22c55e",
    "CRSP": "#3b82f6",
    "Compustat": "#f59e0b",
}


@st.cache_data
def load_data() -> dict[str, pd.DataFrame]:
    return {
        "dq": pd.read_csv(OUTPUTS / "provider_data_quality_scorecard.csv"),
        "risk": pd.read_csv(OUTPUTS / "provider_risk_metrics.csv"),
        "factor": pd.read_csv(OUTPUTS / "factor_exposure_summary.csv"),
        "scenario": pd.read_csv(OUTPUTS / "scenario_sensitivity_analysis.csv"),
        "recommendation": pd.read_csv(OUTPUTS / "recommendation_matrix.csv"),
    }


def read_executive_summary() -> str:
    path = DOCS / "executive_summary.md"
    if not path.exists():
        return "Executive summary not found. Run `python run_analysis.py` first."
    return path.read_text(encoding="utf-8")


def inject_css() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: radial-gradient(circle at 10% -10%, #1e293b 0%, #0b1020 45%, #070b16 100%);
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        h1, h2, h3, h4 {
            letter-spacing: 0.2px;
        }
        .hero-card {
            border: 1px solid rgba(148, 163, 184, 0.25);
            border-radius: 16px;
            padding: 1rem 1.2rem;
            background: linear-gradient(135deg, rgba(30,41,59,0.75), rgba(15,23,42,0.55));
            margin-bottom: 1rem;
        }
        .metric-card {
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 14px;
            background: rgba(15, 23, 42, 0.55);
            padding: 0.6rem 0.8rem;
        }
        div[data-baseweb="tab-list"] {
            gap: 0.4rem;
        }
        button[data-baseweb="tab"] {
            border-radius: 10px;
            border: 1px solid rgba(148, 163, 184, 0.2);
            padding: 0.35rem 0.9rem;
            background: rgba(15, 23, 42, 0.45);
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            border: 1px solid rgba(59, 130, 246, 0.8);
            background: rgba(30, 64, 175, 0.28);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.set_page_config(
        page_title="FE511 Data Provider Intelligence Dashboard",
        page_icon="📈",
        layout="wide",
    )
    inject_css()
    st.markdown(
        """
        <div class="hero-card">
            <h1 style="margin-bottom:0.2rem;">FE511 Data Provider Intelligence</h1>
            <p style="margin-bottom:0;">
                Executive-grade comparison of Yahoo Finance, CRSP (WRDS), and Compustat using
                data-quality scoring, risk diagnostics, and use-case recommendation modeling.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def provider_filter(df: pd.DataFrame, providers: list[str]) -> pd.DataFrame:
    return df[df["provider"].isin(providers)].copy()


def style_fig(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(
        title=title,
        template="plotly_dark",
        margin={"l": 10, "r": 10, "t": 55, "b": 10},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"size": 13},
        legend_title_text="",
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.20)")
    return fig


def kpi_cards(df_reco: pd.DataFrame, use_case: str) -> None:
    score_col = f"{use_case}_score"
    top_row = df_reco.sort_values(score_col, ascending=False).iloc[0]
    median_use_case_score = df_reco[score_col].median()
    median_quality = df_reco["weighted_score"].median()
    median_sharpe = df_reco["sharpe_ratio"].median()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Top Provider", top_row["provider"])
    c2.metric("Use-Case Score", f"{top_row[score_col]:.2f}", f"{top_row[score_col]-median_use_case_score:+.2f} vs median")
    c3.metric("Data Quality", f"{top_row['weighted_score']:.2f}", f"{top_row['weighted_score']-median_quality:+.2f} vs median")
    c4.metric("Sharpe Ratio", f"{top_row['sharpe_ratio']:.3f}", f"{top_row['sharpe_ratio']-median_sharpe:+.3f} vs median")


def render_overview(data: dict[str, pd.DataFrame], providers: list[str], use_case: str) -> None:
    reco = provider_filter(data["recommendation"], providers)
    kpi_cards(reco, use_case)

    col1, col2 = st.columns([1.25, 1])
    with col1:
        score_col = f"{use_case}_score"
        fig = px.bar(
            reco.sort_values(score_col, ascending=False),
            x="provider",
            y=score_col,
            color="provider",
            color_discrete_map=PROVIDER_COLORS,
            text_auto=".2f",
        )
        fig.update_layout(showlegend=False)
        fig = style_fig(fig, f"Provider Ranking: {use_case.replace('_', ' ').title()}")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("#### Executive Summary")
        st.markdown(
            "<div class='metric-card'>" + read_executive_summary().replace("\n", "<br>") + "</div>",
            unsafe_allow_html=True,
        )


def render_data_quality(data: dict[str, pd.DataFrame], providers: list[str]) -> None:
    st.subheader("Data Quality Diagnostics")
    dq = provider_filter(data["dq"], providers)
    metric_cols = [
        "coverage_availability",
        "timeliness_reliability",
        "corporate_actions_integrity",
        "historical_survivorship",
        "schema_consistency",
        "cross_source_consistency",
    ]

    fig_bar = px.bar(
        dq.sort_values("weighted_score", ascending=False),
        x="provider",
        y="weighted_score",
        color="provider",
        color_discrete_map=PROVIDER_COLORS,
        text_auto=".2f",
    )
    fig_bar.update_layout(showlegend=False)
    fig_bar = style_fig(fig_bar, "Weighted Data Quality Score")
    st.plotly_chart(fig_bar, use_container_width=True)

    fig_radar = go.Figure()
    for _, row in dq.iterrows():
        fig_radar.add_trace(
            go.Scatterpolar(
                r=[row[c] for c in metric_cols],
                theta=[c.replace("_", " ").title() for c in metric_cols],
                fill="toself",
                name=row["provider"],
                line={"color": PROVIDER_COLORS.get(row["provider"], None)},
            )
        )
    fig_radar.update_layout(
        template="plotly_dark",
        margin={"l": 10, "r": 10, "t": 50, "b": 10},
        paper_bgcolor="rgba(0,0,0,0)",
        polar={"radialaxis": {"visible": True, "range": [0, 100]}},
        title="Quality Metric Profile by Provider",
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    styled = dq[
        ["provider", "weighted_score"]
        + metric_cols
        + [f"{m}_status" for m in metric_cols]
    ].sort_values("weighted_score", ascending=False)
    st.dataframe(
        styled.style.format(precision=2),
        use_container_width=True,
        hide_index=True,
    )


def render_finance(data: dict[str, pd.DataFrame], providers: list[str]) -> None:
    st.subheader("Finance Performance and Factor Exposure")
    risk = provider_filter(data["risk"], providers)
    factor = provider_filter(data["factor"], providers)
    merged = risk.merge(factor[["provider", "alpha_annual", "beta", "r_squared"]], on="provider", how="left")

    c1, c2 = st.columns(2)
    with c1:
        fig_rr = px.scatter(
            merged,
            x="annualized_volatility",
            y="annualized_return",
            color="provider",
            color_discrete_map=PROVIDER_COLORS,
            size="sharpe_ratio",
            hover_data=["max_drawdown", "sortino_ratio", "r_squared"],
            size_max=36,
        )
        fig_rr = style_fig(fig_rr, "Risk-Return Positioning (Bubble Size = Sharpe)")
        st.plotly_chart(fig_rr, use_container_width=True)
    with c2:
        fig_dd = px.bar(
            merged.sort_values("max_drawdown", ascending=False),
            x="provider",
            y="max_drawdown",
            color="provider",
            color_discrete_map=PROVIDER_COLORS,
            text_auto=".2%",
        )
        fig_dd.update_layout(showlegend=False)
        fig_dd = style_fig(fig_dd, "Maximum Drawdown Comparison")
        st.plotly_chart(fig_dd, use_container_width=True)

    fig_factor = px.bar(
        merged.melt(
            id_vars=["provider"],
            value_vars=["beta", "r_squared", "alpha_annual"],
            var_name="metric",
            value_name="value",
        ),
        x="provider",
        y="value",
        color="metric",
        barmode="group",
        color_discrete_sequence=["#60a5fa", "#22c55e", "#f59e0b"],
    )
    fig_factor = style_fig(fig_factor, "Factor Diagnostics (CAPM Proxy)")
    st.plotly_chart(fig_factor, use_container_width=True)
    st.dataframe(
        merged.sort_values("sharpe_ratio", ascending=False).style.format(precision=4),
        use_container_width=True,
        hide_index=True,
    )


def render_scenarios(data: dict[str, pd.DataFrame], providers: list[str]) -> None:
    st.subheader("Regime and Sensitivity Analysis")
    scenario = provider_filter(data["scenario"], providers)

    fig_regime = px.bar(
        scenario.melt(
            id_vars="provider",
            value_vars=["bull_mean_return", "bear_mean_return"],
            var_name="regime",
            value_name="mean_return",
        ),
        x="provider",
        y="mean_return",
        color="regime",
        barmode="group",
        color_discrete_sequence=["#22c55e", "#ef4444"],
    )
    fig_regime = style_fig(fig_regime, "Bull vs Bear Mean Daily Return")
    st.plotly_chart(fig_regime, use_container_width=True)

    sensitivity_long = scenario.melt(
        id_vars="provider",
        value_vars=["mean_return_63d", "mean_return_126d", "mean_return_252d"],
        var_name="window",
        value_name="mean_return",
    )
    fig_sens = px.line(
        sensitivity_long,
        x="window",
        y="mean_return",
        color="provider",
        color_discrete_map=PROVIDER_COLORS,
        markers=True,
    )
    fig_sens = style_fig(fig_sens, "Return Sensitivity by Lookback Window")
    st.plotly_chart(fig_sens, use_container_width=True)

    st.dataframe(
        scenario.sort_values("regime_delta_bull_minus_bear", ascending=False).style.format(precision=6),
        use_container_width=True,
        hide_index=True,
    )


def render_recommendation(data: dict[str, pd.DataFrame], providers: list[str]) -> None:
    st.subheader("Recommendation Matrix")
    reco = provider_filter(data["recommendation"], providers)
    score_cols = [c for c in reco.columns if c.endswith("_score")]

    heatmap_df = reco.set_index("provider")[score_cols]
    fig_heat = px.imshow(
        heatmap_df,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="Tealgrn",
    )
    fig_heat = style_fig(fig_heat, "Use-Case Recommendation Heatmap")
    st.plotly_chart(fig_heat, use_container_width=True)

    st.dataframe(
        reco.sort_values(score_cols[0], ascending=False).style.format(precision=4),
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        label="Download recommendation matrix (CSV)",
        data=reco.to_csv(index=False).encode("utf-8"),
        file_name="recommendation_matrix_filtered.csv",
        mime="text/csv",
        use_container_width=True,
    )

    with st.expander("Show source output tables"):
        st.markdown("Use these files for your report, resume portfolio screenshots, and deployment checks.")
        for table_name, table_df in data.items():
            st.markdown(f"**{table_name}**")
            st.dataframe(table_df, use_container_width=True, hide_index=True)


def main() -> None:
    render_header()
    data = load_data()
    providers_all = sorted(data["recommendation"]["provider"].unique().tolist())
    use_cases = [
        "research_prototyping",
        "institutional_backtesting",
        "corporate_actions_research",
        "education_demo",
    ]

    with st.sidebar:
        st.header("Controls")
        providers = st.multiselect("Providers", options=providers_all, default=providers_all)
        if not providers:
            st.warning("Select at least one provider to continue.")
            return
        use_case = st.selectbox(
            "Primary Use Case",
            options=use_cases,
            format_func=lambda x: x.replace("_", " ").title(),
        )
        st.markdown("---")
        st.caption("Design notes: visual hierarchy, consistency, and cognitive-load reduction.")
        st.caption("Refresh data before presenting: `python run_analysis.py`")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Executive Overview", "Data Quality", "Finance", "Scenarios", "Recommendation"]
    )
    with tab1:
        render_overview(data, providers, use_case)
    with tab2:
        render_data_quality(data, providers)
    with tab3:
        render_finance(data, providers)
    with tab4:
        render_scenarios(data, providers)
    with tab5:
        render_recommendation(data, providers)


if __name__ == "__main__":
    main()
