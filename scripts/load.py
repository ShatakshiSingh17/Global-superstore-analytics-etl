import pandas as pd
import os
import sqlite3

def load_data(dims, fact, output_dir, db_path=None):
    """
    Saves the dimension and fact tables to CSV/Parquet and optionally SQLite.
    """
    print(f"Loading data to {output_dir}...")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Save Dimensions
    for name, df in dims.items():
        # Save as CSV
        csv_path = os.path.join(output_dir, f"{name}.csv")
        df.to_csv(csv_path, index=False)
        
        # Save as Parquet (good for analytics)
        parquet_path = os.path.join(output_dir, f"{name}.parquet")
        df.to_parquet(parquet_path, index=False)
        
    # Save Fact
    fact.to_csv(os.path.join(output_dir, "fact_sales.csv"), index=False)
    fact.to_parquet(os.path.join(output_dir, "fact_sales.parquet"), index=False)
    
    # Load to SQLite
    if db_path:
        print(f"Loading data into SQLite DB: {db_path}")
        conn = sqlite3.connect(db_path)
        
        for name, df in dims.items():
            df.to_sql(name, conn, if_exists='replace', index=False)
            
        fact.to_sql('fact_sales', conn, if_exists='replace', index=False)
        
        conn.close()
        
    print("Data loading completed.")

if __name__ == "__main__":
    # Integration test handled in main.py
    pass
