# Dashboard Build Guide

This guide explains how to build the dashboard in Power BI or Tableau using the processed data.

## Data Source
- **Files**: `data/analytics/*.csv` or `data/analytics/*.parquet`
- **Database**: `data/analytics/retail_db.sqlite`

## Data Model (Star Schema)
Connect the tables as follows:
- **Fact Table**: `fact_sales`
- **Dimension Tables**: `dim_customer`, `dim_product`, `dim_location`, `dim_date`

**Relationships**:
- `fact_sales.customer_id` -> `dim_customer.customer_id` (Many-to-One)
- `fact_sales.product_id` -> `dim_product.product_id` (Many-to-One)
- `fact_sales.location_id` -> `dim_location.location_id` (Many-to-One)
- `fact_sales.order_date` -> `dim_date.date` (Many-to-One)

## Recommended Visualizations

### 1. Executive Summary (Page 1)
- **KPI Cards**: Total Revenue, Total Profit, Profit Margin %, Total Orders.
- **Line Chart**: Monthly Revenue Trend (Year over Year).
- **Bar Chart**: Sales by Region.
- **Donut Chart**: Sales by Category.

### 2. Product Performance (Page 2)
- **Table/Matrix**: Top 10 Products by Profit.
- **Scatter Plot**: Profit vs. Sales by Sub-Category.
- **Bar Chart**: Bottom 5 Products (Loss makers).

### 3. Customer Insights (Page 3)
- **Bar Chart**: Sales by Customer Segment.
- **Map**: Sales density by City/State.
- **Table**: Top Customers (RFM Analysis).

## Key Measures (DAX / Calculated Fields)
- **Profit Margin %** = `SUM(Profit) / SUM(Sales)`
- **Avg Order Value** = `SUM(Sales) / DISTINCTCOUNT(Order ID)`
- **YTD Sales** = `TOTALYTD(SUM(Sales), 'dim_date'[Date])`
