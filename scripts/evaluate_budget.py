"""Evaluate optimizer behavior when weekly budget is changed."""

import sys
from pathlib import Path

# Ensure the repo root is on sys.path so this can run without pip installing
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.budget_agent import BudgetAgent
from scripts.nutrition_agent import NutritionAgent
from scripts.optimizer import load_merged_food_data, run_optimization


def evaluate_weekly_budget(user_id: str, members: list[str], weekly_budget: float):
    nutrition_agent = NutritionAgent()
    nutrient_targets = nutrition_agent.get_household_weekly_targets(members)
    food_df = load_merged_food_data(halal_only=True)

    result = run_optimization(
        weekly_budget=weekly_budget,
        nutrient_targets=nutrient_targets,
        food_df=food_df,
    )

    print(f"--- Optimization Results (weekly budget = {weekly_budget} SAR) ---")
    print(f"Status: {result['status']}")
    print(f"Total cost (SAR): {result['total_cost_sar']}")
    print(f"Budget utilized (%): {result['total_cost_sar']/weekly_budget*100:.2f}%")
    print(f"Foods selected: {result['n_foods_selected']}")
    print('Nutrient coverage:')
    for k, v in result['nutrient_achieved'].items():
        t = nutrient_targets[k]
        print(f"  {k}: {v:.1f}/{t:.1f} ({v/t*100:.1f}%)")

    print('\nTop items (by cost):')
    print(result['plan'].head(10).to_string(index=False))


if __name__ == '__main__':
    evaluate_weekly_budget(user_id='U017', members=['P1', 'P2', 'P3', 'P4'], weekly_budget=500.0)
