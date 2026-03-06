"""
optimizer.py
------------
MILP meal plan optimizer for FinNutriAgent.

Minimizes weekly food cost while satisfying nutritional requirements,
respecting a budget ceiling, enforcing halal compliance, and maintaining
dietary diversity via binary selection variables.

Example
-------
>>> from scripts.optimizer import run_optimization
>>> result = run_optimization(
...     weekly_budget=912.50,
...     nutrient_targets={"calories": 6696, "protein": 158,
...                       "vitamin_d": 60, "iron": 44},
... )
>>> result["status"]
'Optimal'
"""

import os
import yaml
import pandas as pd
from typing import Optional
from pulp import (LpProblem, LpMinimize, LpVariable, lpSum,
                  LpStatus, PULP_CBC_CMD)

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CFG_PATH = os.path.join(_ROOT, "config", "config.yaml")


def _load_config() -> dict:
    with open(_CFG_PATH, "r") as f:
        return yaml.safe_load(f)


# Maps optimizer nutrient key → food_composition column name
NUTRIENT_COLS = {
    "calories":  "calories_per_100g",
    "protein":   "protein_g",
    "vitamin_d": "vitamin_d_mcg",
    "iron":      "iron_mg",
}


def load_merged_food_data(halal_only: bool = True) -> pd.DataFrame:
    """
    Load food composition merged with average prices across stores.

    Parameters
    ----------
    halal_only : bool
        If True, return only halal-compliant food items.

    Returns
    -------
    pd.DataFrame
        food_id, food_name, nutrient columns, halal, price_per_kg
    """
    cfg = _load_config()
    food_df   = pd.read_csv(os.path.join(_ROOT, cfg["data"]["composition"]),
                             skipinitialspace=True)
    prices_df = pd.read_csv(os.path.join(_ROOT, cfg["data"]["prices"]),
                             skipinitialspace=True)

    for df in [food_df, prices_df]:
        df.columns = df.columns.str.strip()
        df["food_id"] = df["food_id"].str.strip()
    food_df["halal"] = food_df["halal"].str.strip()

    if halal_only:
        food_df = food_df[food_df["halal"] == "Yes"].copy()

    avg_prices = prices_df.groupby("food_id")["price_per_kg"].mean().reset_index()
    merged = food_df.merge(avg_prices, on="food_id", how="left")
    return merged.dropna(subset=["price_per_kg"]).reset_index(drop=True)


