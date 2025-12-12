# Dataset Documentation

This document provides detailed descriptions of all datasets included in the repository.  
All datasets are synthetic and designed for research involving nutrition analytics, dietary modeling, affordability analysis, and personalized nutrition planning.

---

## 1. Dataset Overview

The repository contains the following datasets:

1. **financial_data** – 101 rows × 8 columns  
2. **food_composition** – 351 rows × 7 columns  
3. **food_prices** – 351 rows × 4 columns  
4. **nutrition_requirements** – 501 rows × 7 columns  

Each dataset is described in detail below.

---

## 2. Dataset Descriptions

---

## 2.1 `financial_data`

A synthetic dataset representing household or individual-level monthly financial capacity.  
Useful for affordability modeling, diet planning under budget constraints, and socioeconomic correlation analysis.

### Fields

| Field | Description |
|-------|-------------|
| `user_id` | Unique identifier for a synthetic user |
| `monthly_income` | Total income per month (numeric) |
| `rent` | Monthly rent cost |
| `utilities` | Cost of electricity, water, and other basic utilities |
| `transport` | Monthly transportation expenses |
| `education` | Monthly educational expenses |
| `healthcare` | Monthly healthcare spending |
| `savings_target` | Amount user tries to save per month |

### Shape
- **Rows:** 101  
- **Columns:** 8  

### Source
- Synthetic; no real financial or personal data.

---

## 2.2 `food_composition`

A database of foods with macronutrients and essential micronutrients.  
Useful for nutrition calculations, dietary planning, and fundamental nutrient analysis.

### Fields

| Field | Description |
|-------|-------------|
| `food_id` | Unique identifier for each food item |
| `food_name` | Name of the food (single ingredient or composite) |
| `calories_per_100g` | Calories per 100 grams |
| `protein_g` | Protein content per 100g |
| `vitamin_d_mcg` | Vitamin D content (micrograms) |
| `iron_mg` | Iron content (milligrams) |
| `halal` | Indicates if the food is halal (yes/no) |

### Shape
- **Rows:** 351  
- **Columns:** 7  

### Source
- Synthetic but based on common food composition values.

---

## 2.3 `food_prices`

Daily or periodic market price dataset for food items.  
Useful for cost optimization, price trend analysis, and economic modeling.

### Fields

| Field | Description |
|-------|-------------|
| `food_id` | Foreign key referencing `food_composition` |
| `store` | Store name or category (supermarket, local market, etc.) |
| `price_per_kg` | Price per kilogram in local currency |
| `date` | Date of price record |

### Shape
- **Rows:** 351  
- **Columns:** 4  

### Source
- Fully synthetic; modeled after typical retail food price structures.

---

## 2.4 `nutrition_requirements`

Personalized daily nutrient requirements for different synthetic individuals.  
Useful for personalized meal planning, diet recommendation systems, and nutrition modeling.

### Fields

| Field | Description |
|-------|-------------|
| `person_id` | Unique synthetic person identifier |
| `age` | Age in years |
| `gender` | Male/Female |
| `calories_kcal` | Daily caloric requirement |
| `protein_g` | Daily protein requirement |
| `vitamin_d_mcg` | Daily Vitamin D requirement |
| `iron_mg` | Daily iron requirement |

### Shape
- **Rows:** 501  
- **Columns:** 7  

### Source
- Synthetic; based on widely used nutrient requirement ranges.

---

## 3. Data Source Description

All datasets are:

- Fully **synthetic**  
- Contain **no personal or sensitive real-world data**  
- Generated for academic and analytical model development  
- Suitable for machine learning, statistical modeling, and reproducible research  

---

## 4. License

All datasets in this repository are released under:

**Creative Commons Attribution 4.0 International (CC BY 4.0)**

You may share, remix, adapt, and build upon the data with proper attribution.


