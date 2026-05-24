"""
Task 1 & 2: Data Preparation and Train/Test Split
- Load dataset
- Handle missing values
- Encode categorical variables
- Split into 80/20 train/test
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os

def load_and_prepare(filepath: str = "data/telco_churn.csv"):
    df = pd.read_csv(filepath)
    print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")

    # ── Fix TotalCharges (stored as string, spaces = missing) ──────────────
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    missing = df["TotalCharges"].isnull().sum()
    print(f"Missing TotalCharges (new customers): {missing} — filling with MonthlyCharges")
    df["TotalCharges"] = df["TotalCharges"].fillna(df["MonthlyCharges"])

    # ── Drop customerID (not a feature) ────────────────────────────────────
    df.drop(columns=["customerID"], inplace=True)

    # ── Encode binary Yes/No columns ───────────────────────────────────────
    binary_cols = [
        "Partner", "Dependents", "PhoneService", "PaperlessBilling",
        "Churn", "MultipleLines", "OnlineSecurity", "OnlineBackup",
        "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"
    ]
    for col in binary_cols:
        df[col] = df[col].map({"Yes": 1, "No": 0,
                               "No phone service": 0,
                               "No internet service": 0})

    # ── Encode multi-class categorical columns ──────────────────────────────
    le = LabelEncoder()
    for col in ["gender", "InternetService", "Contract", "PaymentMethod"]:
        df[col] = le.fit_transform(df[col])

    print(f"Churn distribution:\n{df['Churn'].value_counts()}")
    print(f"\nFinal shape: {df.shape}")
    print(f"Missing values: {df.isnull().sum().sum()}")
    return df


def split_data(df: pd.DataFrame, target: str = "Churn", test_size: float = 0.2):
    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    print(f"\nTrain size: {len(X_train)} | Test size: {len(X_test)}")
    print(f"Churn rate — Train: {y_train.mean():.2%} | Test: {y_test.mean():.2%}")
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    df = load_and_prepare()
    X_train, X_test, y_train, y_test = split_data(df)

    # Save processed splits
    os.makedirs("data/processed", exist_ok=True)
    X_train.to_csv("data/processed/X_train.csv", index=False)
    X_test.to_csv("data/processed/X_test.csv",  index=False)
    y_train.to_csv("data/processed/y_train.csv", index=False)
    y_test.to_csv("data/processed/y_test.csv",   index=False)
    print("\nSaved processed splits to data/processed/")
