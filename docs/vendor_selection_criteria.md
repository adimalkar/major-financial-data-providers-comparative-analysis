# Vendor Selection Criteria and Weighting

## Scoring Model
Each provider receives a normalized score from 0 to 100 for each criterion. Final weighted score is:

`Weighted Score = sum(Criterion Score x Criterion Weight)`

## Criteria

| Criterion | Weight | Why It Matters | Example Evidence |
|---|---:|---|---|
| Coverage and Availability | 20% | Determines breadth of usable symbols/time periods. | Missing rate, available date span, delisted coverage. |
| Timeliness and Update Reliability | 15% | Impacts signal freshness and operational confidence. | Relative lag, stale-row checks, update continuity. |
| Corporate Actions Integrity | 15% | Required for clean return series and portfolio accounting. | Split/dividend consistency and adjustment checks. |
| Historical Depth and Survivorship Robustness | 20% | Essential for backtesting realism and bias control. | Delisting support, identifier continuity, long history. |
| Data Consistency and Schema Stability | 15% | Reduces transformation errors and maintenance burden. | Cross-source field consistency and schema drift rate. |
| Cost and Integration Friction | 15% | Impacts team scalability and practical adoption. | Licensing, API ease, compute/engineering overhead. |

## Use-Case Overrides
- Research Prototyping: increase `Cost and Integration Friction` to 25%.
- Institutional Backtesting: increase `Historical Depth and Survivorship Robustness` to 30%.
- Corporate Action Analysis: increase `Corporate Actions Integrity` to 30%.

## Tie-Breaker Rules
1. Prefer provider with higher survivorship robustness when weighted scores are within 3 points.
2. Prefer provider with lower integration friction when scores are within 1 point for non-production analytics.
3. Use blended recommendation if one provider dominates quality while another dominates cost.
