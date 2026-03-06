# FinNutriAgent Dataset Card

Following the *Datasheets for Datasets* framework (Gebru et al., 2021).

**Repository**: [github.com/aliakarma/FinNutriAgent](https://github.com/aliakarma/FinNutriAgent)  
**Author**: Ali Akarma — ORCID [0009-0002-6687-9380](https://orcid.org/0009-0002-6687-9380)  
**License**: CC BY 4.0  
**DOI**: [10.5281/zenodo.18849993](https://doi.org/10.5281/zenodo.18849993)

---

## 1. Motivation

**Purpose**: Enable research on price-aware, nutrition-guided, budget-constrained meal planning using agentic AI. The dataset supports experiments at the intersection of household economics, computational nutrition science, and Islamic dietary compliance.

**Tasks supported**:
- Household food budget optimization under fixed expense constraints
- Nutritional adequacy modeling for multi-member, demographically diverse households
- Halal-compliant dietary planning
- Price volatility simulation and resilience testing
- Multi-agent LLM decision-making benchmarks
- Personalized meal planning for Saudi-context households

**Creator**: Ali Akarma, 2025. No external funding.

---

## 2. Composition

| Sub-dataset | Instances | Fields | Description |
|---|---|---|---|
| `financial_data.csv` | 100 | 8 | Household financial profiles |
| `food_composition.csv` | 350 | 7 | Food items with nutrients and halal label |
| `food_prices.csv` | 350 | 4 | Retail prices per kg per store |
| `nutrition_requirements.csv` | 500 | 7 | Individual daily nutritional targets |

- **Missing values**: None.
- **Sensitive data**: None — all data are fully synthetic.
- **Redundancy**: Food name variants (e.g., "Boiled Lentils Var 3") intentionally represent preparation and brand variation.
- **Target variable**: None (constraint-based optimization, not supervised learning).

---

## 3. Collection and Generation

| Component | Source |
|---|---|
| Nutrient content | USDA FoodData Central; SFDA nutrition tables (synthetically sampled within range) |
| Food prices | Synthetic, sampled from 2023–2024 Saudi market price ranges (Carrefour, Lulu, Panda) |
| Financial data | Synthetic, reflecting Saudi household income distribution statistics |
| Nutritional requirements | WHO Dietary Reference Intakes; Saudi dietary guidelines (synthetically sampled) |

Price date: 01/12/2025 (snapshot).

---

## 4. Preprocessing

- Column names stripped of whitespace.
- `food_id` keys verified as consistent across `food_composition.csv` and `food_prices.csv`.
- All numeric fields validated for plausible ranges.
- Halal labels assigned by food category: pork products and alcohol → `No`; all others → `Yes`.
- No imputation — dataset generated without missing values by construction.

---

## 5. Intended Uses

**Appropriate**:
- Nutrition optimization and meal planning research
- Budget-constrained dietary planning algorithms
- Benchmarking AI agents on structured constraint problems
- Food security and affordability studies
- Islamic dietary compliance modeling

**Avoid**:
- Drawing conclusions about real Saudi households
- Using synthetic prices for commercial or financial decisions
- Treating nutrient values as clinical medical recommendations

---

## 6. Distribution

- GitHub: [github.com/aliakarma/FinNutriAgent](https://github.com/aliakarma/FinNutriAgent)
- Archived: [doi.org/10.5281/zenodo.18849993](https://doi.org/10.5281/zenodo.18849993)
- Format: CSV (UTF-8, comma-delimited)
- License: CC BY 4.0

---

## 7. Maintenance

Maintained by the original author. Corrections and updates submitted via GitHub Issues. New versions released as Zenodo deposits.

---

## 8. Ethical Considerations

- All data are **synthetic** — no real individuals represented.
- No socioeconomic profiling of real people or communities.
- Halal labeling reflects widely accepted Islamic dietary standards and is included as a research-reproducibility feature.
- Safe for public release under CC BY 4.0.

---

## 9. Known Limitations

- Synthetic income distributions may not represent all Saudi regions.
- Only four nutrients tracked: calories, protein, Vitamin D, iron.
- Price data are point-in-time; seasonal and regional variation not modeled.
- Cooking time, preparation complexity, palatability, and perishability not included.
- Food list, while broad, does not cover the full Saudi retail market.

---

## References

- Gebru, T. et al. (2021). Datasheets for datasets. *Communications of the ACM*, 64(12), 86–92.
- U.S. Department of Agriculture. *FoodData Central*. https://fdc.nal.usda.gov/
- Saudi Food & Drug Authority. *Nutrition Labeling*. https://www.sfda.gov.sa/
