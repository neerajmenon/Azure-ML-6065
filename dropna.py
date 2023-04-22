import pandas as pd

names = ['400_households.csv','400_products.csv','400_transactions.csv']

# Load CSV file
for file in names:
    df = pd.read_csv(file)
    df = df.dropna()    
    fname = file.split('.')[0]+'_clean.csv'
    df.to_csv(fname, index=False)
