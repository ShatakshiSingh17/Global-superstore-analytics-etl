import pandas as pd
import numpy as np

def clean_data(df):
    """
    Cleans the dataframe:
    - Standardizes column names
    - Converts dates
    - Handles missing values
    - Validates data
    """
    print("Starting data cleaning...")
    
    # Standardize column names (lowercase, replace spaces with underscores)
    df.columns = [c.lower().replace(' ', '_').replace('-', '_') for c in df.columns]
    
    # Convert Date columns
    date_cols = ['order_date', 'ship_date']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
    # Handle missing values (if any)
    # For this dataset, we might drop rows with missing critical IDs or fill others
    # Checking for nulls
    null_counts = df.isnull().sum()
    if null_counts.sum() > 0:
        print("Found missing values:")
        print(null_counts[null_counts > 0])
        # Simple strategy: drop rows where Order ID is missing (if any)
        df = df.dropna(subset=['order_id'])
        
    # Anomaly Detection / Validation
    # Ensure Sales, Quantity, Profit are numeric
    num_cols = ['sales', 'quantity', 'profit', 'discount']
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # Remove duplicates
    initial_rows = len(df)
    df = df.drop_duplicates()
    if len(df) < initial_rows:
        print(f"Removed {initial_rows - len(df)} duplicate rows.")
        
    print("Data cleaning completed.")
    return df

if __name__ == "__main__":
    # For testing
    from extract import extract_data
    RAW_PATH = "../data/raw/Superstore.csv"
    df = extract_data(RAW_PATH)
    df_clean = clean_data(df)
    print(df_clean.info())
