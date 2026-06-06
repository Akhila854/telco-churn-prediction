# 📊 SQL Cohort Analysis — Telco Customer Churn

SQLite-based analytical layer on top of the ML pipeline.
8 queries identifying churn drivers, high-risk segments,
and revenue impact across 7,043 customers.

---

## Query 1 — Overall Churn Rate

```sql
SELECT
    COUNT(*) AS total_customers,
    SUM(ChurnInt) AS churned,
    ROUND(AVG(ChurnInt) * 100, 2) AS churn_rate_pct
FROM customers
```

| total_customers | churned | churn_rate_pct |
|---|---|---|
| 7,043 | 1,869 | 26.54% |

---

## Query 2 — Churn Rate by Contract Type

```sql
SELECT Contract, COUNT(*), SUM(ChurnInt),
       ROUND(AVG(ChurnInt) * 100, 2) AS churn_rate_pct
FROM customers
GROUP BY Contract
ORDER BY churn_rate_pct DESC
```

| Contract | Customers | Churned | Churn Rate |
|---|---|---|---|
| Month-to-month | 3,875 | 1,655 | **42.71%** |
| One year | 1,473 | 166 | 11.27% |
| Two year | 1,695 | 48 | **2.83%** |

💡 **Key finding: Month-to-month customers churn at 15x the rate
of two-year contract customers (42.71% vs 2.83%).**

---

## Query 3 — Churn Rate by Tenure Group

| Tenure Group | Customers | Churned | Churn Rate |
|---|---|---|---|
| 0–12 months | 2,186 | 1,037 | **47.44%** |
| 13–24 months | 1,024 | 294 | 28.71% |
| 25–48 months | 1,594 | 325 | 20.39% |
| 49+ months | 2,239 | 213 | 9.51% |

💡 **Key finding: Nearly 1 in 2 new customers (0–12 months)
churns. Churn risk drops 5x for customers who stay past 4 years.**

---

## Query 4 — Avg Charges: Churned vs Retained

| Churn | Avg Monthly Charges | Avg Total Charges | Avg Tenure |
|---|---|---|---|
| No | $61.27 | $2,550.00 | 37.6 months |
| Yes | $74.44 | $1,531.80 | 18.0 months |

💡 **Key finding: Churned customers pay 21% more per month
but generate 40% less total revenue — they leave before
lifetime value accumulates.**

---

## Query 5 — Churn Rate by Internet Service

| Internet Service | Customers | Churned | Churn Rate |
|---|---|---|---|
| Fiber optic | 3,096 | 1,297 | **41.89%** |
| DSL | 2,421 | 459 | 18.96% |
| No internet | 1,526 | 113 | 7.40% |

💡 **Key finding: Fiber optic customers churn at 5.7x the rate
of customers with no internet service — likely a pricing or
service quality signal.**

---

## Query 6 — Highest-Risk Customer Segments

Combined segmentation by contract, internet service, and tenure:

| Contract | Internet | Tenure | Segment Size | Churn Rate |
|---|---|---|---|---|
| Month-to-month | Fiber optic | 0–12 months | 916 | **70.20%** |
| Month-to-month | Fiber optic | 13–24 months | 425 | 50.59% |
| Month-to-month | DSL | 0–12 months | 690 | 42.46% |
| Month-to-month | Fiber optic | 25+ months | 787 | 38.63% |
| Month-to-month | DSL | 13–24 months | 232 | 23.71% |

💡 **Key finding: The single highest-risk segment —
month-to-month fiber optic customers in their first year —
has a 70.2% churn rate. 7 in 10 customers in this segment leave.**

---

## Query 7 — Churn Rate by Payment Method

| Payment Method | Customers | Churned | Churn Rate |
|---|---|---|---|
| Electronic check | 2,365 | 1,071 | **45.29%** |
| Mailed check | 1,612 | 308 | 19.11% |
| Bank transfer (automatic) | 1,544 | 258 | 16.71% |
| Credit card (automatic) | 1,522 | 232 | 15.24% |

💡 **Key finding: Electronic check users churn at 3x the rate
of automatic payment users — manual payment methods
strongly correlate with churn risk.**

---

## Query 8 — Monthly Revenue at Risk

| Contract | Revenue Lost/Month | Churned Customers | % Revenue at Risk |
|---|---|---|---|
| Month-to-month | $120,847 | 1,655 | **46.97%** |
| One year | $14,118 | 166 | 14.73% |
| Two year | $4,165 | 48 | 4.04% |

💡 **Key finding: Month-to-month contracts represent $120,847
in lost monthly revenue — nearly 47% of their segment's
total revenue. Retention programs targeting this segment
have the highest potential ROI.**

---

## Summary of Key Findings

| Finding | Impact |
|---|---|
| Month-to-month vs two-year churn | 42.71% vs 2.83% — **15x difference** |
| New customer churn (0–12 months) | **47.44%** — highest risk window |
| Highest-risk single segment | Month-to-month + Fiber + 0–12 months = **70.2% churn** |
| Electronic check churn premium | **3x higher** than automatic payments |
| Monthly revenue at risk | **$120,847/month** from month-to-month alone |
| Churned customers pay more | 21% higher monthly charges but 40% less lifetime value |

---

## How to Run

```bash
python sql_analysis.py
```

Requires: pandas, sqlite3 (built into Python)
Output: prints all 8 query results + saves `churn_analysis.db`