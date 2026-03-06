"""Reproduce key results from the FinNutriAgent paper.

Run this script to regenerate the core numerical summaries and verify that the
optimization pipeline produces stable, reproducible output.

Usage
-----
python scripts/reproduce_results.py

The script produces:
- results/summary.csv              # per-household optimization metrics
- results/summary_stats.json       # aggregated stats (mean/std/min/max)
- results/household_U017.json      # detailed example results for household U017

The `results/` folder is git-ignored by default.
"""

import json
import os
import sys
from pathlib import Path

# Ensure the repository root is on sys.path so this script can be executed
# directly (without requiring `pip install -e .`).
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd

from scripts.budget_agent import BudgetAgent
from scripts.nutrition_agent import NutritionAgent
from scripts.optimizer import load_merged_food_data, run_optimization


def _household_members_from_user_id(user_id: str, members_per_household: int = 5) -> list[str]:
    """Map a household user_id (U001..U100) to a fixed set of person IDs.

    The dataset includes 500 individuals (P1..P500) and 100 households.
    We assign members in contiguous blocks of `members_per_household`.
    """
    base = int(user_id.lstrip("U")) - 1
    start = base * members_per_household + 1
    end = start + members_per_household
    return [f"P{i}" for i in range(start, end)]


def _price_shock(food_df: pd.DataFrame, factor: float = 1.2, keyword: str | None = None) -> pd.DataFrame:
    """Apply a price shock to a subset of foods.

    By default, applies to items that include `keyword` in the food name.
    If keyword is None, applies to all items.
    """
    df = food_df.copy()
    if keyword is None:
        df["price_per_kg"] *= factor
    else:
        mask = df["food_name"].str.lower().str.contains(keyword.lower())
        df.loc[mask, "price_per_kg"] *= factor
    return df


def _ensure_results_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def run_household_optimization(user_id: str, members: list[str], food_df: pd.DataFrame):
    budget_agent = BudgetAgent()
    nutrition_agent = NutritionAgent()

    weekly_budget = budget_agent.get_weekly_budget(user_id)
    nutrient_targets = nutrition_agent.get_household_weekly_targets(members)

    return run_optimization(
        weekly_budget=weekly_budget,
        nutrient_targets=nutrient_targets,
        food_df=food_df,
        halal_only=True,
    )


def main():
    repo_root = Path(__file__).resolve().parents[1]
    results_dir = repo_root / "results"
    _ensure_results_dir(results_dir)

    print("Loading food data...")
    food_df = load_merged_food_data(halal_only=True)

    # (A) Example household that matches the paper figures.
    # U017 uses members P1-P4.
    example_user = "U017"
    example_members = ["P1", "P2", "P3", "P4"]

    print(f"Running optimization for {example_user} (example household)...")
    example_result = run_household_optimization(example_user, example_members, food_df)

    # (B) Price shock simulation (20% on seafood-like items)
    shocked_food_df = _price_shock(food_df, factor=1.2, keyword="fish")
    print("Running price-shock optimization (20% on seafood-like foods)...")
    shocked_result = run_household_optimization(example_user, example_members, shocked_food_df)

    def _serialize_result(result: dict) -> dict:
        """Prepare a result dict for JSON serialization."""
        out = result.copy()
        out["plan"] = out["plan"].to_dict(orient="records")
        return out

    # Save example results
    with open(results_dir / "household_U017.json", "w", encoding="utf-8") as f:
        json.dump({
            "baseline": _serialize_result(example_result),
            "price_shock": _serialize_result(shocked_result),
        }, f, indent=2)

    # (C) Cross-household run (100 households)
    print("Running cross-household optimization (100 households)...")
    financial_df = pd.read_csv(repo_root / "data" / "financial" / "financial_data.csv")
    summary_rows = []

    for user_id in sorted(financial_df["user_id"]):
        members = _household_members_from_user_id(user_id, members_per_household=5)
        res = run_household_optimization(user_id, members, food_df)
        pct_budget = round(res["total_cost_sar"] / res["budget_sar"] * 100, 2)
        summary_rows.append({
            "user_id": user_id,
            "weekly_budget_sar": res["budget_sar"],
            "optimized_cost_sar": res["total_cost_sar"],
            "budget_utilization_pct": pct_budget,
            "status": res["status"],
            "n_foods_selected": res["n_foods_selected"],
        })

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(results_dir / "summary.csv", index=False)

    stats = {
        "weekly_budget_sar": {
            "mean": summary_df["weekly_budget_sar"].mean(),
            "std": summary_df["weekly_budget_sar"].std(),
            "min": summary_df["weekly_budget_sar"].min(),
            "max": summary_df["weekly_budget_sar"].max(),
        },
        "optimized_cost_sar": {
            "mean": summary_df["optimized_cost_sar"].mean(),
            "std": summary_df["optimized_cost_sar"].std(),
            "min": summary_df["optimized_cost_sar"].min(),
            "max": summary_df["optimized_cost_sar"].max(),
        },
        "budget_utilization_pct": {
            "mean": summary_df["budget_utilization_pct"].mean(),
            "std": summary_df["budget_utilization_pct"].std(),
            "min": summary_df["budget_utilization_pct"].min(),
            "max": summary_df["budget_utilization_pct"].max(),
        },
    }

    with open(results_dir / "summary_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    print("Reproducible results saved in:")
    print(f"  - {results_dir / 'summary.csv'}")
    print(f"  - {results_dir / 'summary_stats.json'}")
    print(f"  - {results_dir / 'household_U017.json'}")


if __name__ == "__main__":
    main()
