# FE511: Comparative Analysis of Major Financial Data Providers

This project compares Yahoo Finance, CRSP (WRDS), and Compustat (WRDS) and upgrades the original course deliverable into a portfolio-grade analytics workflow for Data Analyst and Finance Analyst roles.

## Core Outcomes

- Formal data quality scoring across providers.
- Risk-adjusted financial metrics and factor diagnostics.
- Scenario and sensitivity analysis.
- Recommendation matrix by use case.
- One-command reproducible pipeline.

## Repository Structure

- `src/data_quality/`: quality metrics, thresholds, and provider scorecard logic.
- `src/finance/`: return engineering, risk metrics, factor model, and scenario analysis.
- `config/quality_thresholds.yaml`: configurable metric weights and pass/fail thresholds.
- `run_analysis.py`: end-to-end pipeline runner.
- `outputs/`: generated scorecards and analytics tables.
- `docs/`: project brief, criteria, executive summary, and recommendation matrix.
- `tests/`: automated checks for metrics and pipeline smoke tests.
- `FE511_Project/`: original source data exports used as pipeline inputs.
- Root notebooks: original project narrative notebooks.

## Quick Start

1. Install dependencies:
   - `pip install -r requirements.txt`
2. Run the pipeline:
   - `python run_analysis.py`
3. Run tests:
   - `pytest -q`
4. Launch dashboard:
   - `streamlit run dashboard/app.py`

## Generated Artifacts

- `outputs/provider_data_quality_scorecard.csv`
- `outputs/provider_risk_metrics.csv`
- `outputs/factor_exposure_summary.csv`
- `outputs/scenario_sensitivity_analysis.csv`
- `outputs/recommendation_matrix.csv`
- `docs/executive_summary.md`
- `docs/recommendation_matrix.md`

## Dashboard

- App entrypoint: `dashboard/app.py`
- Includes KPI cards, data quality diagnostics, risk-return and factor views, scenario analysis, and recommendation heatmap.

## Legacy Project Files

The original notebooks, final report PDFs, and `FE511_Project/` exports are preserved for transparency and reproducibility.
