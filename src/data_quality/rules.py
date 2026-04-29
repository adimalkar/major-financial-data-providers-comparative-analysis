"""Threshold loading and pass/fail rule evaluation."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import yaml


def load_quality_config(config_path: Path) -> Dict:
    with config_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def evaluate_thresholds(scores: Dict[str, float], thresholds: Dict[str, float]) -> Dict[str, str]:
    evaluation = {}
    for metric, threshold in thresholds.items():
        value = float(scores.get(metric, 0.0))
        evaluation[f"{metric}_status"] = "pass" if value >= float(threshold) else "fail"
    return evaluation
