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

import mlflow
import mlflow.sklearn

from prepare_data      import load_and_prepare, split_data
from feature_selection import select_features
from train_model       import compare_models, train_best_model
from evaluate_model    import evaluate

os.makedirs("outputs", exist_ok=True)
os.makedirs("models",  exist_ok=True)

# ── MLflow setup ─────────────────────────────────────────
mlflow.set_experiment("telco-churn-prediction")

print("\n" + "="*55)
print("  Telco Customer Churn — Full ML Pipeline")
print("="*55)

with mlflow.start_run():

    # Task 1 & 2
    print("\n── Task 1 & 2: Data Preparation & Split ──")
    df                               = load_and_prepare()
    X_train, X_test, y_train, y_test = split_data(df)

    # Log data parameters
    mlflow.log_param("total_rows",    len(df))
    mlflow.log_param("train_size",    len(X_train))
    mlflow.log_param("test_size",     len(X_test))
    mlflow.log_param("num_features",  X_train.shape[1])
    mlflow.log_param("churn_rate_pct",
                     round(y_train.mean() * 100, 2))

    # Task 3
    print("\n── Task 3: Feature Selection ──")
    top_features = select_features(X_train, y_train, top_n=10)
    mlflow.log_param("top_features", str(top_features))

    # Task 4 & 5
    print("\n── Task 4 & 5: Model Selection & Training ──")
    best_name = compare_models(X_train, y_train)
    model     = train_best_model(X_train, y_train, best_name)

    mlflow.log_param("best_model", best_name)

    # Task 6
    print("\n── Task 6: Model Evaluation ──")
    metrics = evaluate(model, X_test, y_test, model_name=best_name)

    # Log all metrics
    mlflow.log_metric("accuracy",  metrics["accuracy"])
    mlflow.log_metric("precision", metrics["precision"])
    mlflow.log_metric("recall",    metrics["recall"])
    mlflow.log_metric("f1_score",  metrics["f1_score"])
    mlflow.log_metric("roc_auc",   metrics["roc_auc"])

    # Log model
    mlflow.sklearn.log_model(model, "model")

    # Log output plots as artifacts
    if os.path.exists("outputs/evaluation.png"):
        mlflow.log_artifact("outputs/evaluation.png")
    if os.path.exists("outputs/feature_importance.png"):
        mlflow.log_artifact("outputs/feature_importance.png")

    run_id = mlflow.active_run().info.run_id

print("\n" + "="*55)
print("  Pipeline complete!")
print(f"  Best model : {best_name}")
print(f"  Accuracy   : {metrics['accuracy']}")
print(f"  F1 Score   : {metrics['f1_score']}")
print(f"  ROC-AUC    : {metrics['roc_auc']}")
print(f"  MLflow run : {run_id}")
print("="*55)
print("\nRun 'mlflow ui' to view experiment dashboard")