"""One-command pipeline for FE511 V2 analytics artifacts."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.data_quality import build_data_quality_scorecard
from src.finance import (
    build_factor_exposure_summary,
    build_provider_risk_metrics,
    build_scenario_sensitivity,
)


def _build_recommendation_matrix(
    dq: pd.DataFrame,
    risk: pd.DataFrame,
    factor: pd.DataFrame,
    output_csv: Path,
    output_md: Path,
) -> pd.DataFrame:
    merged = dq[["provider", "weighted_score"]].merge(
        risk[["provider", "sharpe_ratio", "max_drawdown"]],
        on="provider",
        how="left",
    ).merge(
        factor[["provider", "r_squared"]],
        on="provider",
        how="left",
    )

    merged["research_prototyping_score"] = (
        0.45 * merged["weighted_score"] + 30 * merged["sharpe_ratio"] + 25 * merged["r_squared"]
    )
    merged["institutional_backtesting_score"] = (
        0.55 * merged["weighted_score"] + 35 * merged["sharpe_ratio"] - 15 * merged["max_drawdown"]
    )
    merged["corporate_actions_research_score"] = 0.70 * merged["weighted_score"] + 20 * merged["r_squared"]
    merged["education_demo_score"] = 0.35 * merged["weighted_score"] + 10 * merged["sharpe_ratio"] + 25

    for col in merged.columns:
        if col.endswith("_score"):
            merged[col] = merged[col].round(4)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(output_csv, index=False)
    output_md.write_text(merged.to_markdown(index=False), encoding="utf-8")
    return merged


def _write_executive_summary(
    dq: pd.DataFrame,
    risk: pd.DataFrame,
    recommendation: pd.DataFrame,
    output_path: Path,
) -> None:
    top_quality = dq.sort_values("weighted_score", ascending=False).iloc[0]["provider"]
    top_sharpe = risk.sort_values("sharpe_ratio", ascending=False).iloc[0]["provider"]

    def top_provider(col: str) -> str:
        return recommendation.sort_values(col, ascending=False).iloc[0]["provider"]

    text = f"""# Executive Summary

## Objective
Evaluate Yahoo, CRSP, and Compustat for analyst use cases using a weighted data-quality framework plus risk and factor diagnostics.

## Key Findings
- Highest overall data-quality score: **{top_quality}**
- Strongest risk-adjusted return (Sharpe): **{top_sharpe}**
- Best for research prototyping: **{top_provider('research_prototyping_score')}**
- Best for institutional backtesting: **{top_provider('institutional_backtesting_score')}**
- Best for corporate actions research: **{top_provider('corporate_actions_research_score')}**

## Recommendation by Use Case
- Use a **tiered provider strategy**: keep lower-friction sources for ideation, and use institution-grade sources for production-sensitive analytics.
- Prioritize providers with better survivorship and corporate-actions integrity for backtesting and risk reporting.

## Caveats
- Scores are constrained by available source files and local dataset coverage.
- Licensing, timeliness SLAs, and point-in-time constraints should be validated before production adoption.
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parent
    data_dir = root / "FE511_Project"
    outputs_dir = root / "outputs"
    docs_dir = root / "docs"

    dq = build_data_quality_scorecard(
        data_dir=data_dir,
        config_path=root / "config" / "quality_thresholds.yaml",
        output_csv_path=outputs_dir / "provider_data_quality_scorecard.csv",
        output_md_path=outputs_dir / "provider_data_quality_scorecard.md",
    )
    risk = build_provider_risk_metrics(data_dir, outputs_dir / "provider_risk_metrics.csv")
    factor = build_factor_exposure_summary(data_dir, outputs_dir / "factor_exposure_summary.csv")
    build_scenario_sensitivity(data_dir, outputs_dir / "scenario_sensitivity_analysis.csv")
    recommendation = _build_recommendation_matrix(
        dq,
        risk,
        factor,
        output_csv=outputs_dir / "recommendation_matrix.csv",
        output_md=docs_dir / "recommendation_matrix.md",
    )
    _write_executive_summary(
        dq,
        risk,
        recommendation,
        output_path=docs_dir / "executive_summary.md",
    )

    print("Pipeline complete. Generated files in outputs/ and docs/.")


if __name__ == "__main__":
    main()
