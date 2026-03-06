"""Stress testing FinNutriAgent optimization behavior.

This script runs a set of sensitivity experiments to show how the optimizer
behaves under budget pressure, diversity incentive variations, and vs a simple
greedy baseline.

Usage
-----
python scripts/stress_test.py

Outputs
-------
- results/stress_test.json
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Ensure repository root is on sys.path so this script can be run without
# requiring `pip install -e .`.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.budget_agent import BudgetAgent
from scripts.optimizer import load_merged_food_data, run_optimization
from scripts.nutrition_agent import NutritionAgent


def greedy_baseline(nutrient_targets: dict, food_df, min_grams=50, max_grams=500):
    """Greedy baseline: select cheapest items by calorie cost until targets reached."""
    # Use cost per calorie as the heuristic
    df = food_df.copy()
    df = df.assign(cost_per_kcal=lambda d: d["price_per_kg"] / (d["calories_per_100g"] * 10))
    df = df.sort_values("cost_per_kcal")

    # Start with zero selection
    selected = {f: 0.0 for f in df["food_id"]}

    def achieved(nutrient):
        col = {
            "calories": "calories_per_100g",
            "protein": "protein_g",
            "vitamin_d": "vitamin_d_mcg",
            "iron": "iron_mg",
        }[nutrient]
        return sum(selected[f] * df.loc[df["food_id"] == f, col].values[0] / 100.0
                   for f in selected)

    # Greedy: add minimum quantity of the cheapest food until all targets met
    idx = 0
    while True:
        if all(achieved(n) >= nutrient_targets[n] for n in nutrient_targets):
            break
        if idx >= len(df):
            break
        f = df.iloc[idx]["food_id"]
        selected[f] += min_grams
        # Cap at max_grams
        if selected[f] > max_grams:
            idx += 1

    plan = []
    total_cost = 0.0
    for f, grams in selected.items():
        if grams <= 0:
            continue
        price = float(df.loc[df["food_id"] == f, "price_per_kg"].values[0])
        cost = grams * price / 1000.0
        total_cost += cost
        plan.append({
            "food_id": f,
            "grams_per_week": float(round(grams, 2)),
            "cost_sar": float(round(cost, 4)),
        })

    achieved = {n: float(round(achieved(n), 2)) for n in nutrient_targets}

    return {
        "status": "GreedyBaseline",
        "total_cost_sar": float(round(total_cost, 2)),
        "nutrient_achieved": achieved,
        "plan": plan,
    }


def _ensure_results_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def _serialize_result(result: dict) -> dict:
    """Make a run_optimization result JSON serializable."""
    out = result.copy()
    plan_df = out.get("plan")
    if hasattr(plan_df, "to_dict"):
        out["plan"] = plan_df.to_dict(orient="records")
    return out


def find_minimum_feasible_budget(
    base_budget: float,
    nutrient_targets: dict,
    food_df,
    epsilon: float = 0.01,
    max_multiplier: float = 1000.0,
    tolerance: float = 0.01,
) -> dict:
    """Find the smallest budget multiplier that makes the problem feasible.

    Steps:
    1. If base_budget is feasible, return multiplier=1.0.
    2. Otherwise, exponentially increase budget until feasible or max_multiplier.
    3. Binary-search between last infeasible and feasible budgets to refine.
    """

    def _run(budget):
        return run_optimization(
            weekly_budget=budget,
            nutrient_targets=nutrient_targets,
            food_df=food_df,
            epsilon=epsilon,
        )

    # Step 1: check baseline
    base_res = _run(base_budget)
    if base_res["status"] == "Optimal":
        return {
            "multiplier": 1.0,
            "weekly_budget": base_budget,
            "result": _serialize_result(base_res),
        }

    # Step 2: exponential search
    low = base_budget
    high = base_budget
    feasible_res = None
    while high / base_budget <= max_multiplier:
        high *= 2
        res = _run(high)
        if res["status"] == "Optimal":
            feasible_res = res
            break
    else:
        # exceeded max multiplier without finding a feasible budget
        return {
            "multiplier": None,
            "weekly_budget": None,
            "result": None,
            "note": f"No feasible solution found up to {max_multiplier}× budget",
        }

    # Step 3: binary search to refine
    low = high / 2
    for _ in range(30):
        mid = (low + high) / 2
        res = _run(mid)
        if res["status"] == "Optimal":
            feasible_res = res
            high = mid
        else:
            low = mid
        if high - low < tolerance:
            break

    return {
        "multiplier": round(high / base_budget, 3),
        "weekly_budget": round(high, 2),
        "result": _serialize_result(feasible_res) if feasible_res is not None else None,
    }


def scale_financial_dataset(
    multiplier: float,
    input_path: Path,
    output_path: Path | None = None,
    overwrite: bool = False,
):
    """Scale monetary columns in the financial dataset by a multiplier.

    The budget computation is based on the difference between income and
    expenses, so scaling all monetary columns preserves relative ratios.
    """
    df = pd.read_csv(input_path)
    money_cols = [
        "monthly_income",
        "rent",
        "utilities",
        "transport",
        "education",
        "healthcare",
        "savings_target",
    ]
    for c in money_cols:
        if c in df.columns:
            df[c] = (df[c].astype(float) * multiplier).round(0).astype(int)

    if output_path is None:
        output_path = input_path

    if output_path.exists() and not overwrite and output_path != input_path:
        raise FileExistsError(f"Output path already exists: {output_path}")

    df.to_csv(output_path, index=False)
    return output_path


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Stress test and optional dataset scaling for FinNutriAgent.")
    parser.add_argument(
        "--apply-scaling",
        action="store_true",
        help="Scale the financial dataset using the computed minimum feasible multiplier.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="File path to write the scaled financial dataset (default: overwrite input file if --apply-scaling).",
    )
    parser.add_argument(
        "--user-id",
        type=str,
        default="U017",
        help="Household user_id to use for the scaling computation.",
    )
    parser.add_argument(
        "--members",
        type=str,
        default="P1,P2,P3,P4",
        help="Comma-separated person_ids for the household used in nutrient targeting.",
    )

    args = parser.parse_args()

    results_dir = ROOT / "results"
    _ensure_results_dir(results_dir)

    budget_agent = BudgetAgent()
    nutrition_agent = NutritionAgent()
    food_df = load_merged_food_data(halal_only=True)

    user_id = args.user_id
    members = [m.strip() for m in args.members.split(",") if m.strip()]

    budget = budget_agent.get_weekly_budget(user_id)
    nutrient_targets = nutrition_agent.get_household_weekly_targets(members)

    budgets = {
        "baseline": budget,
        "-20%": budget * 0.8,
        "+20%": budget * 1.2,
    }

    results = {
        "budget_scenarios": {},
        "budget_scaling": {},
        "diversity_impact": {},
        "baseline_comparison": {},
    }

    # 1) Budget sensitivity
    for label, b in budgets.items():
        r = run_optimization(
            weekly_budget=b,
            nutrient_targets=nutrient_targets,
            food_df=food_df,
            epsilon=0.01,
        )
        results["budget_scenarios"][label] = {
            "weekly_budget": float(round(b, 2)),
            "status": r["status"],
            "total_cost_sar": r.get("total_cost_sar"),
            "budget_utilization_pct": None if r.get("total_cost_sar") is None else float(round(r["total_cost_sar"] / b * 100, 2)),
            "n_foods_selected": r["n_foods_selected"],
            "nutrient_achieved": r["nutrient_achieved"],
        }

    # 1b) Find minimum feasible budget multiplier
    scaling = find_minimum_feasible_budget(
        base_budget=budget,
        nutrient_targets=nutrient_targets,
        food_df=food_df,
        epsilon=0.01,
    )
    results["budget_scaling"] = scaling

    # 2) Diversity incentive impact
    for eps in [0.0, 0.01, 0.1]:
        r = run_optimization(
            weekly_budget=budget,
            nutrient_targets=nutrient_targets,
            food_df=food_df,
            epsilon=eps,
        )
        results["diversity_impact"][f"epsilon_{eps}"] = {
            "epsilon": eps,
            "status": r["status"],
            "total_cost_sar": r.get("total_cost_sar"),
            "n_foods_selected": r["n_foods_selected"],
            "nutrient_achieved": r["nutrient_achieved"],
        }

    # 3) Greedy baseline comparison (no budget constraint; shows what the optimizer saves)
    greedy = greedy_baseline(nutrient_targets, food_df)
    results["baseline_comparison"]["greedy"] = greedy

    # Save
    with open(results_dir / "stress_test.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("Stress test completed. Results saved to:")
    print(f"  - {results_dir / 'stress_test.json'}")

    if args.apply_scaling:
        multiplier = results["budget_scaling"]["multiplier"]
        if multiplier is None:
            raise RuntimeError("No feasible budget multiplier found; cannot scale dataset.")

        input_path = ROOT / "data" / "financial" / "financial_data.csv"
        output_path = Path(args.output) if args.output else input_path
        scaled_path = scale_financial_dataset(
            multiplier=multiplier,
            input_path=input_path,
            output_path=output_path,
            overwrite=(output_path == input_path),
        )
        print(f"Scaled financial dataset written to: {scaled_path}")


if __name__ == "__main__":
    main()
