import pandas as pd

try:
    df = pd.read_csv("data/raw/Superstore.csv", encoding='latin1')
    print("Columns:", list(df.columns))
    print("Head:", df.head(1))
    print("Shape:", df.shape)
except Exception as e:
    print(e)
