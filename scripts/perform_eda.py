import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os

def perform_eda():
    print("Starting EDA...")
    
    # Setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data/analytics/retail_db.sqlite")
    img_dir = os.path.join(base_dir, "docs/images")
    os.makedirs(img_dir, exist_ok=True)
    
    # Connect to DB
    conn = sqlite3.connect(db_path)
    
    try:
        # Set style
        sns.set_theme(style="whitegrid")
        
        # 1. Monthly Sales Trend
        print("Generating Monthly Sales Trend...")
        query_trend = """
        SELECT d.date, SUM(f.sales) as sales
        FROM fact_sales f
        JOIN dim_date d ON f.order_date = d.date
        GROUP BY 1
        ORDER BY 1
        """
        df_trend = pd.read_sql(query_trend, conn)
        df_trend['date'] = pd.to_datetime(df_trend['date'])
        
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df_trend, x='date', y='sales', color='dodgerblue')
        plt.title('Global Monthly Sales Trend (2011-2015)')
        plt.xlabel('Date')
        plt.ylabel('Total Sales ($)')
        plt.tight_layout()
        plt.savefig(f"{img_dir}/monthly_sales_trend.png")
        plt.close()

        # 2. Profit by Market
        print("Generating Profit by Market...")
        query_market = """
        SELECT l.market, SUM(f.profit) as total_profit
        FROM fact_sales f
        JOIN dim_location l ON f.location_id = l.location_id
        GROUP BY 1
        ORDER BY 2 DESC
        """
        df_market = pd.read_sql(query_market, conn)
        
        plt.figure(figsize=(10, 6))
        # Fixed: Removed legend=False which causes error in some seaborn/matplotlib versions
        sns.barplot(data=df_market, x='market', y='total_profit', hue='market', palette='viridis')
        plt.title('Total Profit by Market')
        plt.xlabel('Market')
        plt.ylabel('Profit ($)')
        plt.tight_layout()
        plt.savefig(f"{img_dir}/market_profitability.png")
        plt.close()

        # 3. Category Scatter (Sales vs Profit)
        print("Generating Category Performance...")
        query_cat = """
        SELECT p.category, p.sub_category, SUM(f.sales) as sales, SUM(f.profit) as profit
        FROM fact_sales f
        JOIN dim_product p ON f.product_id = p.product_id
        GROUP BY 1, 2
        """
        df_cat = pd.read_sql(query_cat, conn)
        
        plt.figure(figsize=(10, 8))
        sns.scatterplot(data=df_cat, x='sales', y='profit', hue='category', s=100, alpha=0.7)
        plt.axhline(0, color='red', linestyle='--', linewidth=1)
        plt.title('Sub-Category Performance: Sales vs Profit')
        plt.xlabel('Total Sales ($)')
        plt.ylabel('Total Profit ($)')
        plt.legend(title='Category')
        plt.tight_layout()
        plt.savefig(f"{img_dir}/category_scatter.png")
        plt.close()
        
        # 4. Correlation Matrix
        print("Generating Correlation Matrix...")
        query_corr = """
        SELECT sales, quantity, discount, profit, shipping_cost
        FROM fact_sales
        """
        df_corr = pd.read_sql(query_corr, conn)
        corr = df_corr.corr()
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
        plt.title('Feature Correlation Matrix')
        plt.tight_layout()
        plt.savefig(f"{img_dir}/correlation_matrix.png")
        plt.close()
        
        print(f"EDA Complete. Images saved to {img_dir}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    perform_eda()
