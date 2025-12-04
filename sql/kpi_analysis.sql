-- KPI Analysis Queries for Retail Analytics
-- Run these against the retail_db.sqlite database

-- 1. Total Revenue, Profit, and Quantity
SELECT 
    SUM(sales) as total_revenue,
    SUM(profit) as total_profit,
    SUM(quantity) as total_quantity_sold,
    COUNT(DISTINCT order_id) as total_orders
FROM fact_sales;

-- 2. Monthly Revenue Growth (MoM)
WITH monthly_sales AS (
    SELECT 
        d.year,
        d.month,
        SUM(f.sales) as revenue
    FROM fact_sales f
    JOIN dim_date d ON f.order_date = d.date
    GROUP BY 1, 2
),
lagged_sales AS (
    SELECT 
        *,
        LAG(revenue) OVER (ORDER BY year, month) as prev_month_revenue
    FROM monthly_sales
)
SELECT 
    year,
    month,
    revenue,
    prev_month_revenue,
    ROUND((revenue - prev_month_revenue) / prev_month_revenue * 100, 2) as mom_growth_pct
FROM lagged_sales;

-- 3. Top 5 Products by Profit
SELECT 
    p.product_name,
    p.category,
    SUM(f.profit) as total_profit,
    SUM(f.sales) as total_sales
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY 1, 2
ORDER BY total_profit DESC
LIMIT 5;

-- 4. Customer Segmentation (RFM Proxy)
-- Recency (days since last order), Frequency (count orders), Monetary (total sales)
SELECT 
    c.customer_name,
    c.segment,
    MAX(f.order_date) as last_order_date,
    COUNT(DISTINCT f.order_id) as frequency,
    SUM(f.sales) as monetary_value
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
GROUP BY 1, 2
ORDER BY monetary_value DESC
LIMIT 10;

-- 5. Regional Performance
SELECT 
    l.region,
    SUM(f.sales) as total_sales,
    SUM(f.profit) as total_profit,
    ROUND(SUM(f.profit) / SUM(f.sales) * 100, 2) as profit_margin_pct
FROM fact_sales f
JOIN dim_location l ON f.location_id = l.location_id
GROUP BY 1
ORDER BY total_sales DESC;
