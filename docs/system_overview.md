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
