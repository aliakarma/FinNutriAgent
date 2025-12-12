# FinAgent Dataset Card

A dataset card summarizing the motivation, composition, collection process, and ethical considerations of the FinAgent dataset.

---

## 1. Motivation

The FinAgent dataset enables research on price-aware, nutrition-guided, and budget-constrained meal planning using agentic AI systems. It supports experiments on:

- Household financial planning  
- Nutritional optimization  
- Price volatility and price-shock simulations  
- Personalized meal planning for multi-person households  

---

## 2. Dataset Composition

The dataset includes:

1. **Financial data (101 households)**
2. **Nutrition requirements (501 individuals)**
3. **Food composition (351 common foods in Saudi Arabia)**
4. **Food price data (351 items with price history)**

All data is synthetic and does not include real personal information.

---

## 3. Collection and Generation Process

The dataset was generated using:

- Public sources: USDA FoodData Central, SFDA nutrition tables  
- Synthetic sampling for demographics and financial distributions  
- Manually verified Saudi market food lists  
- Price values generated via controlled sampling from 2023–2024 price ranges  

Preprocessing included:

- Range checks (nutrition and price plausibility)  
- Linking food_id across all files  
- Ensuring halal labelling consistency  

---

## 4. Intended Uses

- Diet optimization  
- Household budget planning  
- LLM-based decision-making research  
- Multi-agent nutritional guidance  
- Stress-testing under economic volatility  

---

## 5. Limitations

- Synthetic income distribution may not represent all Saudi regions  
- Price data approximates realistic values but is not collected from live APIs  
- Limited to macronutrients + Vitamin D and Iron  
- Does not include cooking time, recipes, or perishability  

---

## 6. Ethical Considerations

- No personal data  
- No religiously sensitive data beyond halal tagging  
- No socioeconomic profiling of real individuals  
- Safe for public release under CC BY 4.0  

---

## 7. Licensing

Dataset License: **CC BY 4.0**  
Code License: MIT License (recommended)

---

## 8. Contact

For questions or collaboration, please open an issue in the repository.
