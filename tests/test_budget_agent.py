"""Tests for BudgetAgent."""

import pytest
import pandas as pd
import tempfile
import os
from scripts.budget_agent import BudgetAgent, EXPENSE_COLUMNS


@pytest.fixture
def sample_csv(tmp_path):
    """Write a minimal financial_data.csv to a temp location."""
    data = pd.DataFrame([
        {"user_id": "U001", "monthly_income": 10000,
         "rent": 3000, "utilities": 800, "transport": 1200,
         "education": 2000, "healthcare": 300, "savings_target": 2700},
        {"user_id": "U002", "monthly_income": 5000,
         "rent": 1500, "utilities": 400, "transport": 600,
         "education": 500, "healthcare": 200, "savings_target": 1000},
    ])
    p = tmp_path / "financial_data.csv"
    data.to_csv(p, index=False)
    return str(p)


def test_weekly_budget_positive(sample_csv):
    agent = BudgetAgent(filepath=sample_csv)
    budget = agent.get_weekly_budget("U001")
    assert budget > 0


def test_weekly_budget_value(sample_csv):
    agent = BudgetAgent(filepath=sample_csv, weeks_per_month=4.33)
    # U001: income=10000, expenses=10000, residual=0 → actually residual=(10000-10000)=0
    # Use U002: 5000 - (1500+400+600+500+200+1000) = 5000 - 4200 = 800 monthly
    budget = agent.get_weekly_budget("U002")
    expected = round(800 / 4.33, 2)
    assert abs(budget - expected) < 0.05


def test_invalid_user_raises(sample_csv):
    agent = BudgetAgent(filepath=sample_csv)
    with pytest.raises(ValueError, match="not found"):
        agent.get_weekly_budget("U999")


def test_financial_summary_keys(sample_csv):
    agent = BudgetAgent(filepath=sample_csv)
    summary = agent.get_financial_summary("U002")
    assert "weekly_food_budget_sar" in summary
    assert "expenses" in summary
    assert all(k in summary["expenses"] for k in EXPENSE_COLUMNS)


def test_all_weekly_budgets_shape(sample_csv):
    agent = BudgetAgent(filepath=sample_csv)
    df = agent.get_all_weekly_budgets()
    assert len(df) == 2
    assert "weekly_food_budget_sar" in df.columns
    assert (df["weekly_food_budget_sar"] >= 0).all()
