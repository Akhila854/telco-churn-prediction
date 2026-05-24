"""
Task 6: Model Evaluation
- Accuracy, Precision, Recall, F1-score, ROC-AUC
- Confusion matrix
- ROC curve plot
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import json
import os
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix,
    ConfusionMatrixDisplay, roc_curve, classification_report
)
from prepare_data import load_and_prepare, split_data


def evaluate(model, X_test: pd.DataFrame, y_test: pd.Series,
             model_name: str = "Model") -> dict:
    y_pred  = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "model":     model_name,
        "accuracy":  round(accuracy_score(y_test, y_pred),  4),
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall":    round(recall_score(y_test, y_pred),    4),
        "f1_score":  round(f1_score(y_test, y_pred),        4),
        "roc_auc":   round(roc_auc_score(y_test, y_proba),  4),
    }

    print("\n" + "="*50)
    print(f"  Evaluation — {model_name}")
    print("="*50)
    for k, v in metrics.items():
        if k != "model":
            print(f"  {k:12s}: {v}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred,
                                target_names=["No Churn", "Churn"]))

    os.makedirs("outputs", exist_ok=True)

    # Confusion matrix
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    cm = confusion_matrix(y_test, y_pred)
    ConfusionMatrixDisplay(cm, display_labels=["No Churn", "Churn"]).plot(
        ax=axes[0], colorbar=False, cmap="Blues"
    )
    axes[0].set_title("Confusion Matrix")

    # ROC curve
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    axes[1].plot(fpr, tpr, color="steelblue", lw=2,
                 label=f"ROC AUC = {metrics['roc_auc']:.4f}")
    axes[1].plot([0, 1], [0, 1], "k--", lw=1)
    axes[1].set_xlabel("False Positive Rate")
    axes[1].set_ylabel("True Positive Rate")
    axes[1].set_title("ROC Curve")
    axes[1].legend(loc="lower right")

    plt.suptitle(f"{model_name} — Churn Prediction", fontsize=13)
    plt.tight_layout()
    plt.savefig("outputs/evaluation.png", dpi=150)
    plt.show()
    print("Saved: outputs/evaluation.png")

    # Save metrics to JSON
    with open("outputs/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    print("Saved: outputs/metrics.json")

    return metrics


if __name__ == "__main__":
    df = load_and_prepare()
    X_train, X_test, y_train, y_test = split_data(df)

    artifact = joblib.load("models/churn_model.joblib")
    model     = artifact["model"]
    name      = artifact["name"]

    metrics = evaluate(model, X_test, y_test, model_name=name)
    print(f"\n✅ Final ROC-AUC: {metrics['roc_auc']}")
