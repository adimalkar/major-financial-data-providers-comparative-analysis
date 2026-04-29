"""Risk and performance metric calculations."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

from .returns import load_provider_return_series


TRADING_DAYS = 252


def annualized_return(returns: pd.Series) -> float:
    if returns.empty:
        return 0.0
    compounded = float((1.0 + returns).prod())
    years = max(len(returns) / TRADING_DAYS, 1e-9)
    return compounded ** (1.0 / years) - 1.0


def annualized_volatility(returns: pd.Series) -> float:
    if returns.empty:
        return 0.0
    return float(returns.std(ddof=1) * np.sqrt(TRADING_DAYS))


def sharpe_ratio(returns: pd.Series, risk_free_annual: float = 0.02) -> float:
    if returns.empty:
        return 0.0
    daily_rf = risk_free_annual / TRADING_DAYS
    excess = returns - daily_rf
    vol = excess.std(ddof=1)
    if np.isnan(vol) or abs(vol) < 1e-12:
        return 0.0
    return float((excess.mean() / vol) * np.sqrt(TRADING_DAYS))


def sortino_ratio(returns: pd.Series, risk_free_annual: float = 0.02) -> float:
    if returns.empty:
        return 0.0
    daily_rf = risk_free_annual / TRADING_DAYS
    excess = returns - daily_rf
    downside = excess[excess < 0]
    downside_std = downside.std(ddof=1)
    if np.isnan(downside_std) or abs(downside_std) < 1e-12:
        return 0.0
    return float((excess.mean() / downside_std) * np.sqrt(TRADING_DAYS))


def max_drawdown(returns: pd.Series) -> float:
    if returns.empty:
        return 0.0
    wealth = (1.0 + returns).cumprod()
    running_peak = wealth.cummax()
    drawdown = wealth / running_peak - 1.0
    return float(drawdown.min())


def build_provider_risk_metrics(data_dir: Path, output_path: Path) -> pd.DataFrame:
    series_map: Dict[str, pd.Series] = load_provider_return_series(data_dir)
    rows = []
    for provider, returns in series_map.items():
        rows.append(
            {
                "provider": provider,
                "observations": int(returns.shape[0]),
                "annualized_return": round(annualized_return(returns), 6),
                "annualized_volatility": round(annualized_volatility(returns), 6),
                "sharpe_ratio": round(sharpe_ratio(returns), 6),
                "sortino_ratio": round(sortino_ratio(returns), 6),
                "max_drawdown": round(max_drawdown(returns), 6),
            }
        )
    df = pd.DataFrame(rows).sort_values("sharpe_ratio", ascending=False).reset_index(drop=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df
