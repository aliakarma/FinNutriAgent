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
