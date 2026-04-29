"""CAPM-style factor exposure summary for provider returns."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

from .returns import build_market_proxy, load_provider_return_series


TRADING_DAYS = 252


def _ols_alpha_beta(y: pd.Series, x: pd.Series) -> Dict[str, float]:
    aligned = pd.concat([y, x], axis=1, join="inner").dropna()
    if aligned.empty or aligned.shape[0] < 5:
        return {"alpha_annual": 0.0, "beta": 0.0, "r_squared": 0.0}

    y_vals = aligned.iloc[:, 0].to_numpy()
    x_vals = aligned.iloc[:, 1].to_numpy()
    x_mean = x_vals.mean()
    y_mean = y_vals.mean()
    cov = float(np.mean((x_vals - x_mean) * (y_vals - y_mean)))
    var_x = float(np.mean((x_vals - x_mean) ** 2))
    beta = cov / var_x if var_x != 0 else 0.0
    alpha_daily = y_mean - beta * x_mean

    y_hat = alpha_daily + beta * x_vals
    ss_res = float(np.sum((y_vals - y_hat) ** 2))
    ss_tot = float(np.sum((y_vals - y_mean) ** 2))
    r_squared = 1.0 - ss_res / ss_tot if ss_tot != 0 else 0.0

    return {
        "alpha_annual": (1.0 + alpha_daily) ** TRADING_DAYS - 1.0,
        "beta": beta,
        "r_squared": r_squared,
    }


def build_factor_exposure_summary(data_dir: Path, output_path: Path) -> pd.DataFrame:
    returns_map = load_provider_return_series(data_dir)
    market = build_market_proxy(returns_map)

    rows = []
    for provider, provider_returns in returns_map.items():
        fit = _ols_alpha_beta(provider_returns, market)
        rows.append(
            {
                "provider": provider,
                "alpha_annual": round(float(fit["alpha_annual"]), 6),
                "beta": round(float(fit["beta"]), 6),
                "r_squared": round(float(fit["r_squared"]), 6),
                "model": "CAPM (market proxy)",
            }
        )

    df = pd.DataFrame(rows).sort_values("r_squared", ascending=False).reset_index(drop=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df
