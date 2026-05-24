"""
Task 4 & 5: Model Selection and Training
- Compare Logistic Regression, Decision Tree, Random Forest, Gradient Boosting
- Train best model on full training set
- Save trained model
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from prepare_data import load_and_prepare, split_data


MODELS = {
    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000, random_state=42))
    ]),
    "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=42),
    "Random Forest": RandomForestClassifier(
        n_estimators=200, max_depth=8, random_state=42, n_jobs=-1
    ),
    "Gradient Boosting": GradientBoostingClassifier(
        n_estimators=200, learning_rate=0.05, max_depth=4, random_state=42
    ),
}


def compare_models(X_train: pd.DataFrame, y_train: pd.Series) -> str:
    print("Comparing models with 5-fold cross-validation (F1 score)...\n")
    results = {}
    for name, model in MODELS.items():
        scores = cross_val_score(model, X_train, y_train,
                                 cv=5, scoring="f1", n_jobs=-1)
        results[name] = scores
        print(f"{name:25s} — F1: {scores.mean():.4f} ± {scores.std():.4f}")

    best = max(results, key=lambda k: results[k].mean())
    print(f"\n✅ Best model: {best} (F1={results[best].mean():.4f})")
    return best


def train_best_model(X_train: pd.DataFrame, y_train: pd.Series,
                     best_name: str) -> object:
    print(f"\nTraining {best_name} on full training set...")
    model = MODELS[best_name]
    model.fit(X_train, y_train)

    os.makedirs("models", exist_ok=True)
    path = "models/churn_model.joblib"
    joblib.dump({"model": model, "name": best_name,
                 "features": X_train.columns.tolist()}, path)
    print(f"Model saved to {path}")
    return model


if __name__ == "__main__":
    df = load_and_prepare()
    X_train, X_test, y_train, y_test = split_data(df)

    best_name = compare_models(X_train, y_train)
    model     = train_best_model(X_train, y_train, best_name)
