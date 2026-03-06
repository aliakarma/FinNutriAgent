# FinNutriAgent: Agentic AI for Household Nutrition and Budget Optimization

[![DOI](https://zenodo.org/badge/1115326129.svg)](https://doi.org/10.5281/zenodo.18849993)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## Abstract

**FinNutriAgent** is an open agentic AI framework that jointly optimizes household meal planning and financial budgets under nutritional, cultural, and economic constraints. It combines Mixed-Integer Linear Programming (MILP), multi-agent reasoning, and large language model (LLM) orchestration to produce weekly meal plans that are cost-effective, nutritionally complete, and halal-compliant. The system is evaluated on a synthetic dataset reflecting realistic conditions in Saudi Arabia, covering 100 households, 500 individuals, and 350 food items with market prices from three major retail chains.

This repository accompanies the research paper:

> **Ali Akarma**, "FinNutriAgent: Agentic AI for Household Nutrition and Budgeting," 2025.  
> DOI: [10.5281/zenodo.18849993](https://doi.org/10.5281/zenodo.18849993)

---

## Key Features

- **Budget-aware planning** — derives weekly food budgets from household financial profiles
- **Demographic nutrition modeling** — aggregates per-person requirements (age, gender, WHO guidelines)
- **Multi-store price tracking** — monitors prices across Carrefour, Lulu, and Panda
- **MILP optimization** — guarantees cost-minimal, nutritionally complete meal plans
- **Halal compliance** — filters food selections to Islamic dietary law
- **Dietary diversity** — binary selection variables enforce food variety
- **Price shock resilience** — triggers re-optimization when market prices shift beyond threshold
- **Reproducible** — fully deterministic pipeline, all data versioned on Zenodo

---

## Repository Structure

```
FinNutriAgent/
├── README.md                         # This file
├── LICENSE                           # CC BY 4.0
├── requirements.txt                  # Python package dependencies
├── environment.yml                   # Conda environment specification
├── CITATION.cff                      # Machine-readable citation
├── CONTRIBUTING.md                   # Contribution guidelines
├── RESULTS.md                        # Summary of key experimental results
├── .gitignore
│
├── config/
│   └── config.yaml                   # Centralized configuration (paths, solver params)
│
├── data/
│   ├── README.md                     # Dataset overview
│   ├── financial/
│   │   └── financial_data.csv        # 100 household financial profiles
│   ├── composition/
│   │   └── food_composition.csv      # 350 food items: nutrients + halal label
│   ├── prices/
│   │   └── food_prices.csv           # Per-item prices across 3 stores
│   └── nutrition/
│       └── nutrition_requirements.csv # 500 individual nutritional profiles
│
├── docs/
│   ├── data_card.md                  # Datasheet for Datasets (Gebru et al., 2021)
│   ├── dataset_documentation.md      # Field-level schema and relationships
│   └── system_overview.md            # Architecture, MILP formulation, data flow
│
├── scripts/
│   ├── __init__.py
│   ├── budget_agent.py               # Household food budget computation
│   ├── nutrition_agent.py            # Nutritional target aggregation
│   ├── price_agent.py                # Price loading and volatility detection
│   ├── optimizer.py                  # MILP optimization engine (PuLP/CBC)
│   └── validate_data.py              # Data integrity validation
│
├── tests/
│   ├── test_budget_agent.py
│   ├── test_nutrition_agent.py
│   ├── test_price_agent.py
│   └── test_optimizer.py
│
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions CI pipeline
│
└── example/
    └── demo_finagent.ipynb           # Full reproducible demo (Colab-ready)
```

---

## Datasets

| Dataset | Rows | Columns | Primary Key | Description |
|---|---|---|---|---|
| `financial_data.csv` | 100 | 8 | `user_id` | Household income, fixed expenses, savings targets |
| `food_composition.csv` | 350 | 7 | `food_id` | Nutrient content + halal compliance per food item |
| `food_prices.csv` | 350 | 4 | `food_id` | Price per kg across Carrefour, Lulu, Panda |
| `nutrition_requirements.csv` | 500 | 7 | `person_id` | Per-person daily nutritional requirements |

Full documentation: [`docs/dataset_documentation.md`](docs/dataset_documentation.md)  
Dataset card: [`docs/data_card.md`](docs/data_card.md)

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      LLM Orchestrator                        │
│          (Coordinates agents · Generates explanations)       │
└────────┬─────────────────┬──────────────────┬───────────────┘
         │                 │                  │
   ┌─────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
   │   Budget   │   │  Nutrition  │   │    Price    │
   │   Agent    │   │    Agent    │   │    Agent    │
   │            │   │             │   │             │
   │ financial  │   │ nutrition_  │   │ food_prices │
   │ _data.csv  │   │ req.csv     │   │ .csv        │
   └─────┬──────┘   └──────┬──────┘   └──────┬──────┘
         │                 │                  │
         └─────────────────▼──────────────────┘
                    ┌───────────────┐
                    │  MILP Engine  │
                    │   (PuLP/CBC)  │
                    │               │
                    │ food_         │
                    │ composition   │
                    └───────┬───────┘
                            │
                    ┌───────▼───────┐
                    │  Weekly Meal  │
                    │     Plan      │
                    └───────────────┘
```

---

## MILP Problem Formulation

```
Minimize:    Σ_f  cost_f · x_f  −  ε · Σ_f y_f

Subject to:
  Σ_f  (nutrient_{f,n} / 100) · x_f  ≥  target_n     ∀ nutrient n
  Σ_f  cost_f · x_f                  ≤  weekly_budget
  min_g · y_f  ≤  x_f  ≤  max_g · y_f                ∀ food f
  x_f ≥ 0,   y_f ∈ {0, 1}
```

Where `x_f` (grams/week) is the quantity of food `f`, `y_f` is a binary selection indicator, and `ε` is a small diversity incentive weight.

---

## Quick Start

### Option A — Google Colab (Recommended)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aliakarma/FinNutriAgent/blob/main/example/demo_finagent.ipynb)

### Option B — Local Setup (pip)

```bash
git clone https://github.com/aliakarma/FinNutriAgent.git
cd FinNutriAgent
pip install -e .
# For fully reproducible installs, use the pinned lockfile:
pip install -r requirements.lock.txt
```

### Option C — Local Setup (Conda)

```bash
git clone https://github.com/aliakarma/FinNutriAgent.git
cd FinNutriAgent
conda env create -f environment.yml
conda activate finnutriagent
```

### Run the Demo Notebook

```bash
jupyter notebook example/demo_finagent.ipynb
```

### Validate Data Integrity

```bash
python scripts/validate_data.py
```

### Run the Optimizer

```python
from scripts.optimizer import run_optimization

result = run_optimization(
    weekly_budget=912.50,
    nutrient_targets={"calories": 6696, "protein": 158, "vitamin_d": 60, "iron": 44},
    halal_only=True,
)
print(result["status"])          # Optimal
print(result["total_cost_sar"])  # e.g., 24.73
print(result["plan"])            # DataFrame of recommended foods
```

### Run Tests

```bash
pytest tests/ -v
```

---

## Reproducible Results (Recommended)

To regenerate the core tables and figures from the paper, run the reproducibility script.

```bash
python scripts/reproduce_results.py
```

This produces `results/summary.csv`, `results/summary_stats.json`, and a sample output for household `U017`.

---

## Results Summary

Key results from the paper are summarized in [`RESULTS.md`](RESULTS.md). The optimizer consistently finds feasible, cost-minimal halal meal plans across all 100 households, using only 3–7% of the available weekly food budget to satisfy all four nutritional constraints. Full results are reproducible via `example/demo_finagent.ipynb`.

---




---

## License

| Component | License |
|---|---|
| Code (`scripts/`, `tests/`, `example/`) | [MIT License](LICENSE) |
| Datasets (`data/`) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| Documentation (`docs/`) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

---

## Contributing

Contributions are welcome. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before submitting a pull request.

---

## Contact

**Ali Akarma**  
ORCID: [0009-0002-6687-9380](https://orcid.org/0009-0002-6687-9380)  
GitHub: [@aliakarma](https://github.com/aliakarma)  
Issues: [github.com/aliakarma/FinNutriAgent/issues](https://github.com/aliakarma/FinNutriAgent/issues)
