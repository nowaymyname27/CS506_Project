import pandas as pd

df = pd.read_csv("tsla_dec_daily.csv")

df.columns = df.columns.str.lower()
df = df[['date', 'open', 'close']]
df['date'] = df['date'].astype(str).str[:10]

df.to_csv("TSLA_Dec_Processed.csv", index=False)
print("The data has been processed and saved to TSLA_Dec_Processed.csv")