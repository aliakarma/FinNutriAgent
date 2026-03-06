"""Tests for the MILP optimizer."""

import pytest
import pandas as pd
from scripts.optimizer import run_optimization


@pytest.fixture
def minimal_food_df():
    """Small synthetic food DataFrame sufficient to satisfy test targets."""
    return pd.DataFrame([
        {"food_id": "F001", "food_name": "Chicken Breast",
         "calories_per_100g": 165, "protein_g": 31, "vitamin_d_mcg": 0.1,
         "iron_mg": 1.3, "halal": "Yes", "price_per_kg": 25},
        {"food_id": "F002", "food_name": "Lentils",
         "calories_per_100g": 116, "protein_g": 9, "vitamin_d_mcg": 0,
         "iron_mg": 3.3, "halal": "Yes", "price_per_kg": 8},
        {"food_id": "F017", "food_name": "Roasted Mackerel",
         "calories_per_100g": 322, "protein_g": 20, "vitamin_d_mcg": 17.9,
         "iron_mg": 1.9, "halal": "Yes", "price_per_kg": 28},
        {"food_id": "F025", "food_name": "Fried Salmon",
         "calories_per_100g": 263, "protein_g": 19, "vitamin_d_mcg": 10.4,
         "iron_mg": 0.3, "halal": "Yes", "price_per_kg": 75},
        {"food_id": "F053", "food_name": "Boiled Peanuts",
         "calories_per_100g": 584, "protein_g": 26, "vitamin_d_mcg": 0,
         "iron_mg": 5.2, "halal": "Yes", "price_per_kg": 16},
    ])


def test_optimizer_returns_optimal(minimal_food_df):
    result = run_optimization(
        weekly_budget=500.0,
        nutrient_targets={"calories": 3000, "protein": 100,
                          "vitamin_d": 20, "iron": 20},
        food_df=minimal_food_df,
    )
    assert result["status"] == "Optimal"


def test_optimizer_plan_is_dataframe(minimal_food_df):
    result = run_optimization(
        weekly_budget=500.0,
        nutrient_targets={"calories": 3000, "protein": 100,
                          "vitamin_d": 20, "iron": 20},
        food_df=minimal_food_df,
    )
    assert isinstance(result["plan"], pd.DataFrame)
    assert "food_name" in result["plan"].columns
    assert "grams_per_week" in result["plan"].columns
    assert "cost_sar" in result["plan"].columns
    # Nutrient contributions per food item should be included.
    assert "calories" in result["plan"].columns
    assert "protein" in result["plan"].columns
    assert "vitamin_d" in result["plan"].columns
    assert "iron" in result["plan"].columns


def test_optimizer_cost_within_budget(minimal_food_df):
    budget = 500.0
    result = run_optimization(
        weekly_budget=budget,
        nutrient_targets={"calories": 3000, "protein": 100,
                          "vitamin_d": 20, "iron": 20},
        food_df=minimal_food_df,
    )
    assert result["total_cost_sar"] <= budget + 1e-3  # small tolerance for float


def test_optimizer_nutrient_targets_met(minimal_food_df):
    targets = {"calories": 3000, "protein": 100, "vitamin_d": 20, "iron": 20}
    result = run_optimization(
        weekly_budget=500.0,
        nutrient_targets=targets,
        food_df=minimal_food_df,
    )
    for nut, target in targets.items():
        assert result["nutrient_achieved"][nut] >= target * 0.99  # ≥99% of target


def test_optimizer_result_keys(minimal_food_df):
    result = run_optimization(
        weekly_budget=500.0,
        nutrient_targets={"calories": 3000},
        food_df=minimal_food_df,
    )
    for key in ["status", "total_cost_sar", "budget_sar",
                "nutrient_targets", "nutrient_achieved",
                "n_foods_selected", "plan"]:
        assert key in result
