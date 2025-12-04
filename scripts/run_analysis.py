import sqlite3
import pandas as pd
import os

def run_analysis():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data/analytics/retail_db.sqlite")
    sql_path = os.path.join(base_dir, "sql/kpi_analysis.sql")
    
    print(f"Connecting to DB: {db_path}")
    conn = sqlite3.connect(db_path)
    
    with open(sql_path, 'r') as f:
        sql_script = f.read()
        
    # Split by semicolon to execute individual queries
    queries = sql_script.split(';')
    
    for i, query in enumerate(queries):
        query = query.strip()
        if not query:
            continue
            
        print(f"\n--- Executing Query {i+1} ---")
        # Extract comment if present
        lines = query.split('\n')
        for line in lines:
            if line.startswith('--'):
                print(line)
                
        try:
            df = pd.read_sql_query(query, conn)
            print(df)
        except Exception as e:
            print(f"Error executing query: {e}")
            
    conn.close()

if __name__ == "__main__":
    run_analysis()
