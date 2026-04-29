"""Core metric functions for provider data-quality scoring."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

import pandas as pd


@dataclass(frozen=True)
class MetricResult:
    name: str
    score: float
    detail: str


def clamp_0_100(value: float) -> float:
    return float(max(0.0, min(100.0, value)))


def completeness_score(df: pd.DataFrame, required_columns: Iterable[str]) -> float:
    """Score based on non-null share of selected columns."""
    cols = [c for c in required_columns if c in df.columns]
    if df.empty or not cols:
        return 0.0
    non_null_share = 1.0 - float(df[cols].isna().sum().sum()) / float(len(df) * len(cols))
    return clamp_0_100(non_null_share * 100.0)


def uniqueness_score(df: pd.DataFrame, key_columns: Iterable[str]) -> float:
    """Score based on duplicate ratio over provider's primary key."""
    cols = [c for c in key_columns if c in df.columns]
    if df.empty or not cols:
        return 0.0
    dup_ratio = float(df.duplicated(subset=cols).mean())
    return clamp_0_100((1.0 - dup_ratio) * 100.0)


def timeliness_score(provider_max_date: Optional[pd.Timestamp], global_max_date: Optional[pd.Timestamp]) -> float:
    """Proxy timeliness score from staleness in days vs freshest provider."""
    if provider_max_date is None or global_max_date is None:
        return 0.0
    lag_days = max(0, int((global_max_date - provider_max_date).days))
    # 0-day lag => 100, 365+ day lag => 0
    return clamp_0_100(100.0 * (1.0 - min(lag_days, 365) / 365.0))


def consistency_score(abs_percent_diff_series: pd.Series) -> float:
    """Score from relative price disagreement vs other sources."""
    clean = pd.to_numeric(abs_percent_diff_series, errors="coerce").dropna()
    if clean.empty:
        return 0.0
    # 0% median diff => 100, 10% or worse => 0
    median_diff = float(clean.median())
    return clamp_0_100(100.0 * (1.0 - min(median_diff, 10.0) / 10.0))


def integrity_score(non_null_ratio: float) -> float:
    """Translate integrity ratio to score."""
    return clamp_0_100(non_null_ratio * 100.0)
