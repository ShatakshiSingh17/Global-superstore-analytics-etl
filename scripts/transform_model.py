import pandas as pd

def build_dims(df):
    print("Building dimensions...")
    
    # Customer Dim
    dim_customer = df[['customer_id', 'customer_name', 'segment']].drop_duplicates().reset_index(drop=True)
    
    # Product Dim
    dim_product = df[['product_id', 'product_name', 'category', 'sub_category']].drop_duplicates().reset_index(drop=True)
    
    # Location Dim (needs surrogate key)
    # Added market
    dim_location = df[['city', 'state', 'country', 'region', 'market']].drop_duplicates().reset_index(drop=True)
    dim_location['location_id'] = dim_location.index + 1
    
    # Date Dim
    dates = df['order_date'].drop_duplicates().sort_values().reset_index(drop=True)
    dim_date = pd.DataFrame({'date': dates})
    dim_date['year'] = dim_date['date'].dt.year
    dim_date['quarter'] = dim_date['date'].dt.quarter
    dim_date['month'] = dim_date['date'].dt.month
    dim_date['day_name'] = dim_date['date'].dt.day_name()
    
    return {
        'dim_customer': dim_customer,
        'dim_product': dim_product,
        'dim_location': dim_location,
        'dim_date': dim_date
    }

def build_fact(df, dims):
    print("Building fact table...")
    
    fact = df.copy()
    
    # join with location to get the ID
    # Added market to join keys
    fact = fact.merge(dims['dim_location'], on=['city', 'state', 'country', 'region', 'market'], how='left')
    
    cols = [
        'order_id', 'order_date', 'ship_date', 'ship_mode',
        'customer_id', 'product_id', 'location_id',
        'sales', 'quantity', 'discount', 'profit',
        'shipping_cost', 'order_priority'
    ]
    
    return fact[cols]

if __name__ == "__main__":
    # test run
    from extract import extract_data
    from transform_clean import clean_data
    
    df = clean_data(extract_data("../data/raw/Global_Superstore.csv"))
    dims = build_dims(df)
    fact = build_fact(df, dims)
    print(fact.head())
