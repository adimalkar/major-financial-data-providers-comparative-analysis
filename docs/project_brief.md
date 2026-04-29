# Project Brief: Comparative Analysis of Major Financial Data Providers

## Decision Objective
Select the most suitable financial data provider by use case (research, portfolio analytics, and risk reporting) using evidence-driven data quality and financial analysis metrics.

## Problem Statement
Financial teams often combine low-cost and institutional datasets without a formal framework for provider selection. This creates risks in data consistency, survivorship bias, and reproducibility. This project upgrades the FE511 course work into a practical decision-support framework.

## Stakeholder Personas
- Research Analyst: needs broad, timely market coverage and easy export for ad-hoc analysis.
- Portfolio Analyst: needs reliable historical returns, corporate actions handling, and reproducible portfolio backtests.
- Risk Team: needs consistent identifiers, delisting-aware history, and auditable data lineage.
- Data Platform Team: needs maintainable ingestion, validation checks, and stable schema assumptions.

## Scope
- Providers: Yahoo Finance, CRSP (WRDS), Compustat (WRDS).
- Asset examples: large-cap equities and selected case studies from the existing FE511 dataset.
- Outputs: data quality scorecard, risk-performance comparison, recommendation matrix.

## Constraints
- Access and licensing vary by provider and institution.
- Timestamp granularity and corporate action conventions differ by source.
- Some fields are unavailable in all providers and require fallback rules.

## Core Questions
1. Which provider best supports analyst workflows by use case?
2. How much does data quality variance affect portfolio and risk conclusions?
3. What provider mix balances cost, reliability, and research depth?

## Decision Principle
Recommendation quality must be traceable to measured data quality and finance metrics, not narrative preference.
