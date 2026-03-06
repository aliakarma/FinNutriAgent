<div align="center">

<!-- LOGO / BANNER -->
<img src="https://raw.githubusercontent.com/aliakarma/FinNutriAgent/main/docs/assets/banner.png" alt="FinNutriAgent Banner" width="100%" onerror="this.style.display='none'"/>

<h1>
  💰 FinNutriAgent 🥗
</h1>

<h3><em>Agentic AI for Household Nutrition and Budget Optimization</em></h3>

<br/>

<!-- BADGES ROW 1 — Identity & Citation -->
[![DOI](https://zenodo.org/badge/1115326129.svg)](https://doi.org/10.5281/zenodo.18849993)
[![License: MIT](https://img.shields.io/badge/Code-MIT-green.svg)](LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/Data%20%26%20Docs-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0002--6687--9380-a6ce39?logo=orcid&logoColor=white)](https://orcid.org/0009-0002-6687-9380)

<!-- BADGES ROW 2 — Tech Stack -->
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![PuLP](https://img.shields.io/badge/Optimizer-PuLP%2FCBC-orange)](https://coin-or.github.io/pulp/)
[![LLM Powered](https://img.shields.io/badge/LLM-Orchestrated-blueviolet?logo=openai&logoColor=white)](#system-architecture)
[![MILP](https://img.shields.io/badge/Method-MILP-blue)](#milp-problem-formulation)

<!-- BADGES ROW 3 — Quality & CI -->
[![CI](https://img.shields.io/github/actions/workflow/status/aliakarma/FinNutriAgent/ci.yml?label=CI&logo=github)](https://github.com/aliakarma/FinNutriAgent/actions)
[![Tests](https://img.shields.io/badge/Tests-pytest-yellow?logo=pytest&logoColor=white)](tests/)
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP8-black)](https://peps.python.org/pep-0008/)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](CONTRIBUTING.md)

<br/>

<!-- CTA BUTTONS -->
<a href="https://colab.research.google.com/github/aliakarma/FinNutriAgent/blob/main/example/demo_finagent.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" height="28"/>
</a>
&nbsp;
<a href="https://doi.org/10.5281/zenodo.18849993">
  <img src="https://img.shields.io/badge/Paper-Zenodo-blue?style=for-the-badge&logo=zenodo&logoColor=white" alt="Paper" height="28"/>
</a>
&nbsp;
<a href="docs/system_overview.md">
  <img src="https://img.shields.io/badge/Docs-Read%20More-informational?style=for-the-badge&logo=readthedocs&logoColor=white" alt="Docs" height="28"/>
</a>
&nbsp;
<a href="https://github.com/aliakarma/FinNutriAgent/issues">
  <img src="https://img.shields.io/badge/Issues-Report%20a%20Bug-red?style=for-the-badge&logo=github&logoColor=white" alt="Issues" height="28"/>
</a>

<br/><br/>

</div>

---

## 📋 Table of Contents

- [Abstract](#-abstract)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [MILP Formulation](#-milp-problem-formulation)
- [Datasets](#-datasets)
- [Quick Start](#-quick-start)
- [Results](#-results-summary)
- [Repository Structure](#-repository-structure)
- [Citation](#-citation)
- [License](#-license)
- [Contributing](#-contributing)
- [Contact](#-contact)

---

## 🔬 Abstract

**FinNutriAgent** is an open agentic AI framework that **jointly optimizes household meal planning and financial budgets** under nutritional, cultural, and economic constraints. It combines:

- 🔢 **Mixed-Integer Linear Programming (MILP)** for provably optimal solutions  
- 🤝 **Multi-agent reasoning** across budget, nutrition, and pricing domains  
- 🧠 **LLM orchestration** for natural-language explanations and coordination  

The system is evaluated on a **synthetic dataset** reflecting realistic conditions in **Saudi Arabia**, covering **100 households**, **500 individuals**, and **350 food items** with market prices from three major retail chains.

> **Ali Akarma**, *"FinNutriAgent: Agentic AI for Household Nutrition and Budgeting"*, 2025.  
> 📄 DOI: [10.5281/zenodo.18849993](https://doi.org/10.5281/zenodo.18849993)

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 💸 **Budget-aware planning** | Derives weekly food budgets from household financial profiles |
| 👨‍👩‍👧‍👦 **Demographic nutrition modeling** | Aggregates per-person requirements (age, gender, WHO guidelines) |
| 🏪 **Multi-store price tracking** | Monitors prices across Carrefour, Lulu, and Panda |
| ⚙️ **MILP optimization** | Guarantees cost-minimal, nutritionally complete meal plans |
| ☪️ **Halal compliance** | Filters food selections to Islamic dietary law |
| 🥦 **Dietary diversity** | Binary selection variables enforce food variety |
| 📈 **Price shock resilience** | Triggers re-optimization when market prices shift beyond threshold |
| 🔁 **Reproducible pipeline** | Fully deterministic, all data versioned on Zenodo |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      LLM Orchestrator                       │
│          (Coordinates agents · Generates explanations)      │
└────────┬─────────────────┬──────────────────┬───────────────┘
         │                 │                  │
   ┌─────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
   │   Budget   │   │  Nutrition  │   │    Price    │
   │   Agent    │   │    Agent    │   │    Agent    │
   │            │   │             │   │             │
   │ financial  │   │ nutrition_  │   │ food_prices │
   │ _data.csv  │   │ req.csv     │   │ .csv        │
   └─────┬──────┘   └──────┬──────┘   └──────┬──────┘
         │                 │                 │
         └─────────────────▼─────────────────┘
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

Three specialized agents feed into a central MILP engine, coordinated by an LLM orchestrator that synthesizes constraints and generates human-readable meal plan explanations.

---

## 📐 MILP Problem Formulation

The optimizer minimizes total weekly food cost while incentivizing dietary diversity:

**Objective Function**

$$\min_{x_f,\, y_f} \sum_{f} c_f \cdot x_f \;-\; \varepsilon \sum_{f} y_f$$

**Subject to**

$$\sum_{f} \frac{n_{f,k}}{100} \cdot x_f \;\geq\; T_k \qquad \forall \text{ nutrient } k$$

$$\sum_{f} c_f \cdot x_f \;\leq\; B_{\text{weekly}}$$

$$\sum_{f} y_f \;\geq\; F_{\min}$$

$$g_{\min} \cdot y_f \;\leq\; x_f \;\leq\; g_{\max} \cdot y_f \qquad \forall f$$

$$x_f \geq 0, \quad y_f \in \{0, 1\} \qquad \forall f$$

**Variables & Parameters**

| Symbol | Type | Description |
|:---:|:---:|---|
| $x_f$ | Continuous | Grams of food $f$ per week |
| $y_f$ | Binary | 1 if food $f$ is selected, 0 otherwise |
| $c_f$ | Parameter | Cost per gram of food $f$ (SAR) |
| $T_k$ | Parameter | Minimum weekly requirement for nutrient $k$ |
| $B_{\text{weekly}}$ | Parameter | Household weekly food budget (SAR) |
| $\varepsilon$ | Parameter | Diversity incentive weight |
| $g_{\min},\, g_{\max}$ | Parameter | Minimum/maximum serving bounds (grams) |

---

## 📊 Datasets

| Dataset | Rows | Key Columns | Description |
|---|---|---|---|
| [`financial_data.csv`](data/financial/) | 100 | `user_id`, income, fixed expenses, savings targets | Household financial profiles |
| [`food_composition.csv`](data/composition/) | 350 | `food_id`, nutrients, `halal` flag | Nutrient content per food item |
| [`food_prices.csv`](data/prices/) | 350 | `food_id`, Carrefour, Lulu, Panda prices | Per-item prices across 3 stores |
| [`nutrition_requirements.csv`](data/nutrition/) | 500 | `person_id`, age, gender, daily targets | Per-person nutritional requirements |

> 📖 Full schema documentation: [`docs/dataset_documentation.md`](docs/dataset_documentation.md)  
> 📋 Dataset card (Gebru et al., 2021): [`docs/data_card.md`](docs/data_card.md)

---

## 🚀 Quick Start

### ☁️ Option A — Google Colab *(Recommended)*

No local setup required. Click below to launch the full demo:

<a href="https://colab.research.google.com/github/aliakarma/FinNutriAgent/blob/main/example/demo_finagent.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

---

### 🐍 Option B — Local Setup (pip)

```bash
# 1. Clone the repository
git clone https://github.com/aliakarma/FinNutriAgent.git
cd FinNutriAgent

# 2. Install in editable mode
pip install -e .

# 3. (Optional) Fully reproducible install with pinned lockfile
pip install -r requirements.lock.txt
```

### 🐍 Option C — Local Setup (Conda)

```bash
git clone https://github.com/aliakarma/FinNutriAgent.git
cd FinNutriAgent
conda env create -f environment.yml
conda activate finnutriagent
```

---

### ▶️ Run the Demo Notebook

```bash
jupyter notebook example/demo_finagent.ipynb
```

### ✅ Validate Data Integrity

```bash
python scripts/validate_data.py
```

### ⚙️ Run the Optimizer

```python
from scripts.optimizer import run_optimization

result = run_optimization(
    weekly_budget=912.50,
    nutrient_targets={
        "calories":   6696,
        "protein":     158,
        "vitamin_d":    60,
        "iron":         44,
    },
    halal_only=True,
)

print(result["status"])           # Optimal
print(result["total_cost_sar"])   # e.g., 24.73
print(result["plan"])             # DataFrame with recommended foods + nutrient contributions
```

### 🧪 Run Tests

```bash
pytest tests/ -v
```

---

### 🔁 Reproducibility

To regenerate all core tables and figures from the paper:

```bash
python scripts/reproduce_results.py
```

Outputs: `results/summary.csv`, `results/summary_stats.json`, and a sample plan for household `U017`.

For a quick budget sensitivity evaluation:

```bash
python scripts/evaluate_budget.py
```

Evaluates household `U017` at a fixed 500 SAR weekly budget and prints cost/utilization with selected foods.

---

## 📈 Results Summary

> Full results: [`RESULTS.md`](RESULTS.md) · Full reproduction: [`example/demo_finagent.ipynb`](example/demo_finagent.ipynb)

The optimizer consistently finds **feasible, cost-minimal halal meal plans** across all 100 households, satisfying all four nutritional constraints while consuming only **3–7% of the available weekly food budget** — demonstrating strong economic efficiency.

---

## 📁 Repository Structure

```
FinNutriAgent/
├── README.md                         # This file
├── LICENSE                           # MIT (code) / CC BY 4.0 (data & docs)
├── requirements.txt                  # Python package dependencies
├── requirements.lock.txt             # Pinned lockfile for reproducibility
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
│   ├── reproduce_results.py          # Full paper result reproduction
│   ├── evaluate_budget.py            # Budget sensitivity evaluation
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

## 📝 Citation

If you use FinNutriAgent in your research, please cite:

```bibtex
@software{syedfinagent2026,
  author    = {Toqeer Ali Syed, Abdulaziz Alshahrani, Ali Akarma, Sohail Khan, Muhammad Nauman, It Ee Lee, Salman Jan and Ali Ullah},
  title     = {{FinNutriAgent: Agentic AI for Household Nutrition and Budget Optimization}},
  year      = {2026},
  publisher = {Engineering, Technology & Applied Science Research},
  doi       = {},
  url       = {}
}
```

Or use the machine-readable [`CITATION.cff`](CITATION.cff).

---

## ⚖️ License

| Component | License |
|---|---|
| Code (`scripts/`, `tests/`, `example/`) | [![MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) |
| Datasets (`data/`) | [![CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/) |
| Documentation (`docs/`) | [![CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/) |

---

## 🤝 Contributing

Contributions are warmly welcome! Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before submitting a pull request.

[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Open Issues](https://img.shields.io/github/issues/aliakarma/FinNutriAgent)](https://github.com/aliakarma/FinNutriAgent/issues)
[![GitHub Stars](https://img.shields.io/github/stars/aliakarma/FinNutriAgent?style=social)](https://github.com/aliakarma/FinNutriAgent)

---

## 📬 Contact

<div align="center">

**Ali Akarma**

[![ORCID](https://img.shields.io/badge/ORCID-0009--0002--6687--9380-a6ce39?style=for-the-badge&logo=orcid&logoColor=white)](https://orcid.org/0009-0002-6687-9380)
[![GitHub](https://img.shields.io/badge/GitHub-@aliakarma-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/aliakarma)
[![Issues](https://img.shields.io/badge/Bug%20Reports-Open%20an%20Issue-red?style=for-the-badge&logo=github)](https://github.com/aliakarma/FinNutriAgent/issues)

</div>

---

<div align="center">

*Built with ❤️ for household food security and financial wellbeing.*

[![DOI](https://zenodo.org/badge/1115326129.svg)](https://doi.org/10.5281/zenodo.18849993)

</div>
