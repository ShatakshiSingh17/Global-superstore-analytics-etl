import pandas as pd
import os

def extract_data(filepath):
    """
    Reads the raw CSV data.
    """
    print(f"Extracting data from {filepath}...")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    # The dataset might have different encodings, trying common ones
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
    except UnicodeDecodeError:
        print("UTF-8 decode failed, trying latin1...")
        df = pd.read_csv(filepath, encoding='latin1')
        
    print(f"Data extracted successfully. Shape: {df.shape}")
    return df

if __name__ == "__main__":
    # For testing
    RAW_PATH = "../data/raw/Superstore.csv"
    df = extract_data(RAW_PATH)
    print(df.head())
