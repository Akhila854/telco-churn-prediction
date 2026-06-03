# SQL Analysis — Telco Churn Dataset

SQL queries run on the Telco churn dataset loaded into SQLite.  
Run: `python sql_analysis.py`

---

## Setup

The raw CSV is loaded into a local SQLite database (`data/churn_analysis.db`).  
All queries run against a `customers` table with 7,032 rows (11 dropped due to blank TotalCharges).

---

## Query 1 — Churn Rate by Contract Type

```sql
SELECT
    Contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY Contract
ORDER BY churn_rate_pct DESC;
```

**Key finding:** Month-to-month customers churn at ~42.71% vs ~2.85% for two-year contract customers.

---

## Query 2 — Average Tenure by Payment Method

```sql
SELECT
    PaymentMethod,
    ROUND(AVG(tenure), 2) AS avg_tenure_months,
    COUNT(*) AS customer_count
FROM customers
GROUP BY PaymentMethod
ORDER BY avg_tenure_months DESC;
```

**Key finding:** Credit card (automatic) customers stay longest on average.

---

## Query 3 — Monthly Charges Distribution by Churn Status

```sql
SELECT
    Churn,
    ROUND(MIN(MonthlyCharges), 2) AS min_charge,
    ROUND(AVG(MonthlyCharges), 2) AS avg_charge,
    ROUND(MAX(MonthlyCharges), 2) AS max_charge,
    COUNT(*) AS customer_count
FROM customers
GROUP BY Churn;
```

**Key finding:** Churned customers pay ~$74.44/month avg vs $61.31 for retained customers.

---

## Query 4 — Churn Rate by Internet Service Type

```sql
SELECT
    InternetService,
    COUNT(*) AS total,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY InternetService
ORDER BY churn_rate_pct DESC;
```

**Key finding:** Fiber optic customers churn at nearly 2x the rate of DSL customers.

---

## Query 5 — Top 10 Highest Tenure Churned Customers

```sql
SELECT customerID, tenure, Contract, MonthlyCharges, TotalCharges
FROM customers
WHERE Churn = 'Yes'
ORDER BY tenure DESC
LIMIT 10;
```

**Key finding:** Even long-tenure customers (~70 months) churn — typically on month-to-month contracts with high charges.

---

## Query 6 — Churn Rate by Tenure Bucket (CTE)

```sql
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
```

**Key finding:** First-year customers churn at 47.68%, drops to 9.51% after 4 years

---

## Query 7 — Avg Charges by Churn Segment (Window Function)

```sql
SELECT DISTINCT
    Churn,
    ROUND(AVG(MonthlyCharges) OVER (PARTITION BY Churn), 2) AS avg_monthly_charge,
    ROUND(AVG(TotalCharges) OVER (PARTITION BY Churn), 2) AS avg_total_charge,
    COUNT(*) OVER (PARTITION BY Churn) AS segment_size
FROM customers;
```

**Key finding:** Churned customers have lower total charges ($1,531) despite higher monthly — confirms they leave early.

---

## Query 8 — Above-Average Charge Churners by Contract (Subquery)

```sql
SELECT
    Contract,
    COUNT(*) AS high_charge_churners
FROM customers
WHERE Churn = 'Yes'
  AND MonthlyCharges > (SELECT AVG(MonthlyCharges) FROM customers)
GROUP BY Contract
ORDER BY high_charge_churners DESC;
```

**Key finding:** Month-to-month is the dominant contract type even among high-paying churners — a key retention target.

---

## SQL Concepts Covered

| Concept | Used In |
|---|---|
| GROUP BY + aggregations | Q1, Q2, Q3, Q4, Q8 |
| CASE WHEN | Q1, Q4, Q6 |
| CTE (WITH clause) | Q6 |
| Window functions (OVER, PARTITION BY) | Q7 |
| Subquery | Q8 |
| ORDER BY + LIMIT | Q5 |