import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the full-year daily profit file
df = pd.read_csv("Trading_Strategy_Yearly.csv")

# Compute normalized cumulative profits
df['Cumulative Model Profit'] = np.cumsum(df['Profit Model Strategy'])
df['Cumulative Model Profit'] -= df['Cumulative Model Profit'].iloc[0]

df['Cumulative Always Buy Profit'] = np.cumsum(df['Profit Always Buy Strategy'])
df['Cumulative Always Buy Profit'] -= df['Cumulative Always Buy Profit'].iloc[0]

# Plot the results
plt.figure(figsize=(14, 7))
plt.plot(df['Date'], df['Cumulative Model Profit'], label='Model Strategy', linewidth=2)
plt.plot(df['Date'], df['Cumulative Always Buy Profit'], label='Always Buy Strategy', linestyle='--', linewidth=2)

# Highlight buy days
buy_days = df[df['Model Prediction (1=buy, 0=skip)'] == 1]
plt.scatter(buy_days['Date'], buy_days['Cumulative Model Profit'], color='green', label='Buy Days', s=30, marker='o', alpha=0.7)

plt.xlabel('Date')
plt.ylabel('Cumulative Profit ($)')
plt.title('Cumulative Profit Over Full Year (Model vs Always Buy)')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

