"""Provider-level data quality scorecard generator."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd

from .metrics import (
    completeness_score,
    consistency_score,
    integrity_score,
    timeliness_score,
    uniqueness_score,
)
from .rules import evaluate_thresholds, load_quality_config


def _find_column_case_insensitive(df: pd.DataFrame, target: str) -> str | None:
    mapping = {col.lower(): col for col in df.columns}
    return mapping.get(target.lower())


def _load_provider_frames(data_dir: Path) -> Dict[str, pd.DataFrame]:
    return {
        "Yahoo": pd.read_csv(data_dir / "yahoo_portfolio_history.csv"),
        "CRSP": pd.read_csv(data_dir / "crsp_daily_data.csv"),
        "Compustat": pd.read_csv(data_dir / "compustat_daily_prices.csv"),
    }


def _provider_date_columns(frames: Dict[str, pd.DataFrame]) -> Dict[str, str | None]:
    return {provider: _find_column_case_insensitive(df, "date") for provider, df in frames.items()}


def _compute_timeliness(frames: Dict[str, pd.DataFrame]) -> Dict[str, float]:
    date_cols = _provider_date_columns(frames)
    provider_max_dates: Dict[str, pd.Timestamp | None] = {}
    for provider, df in frames.items():
        date_col = date_cols.get(provider)
        if not date_col:
            provider_max_dates[provider] = None
            continue
        series = pd.to_datetime(df[date_col], errors="coerce", utc=True).dt.tz_localize(None)
        provider_max_dates[provider] = series.max() if not series.dropna().empty else None

    global_max = max([d for d in provider_max_dates.values() if d is not None], default=None)
    return {p: timeliness_score(d, global_max) for p, d in provider_max_dates.items()}


def _compute_consistency(data_dir: Path) -> Dict[str, float]:
    comparison_path = data_dir / "price_comparison_analysis.csv"
    if not comparison_path.exists():
        return {"Yahoo": 0.0, "CRSP": 0.0, "Compustat": 0.0}

    comp = pd.read_csv(comparison_path)
    score_yahoo = consistency_score(
        pd.concat(
            [
                comp.get("Yahoo_vs_CRSP_Diff", pd.Series(dtype=float)).abs(),
                comp.get("Yahoo_vs_Comp_Diff", pd.Series(dtype=float)).abs(),
            ],
            ignore_index=True,
        )
    )
    score_crsp = consistency_score(
        pd.concat(
            [
                comp.get("Yahoo_vs_CRSP_Diff", pd.Series(dtype=float)).abs(),
                comp.get("CRSP_vs_Comp_Diff", pd.Series(dtype=float)).abs(),
            ],
            ignore_index=True,
        )
    )
    score_comp = consistency_score(
        pd.concat(
            [
                comp.get("Yahoo_vs_Comp_Diff", pd.Series(dtype=float)).abs(),
                comp.get("CRSP_vs_Comp_Diff", pd.Series(dtype=float)).abs(),
            ],
            ignore_index=True,
        )
    )
    return {"Yahoo": score_yahoo, "CRSP": score_crsp, "Compustat": score_comp}


def _compute_integrity(data_dir: Path, frames: Dict[str, pd.DataFrame]) -> Dict[str, float]:
    y_meta_path = data_dir / "meta_ticker_yahoo.csv"
    cfacpr_col = _find_column_case_insensitive(frames["CRSP"], "cfacpr")
    ajexdi_col = _find_column_case_insensitive(frames["Compustat"], "ajexdi")
    trfd_col = _find_column_case_insensitive(frames["Compustat"], "trfd")

    yahoo_ratio = 0.0
    if y_meta_path.exists():
        y_meta = pd.read_csv(y_meta_path)
        div_col = _find_column_case_insensitive(y_meta, "dividends")
        split_col = _find_column_case_insensitive(y_meta, "stock splits")
        if div_col and split_col:
            any_event = ((pd.to_numeric(y_meta[div_col], errors="coerce").fillna(0) != 0) |
                         (pd.to_numeric(y_meta[split_col], errors="coerce").fillna(0) != 0))
            yahoo_ratio = float(any_event.mean())

    crsp_ratio = (
        float(frames["CRSP"][cfacpr_col].notna().mean())
        if cfacpr_col is not None and not frames["CRSP"].empty
        else 0.0
    )

    comp_parts = []
    for col in (ajexdi_col, trfd_col):
        if col is not None and not frames["Compustat"].empty:
            comp_parts.append(float(frames["Compustat"][col].notna().mean()))
    comp_ratio = sum(comp_parts) / len(comp_parts) if comp_parts else 0.0

    return {
        "Yahoo": integrity_score(yahoo_ratio),
        "CRSP": integrity_score(crsp_ratio),
        "Compustat": integrity_score(comp_ratio),
    }


def _required_and_keys() -> Dict[str, Tuple[List[str], List[str]]]:
    return {
        "Yahoo": (["Date", "total_value", "returns", "cumulative_returns"], ["Date"]),
        "CRSP": (["date", "permno", "ticker", "prc", "ret"], ["date", "permno"]),
        "Compustat": (["datadate", "gvkey", "tic", "prccd"], ["datadate", "gvkey"]),
    }


def _metric_scores(frames: Dict[str, pd.DataFrame], data_dir: Path) -> Dict[str, Dict[str, float]]:
    req_keys = _required_and_keys()
    timeliness = _compute_timeliness(frames)
    consistency = _compute_consistency(data_dir)
    integrity = _compute_integrity(data_dir, frames)

    provider_scores: Dict[str, Dict[str, float]] = {}
    for provider, frame in frames.items():
        required_cols, key_cols = req_keys[provider]
        provider_scores[provider] = {
            "coverage_availability": completeness_score(frame, required_cols),
            "schema_consistency": uniqueness_score(frame, key_cols),
            "timeliness_reliability": timeliness[provider],
            "corporate_actions_integrity": integrity[provider],
            "historical_survivorship": completeness_score(frame, [required_cols[0], key_cols[-1]]),
            "cross_source_consistency": consistency[provider],
        }
    return provider_scores


def build_data_quality_scorecard(
    data_dir: Path,
    config_path: Path,
    output_csv_path: Path,
    output_md_path: Path,
) -> pd.DataFrame:
    config = load_quality_config(config_path)
    weights: Dict[str, float] = config["weights"]
    thresholds: Dict[str, float] = config["thresholds"]

    frames = _load_provider_frames(data_dir)
    per_provider = _metric_scores(frames, data_dir)

    rows = []
    for provider, metric_map in per_provider.items():
        weighted_score = 0.0
        for metric, weight in weights.items():
            weighted_score += float(metric_map.get(metric, 0.0)) * float(weight)
        row = {"provider": provider, **metric_map, "weighted_score": round(weighted_score, 2)}
        row.update(evaluate_thresholds(metric_map, thresholds))
        rows.append(row)

    scorecard = pd.DataFrame(rows).sort_values("weighted_score", ascending=False).reset_index(drop=True)
    output_csv_path.parent.mkdir(parents=True, exist_ok=True)
    scorecard.to_csv(output_csv_path, index=False)
    output_md_path.write_text(scorecard.to_markdown(index=False), encoding="utf-8")
    return scorecard
