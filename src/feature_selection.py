"""
Task 3: Feature Selection
- Analyse feature importance using Random Forest
- Select top features influencing churn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from prepare_data import load_and_prepare, split_data


def select_features(X_train: pd.DataFrame, y_train: pd.Series,
                    top_n: int = 10) -> list:
    print("Running feature importance analysis with Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)

    importances = pd.Series(rf.feature_importances_, index=X_train.columns)
    importances = importances.sort_values(ascending=False)

    print(f"\nTop {top_n} features influencing churn:")
    print(importances.head(top_n).to_string())

    # Plot
    plt.figure(figsize=(10, 6))
    importances.head(top_n).plot(kind="barh", color="steelblue")
    plt.xlabel("Feature Importance Score")
    plt.title(f"Top {top_n} Features for Churn Prediction")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("outputs/feature_importance.png", dpi=150)
    plt.show()
    print("Saved: outputs/feature_importance.png")

    return importances.head(top_n).index.tolist()


if __name__ == "__main__":
    import os
    os.makedirs("outputs", exist_ok=True)

    df = load_and_prepare()
    X_train, X_test, y_train, y_test = split_data(df)
    top_features = select_features(X_train, y_train, top_n=10)
    print(f"\nSelected features: {top_features}")
