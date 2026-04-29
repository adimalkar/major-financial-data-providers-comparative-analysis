from pathlib import Path

import pandas as pd

from src.data_quality.metrics import completeness_score, timeliness_score, uniqueness_score
from src.data_quality.scorecard import build_data_quality_scorecard


def test_completeness_score_simple_case():
    df = pd.DataFrame({"a": [1, None], "b": [1, 2]})
    score = completeness_score(df, ["a", "b"])
    assert 74.0 <= score <= 76.0


def test_uniqueness_score_detects_duplicates():
    df = pd.DataFrame({"id": [1, 1, 2], "v": [10, 11, 12]})
    score = uniqueness_score(df, ["id"])
    assert 66.0 <= score <= 67.0


def test_timeliness_score_degrades_with_lag():
    fresh = pd.Timestamp("2025-01-10")
    stale = pd.Timestamp("2024-01-10")
    assert timeliness_score(fresh, fresh) == 100.0
    assert timeliness_score(stale, fresh) < 1.0


def test_build_data_quality_scorecard(tmp_path: Path):
    root = Path(__file__).resolve().parents[1]
    scorecard = build_data_quality_scorecard(
        data_dir=root / "FE511_Project",
        config_path=root / "config" / "quality_thresholds.yaml",
        output_csv_path=tmp_path / "dq.csv",
        output_md_path=tmp_path / "dq.md",
    )
    assert not scorecard.empty
    assert {"provider", "weighted_score"}.issubset(scorecard.columns)
