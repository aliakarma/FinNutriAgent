# Data Card for FinAgent Synthetic Datasets

This Data Card provides a structured and transparent description of the datasets used in the FinAgent system. It follows recommended practices for dataset documentation in AI research to ensure clarity, reproducibility, and responsible use.

---

## 1. Motivation

The datasets support research on cost-aware, nutrition-aware, and culturally aligned meal planning using agentic AI. They are designed to simulate realistic household budgeting, nutrient needs, food composition, and market pricing in a Middle Eastern context (with emphasis on Saudi Arabia). The goal is to enable reproducible experiments in nutrition optimization, affordability analysis, and autonomous household assistance.

The datasets do **not** represent real individuals or real financial records.

---

## 2. Composition

### Included Datasets

1. **financial_data**  
   - **Rows:** 101  
   - **Columns:** 8  
   - Represents synthetic monthly financial profiles (income, expenses, savings targets).

2. **food_composition**  
   - **Rows:** 351  
   - **Columns:** 7  
   - Contains macro- and micronutrient profiles for foods commonly consumed in Saudi Arabia, including halal status.

3. **food_prices**  
   - **Rows:** 351  
   - **Columns:** 4  
   - Synthetic daily or periodic food price entries aligned with foods in `food_composition`.

4. **nutrition_requirements**  
   - **Rows:** 501  
   - **Columns:** 7  
   - Individual-level nutrient requirements (age, gender, calorie need, protein, vitamin D, iron).

### Data Types

- Numeric financial values  
- Nutritional composition data  
- Daily food prices  
- Basic demographic fields (age/gender), fully synthetic  
- No identifiers relate to real persons

---

## 3. Collection Process

### Data Sources
All datasets are **synthetically generated** using:

- Public nutrition ranges (USDA, WHO, FAO nutrient tables)
- Common foods and price behavior in Saudi Arabia
- Typical household expense distributions derived from publicly available economic reports
- No web scraping of identifiable personal data

### No Real Users
No data originates from real households. All entries are artificially constructed for research and benchmarking.

---

## 4. Preprocessing

- Normalized nutrient units (per 100g foods)
- Standardized price units (per kg)
- Halal classification using rule-based tagging
- Date formatting normalized to ISO-8601
- Outliers removed from synthetic data generation
- All categorical values cleaned and validated

---

## 5. Intended Use

The datasets are intended for:

- Academic research  
- Reproducible experiments in nutrition optimization  
- Agent-based meal planning  
- Cost-sensitive household modeling  
- Prototyping intelligent diet and budgeting systems  

They are not intended for:

- Real population studies  
- Medical diagnosis  
- Individualized dietary prescriptions without expert supervision

---

## 6. Ethical Considerations

- The datasets contain no personally identifiable information.  
- All individuals are synthetic; age/gender fields reflect no real people.  
- Cultural food representations aim to avoid bias but may not capture the full diversity of Saudi communities.  
- Responsible use is encouraged, especially when deploying diet optimization tools to real users.

---

## 7. Licensing

All datasets are released under:

**Creative Commons Attribution 4.0 International (CC BY 4.0)**

This permits reuse with attribution.

---

## 8. Maintenance

The datasets will be revised if:

- New synthetic items are added  
- Additional nutrient fields are included  
- Price models are updated  

Please raise an issue in the GitHub repository for updates or corrections.

---
