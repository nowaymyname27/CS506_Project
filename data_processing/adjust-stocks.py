import pandas as pd

df = pd.read_csv("tsla_daily_2024.csv")

df.columns = df.columns.str.lower()
df = df[['date', 'open', 'close']]
df['date'] = df['date'].astype(str).str[:10]
df[['open', 'close']] = df[['open', 'close']].round(2)

df.to_csv("tsla_processed_2024.csv", index=False)
print("The data has been processed and saved to tsla_processed_2024.csv")