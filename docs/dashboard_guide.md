# Tableau Public Dashboard Guide

This guide details how to build the Retail Analytics dashboard using **Tableau Public** (free version).

## 1. Prepare Data
Tableau Public works best with flat files (CSV/Excel). We will use the CSV files generated in `data/analytics/`.

**Files needed:**
- `fact_sales.csv`
- `dim_customer.csv`
- `dim_product.csv`
- `dim_location.csv`
- `dim_date.csv`

## 2. Connect Data in Tableau Public

1.  Open Tableau Public.
2.  Under **Connect**, select **Text file**.
3.  Navigate to `retail_analytics_etl/data/analytics/` and select `fact_sales.csv`.
4.  Once loaded, you will see the "Logical Layer" (canvas).
5.  Drag and drop the dimension files (`dim_customer.csv`, etc.) onto the canvas to create relationships.
    -   **Drag `dim_customer.csv`** next to `fact_sales`. Tableau should auto-detect the link on `Customer Id`.
    -   **Drag `dim_product.csv`**: Link on `Product Id`.
    -   **Drag `dim_location.csv`**: Link on `Location Id`.
    -   **Drag `dim_date.csv`**: Link `Order Date` (from Fact) to `Date` (from Dim).

*Tip: Ensure the "Performance Options" (Cardinality) are set to Many-to-One (Fact is Many, Dim is One) if asked, though Tableau usually handles this automatically.*

## 3. Create Calculated Fields

Go to **Sheet 1**. Right-click in the Data pane -> **Create Calculated Field**.

1.  **Profit Margin %**:
    ```
    SUM([Profit]) / SUM([Sales])
    ```
    *Right-click the new field -> Default Properties -> Number Format -> Percentage (1 decimal).*

2.  **Average Order Value (AOV)**:
    ```
    SUM([Sales]) / COUNTD([Order Id])
    ```

## 4. Build Visualizations

### Sheet 1: KPI Cards
-   Drag `Sales` to Text.
-   Drag `Profit` to Text.
-   Drag `Profit Margin %` to Text.
-   Format the text to be large and bold (e.g., "Sales: <SUM(Sales)>").

### Sheet 2: Regional Performance (Map)
-   Double-click `State` (ensure it has the geographic role).
-   Drag `Sales` to Color.
-   Drag `Region` to Filters (optional).

### Sheet 3: Monthly Trend
-   Drag `Date` (from dim_date) to Columns. Right-click -> Select "Month" (May 2015 format).
-   Drag `Sales` to Rows.
-   Drag `Profit` to Rows (Dual Axis if you like, or just separate lines).

### Sheet 4: Top Products
-   Drag `Product Name` to Rows.
-   Drag `Profit` to Columns.
-   Sort descending.
-   Filter on `Product Name` -> Top 10 by Profit.

## 5. Assemble Dashboard

1.  Click the **New Dashboard** button (bottom tab).
2.  Set Size to **Automatic** or **Fixed (1200 x 800)**.
3.  Drag your sheets onto the canvas.
    -   Put KPIs at the top.
    -   Map and Trend in the middle.
    -   Top Products at the bottom.
4.  Add a Title text box: "Retail Sales Performance".

## 6. Publish
1.  File -> **Save to Tableau Public As...**
2.  Sign in to your Tableau Public account.
3.  Name your workbook (e.g., "Retail Analytics Demo").
4.  The dashboard is now live on the web!

## 7. Update Data
Since Tableau Public doesn't auto-refresh from local files:
1.  Run your ETL script (`python scripts/main.py`) to get new data.
2.  Open the workbook in Tableau Public Desktop.
3.  Go to Data Source tab -> Refresh.
4.  Save to Tableau Public again to overwrite.
