import pandas as pd

from src.finance.risk_metrics import annualized_return, max_drawdown, sharpe_ratio


def test_annualized_return_positive_series():
    returns = pd.Series([0.01] * 252)
    value = annualized_return(returns)
    assert value > 0


def test_sharpe_ratio_flat_series():
    returns = pd.Series([0.0] * 50)
    assert sharpe_ratio(returns) == 0.0


def test_max_drawdown_expected_sign():
    returns = pd.Series([0.10, -0.20, 0.05])
    dd = max_drawdown(returns)
    assert dd < 0