def run_optimization(
    weekly_budget: float,
    nutrient_targets: dict,
    food_df: Optional[pd.DataFrame] = None,
    halal_only: bool = True,
    min_grams: Optional[float] = None,
    max_grams: Optional[float] = None,
    epsilon: Optional[float] = None,
    verbose: bool = False,
) -> dict:
    """
    Run the FinNutriAgent MILP optimization.

    Parameters
    ----------
    weekly_budget : float
        Maximum weekly food spend in SAR.
    nutrient_targets : dict
        Required weekly nutrient totals.
        Keys: 'calories', 'protein', 'vitamin_d', 'iron'.
    food_df : pd.DataFrame, optional
        Pre-loaded merged food+price DataFrame. Loaded from disk if None.
    halal_only : bool
        Filter to halal foods only.
    min_grams : float, optional
        Minimum grams per selected food item per week. Default from config.
    max_grams : float, optional
        Maximum grams per selected food item per week. Default from config.
    epsilon : float, optional
        Diversity incentive weight. Default from config.
    verbose : bool
        Print solver output.

    Returns
    -------
    dict
        status (str), total_cost_sar (float), budget_sar (float),
        nutrient_targets (dict), nutrient_achieved (dict),
        n_foods_selected (int), plan (pd.DataFrame)
    """
    cfg = _load_config()["optimizer"]
    if min_grams is None:
        min_grams = cfg["min_grams"]
    if max_grams is None:
        max_grams = cfg["max_grams"]
    if epsilon is None:
        epsilon = cfg["diversity_epsilon"]

    if food_df is None:
        food_df = load_merged_food_data(halal_only=halal_only)

    food_ids = food_df["food_id"].tolist()
    costs    = {r["food_id"]: r["price_per_kg"] / 1000.0
                for _, r in food_df.iterrows()}

    # Decision variables
    x = {f: LpVariable(f"x_{f}", lowBound=0)   for f in food_ids}
    y = {f: LpVariable(f"y_{f}", cat="Binary") for f in food_ids}

    prob = LpProblem("FinNutriAgent_MealPlan", LpMinimize)

    # Objective: minimize cost with small diversity incentive
    prob += (lpSum(x[f] * costs[f] for f in food_ids)
             - epsilon * lpSum(y[f] for f in food_ids))

    # Quantity bounds linked to binary selection
    for f in food_ids:
        prob += x[f] >= min_grams * y[f]
        prob += x[f] <= max_grams * y[f]

    # Nutritional lower bounds
    for nut_key, col in NUTRIENT_COLS.items():
        if nut_key not in nutrient_targets:
            continue
        nut_val = food_df.set_index("food_id")[col].to_dict()
        prob += (lpSum(x[f] * nut_val[f] / 100.0 for f in food_ids)
                 >= nutrient_targets[nut_key])

    # Budget upper bound
    prob += lpSum(x[f] * costs[f] for f in food_ids) <= weekly_budget

    # Solve
    solver = PULP_CBC_CMD(msg=1 if verbose else 0)
    prob.solve(solver)

    status = LpStatus[prob.status]
    if status != "Optimal":
        return {
            "status": status,
            "total_cost_sar": None,
            "budget_sar": weekly_budget,
            "nutrient_targets": nutrient_targets,
            "nutrient_achieved": {},
            "n_foods_selected": 0,
            "plan": pd.DataFrame(),
        }

    # Collect plan
    plan_rows, total_cost = [], 0.0
    for f in food_ids:
        val = x[f].varValue or 0.0
        if val > 1e-4:
            item_cost = val * costs[f]
            total_cost += item_cost
            name = food_df.loc[food_df["food_id"] == f, "food_name"].values[0]
            plan_rows.append({
                "food_id":        f,
                "food_name":      name,
                "grams_per_week": round(val, 2),
                "cost_sar":       round(item_cost, 4),
            })

    plan_df = (pd.DataFrame(plan_rows)
               .sort_values("cost_sar", ascending=False)
               .reset_index(drop=True))

    # Compute achieved nutrients
    nutrient_achieved = {}
    for nut_key, col in NUTRIENT_COLS.items():
        nut_val = food_df.set_index("food_id")[col].to_dict()
        achieved = sum((x[f].varValue or 0.0) * nut_val[f] / 100.0 for f in food_ids)
        nutrient_achieved[nut_key] = round(achieved, 2)

    return {
        "status":            status,
        "total_cost_sar":    round(total_cost, 2),
        "budget_sar":        weekly_budget,
        "nutrient_targets":  nutrient_targets,
        "nutrient_achieved": nutrient_achieved,
        "n_foods_selected":  len(plan_df),
        "plan":              plan_df,
    }


if __name__ == "__main__":
    r = run_optimization(
        weekly_budget=912.50,
        nutrient_targets={"calories": 6696, "protein": 158,
                          "vitamin_d": 60, "iron": 44},
    )
    print(f"Status:         {r['status']}")
    print(f"Cost:           {r['total_cost_sar']:.2f} SAR  "
          f"(budget {r['budget_sar']:.2f} SAR)")
    print(f"Foods selected: {r['n_foods_selected']}")
    print("\nNutrient coverage:")
    for k in r["nutrient_targets"]:
        t, a = r["nutrient_targets"][k], r["nutrient_achieved"][k]
        print(f"  {k:<12}: target={t:.1f}  achieved={a:.1f}  ({a/t*100:.1f}%)")
    print("\nPlan:")
    print(r["plan"].to_string(index=False))
