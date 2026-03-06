"""
validate_data.py
----------------
Validates integrity of all FinNutriAgent datasets.

Run:
    python scripts/validate_data.py

Exit code 0 = all checks passed.
Exit code 1 = one or more checks failed.
"""

import os
import sys
import yaml
import pandas as pd

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CFG_PATH = os.path.join(_ROOT, "config", "config.yaml")


def _load_config() -> dict:
    with open(_CFG_PATH, "r") as f:
        return yaml.safe_load(f)


def _load_datasets(cfg: dict):
    financial_df = pd.read_csv(os.path.join(_ROOT, cfg["data"]["financial"]))
    food_df      = pd.read_csv(os.path.join(_ROOT, cfg["data"]["composition"]),
                                skipinitialspace=True)
    prices_df    = pd.read_csv(os.path.join(_ROOT, cfg["data"]["prices"]),
                                skipinitialspace=True)
    nutrition_df = pd.read_csv(os.path.join(_ROOT, cfg["data"]["nutrition"]))

    for df in [food_df, prices_df]:
        df.columns = df.columns.str.strip()
        df["food_id"] = df["food_id"].str.strip()
    food_df["halal"] = food_df["halal"].str.strip()

    return financial_df, food_df, prices_df, nutrition_df


def _check(label: str, condition: bool, msg: str) -> bool:
    if condition:
        print(f"  [PASS] {label}")
    else:
        print(f"  [FAIL] {label}: {msg}")
    return condition


def run_validation() -> bool:
    cfg = _load_config()
    try:
        financial_df, food_df, prices_df, nutrition_df = _load_datasets(cfg)
    except FileNotFoundError as e:
        print(f"[ERROR] Cannot load data: {e}")
        return False

    expected = cfg["validation"]["expected_rows"]
    results  = []

    # ── 1. Row counts ─────────────────────────────────────────────────────────
    print("\n[1] Row counts")
    results += [
        _check("financial_data rows",         len(financial_df) == expected["financial"],
               f"expected {expected['financial']}, got {len(financial_df)}"),
        _check("food_composition rows",        len(food_df) == expected["composition"],
               f"expected {expected['composition']}, got {len(food_df)}"),
        _check("food_prices rows",             len(prices_df) == expected["prices"],
               f"expected {expected['prices']}, got {len(prices_df)}"),
        _check("nutrition_requirements rows",  len(nutrition_df) == expected["nutrition"],
               f"expected {expected['nutrition']}, got {len(nutrition_df)}"),
    ]

    # ── 2. Missing values ─────────────────────────────────────────────────────
    print("\n[2] Missing values")
    for name, df in [("financial_data", financial_df), ("food_composition", food_df),
                     ("food_prices", prices_df), ("nutrition_requirements", nutrition_df)]:
        n_missing = df.isnull().sum().sum()
        results.append(
            _check(f"{name} — no nulls", n_missing == 0, f"{n_missing} missing values found")
        )

    # ── 3. food_id consistency ────────────────────────────────────────────────
    print("\n[3] food_id key consistency")
    food_ids  = set(food_df["food_id"])
    price_ids = set(prices_df["food_id"])
    only_food  = food_ids  - price_ids
    only_price = price_ids - food_ids
    results.append(
        _check("food_id match across composition & prices",
               not only_food and not only_price,
               f"in food not prices: {only_food}; in prices not food: {only_price}")
    )

    # ── 4. Numeric ranges ─────────────────────────────────────────────────────
    print("\n[4] Numeric ranges")
    results += [
        _check("calories_per_100g > 0",
               (food_df["calories_per_100g"] > 0).all(), "non-positive calories found"),
        _check("protein_g >= 0",
               (food_df["protein_g"] >= 0).all(), "negative protein found"),
        _check("price_per_kg > 0",
               (prices_df["price_per_kg"] > 0).all(), "non-positive price found"),
        _check("calories_kcal > 0",
               (nutrition_df["calories_kcal"] > 0).all(), "non-positive calories found"),
    ]
    expense_cols = ["rent", "utilities", "transport", "education", "healthcare", "savings_target"]
    total_exp = financial_df[expense_cols].sum(axis=1)
    results.append(
        _check("expenses < income for all households",
               (total_exp < financial_df["monthly_income"]).all(),
               "some households have expenses ≥ income")
    )

    # ── 5. Categorical values ─────────────────────────────────────────────────
    print("\n[5] Categorical fields")
    results += [
        _check("halal values in {Yes, No}",
               set(food_df["halal"].unique()).issubset({"Yes", "No"}),
               f"unexpected values: {food_df['halal'].unique()}"),
        _check("gender values in {Male, Female}",
               set(nutrition_df["gender"].unique()).issubset({"Male", "Female"}),
               f"unexpected values: {nutrition_df['gender'].unique()}"),
    ]

    return all(results)


if __name__ == "__main__":
    print("=" * 58)
    print("FinNutriAgent — Data Validation")
    print("=" * 58)
    passed = run_validation()
    print("\n" + "=" * 58)
    if passed:
        print("All checks PASSED.")
        sys.exit(0)
    else:
        print("Some checks FAILED. See messages above.")
        sys.exit(1)
