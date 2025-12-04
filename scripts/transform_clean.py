import pandas as pd
import numpy as np

def clean_data(df):
    print("Cleaning data...")
    
    # fix column names
    df.columns = [c.lower().replace(' ', '_').replace('-', '_') for c in df.columns]
    
    # handle dates
    for col in ['order_date', 'ship_date']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
    # basic null check
    if df['order_id'].isnull().any():
        print("Dropping rows with missing Order ID")
        df = df.dropna(subset=['order_id'])
        
    # ensure numerics are actually numeric
    num_cols = ['sales', 'quantity', 'profit', 'discount']
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # dedup
    orig_len = len(df)
    df = df.drop_duplicates()
    if len(df) < orig_len:
        print(f"Dropped {orig_len - len(df)} duplicates")
        
    return df

if __name__ == "__main__":
    from extract import extract_data
    df = extract_data("../data/raw/Superstore.csv")
    print(clean_data(df).info())
