# 📉 Telco Customer Churn Prediction

An end-to-end machine learning pipeline for predicting customer churn in a 
telecommunications company, built as part of a Saiket Systems ML internship (2025).

Covers the full ML lifecycle — data preparation, feature engineering, model 
selection, training, and evaluation — on a real 7,043-customer dataset.

---

## 📊 Dataset

| Property | Value |
|----------|-------|
| Source | Telco Customer Churn Dataset |
| Rows | 7,043 customers |
| Features | 20 (after dropping customerID) |
| Target | `Churn` (Yes / No) |
| Class balance | 73.5% No Churn / 26.5% Churn |

Key features: `tenure`, `Contract`, `MonthlyCharges`, `TotalCharges`,
`InternetService`, `OnlineSecurity`, `TechSupport`, `PaymentMethod`

---

## 🏗️ Pipeline

```
Raw CSV (7,043 rows)
       │
Task 1 — Data Preparation
       │  Fix TotalCharges dtype
       │  Encode binary & categorical columns
       │  Handle missing values
       │
Task 2 — Train / Test Split (80 / 20, stratified)
       │
Task 3 — Feature Selection
       │  Random Forest importance analysis
       │  Top 10 features identified
       │
Task 4 — Model Selection (5-fold CV comparison)
       │  Logistic Regression
       │  Decision Tree
       │  Random Forest
       │  Gradient Boosting
       │
Task 5 — Train Best Model
       │
Task 6 — Evaluation
          Accuracy, Precision, Recall, F1, ROC-AUC
          Confusion Matrix + ROC Curve
```

---

## 📈 Results

| Metric | Score |
|--------|-------|
| Best Model | Logistic Regression |
| Accuracy | 0.80 |
| Precision | 0.64 |
| Recall | 0.55 |
| F1 Score | 0.59 |
| ROC-AUC | 0.84 |

> Best model selected via 5-fold cross-validation across 4 classifiers.
> Logistic Regression chosen for superior F1 and lower inference complexity.

---

| Query | Key SQL Concept |
|---|---|
| Overall churn rate | COUNT, AVG aggregation |
| Churn rate by contract type | GROUP BY, ORDER BY |
| Churn rate by tenure bucket | CASE WHEN, GROUP BY |
| Avg charges — churned vs retained | GROUP BY, ROUND |
| Churn rate by internet service | GROUP BY, filtering |
| Highest-risk segments | Multi-column GROUP BY, HAVING |
| Churn rate by payment method | GROUP BY, ORDER BY |
| Monthly revenue at risk | Conditional SUM, division |
---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Data processing | pandas, numpy |
| ML models | scikit-learn |
| Visualisation | matplotlib |
| Model persistence | joblib |
| Language | Python 3.10+ |

---

## 🚀 Quick Start

```bash
git clone https://github.com/Akhila854/telco-churn-prediction.git
cd telco-churn-prediction
pip install -r requirements.txt
```

Add your dataset:
```
data/
└── telco_churn.csv
```

Run full pipeline:
```bash
python main.py
```

Or run individual tasks:
```bash
python src/prepare_data.py      # Task 1 & 2
python src/feature_selection.py # Task 3
python src/train_model.py       # Task 4 & 5
python src/evaluate_model.py    # Task 6
```

---

## 📁 Project Structure

```
telco-churn-prediction/
├── main.py
├── sql_analysis.py
├── src/
│   ├── prepare_data.py
│   ├── feature_selection.py
│   ├── train_model.py
│   └── evaluate_model.py
├── data/
│   └── telco_churn.csv
├── SQL_ANALYSIS.md
├── README.md
├── requirements.txt
└── .gitignore
```
