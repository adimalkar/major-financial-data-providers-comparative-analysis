# Executive Summary

## Objective
Evaluate Yahoo, CRSP, and Compustat for analyst use cases using a weighted data-quality framework plus risk and factor diagnostics.

## Key Findings
- Highest overall data-quality score: **CRSP**
- Strongest risk-adjusted return (Sharpe): **Yahoo**
- Best for research prototyping: **Yahoo**
- Best for institutional backtesting: **CRSP**
- Best for corporate actions research: **CRSP**

## Recommendation by Use Case
- Use a **tiered provider strategy**: keep lower-friction sources for ideation, and use institution-grade sources for production-sensitive analytics.
- Prioritize providers with better survivorship and corporate-actions integrity for backtesting and risk reporting.

## Caveats
- Scores are constrained by available source files and local dataset coverage.
- Licensing, timeliness SLAs, and point-in-time constraints should be validated before production adoption.
