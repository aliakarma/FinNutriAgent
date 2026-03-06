"""
price_agent.py
--------------
Loads food price data, computes per-gram costs, and detects price volatility.

Example
-------
>>> from scripts.price_agent import PriceAgent
>>> agent = PriceAgent()
>>> agent.simulate_price_shock(["F001", "F015"], shock_pct=0.20)
>>> agent.detect_volatility()
"""

import os
import yaml
import pandas as pd
import numpy as np
from typing import Optional

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CFG_PATH = os.path.join(_ROOT, "config", "config.yaml")


def _load_config() -> dict:
    with open(_CFG_PATH, "r") as f:
        return yaml.safe_load(f)


class PriceAgent:
    """
    Manages food price data and detects price shocks.

    Parameters
    ----------
    filepath : str, optional
        Path to food_prices.csv.
    volatility_threshold : float, optional
        Fractional price change that triggers a volatility alert. Default: 0.15.
    """

    def __init__(self, filepath: Optional[str] = None,
                 volatility_threshold: Optional[float] = None):
        cfg = _load_config()
        if filepath is None:
            filepath = os.path.join(_ROOT, cfg["data"]["prices"])
        self.volatility_threshold = (
            volatility_threshold or cfg["price_agent"]["volatility_threshold"]
        )
        self.df = pd.read_csv(filepath, skipinitialspace=True)
        self.df.columns = self.df.columns.str.strip()
        self.df["food_id"] = self.df["food_id"].str.strip()
        self._base_prices    = self.df.groupby("food_id")["price_per_kg"].mean().to_dict()
        self._current_prices = dict(self._base_prices)

    # ── Core accessors ────────────────────────────────────────────────────────

    def get_cost_per_gram(self) -> dict:
        """Return {food_id: SAR per gram} using current prices."""
        return {fid: p / 1000.0 for fid, p in self._current_prices.items()}

    def get_price_dataframe(self) -> pd.DataFrame:
        """Return a DataFrame of current prices with cost_per_gram column."""
        records = [
            {"food_id": fid, "price_per_kg": p, "cost_per_gram": p / 1000.0}
            for fid, p in self._current_prices.items()
        ]
        return pd.DataFrame(records)

    # ── Shock simulation ──────────────────────────────────────────────────────

    def simulate_price_shock(self, food_ids: list, shock_pct: float) -> dict:
        """
        Simulate a price shock on specified foods.

        Parameters
        ----------
        food_ids : list of str   (empty list = apply to all foods)
        shock_pct : float        fractional increase (e.g. 0.20 = +20%)

        Returns
        -------
        dict  {food_id: new_price_per_kg}
        """
        targets = food_ids if food_ids else list(self._current_prices.keys())
        affected = {}
        for fid in targets:
            if fid in self._current_prices:
                self._current_prices[fid] = self._base_prices[fid] * (1 + shock_pct)
                affected[fid] = round(self._current_prices[fid], 4)
        return affected

    def reset_prices(self) -> None:
        """Reset all prices to baseline values."""
        self._current_prices = dict(self._base_prices)

    # ── Volatility detection ─────────────────────────────────────────────────

    def detect_volatility(self) -> list:
        """
        Return list of food items whose price changed beyond the threshold.

        Returns
        -------
        list of dict — food_id, base_price, current_price, change_pct
        """
        volatile = []
        for fid, base in self._base_prices.items():
            current = self._current_prices.get(fid, base)
            if base > 0 and abs(current - base) / base > self.volatility_threshold:
                volatile.append({
                    "food_id": fid,
                    "base_price_sar_kg":    round(base, 2),
                    "current_price_sar_kg": round(current, 2),
                    "change_pct":           round(abs(current - base) / base * 100, 1),
                })
        return volatile

    # ── Analysis ──────────────────────────────────────────────────────────────

    def cheapest_per_nutrient(self, food_df: pd.DataFrame, nutrient: str,
                               halal_only: bool = True, top_n: int = 10) -> pd.DataFrame:
        """
        Rank foods by cost-efficiency for a given nutrient.

        Parameters
        ----------
        food_df   : pd.DataFrame  food composition data
        nutrient  : str           column name (e.g. 'protein_g', 'iron_mg')
        halal_only: bool
        top_n     : int

        Returns
        -------
        pd.DataFrame sorted by cost per unit of nutrient
        """
        df = food_df.copy()
        df["food_id"] = df["food_id"].str.strip()
        if halal_only:
            df = df[df["halal"].str.strip() == "Yes"]
        costs = self.get_cost_per_gram()
        df["cost_per_gram"] = df["food_id"].map(costs)
        df = df.dropna(subset=["cost_per_gram"])
        col_key = f"cost_per_g_{nutrient}"
        df[col_key] = df.apply(
            lambda r: r["cost_per_gram"] / (r[nutrient] / 100.0)
            if r[nutrient] > 0 else np.inf,
            axis=1,
        )
        return (df[["food_id", "food_name", nutrient, "cost_per_gram", col_key]]
                .sort_values(col_key)
                .head(top_n)
                .reset_index(drop=True))


if __name__ == "__main__":
    agent = PriceAgent()
    costs = agent.get_cost_per_gram()
    print(f"Loaded {len(costs)} food prices.")
    print(f"Price range: {min(costs.values()):.5f} – {max(costs.values()):.5f} SAR/g")
    agent.simulate_price_shock(["F001", "F015", "F025"], shock_pct=0.20)
    volatile = agent.detect_volatility()
    print(f"Volatile items after shock: {len(volatile)}")
    for v in volatile:
        print(f"  {v['food_id']}: {v['base_price_sar_kg']} → "
              f"{v['current_price_sar_kg']} SAR/kg (+{v['change_pct']}%)")
