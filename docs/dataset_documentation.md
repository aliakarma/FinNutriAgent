<<<<<<< HEAD
# Dataset Documentation — FinNutriAgent

Field-level schema, value ranges, and inter-dataset relationships.

**Repository**: [github.com/aliakarma/FinNutriAgent](https://github.com/aliakarma/FinNutriAgent)

---

## 1. Overview

| File | Location | Rows | Primary Key |
|------|----------|------|-------------|
| `financial_data.csv` | `data/financial/` | 100 | `user_id` |
| `food_composition.csv` | `data/composition/` | 350 | `food_id` |
| `food_prices.csv` | `data/prices/` | 350 | `food_id` |
| `nutrition_requirements.csv` | `data/nutrition/` | 500 | `person_id` |

**Key relationship**: `food_id` in `food_prices.csv` maps one-to-one to `food_id` in `food_composition.csv`.

---

## 2. financial_data.csv

**Purpose**: Encodes monthly household income and fixed expenditures. Used by the Budget Agent to derive the weekly food budget.

**Formula**: `weekly_food_budget = (monthly_income − rent − utilities − transport − education − healthcare − savings_target) / 4.33`

| Field | Type | Unit | Range | Description |
|-------|------|------|-------|-------------|
| `user_id` | string | — | U001–U100 | Unique household ID |
| `monthly_income` | integer | SAR | 5,100–14,900 | Total monthly income |
| `rent` | integer | SAR | 1,600–4,600 | Monthly rent or mortgage |
| `utilities` | integer | SAR | 400–1,150 | Electricity, water, internet |
| `transport` | integer | SAR | 550–1,700 | Fuel, transit, maintenance |
| `education` | integer | SAR | 500–2,600 | School, university fees |
| `healthcare` | integer | SAR | 200–700 | Insurance, medications |
| `savings_target` | integer | SAR | 1,850–4,350 | Monthly savings goal |

All residuals (income minus all expenses) are positive — no household has a negative food budget.

---

## 3. food_composition.csv

**Purpose**: Nutrient content per 100g and halal compliance for each food item. Used by the Optimization Engine.

| Field | Type | Unit | Range | Description |
|-------|------|------|-------|-------------|
| `food_id` | string | — | F001–F350 | Unique food ID |
| `food_name` | string | — | — | Name including preparation method and variant |
| `calories_per_100g` | float | kcal | 16–1,102 | Energy per 100g |
| `protein_g` | float | g | 0.1–39.7 | Protein per 100g |
| `vitamin_d_mcg` | float | mcg | 0–17.9 | Vitamin D per 100g |
| `iron_mg` | float | mg | 0–8.8 | Iron per 100g |
| `halal` | string | — | Yes / No | Halal compliance |

**Non-halal items**: pork products (sausage, bacon, ham, pork chop) and alcohol (wine, beer).  
**Food name conventions**: preparation prefix (Grilled, Boiled, Steamed, Fried, etc.) + variant suffix (Var N).

---

## 4. food_prices.csv

**Purpose**: Retail price per kg from three Saudi stores. Used by the Price Agent.

| Field | Type | Unit | Range | Description |
|-------|------|------|-------|-------------|
| `food_id` | string | — | F001–F350 | FK → food_composition.food_id |
| `store` | string | — | Carrefour, Lulu, Panda | Retail chain |
| `price_per_kg` | float | SAR | 5–95 | Price per kilogram |
| `date` | string | DD/MM/YYYY | 01/12/2025 | Price observation date |

Each food item appears once (one store per item). Average prices are used when merging.

---

## 5. nutrition_requirements.csv

**Purpose**: Individual daily nutritional requirements. Used by the Nutrition Agent to aggregate household targets.

| Field | Type | Unit | Range | Description |
|-------|------|------|-------|-------------|
| `person_id` | string | — | P1–P500 | Unique individual ID |
| `age` | integer | years | 1–90 | Age |
| `gender` | string | — | Male / Female | Biological sex |
| `calories_kcal` | integer | kcal/day | 725–2,760 | Daily caloric requirement |
| `protein_g` | integer | g/day | 12–64 | Daily protein requirement |
| `vitamin_d_mcg` | integer | mcg/day | 15 or 20 | 20 mcg/day for age ≥ 70; 15 otherwise |
| `iron_mg` | integer | mg/day | 7–18 | 18 mg/day for females aged 10–50; lower otherwise |

---

## 6. Inter-Dataset Relationships

```
financial_data.csv
    user_id → weekly food budget (SAR)
                         │
nutrition_requirements   │          food_prices.csv
    person_ids → weekly  │               food_id
    nutrient targets     │          price_per_kg
                         ▼               │
                   MILP Optimizer ◄──────┘
                         ▲
                         │
               food_composition.csv
                    food_id, nutrients, halal
```

---

## 7. Loading Example

```python
import pandas as pd

financial_df  = pd.read_csv("data/financial/financial_data.csv")
food_df       = pd.read_csv("data/composition/food_composition.csv",
                             skipinitialspace=True)
prices_df     = pd.read_csv("data/prices/food_prices.csv",
                             skipinitialspace=True)
nutrition_df  = pd.read_csv("data/nutrition/nutrition_requirements.csv")

# Strip whitespace (food_composition and food_prices have leading spaces)
for df in [food_df, prices_df]:
    df.columns   = df.columns.str.strip()
    df["food_id"] = df["food_id"].str.strip()
food_df["halal"] = food_df["halal"].str.strip()
```

---

## 8. Validation

```bash
python scripts/validate_data.py
```

Checks: row counts, missing values, food_id key consistency, numeric ranges, categorical field values, budget feasibility.
=======
# Dataset Documentation for FinAgent

This document provides detailed descriptions of all datasets used in the FinAgent system. These datasets support nutritional optimization, household budgeting, and price-sensitive dietary planning.

---

## 1. Overview of Datasets

The repository contains four primary datasets stored in CSV format:

1. **financial_data.csv**  
2. **food_composition.csv**  
3. **food_prices.csv**  
4. **nutrition_requirements.csv**

The datasets are synthetic but constructed to reflect realistic conditions in Saudi Arabia, including common food items, typical household incomes, and nutrient requirements based on established guidelines.

All files follow tabular, machine-readable formatting and are designed for reproducibility.

---

## 2. Dataset Descriptions

### **2.1 financial_data.csv**

| Attribute | Description |
|----------|-------------|
| `user_id` | Unique household identifier |
| `monthly_income` | Monthly income in SAR |
| `rent` | Monthly rent cost |
| `utilities` | Electricity, water, and other utilities |
| `transport` | Transportation cost |
| `education` | School or university expenses |
| `healthcare` | Monthly healthcare expenses |
| `savings_target` | Target amount to save per month |

**Rows:** 101  
**Columns:** 8  
**Purpose:** Computes available food budget per household.  
**Source:** Synthetic data based on Saudi household statistics.

---

### **2.2 food_composition.csv**

| Attribute | Description |
|----------|-------------|
| `food_id` | Unique food item identifier |
| `food_name` | Name of food item |
| `calories_per_100g` | Energy per 100 grams |
| `protein_g` | Protein content (grams) |
| `vitamin_d_mcg` | Vitamin D content (micrograms) |
| `iron_mg` | Iron content (milligrams) |
| `halal` | Halal compliance (Yes/No) |

**Rows:** 351  
**Columns:** 7  
**Purpose:** Provides nutrient data for dietary optimization.  
**Source:** Partially synthetic; values based on USDA, SFDA (Saudi Food & Drug Authority), and regional food products.

---

### **2.3 food_prices.csv**

| Attribute | Description |
|----------|-------------|
| `food_id` | ID linked to food_composition |
| `store` | Store name (e.g., Carrefour, Lulu, Danube) |
| `price_per_kg` | Current price per kilogram |
| `date` | Price timestamp |

**Rows:** 351  
**Columns:** 4  
**Purpose:** Real-time price integration and price-shock simulation.  
**Source:** Synthetic but reflects realistic Saudi market pricing.

---

### **2.4 nutrition_requirements.csv**

| Attribute | Description |
|----------|-------------|
| `person_id` | Unique person identifier |
| `age` | Age in years |
| `gender` | Male/Female |
| `calories_kcal` | Daily calorie requirement |
| `protein_g` | Protein requirement |
| `vitamin_d_mcg` | Vitamin D requirement |
| `iron_mg` | Iron requirement |

**Rows:** 501  
**Columns:** 7  
**Purpose:** Sets nutritional targets for household members.  
**Source:** Derived from WHO and Saudi dietary guidelines (synthetically sampled).

---

## 3. Data Quality and Validation

- No missing values  
- All numeric fields validated for realistic ranges  
- food_prices rows align one-to-one with food_composition  
- Normalized field names support reproducibility and programmatic loading  

---

## 4. Licensing

The datasets are released under **CC BY 4.0**, allowing reuse with proper attribution.

---

## 5. Ethical Considerations

- All datasets are **synthetic**—no personal or identifiable real-world data is included.  
- Financial and nutritional profiles do **not** represent any specific individuals.  
- Food and nutrient information reflect publicly documented averages.  

---

## 6. Citation

If you use this dataset, please cite the associated research paper or this repository.
>>>>>>> f9098430481c9bbf225fbfb7aeaa02acf3cea53f
