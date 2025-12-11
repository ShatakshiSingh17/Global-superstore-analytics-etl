# Retail Analytics ETL

End-to-end ETL pipeline and analytics for the Global Superstore dataset. Built with Python (Pandas) and SQLite.

## Overview

Takes raw sales data from the [Superstore Dataset (Kaggle)](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final), cleans it, builds a Star Schema (Facts/Dims), and loads it into a local SQLite DB for analysis.

**Stack:** Python, Pandas, SQLite, Parquet.

## Files

- `data/`: Raw csv and processed parquet/db files.
- `scripts/`:
    - `extract.py`: Loads the csv.
    - `transform_clean.py`: Fixes types, column names, etc.
    - `transform_model.py`: Builds the Star Schema.
    - `load.py`: Saves everything.
    - `main.py`: Runs the whole flow.
- `sql/`: Analysis queries.

## Data Model

Simple Star Schema:

```mermaid
erDiagram
    FACT_SALES {
        string order_id
        int customer_id FK
        int product_id FK
        int location_id FK
        date order_date FK
        float sales
        float profit
    }
    DIM_CUSTOMER {
        int customer_id PK
        string name
        string segment
    }
    DIM_PRODUCT {
        int product_id PK
        string name
        string category
    }
    DIM_LOCATION {
        int location_id PK
        string region
    }
    DIM_DATE {
        date date PK
        int year
        int month
    }

    FACT_SALES }|..|| DIM_CUSTOMER : "has"
    FACT_SALES }|..|| DIM_PRODUCT : "sells"
    FACT_SALES }|..|| DIM_LOCATION : "delivered_to"
    FACT_SALES }|..|| DIM_DATE : "ordered_on"
```

## Running it

1.  **Install deps**:
    ```bash
    pip install pandas pyarrow fastparquet openpyxl
    ```

2.  **Run ETL**:
    ```bash
    python scripts/main.py
    ```
    Check `data/analytics/` for the output.

3.  **Analyze**:
    Run the queries in `sql/kpi_analysis.sql` against `data/analytics/retail_db.sqlite`.

## Analysis Results

**Regional Stats (Sales):**

| Market | Sales | Profit |
| :--- | :--- | :--- |
| APAC | $3.59M | $436k |
| EU | $2.94M | $373k |
| US | $2.30M | $286k |
| LATAM | $2.16M | $222k |
| EMEA | $806k | $44k |

**Top Regions:** Central ($2.8M), South ($1.6M), North ($1.2M).

## Key Analysis & EDA

On performing exploratory data analysis it answers critical business questions:

### 1. Market Profitability
*Which markets are the most lucrative?*
![Market Profit](docs/images/market_profitability.png)
**Insight:** APAC and EU are the clear leaders in total profit, while EMEA lags behind.

### 2. Seasonality Trends
*Is there a seasonal pattern in global sales?*
![Sales Trend](docs/images/monthly_sales_trend.png)
**Insight:** Sales show a consistent upward trend with strong peaks in Q4 (Holiday Season) each year.

### 3. Product Performance
*How do categories compare in Sales vs. Profit?*
![Category Scatter](docs/images/category_scatter.png)
**Insight:** 'Technology' products generally yield high sales and high profit (upper right), while some 'Furniture' sub-categories struggle with profitability despite decent volume.

### 4. Feature Correlation
*What drives profit?*
![Correlation](docs/images/correlation_matrix.png)
**Insight:** Sales and Shipping Cost are highly correlated (0.77). Discount has a negative correlation with Profit, indicating that heavy discounting hurts the bottom line.
