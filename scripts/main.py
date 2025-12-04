import os
from extract import extract_data
from transform_clean import clean_data
from transform_model import create_dimension_tables, create_fact_table
from load import load_data

def main():
    # Configuration
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RAW_PATH = os.path.join(BASE_DIR, "data/raw/Superstore.csv")
    ANALYTICS_DIR = os.path.join(BASE_DIR, "data/analytics")
    DB_PATH = os.path.join(BASE_DIR, "data/analytics/retail_db.sqlite")
    
    # 1. Extract
    try:
        df_raw = extract_data(RAW_PATH)
    except Exception as e:
        print(f"Extraction failed: {e}")
        return

    # 2. Transform (Clean)
    df_clean = clean_data(df_raw)
    
    # 3. Transform (Model)
    dims = create_dimension_tables(df_clean)
    fact = create_fact_table(df_clean, dims)
    
    # 4. Load
    load_data(dims, fact, ANALYTICS_DIR, DB_PATH)
    
    print("\nETL Pipeline finished successfully!")
    print(f"Analytics data available in: {ANALYTICS_DIR}")
    print(f"SQLite Database: {DB_PATH}")

if __name__ == "__main__":
    main()
