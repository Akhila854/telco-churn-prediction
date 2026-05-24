"""
Main pipeline — runs all tasks end to end:
  Task 1: Data preparation
  Task 2: Train/test split
  Task 3: Feature selection
  Task 4: Model selection
  Task 5: Model training
  Task 6: Model evaluation
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from prepare_data     import load_and_prepare, split_data
from feature_selection import select_features
from train_model      import compare_models, train_best_model
from evaluate_model   import evaluate

os.makedirs("outputs", exist_ok=True)
os.makedirs("models",  exist_ok=True)

print("\n" + "="*55)
print("  Telco Customer Churn — Full ML Pipeline")
print("="*55)

# Task 1 & 2
print("\n── Task 1 & 2: Data Preparation & Split ──")
df                              = load_and_prepare()
X_train, X_test, y_train, y_test = split_data(df)

# Task 3
print("\n── Task 3: Feature Selection ──")
top_features = select_features(X_train, y_train, top_n=10)

# Task 4 & 5
print("\n── Task 4 & 5: Model Selection & Training ──")
best_name = compare_models(X_train, y_train)
model     = train_best_model(X_train, y_train, best_name)

# Task 6
print("\n── Task 6: Model Evaluation ──")
metrics = evaluate(model, X_test, y_test, model_name=best_name)

print("\n" + "="*55)
print("  Pipeline complete!")
print(f"  Best model : {best_name}")
print(f"  Accuracy   : {metrics['accuracy']}")
print(f"  F1 Score   : {metrics['f1_score']}")
print(f"  ROC-AUC    : {metrics['roc_auc']}")
print("="*55)
