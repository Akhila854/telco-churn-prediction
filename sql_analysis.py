import sqlite3
import pandas as pd
import os

# --- Setup ---
DB_PATH = "data/churn_analysis.db"
CSV_PATH = "data/telco_churn.csv"

def load_data_to_sqlite():
    df = pd.read_csv(CSV_PATH)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df.dropna(subset=['TotalCharges'], inplace=True)

    conn = sqlite3.connect(DB_PATH)
    df.to_sql("customers", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Loaded {len(df)} rows into SQLite: {DB_PATH}\n")

def run_queries():
    conn = sqlite3.connect(DB_PATH)

    queries = {
        "1. Churn Rate by Contract Type": """
            SELECT
                Contract,
                COUNT(*) AS total_customers,
                SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
                ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
            FROM customers
            GROUP BY Contract
            ORDER BY churn_rate_pct DESC;
        """,

        "2. Average Tenure by Payment Method": """
            SELECT
                PaymentMethod,
                ROUND(AVG(tenure), 2) AS avg_tenure_months,
                COUNT(*) AS customer_count
            FROM customers
            GROUP BY PaymentMethod
            ORDER BY avg_tenure_months DESC;
        """,

        "3. Monthly Charges Distribution by Churn Status": """
            SELECT
                Churn,
                ROUND(MIN(MonthlyCharges), 2) AS min_charge,
                ROUND(AVG(MonthlyCharges), 2) AS avg_charge,
                ROUND(MAX(MonthlyCharges), 2) AS max_charge,
                COUNT(*) AS customer_count
            FROM customers
            GROUP BY Churn;
        """,

        "4. Churn Rate by Internet Service Type": """
            SELECT
                InternetService,
                COUNT(*) AS total,
                SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
                ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
            FROM customers
            GROUP BY InternetService
            ORDER BY churn_rate_pct DESC;
        """,

        "5. Top 10 Highest Tenure Churned Customers": """
            SELECT
                customerID,
                tenure,
                Contract,
                MonthlyCharges,
                TotalCharges
            FROM customers
            WHERE Churn = 'Yes'
            ORDER BY tenure DESC
            LIMIT 10;
        """,

        "6. Churn Rate by Tenure Bucket (CTE)": """
            WITH tenure_buckets AS (
                SELECT *,
                    CASE
                        WHEN tenure <= 12 THEN '0-12 months'
                        WHEN tenure <= 24 THEN '13-24 months'
                        WHEN tenure <= 48 THEN '25-48 months'
                        ELSE '49+ months'
                    END AS tenure_group
                FROM customers
            )
            SELECT
                tenure_group,
                COUNT(*) AS total,
                SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
                ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
            FROM tenure_buckets
            GROUP BY tenure_group
            ORDER BY churn_rate_pct DESC;
        """,

        "7. Average Monthly Charges — Churned vs Retained (Window Function)": """
            SELECT DISTINCT
                Churn,
                ROUND(AVG(MonthlyCharges) OVER (PARTITION BY Churn), 2) AS avg_monthly_charge,
                ROUND(AVG(TotalCharges) OVER (PARTITION BY Churn), 2) AS avg_total_charge,
                COUNT(*) OVER (PARTITION BY Churn) AS segment_size
            FROM customers;
        """,

        "8. Customers with Above-Average Monthly Charges who Churned (Subquery)": """
            SELECT
                Contract,
                COUNT(*) AS high_charge_churners
            FROM customers
            WHERE Churn = 'Yes'
              AND MonthlyCharges > (SELECT AVG(MonthlyCharges) FROM customers)
            GROUP BY Contract
            ORDER BY high_charge_churners DESC;
        """
    }

    for title, sql in queries.items():
        print(f"\n{'='*60}")
        print(f"Query: {title}")
        print('='*60)
        df = pd.read_sql_query(sql, conn)
        print(df.to_string(index=False))

    conn.close()

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    load_data_to_sqlite()
    run_queries()