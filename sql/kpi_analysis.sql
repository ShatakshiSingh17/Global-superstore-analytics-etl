-- Retail Analytics Queries

-- 1. High-level metrics
SELECT 
    SUM(sales) as revenue,
    SUM(profit) as profit,
    SUM(quantity) as units_sold,
    COUNT(DISTINCT order_id) as orders
FROM fact_sales;

-- 2. MoM Growth
WITH monthly AS (
    SELECT 
        d.year, d.month,
        SUM(f.sales) as revenue
    FROM fact_sales f
    JOIN dim_date d ON f.order_date = d.date
    GROUP BY 1, 2
)
SELECT 
    year, month, revenue,
    LAG(revenue) OVER (ORDER BY year, month) as prev_revenue,
    ROUND((revenue - LAG(revenue) OVER (ORDER BY year, month)) / LAG(revenue) OVER (ORDER BY year, month) * 100, 2) as growth_pct
FROM monthly;

-- 3. Top Products (Profitability)
SELECT 
    p.product_name,
    p.category,
    SUM(f.profit) as total_profit
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY 1, 2
ORDER BY total_profit DESC
LIMIT 5;

-- 4. Best Customers (RFM-ish)
SELECT 
    c.customer_name,
    c.segment,
    MAX(f.order_date) as last_order,
    COUNT(DISTINCT f.order_id) as orders,
    SUM(f.sales) as total_spend
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
GROUP BY 1, 2
ORDER BY total_spend DESC
LIMIT 10;

-- 5. Region Stats
SELECT 
    l.region,
    SUM(f.sales) as sales,
    SUM(f.profit) as profit,
    ROUND(SUM(f.profit) / SUM(f.sales) * 100, 2) as margin
FROM fact_sales f
JOIN dim_location l ON f.location_id = l.location_id
GROUP BY 1
ORDER BY sales DESC;

-- 6. Sales by Market
SELECT 
    l.market,
    SUM(f.sales) as sales,
    SUM(f.shipping_cost) as total_shipping_cost,
    SUM(f.profit) as profit
FROM fact_sales f
JOIN dim_location l ON f.location_id = l.location_id
GROUP BY 1
ORDER BY sales DESC;
