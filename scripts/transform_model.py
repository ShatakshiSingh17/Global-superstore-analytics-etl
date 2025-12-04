import pandas as pd

def create_dimension_tables(df):
    """
    Creates dimension tables from the cleaned dataframe.
    """
    print("Creating dimension tables...")
    
    # 1. Dim Customer
    dim_customer = df[['customer_id', 'customer_name', 'segment']].drop_duplicates().reset_index(drop=True)
    
    # 2. Dim Product
    dim_product = df[['product_id', 'product_name', 'category', 'sub_category']].drop_duplicates().reset_index(drop=True)
    
    # 3. Dim Location
    # We can create a surrogate key for location since there isn't a unique Location ID in source usually
    dim_location = df[['city', 'state', 'country', 'region']].drop_duplicates().reset_index(drop=True)
    dim_location['location_id'] = dim_location.index + 1
    
    # 4. Dim Date (Derived from Order Date)
    # Get all unique dates from order_date
    unique_dates = df['order_date'].drop_duplicates().sort_values().reset_index(drop=True)
    dim_date = pd.DataFrame({'date': unique_dates})
    dim_date['year'] = dim_date['date'].dt.year
    dim_date['quarter'] = dim_date['date'].dt.quarter
    dim_date['month'] = dim_date['date'].dt.month
    dim_date['day'] = dim_date['date'].dt.day
    dim_date['day_of_week'] = dim_date['date'].dt.day_name()
    dim_date['is_weekend'] = dim_date['day_of_week'].isin(['Saturday', 'Sunday'])
    
    dims = {
        'dim_customer': dim_customer,
        'dim_product': dim_product,
        'dim_location': dim_location,
        'dim_date': dim_date
    }
    
    print("Dimension tables created.")
    return dims

def create_fact_table(df, dims):
    """
    Creates the fact table by merging with dimensions to get surrogate keys (if any) 
    or just ensuring foreign keys exist.
    """
    print("Creating fact table...")
    
    # Start with base columns
    fact_sales = df.copy()
    
    # Merge with Dim Location to get Location ID
    dim_location = dims['dim_location']
    fact_sales = fact_sales.merge(dim_location, on=['city', 'state', 'country', 'region'], how='left')
    
    # Select columns for Fact Table
    # We keep the natural keys (Customer ID, Product ID, Order Date) as FKs
    # And the new surrogate key Location ID
    fact_cols = [
        'order_id', 
        'order_date',       # FK to Dim Date
        'ship_date', 
        'ship_mode',
        'customer_id',      # FK to Dim Customer
        'product_id',       # FK to Dim Product
        'location_id',      # FK to Dim Location
        'sales', 
        'quantity', 
        'discount', 
        'profit'
    ]
    
    fact_sales = fact_sales[fact_cols]
    
    print(f"Fact table created. Shape: {fact_sales.shape}")
    return fact_sales

if __name__ == "__main__":
    # For testing
    from extract import extract_data
    from transform_clean import clean_data
    
    RAW_PATH = "../data/raw/Superstore.csv"
    df = extract_data(RAW_PATH)
    df_clean = clean_data(df)
    dims = create_dimension_tables(df_clean)
    fact = create_fact_table(df_clean, dims)
    print(fact.head())
