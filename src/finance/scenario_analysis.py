"""Scenario and sensitivity analysis for provider returns."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd

from .returns import build_market_proxy, load_provider_return_series


def _scenario_labels(market_returns: pd.Series) -> pd.Series:
    labels = pd.Series(index=market_returns.index, dtype="object")
    labels[market_returns >= 0] = "bull"
    labels[market_returns < 0] = "bear"
    return labels


def _window_sensitivity(returns: pd.Series, windows: List[int]) -> Dict[str, float]:
    out: Dict[str, float] = {}
    for window in windows:
        if len(returns) < window:
            out[f"mean_return_{window}d"] = 0.0
            continue
        out[f"mean_return_{window}d"] = float(returns.tail(window).mean())
    return out


def build_scenario_sensitivity(data_dir: Path, output_path: Path) -> pd.DataFrame:
    provider_returns = load_provider_return_series(data_dir)
    market = build_market_proxy(provider_returns).dropna()
    labels = _scenario_labels(market)

    rows = []
    windows = [63, 126, 252]
    for provider, ret in provider_returns.items():
        aligned = pd.concat([ret, labels], axis=1, join="inner").dropna()
        aligned.columns = ["returns", "scenario"]
        bull_mean = float(aligned.loc[aligned["scenario"] == "bull", "returns"].mean())
        bear_mean = float(aligned.loc[aligned["scenario"] == "bear", "returns"].mean())
        sensitivity = _window_sensitivity(ret.dropna(), windows)
        rows.append(
            {
                "provider": provider,
                "bull_mean_return": round(bull_mean, 6),
                "bear_mean_return": round(bear_mean, 6),
                "regime_delta_bull_minus_bear": round(bull_mean - bear_mean, 6),
                **{k: round(v, 6) for k, v in sensitivity.items()},
            }
        )

    df = pd.DataFrame(rows).sort_values("regime_delta_bull_minus_bear", ascending=False).reset_index(drop=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df
