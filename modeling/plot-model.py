import matplotlib.pyplot as plt
import pandas as pd

# ------------------ Fancy Cumulative Profit Plot ------------------

# Load trading results
trading_results = pd.read_csv("Trading_Strategy_Comparison.csv")

# Calculate cumulative profits
trading_results['Cumulative Model Profit'] = trading_results['Profit Model Strategy'].cumsum()
trading_results['Cumulative Always Buy Profit'] = trading_results['Profit Always Buy Strategy'].cumsum()

# Plot
plt.figure(figsize=(14, 7))

# Plot cumulative profits
plt.plot(trading_results['Date'], trading_results['Cumulative Model Profit'], label='Model Strategy', linewidth=2)
plt.plot(trading_results['Date'], trading_results['Cumulative Always Buy Profit'], label='Always Buy Strategy', linewidth=2, linestyle='--')

# Highlight buy days
buy_days = trading_results[trading_results['Model Prediction (1=buy, 0=skip)'] == 1]
plt.scatter(buy_days['Date'], buy_days['Cumulative Model Profit'], color='green', label='Buy Days', s=30, marker='o', alpha=0.7)

# Labels and grid
plt.xlabel('Date')
plt.ylabel('Cumulative Profit ($)')
plt.title('Cumulative Profit Over Time with Buy Days Highlighted')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
