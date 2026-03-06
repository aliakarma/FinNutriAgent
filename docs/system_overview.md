<<<<<<< HEAD
# System Overview — FinNutriAgent

**Repository**: [github.com/aliakarma/FinNutriAgent](https://github.com/aliakarma/FinNutriAgent)  
**Author**: Ali Akarma — ORCID [0009-0002-6687-9380](https://orcid.org/0009-0002-6687-9380)

---

## 1. Problem Formulation

Given a household with fixed income and expenses, a set of members with individual nutritional needs, and a catalog of foods with nutrients and prices, FinNutriAgent solves:

**Minimize** weekly food cost subject to nutritional requirements, budget, and dietary constraints.

### MILP Formulation

```
Minimize:    Σ_f  cost_f · x_f  −  ε · Σ_f y_f

Subject to:
  Σ_f  (nutrient_{f,n} / 100) · x_f  ≥  target_n       ∀ nutrient n ∈ {calories, protein, vitamin_d, iron}
  Σ_f  cost_f · x_f                  ≤  weekly_budget
  min_g · y_f                        ≤  x_f              ∀ food f
  x_f                                ≤  max_g · y_f      ∀ food f
  x_f ≥ 0,   y_f ∈ {0, 1}
```

Variables: `x_f` (grams/week of food f), `y_f` (binary selection indicator).  
Diversity term `ε · Σ y_f` encourages food variety at negligible cost impact.

---

## 2. Module Descriptions

### Budget Agent (`scripts/budget_agent.py`)

- **Input**: `data/financial/financial_data.csv`
- **Output**: Weekly food budget in SAR
- **Formula**: `weekly_budget = (income − Σ expenses) / 4.33`

### Nutrition Agent (`scripts/nutrition_agent.py`)

- **Input**: `data/nutrition/nutrition_requirements.csv`
- **Output**: Aggregated household daily and weekly nutritional targets
- **Method**: Sum individual requirements across household members; multiply daily totals × 7

### Price Agent (`scripts/price_agent.py`)

- **Input**: `data/prices/food_prices.csv`
- **Output**: Cost per gram per food item; volatility alerts
- **Method**: Average prices across stores; flags items with > 15% change from baseline

### Optimization Engine (`scripts/optimizer.py`)

- **Input**: Merged food+price data, budget, nutrient targets, halal filter
- **Output**: Optimal weekly meal plan with quantities and costs
- **Solver**: PuLP / CBC (exact MILP, deterministic)
- **Parameters** (configurable in `config/config.yaml`): min_grams=50, max_grams=500, ε=0.01

### LLM Orchestrator (research extension)

- Translates gram quantities into meal slots and shopping lists
- Provides natural-language nutritional summaries
- Coordinates re-planning when Price Agent detects volatility

---

## 3. Data Flow

```
financial_data.csv ──→ Budget Agent ──→ weekly_budget ──────────────┐
                                                                      │
nutrition_requirements.csv ──→ Nutrition Agent ──→ nutrient_targets  │
                                                                      ▼
food_composition.csv ──────────────────────────→ MILP Optimizer ◄────┘
food_prices.csv ────────────────────────────────→ (via Price Agent)
                                                        │
                                                        ▼
                                                 Weekly Meal Plan
                                                        │
                                                        ▼
                                               LLM Orchestrator
                                                        │
                                                        ▼
                                            User-facing explanation
```

---

## 4. Configuration

All parameters are centralized in `config/config.yaml`:

```yaml
optimizer:
  min_grams: 50
  max_grams: 500
  diversity_epsilon: 0.01
  halal_only: true

price_agent:
  volatility_threshold: 0.15

budget:
  weeks_per_month: 4.33
```

---

## 5. Performance

| Metric | Value |
|---|---|
| Food decision variables | 350 (310 halal) |
| Binary selection variables | 350 |
| Nutritional constraints | 4 |
| Solver | PuLP / CBC |
| Typical solve time | < 1 second |
| Optimality guarantee | Exact (MILP) |
| Feasibility across 100 households | 100% |

---

## 6. Extending the System

**Add new foods**: append rows to `data/composition/food_composition.csv` and `data/prices/food_prices.csv`, then run `python scripts/validate_data.py`.

**Add new nutrients**: add columns to both `food_composition.csv` and `nutrition_requirements.csv`, update `NUTRIENT_COLS` in `scripts/optimizer.py`, and add the new target to `nutrient_targets`.

**Add new households**: append rows to `data/financial/financial_data.csv`.

---

## 7. Reproducibility

All components are deterministic. The CBC solver produces identical results given identical inputs. All datasets are versioned on Zenodo (DOI: [10.5281/zenodo.18849993](https://doi.org/10.5281/zenodo.18849993)). The demo notebook `example/demo_finagent.ipynb` includes all expected outputs for reference.
=======
# System Overview: FinAgent

FinAgent is an agentic AI system that integrates financial modeling, price monitoring, and nutritional optimization to generate affordable and culturally appropriate weekly meal plans.

---

## 1. System Architecture

FinAgent consists of five main modules:

### **1. Budget Agent**
- Computes weekly food budget  
- Uses financial_data.csv  
- Handles savings and fixed expenses  

### **2. Nutrition Agent**
- Reads nutrient requirements from nutrition_requirements.csv  
- Calculates household-level combined targets  
- Ensures age- and gender-appropriate coverage  

### **3. Price Agent**
- Loads current prices from food_prices.csv  
- Detects price volatility  
- Triggers re-planning when changes exceed thresholds  

### **4. Optimization Engine**
- Mathematical optimization using PuLP / OR-Tools  
- Minimizes weekly food cost  
- Satisfies nutritional constraints  
- Enforces halal and cultural constraints  

### **5. LLM Orchestrator**
- Provides reasoning and explanations  
- Coordinates agents  
- Produces user-facing meal plans  

---

## 2. Data Flow
- financial_data → Budget Agent → weekly budget
- nutrition_requirements → Nutrition Agent → nutrient targets
- food_composition → Optimizer → feasible food options
- food_prices → Price Agent → triggers re-planning
- LLM → integrates all outputs → final meal plan


---

## 3. Reproducibility Notes

- All datasets are static and included in the repository  
- Scripts in /scripts load and validate datasets  
- Optimizer uses deterministic processes  

---

## 4. Deployment Notes

FinAgent can run locally or on cloud environments using:

- Python 3.10+
- Pandas, OR-Tools, PuLP
- Optional: lightweight FastAPI frontend
>>>>>>> f9098430481c9bbf225fbfb7aeaa02acf3cea53f
