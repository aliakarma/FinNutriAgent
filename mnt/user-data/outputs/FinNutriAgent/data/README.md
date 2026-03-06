# FinNutriAgent Datasets

All datasets are synthetic and do not contain real personal information. They are constructed to reflect realistic conditions in Saudi Arabia. Full documentation is in [`../docs/dataset_documentation.md`](../docs/dataset_documentation.md).

## Files

| File | Rows | Columns | Description |
|------|------|---------|-------------|
| `financial/financial_data.csv` | 100 | 8 | Household income, expenses, savings targets |
| `composition/food_composition.csv` | 350 | 7 | Nutrients + halal compliance per food item |
| `prices/food_prices.csv` | 350 | 4 | Price per kg at Carrefour, Lulu, Panda |
| `nutrition/nutrition_requirements.csv` | 500 | 7 | Daily nutritional requirements per individual |

## Key Relationship

`food_id` in `food_prices.csv` maps one-to-one with `food_id` in `food_composition.csv`.

## License

CC BY 4.0 — See [`../LICENSE`](../LICENSE)
