"""
budget_agent.py
---------------
Computes available weekly food budget per household from financial_data.csv.

Example
-------
>>> from scripts.budget_agent import BudgetAgent
>>> agent = BudgetAgent()
>>> agent.get_weekly_budget("U017")
912.47...
"""

import os
import yaml
import pandas as pd
from typing import Optional

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CFG_PATH = os.path.join(_ROOT, "config", "config.yaml")


def _load_config() -> dict:
    with open(_CFG_PATH, "r") as f:
        return yaml.safe_load(f)


EXPENSE_COLUMNS = [
    "rent", "utilities", "transport", "education", "healthcare", "savings_target"
]


class BudgetAgent:
    """
    Reads household financial data and computes weekly food budgets.

    Parameters
    ----------
    filepath : str, optional
        Path to financial_data.csv. Defaults to path in config.yaml.
    weeks_per_month : float, optional
        Conversion factor. Defaults to value in config.yaml (4.33).
    """

    def __init__(self, filepath: Optional[str] = None, weeks_per_month: Optional[float] = None):
        cfg = _load_config()
        if filepath is None:
            filepath = os.path.join(_ROOT, cfg["data"]["financial"])
        self.weeks_per_month = weeks_per_month or cfg["budget"]["weeks_per_month"]
        self.df = pd.read_csv(filepath)
        self.df["user_id"] = self.df["user_id"].str.strip()

    def _get_row(self, user_id: str) -> pd.Series:
        row = self.df[self.df["user_id"] == user_id]
        if row.empty:
            raise ValueError(f"user_id '{user_id}' not found in financial data.")
        return row.iloc[0]

    def get_monthly_food_budget(self, user_id: str) -> float:
        """Return monthly residual income available for food (SAR)."""
        row = self._get_row(user_id)
        residual = row["monthly_income"] - sum(row[c] for c in EXPENSE_COLUMNS)
        if residual < 0:
            raise ValueError(
                f"Household {user_id} has a negative food budget ({residual:.2f} SAR). "
                "Check financial_data.csv."
            )
        return float(residual)

    def get_weekly_budget(self, user_id: str) -> float:
        """Return weekly food budget (SAR)."""
        return round(self.get_monthly_food_budget(user_id) / self.weeks_per_month, 2)

    def get_financial_summary(self, user_id: str) -> dict:
        """Return a full financial breakdown for a household."""
        row = self._get_row(user_id)
        monthly_food = self.get_monthly_food_budget(user_id)
        return {
            "user_id": user_id,
            "monthly_income_sar": int(row["monthly_income"]),
            "expenses": {c: int(row[c]) for c in EXPENSE_COLUMNS},
            "monthly_food_budget_sar": round(monthly_food, 2),
            "weekly_food_budget_sar": round(monthly_food / self.weeks_per_month, 2),
        }

    def get_all_weekly_budgets(self) -> pd.DataFrame:
        """Return weekly food budgets for all households."""
        df = self.df.copy()
        df["total_fixed_expenses"] = df[EXPENSE_COLUMNS].sum(axis=1)
        df["monthly_food_budget"]  = df["monthly_income"] - df["total_fixed_expenses"]
        df["weekly_food_budget_sar"] = (df["monthly_food_budget"] / self.weeks_per_month).round(2)
        return df[["user_id", "monthly_income", "total_fixed_expenses",
                   "monthly_food_budget", "weekly_food_budget_sar"]]


if __name__ == "__main__":
    agent = BudgetAgent()
    summary = agent.get_financial_summary("U017")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    all_budgets = agent.get_all_weekly_budgets()
    print(f"\nBudget range: {all_budgets['weekly_food_budget_sar'].min():.2f} – "
          f"{all_budgets['weekly_food_budget_sar'].max():.2f} SAR/week")
