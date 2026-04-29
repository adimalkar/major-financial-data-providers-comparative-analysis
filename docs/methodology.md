# Methodology

## 1) Standardized Inputs
The pipeline uses local source exports in `FE511_Project/` and maps them into provider-level return and quality calculations:
- Yahoo portfolio history
- CRSP daily and portfolio history
- Compustat daily prices
- Cross-source comparison tables

## 2) Data Quality Scoring
For each provider, the framework computes:
- Coverage and availability (required field completeness)
- Timeliness and update reliability (relative staleness proxy)
- Corporate actions integrity (event/adjustment data presence)
- Historical survivorship proxy
- Schema consistency (duplicate ratio on provider keys)
- Cross-source consistency (median absolute relative price gap)

Weighted aggregation uses `config/quality_thresholds.yaml`.

## 3) Financial Analytics
The finance module computes:
- Annualized return and volatility
- Sharpe and Sortino ratios
- Max drawdown
- CAPM-style alpha/beta and model fit against a market proxy
- Bull/bear regime return comparison and window sensitivity (63/126/252-day means)

## 4) Recommendation Layer
The recommendation matrix blends data quality, risk performance, and factor fit to generate scenario-specific rankings:
- research prototyping
- institutional backtesting
- corporate actions research
- education and demo usage

## 5) Validation
Automated tests validate:
- metric correctness on deterministic examples
- scorecard generation behavior
- end-to-end pipeline execution
