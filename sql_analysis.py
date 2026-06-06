import sqlite3
import pandas as pd
import os

# ── Setup ────────────────────────────────────────────────
DB_PATH = "churn_analysis.db"
CSV_PATH = "data/telco_churn.csv"

def load_data_to_sqlite():
    """Load CSV into SQLite database."""
    df = pd.read_csv(CSV_PATH)

    # Fix TotalCharges — same as your existing pipeline
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"] = df["TotalCharges"].fillna(df["MonthlyCharges"])

    # Convert Churn to 0/1 integer for SQL aggregations
    df["ChurnInt"] = df["Churn"].map({"Yes": 1, "No": 0})

    conn = sqlite3.connect(DB_PATH)
    df.to_sql("customers", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Loaded {len(df)} rows into SQLite: {DB_PATH}")
    return df


def run_query(conn, title, sql):
    """Run a query, print results, return dataframe."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)
    df = pd.read_sql_query(sql, conn)
    print(df.to_string(index=False))
    return df


def main():
    # Load data
    load_data_to_sqlite()
    conn = sqlite3.connect(DB_PATH)

    results = {}

    # ── Query 1: Overall churn rate ───────────────────────
    results["overall_churn"] = run_query(conn, "Overall Churn Rate", """
        SELECT
            COUNT(*) AS total_customers,
            SUM(ChurnInt) AS churned,
            ROUND(AVG(ChurnInt) * 100, 2) AS churn_rate_pct
        FROM customers
    """)

    # ── Query 2: Churn rate by contract type ─────────────
    results["churn_by_contract"] = run_query(conn, "Churn Rate by Contract Type", """
        SELECT
            Contract,
            COUNT(*) AS total_customers,
            SUM(ChurnInt) AS churned,
            ROUND(AVG(ChurnInt) * 100, 2) AS churn_rate_pct
        FROM customers
        GROUP BY Contract
        ORDER BY churn_rate_pct DESC
    """)

    # ── Query 3: Churn rate by tenure group ──────────────
    results["churn_by_tenure"] = run_query(conn, "Churn Rate by Tenure Group", """
        SELECT
            CASE
                WHEN tenure <= 12  THEN '0-12 months'
                WHEN tenure <= 24  THEN '13-24 months'
                WHEN tenure <= 48  THEN '25-48 months'
                ELSE '49+ months'
            END AS tenure_group,
            COUNT(*) AS total_customers,
            SUM(ChurnInt) AS churned,
            ROUND(AVG(ChurnInt) * 100, 2) AS churn_rate_pct
        FROM customers
        GROUP BY tenure_group
        ORDER BY churn_rate_pct DESC
    """)

    # ── Query 4: Avg monthly charges — churned vs retained
    results["charges_comparison"] = run_query(conn,
        "Avg Monthly Charges — Churned vs Retained", """
        SELECT
            Churn,
            ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
            ROUND(AVG(TotalCharges), 2)   AS avg_total_charges,
            ROUND(AVG(tenure), 1)          AS avg_tenure_months
        FROM customers
        GROUP BY Churn
    """)

    # ── Query 5: Churn by internet service type ──────────
    results["churn_by_internet"] = run_query(conn,
        "Churn Rate by Internet Service", """
        SELECT
            InternetService,
            COUNT(*) AS total_customers,
            SUM(ChurnInt) AS churned,
            ROUND(AVG(ChurnInt) * 100, 2) AS churn_rate_pct
        FROM customers
        GROUP BY InternetService
        ORDER BY churn_rate_pct DESC
    """)

    # ── Query 6: Top 5 highest-risk customer segments ────
    results["high_risk"] = run_query(conn,
        "Highest-Risk Segments (Contract + Internet + Tenure)", """
        SELECT
            Contract,
            InternetService,
            CASE
                WHEN tenure <= 12 THEN '0-12 months'
                WHEN tenure <= 24 THEN '13-24 months'
                ELSE '25+ months'
            END AS tenure_group,
            COUNT(*) AS segment_size,
            ROUND(AVG(ChurnInt) * 100, 2) AS churn_rate_pct
        FROM customers
        GROUP BY Contract, InternetService, tenure_group
        HAVING segment_size >= 30
        ORDER BY churn_rate_pct DESC
        LIMIT 5
    """)

    # ── Query 7: Churn by payment method ─────────────────
    results["churn_by_payment"] = run_query(conn,
        "Churn Rate by Payment Method", """
        SELECT
            PaymentMethod,
            COUNT(*) AS total_customers,
            SUM(ChurnInt) AS churned,
            ROUND(AVG(ChurnInt) * 100, 2) AS churn_rate_pct
        FROM customers
        GROUP BY PaymentMethod
        ORDER BY churn_rate_pct DESC
    """)

    # ── Query 8: Revenue at risk ──────────────────────────
    results["revenue_at_risk"] = run_query(conn,
        "Monthly Revenue at Risk from Churned Customers", """
        SELECT
            Contract,
            SUM(CASE WHEN ChurnInt=1 THEN MonthlyCharges ELSE 0 END)
                AS monthly_revenue_lost,
            COUNT(CASE WHEN ChurnInt=1 THEN 1 END)
                AS churned_customers,
            ROUND(
                SUM(CASE WHEN ChurnInt=1 THEN MonthlyCharges ELSE 0 END) /
                SUM(MonthlyCharges) * 100, 2
            ) AS pct_revenue_at_risk
        FROM customers
        GROUP BY Contract
        ORDER BY monthly_revenue_lost DESC
    """)

    conn.close()

    print("\n" + "="*60)
    print("  SQL Analysis Complete — 8 queries executed")
    print("="*60)
    print(f"\nDatabase saved to: {DB_PATH}")
    print("Copy output above into SQL_ANALYSIS.md")

    return results


if __name__ == "__main__":
    main()