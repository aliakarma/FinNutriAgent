"""
nutrition_agent.py
------------------
Aggregates individual nutritional requirements to household-level weekly targets.

Example
-------
>>> from scripts.nutrition_agent import NutritionAgent
>>> agent = NutritionAgent()
>>> agent.get_household_weekly_targets(["P1", "P2", "P3", "P4"])
{'calories': 14322.0, 'protein': 357.0, 'vitamin_d': 105.0, 'iron': 56.0}
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


NUTRIENT_COLS = ["calories_kcal", "protein_g", "vitamin_d_mcg", "iron_mg"]


class NutritionAgent:
    """
    Reads individual nutritional requirements and aggregates to household level.

    Parameters
    ----------
    filepath : str, optional
        Path to nutrition_requirements.csv. Defaults to config.yaml path.
    """

    def __init__(self, filepath: Optional[str] = None):
        cfg = _load_config()
        if filepath is None:
            filepath = os.path.join(_ROOT, cfg["data"]["nutrition"])
        self.df = pd.read_csv(filepath)
        self.df["person_id"] = self.df["person_id"].str.strip()

    def get_individual_requirements(self, person_id: str) -> dict:
        """
        Return daily nutritional requirements for one individual.

        Parameters
        ----------
        person_id : str  e.g. 'P1'

        Returns
        -------
        dict
        """
        row = self.df[self.df["person_id"] == person_id]
        if row.empty:
            raise ValueError(f"person_id '{person_id}' not found.")
        row = row.iloc[0]
        return {
            "person_id": person_id,
            "age": int(row["age"]),
            "gender": row["gender"],
            **{col: float(row[col]) for col in NUTRIENT_COLS},
        }

    def get_household_daily_targets(self, person_ids: list) -> dict:
        """
        Sum daily nutritional requirements across household members.

        Parameters
        ----------
        person_ids : list of str

        Returns
        -------
        dict — summed daily nutrient targets
        """
        subset = self.df[self.df["person_id"].isin(person_ids)]
        missing = set(person_ids) - set(subset["person_id"])
        if missing:
            raise ValueError(f"person_id(s) not found: {missing}")
        return {col: float(subset[col].sum()) for col in NUTRIENT_COLS}

    def get_household_weekly_targets(self, person_ids: list) -> dict:
        """
        Compute weekly nutritional targets for the household (daily × 7).

        Returns
        -------
        dict — keys: calories, protein, vitamin_d, iron
        """
        daily = self.get_household_daily_targets(person_ids)
        return {
            "calories":  round(daily["calories_kcal"] * 7, 1),
            "protein":   round(daily["protein_g"] * 7, 1),
            "vitamin_d": round(daily["vitamin_d_mcg"] * 7, 1),
            "iron":      round(daily["iron_mg"] * 7, 1),
        }

    def describe_household(self, person_ids: list) -> pd.DataFrame:
        """Return a summary DataFrame of household members."""
        return (self.df[self.df["person_id"].isin(person_ids)]
                .reset_index(drop=True))


if __name__ == "__main__":
    agent = NutritionAgent()
    members = ["P1", "P2", "P3", "P4"]
    print("Household members:")
    print(agent.describe_household(members).to_string(index=False))
    weekly = agent.get_household_weekly_targets(members)
    print("\nWeekly household targets:")
    for k, v in weekly.items():
        print(f"  {k}: {v}")
