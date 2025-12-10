import pandas as pd
import os

def extract_data(filepath):
    # simple load wrapper
    print(f"Loading raw data from {filepath}...")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing file: {filepath}")
    
    # try utf-8 first, fallback to latin1 if needed
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
    except UnicodeDecodeError:
        print("UTF-8 failed, trying latin1")
        df = pd.read_csv(filepath, encoding='latin1')
        
    print(f"Loaded {len(df)} rows")
    return df

if __name__ == "__main__":
    # quick test
    # Ensure data/raw exists
    os.makedirs("../data/raw", exist_ok=True)
    # Changed to Global_Superstore.csv
    df = extract_data("../data/raw/Global_Superstore.csv")
    print(df.head())
