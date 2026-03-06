"""Tests for PriceAgent."""

import pytest
import pandas as pd
from scripts.price_agent import PriceAgent


@pytest.fixture
def sample_csv(tmp_path):
    data = pd.DataFrame([
        {"food_id": "F001", "store": "Carrefour", "price_per_kg": 25.0, "date": "01/12/2025"},
        {"food_id": "F002", "store": "Lulu",      "price_per_kg": 8.0,  "date": "01/12/2025"},
        {"food_id": "F003", "store": "Panda",     "price_per_kg": 32.5, "date": "01/12/2025"},
    ])
    p = tmp_path / "food_prices.csv"
    data.to_csv(p, index=False)
    return str(p)


def test_cost_per_gram_values(sample_csv):
    agent = PriceAgent(filepath=sample_csv)
    costs = agent.get_cost_per_gram()
    assert costs["F001"] == pytest.approx(0.025)
    assert costs["F002"] == pytest.approx(0.008)


def test_price_shock_increases_price(sample_csv):
    agent = PriceAgent(filepath=sample_csv)
    agent.simulate_price_shock(["F001"], shock_pct=0.20)
    costs = agent.get_cost_per_gram()
    assert costs["F001"] == pytest.approx(0.025 * 1.20, rel=1e-4)


def test_reset_restores_baseline(sample_csv):
    agent = PriceAgent(filepath=sample_csv)
    agent.simulate_price_shock(["F001"], shock_pct=0.50)
    agent.reset_prices()
    costs = agent.get_cost_per_gram()
    assert costs["F001"] == pytest.approx(0.025)


def test_volatility_detected_after_shock(sample_csv):
    agent = PriceAgent(filepath=sample_csv, volatility_threshold=0.10)
    agent.simulate_price_shock(["F001"], shock_pct=0.20)
    volatile = agent.detect_volatility()
    ids = [v["food_id"] for v in volatile]
    assert "F001" in ids


def test_no_volatility_before_shock(sample_csv):
    agent = PriceAgent(filepath=sample_csv)
    assert agent.detect_volatility() == []


def test_global_shock(sample_csv):
    agent = PriceAgent(filepath=sample_csv)
    affected = agent.simulate_price_shock([], shock_pct=0.10)
    assert len(affected) == 3  # all items
