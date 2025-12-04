import pandas as pd
import os
import sqlite3

def save_data(dims, fact, output_dir, db_path=None):
    print(f"Saving to {output_dir}...")
    os.makedirs(output_dir, exist_ok=True)
        
    # save dims
    for name, df in dims.items():
        df.to_csv(f"{output_dir}/{name}.csv", index=False)
        df.to_parquet(f"{output_dir}/{name}.parquet", index=False)
        
    # save fact
    fact.to_csv(f"{output_dir}/fact_sales.csv", index=False)
    fact.to_parquet(f"{output_dir}/fact_sales.parquet", index=False)
    
    # sqlite dump
    if db_path:
        print(f"Updating DB: {db_path}")
        with sqlite3.connect(db_path) as conn:
            for name, df in dims.items():
                df.to_sql(name, conn, if_exists='replace', index=False)
            fact.to_sql('fact_sales', conn, if_exists='replace', index=False)
        
    print("Done.")
