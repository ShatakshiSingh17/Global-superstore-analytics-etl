import os
from extract import extract_data
from transform_clean import clean_data
from transform_model import build_dims, build_fact
from load import save_data

def main():
    # setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, "data/raw/Superstore.csv")
    out_dir = os.path.join(base_dir, "data/analytics")
    db_path = os.path.join(out_dir, "retail_db.sqlite")
    
    # run pipeline
    try:
        df = extract_data(raw_path)
        df = clean_data(df)
        
        dims = build_dims(df)
        fact = build_fact(df, dims)
        
        save_data(dims, fact, out_dir, db_path)
        
        print("\nSuccess! Data is ready.")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()
