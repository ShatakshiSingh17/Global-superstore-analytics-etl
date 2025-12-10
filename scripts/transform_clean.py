import pandas as pd
import numpy as np

def clean_data(df):
    print("Cleaning data...")
    
    # fix column names
    df.columns = [c.lower().replace(' ', '_').replace('-', '_') for c in df.columns]
    
    # handle dates
    for col in ['order_date', 'ship_date']:
        if col in df.columns:
            # Global Superstore uses DD-MM-YYYY (e.g. 31-07-2012)
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
            
    # basic null check
    if df['order_id'].isnull().any():
        print("Dropping rows with missing Order ID")
        df = df.dropna(subset=['order_id'])

    # Fill missing postal codes (common in Global dataset)
    if 'postal_code' in df.columns:
        df['postal_code'] = df['postal_code'].fillna('00000')
        
    # ensure numerics are actually numeric
    # Added shipping_cost
    num_cols = ['sales', 'quantity', 'profit', 'discount', 'shipping_cost']
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
    df = extract_data("../data/raw/Global_Superstore.csv")
    print(clean_data(df).info())
