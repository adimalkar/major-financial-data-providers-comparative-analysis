"""Return-series loading and standardization helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def _to_datetime(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce", utc=True).dt.tz_localize(None)


def _normalize_returns(series: pd.Series) -> pd.Series:
    vals = pd.to_numeric(series, errors="coerce")
    # If values are likely in percent units, scale to decimal.
    if vals.abs().median(skipna=True) > 1:
        vals = vals / 100.0
    return vals


def _build_compustat_returns(df: pd.DataFrame) -> pd.Series:
    work = df.copy()
    work["datadate"] = _to_datetime(work["datadate"])
    work["prccd"] = pd.to_numeric(work["prccd"], errors="coerce")
    work = work.dropna(subset=["datadate", "prccd"]).sort_values("datadate")
    if work.empty:
        return pd.Series(dtype=float)
    daily = work.groupby("datadate", as_index=True)["prccd"].mean()
    return daily.pct_change().dropna()


def load_provider_return_series(data_dir: Path) -> Dict[str, pd.Series]:
    yahoo = pd.read_csv(data_dir / "yahoo_portfolio_history.csv")
    crsp = pd.read_csv(data_dir / "crsp_portfolio_history.csv")
    comp = pd.read_csv(data_dir / "compustat_daily_prices.csv")

    y_date_col = "Date" if "Date" in yahoo.columns else "date"
    c_date_col = "date"

    y = pd.Series(_normalize_returns(yahoo["returns"]).values, index=_to_datetime(yahoo[y_date_col]), name="Yahoo")
    c = pd.Series(_normalize_returns(crsp["returns"]).values, index=_to_datetime(crsp[c_date_col]), name="CRSP")
    p = _build_compustat_returns(comp)
    p.name = "Compustat"

    series_map = {"Yahoo": y.dropna().sort_index(), "CRSP": c.dropna().sort_index(), "Compustat": p.dropna().sort_index()}
    return series_map


def build_market_proxy(provider_returns: Dict[str, pd.Series]) -> pd.Series:
    aligned = pd.concat(provider_returns.values(), axis=1, join="outer")
    aligned.columns = list(provider_returns.keys())
    return aligned.mean(axis=1, skipna=True).dropna().rename("market_proxy")
