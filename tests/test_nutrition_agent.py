"""Tests for NutritionAgent."""

import pytest
import pandas as pd
from scripts.nutrition_agent import NutritionAgent, NUTRIENT_COLS


@pytest.fixture
def sample_csv(tmp_path):
    data = pd.DataFrame([
        {"person_id": "P1", "age": 40, "gender": "Male",
         "calories_kcal": 2500, "protein_g": 56, "vitamin_d_mcg": 15, "iron_mg": 8},
        {"person_id": "P2", "age": 36, "gender": "Female",
         "calories_kcal": 2000, "protein_g": 46, "vitamin_d_mcg": 15, "iron_mg": 18},
        {"person_id": "P3", "age": 10, "gender": "Male",
         "calories_kcal": 1800, "protein_g": 34, "vitamin_d_mcg": 15, "iron_mg": 8},
    ])
    p = tmp_path / "nutrition.csv"
    data.to_csv(p, index=False)
    return str(p)


def test_individual_requirements(sample_csv):
    agent = NutritionAgent(filepath=sample_csv)
    req = agent.get_individual_requirements("P1")
    assert req["age"] == 40
    assert req["gender"] == "Male"
    assert req["calories_kcal"] == 2500.0


def test_invalid_person_raises(sample_csv):
    agent = NutritionAgent(filepath=sample_csv)
    with pytest.raises(ValueError, match="not found"):
        agent.get_individual_requirements("P999")


def test_household_daily_targets_sum(sample_csv):
    agent = NutritionAgent(filepath=sample_csv)
    targets = agent.get_household_daily_targets(["P1", "P2"])
    assert targets["calories_kcal"] == pytest.approx(4500.0)
    assert targets["protein_g"] == pytest.approx(102.0)


def test_weekly_targets_multiply_by_7(sample_csv):
    agent = NutritionAgent(filepath=sample_csv)
    daily  = agent.get_household_daily_targets(["P1"])
    weekly = agent.get_household_weekly_targets(["P1"])
    assert weekly["calories"] == pytest.approx(daily["calories_kcal"] * 7, rel=1e-3)
    assert weekly["protein"]  == pytest.approx(daily["protein_g"] * 7, rel=1e-3)


def test_describe_household_rows(sample_csv):
    agent = NutritionAgent(filepath=sample_csv)
    df = agent.describe_household(["P1", "P3"])
    assert len(df) == 2


def test_missing_member_raises(sample_csv):
    agent = NutritionAgent(filepath=sample_csv)
    with pytest.raises(ValueError):
        agent.get_household_weekly_targets(["P1", "P999"])
