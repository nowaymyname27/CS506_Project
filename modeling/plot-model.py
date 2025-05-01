import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === 1. Monthly Profit Comparison ===
df_profit = pd.read_csv("Trading_Strategy_Yearly.csv")
df_profit['Date'] = pd.to_datetime(df_profit['Date'])
df_profit['Month'] = df_profit['Date'].dt.strftime('%b')

monthly_profit = df_profit.groupby('Month')[['Profit Model Strategy', 'Profit Always Buy Strategy']].sum()
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_profit = monthly_profit.reindex(month_order)

plt.figure(figsize=(12, 6))
ax = monthly_profit.plot(kind='bar', edgecolor='black')
plt.axhline(0, color='black', linewidth=1)
handles, _ = ax.get_legend_handles_labels()
ax.legend(handles, ['Model Strategy', 'Always Buy'])
plt.title("Monthly Profit: Model vs Always Buy Strategy")
plt.ylabel("Total Profit ($)")
plt.xlabel("Month")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("plots/Monthly_Profit_Comparison.png")
plt.close()

# === 2. Buy Signal Timeline (Lollipop Plot) ===
buy_dates = df_profit[df_profit['Model Prediction (1=buy, 0=skip)'] == 1]['Date']
plt.figure(figsize=(14, 4))
plt.vlines(buy_dates, ymin=0, ymax=1, color='blue', alpha=0.7)
plt.scatter(buy_dates, [1]*len(buy_dates), color='blue', label='Buy Signal', s=10)
plt.title("Buy Signal Timeline (Only Buy Days Marked)")
plt.xlabel("Date")
plt.yticks([])
plt.tight_layout()
plt.savefig("plots/Buy_Signal_Timeline.png")
plt.close()

# === 3. Smoothed Buy Frequency (Rolling Average) ===
df_profit['Rolling Buy Frequency'] = df_profit['Model Prediction (1=buy, 0=skip)'].rolling(window=7).mean()
plt.figure(figsize=(14, 4))
plt.plot(df_profit['Date'], df_profit['Rolling Buy Frequency'], label='7-Day Rolling Buy Frequency', color='blue')
plt.title("Smoothed Buy Frequency Over Time")
plt.ylabel("Buy Probability")
plt.xlabel("Date")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig("plots/Buy_Frequency_Smoothed.png")
plt.close()

# === 4. Cumulative Sentiment vs Stock Price ===
df_sentiment = pd.read_csv("model_input.csv")
df_sentiment['date'] = pd.to_datetime(df_sentiment['date'])

fig, ax1 = plt.subplots(figsize=(14, 6))
ax1.plot(df_sentiment['date'], df_sentiment['close'], label='TSLA Close Price', linewidth=2)
ax1.set_ylabel('Close Price ($)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

ax2 = ax1.twinx()
ax2.plot(df_sentiment['date'], df_sentiment['sentiment_reddit'], color='green', alpha=0.5, label='Numerical Sentiment')
ax2.set_ylabel("Numerical Sentiment", color='green')
ax2.tick_params(axis='y', labelcolor='green')

plt.title("Cumulative Sentiment vs. TSLA Closing Price")
fig.tight_layout()
plt.savefig("plots/Sentiment_vs_Price.png")
plt.close()

# === 5. Cumulative Profit Over Full Year ===
df = pd.read_csv("Trading_Strategy_Yearly.csv")
df['Date'] = pd.to_datetime(df['Date'])
df['Cumulative Model Profit'] = np.cumsum(df['Profit Model Strategy'])
df['Cumulative Model Profit'] -= df['Cumulative Model Profit'].iloc[0]
df['Cumulative Always Buy Profit'] = np.cumsum(df['Profit Always Buy Strategy'])
df['Cumulative Always Buy Profit'] -= df['Cumulative Always Buy Profit'].iloc[0]

plt.figure(figsize=(14, 7))
plt.plot(df['Date'], df['Cumulative Model Profit'], label='Model Strategy', linewidth=2)
plt.plot(df['Date'], df['Cumulative Always Buy Profit'], label='Always Buy Strategy', linestyle='--', linewidth=2)

buy_days = df[df['Model Prediction (1=buy, 0=skip)'] == 1]
plt.scatter(buy_days['Date'], buy_days['Cumulative Model Profit'], color='green', label='Buy Days', s=30, marker='o', alpha=0.7)

weekly_ticks = df.groupby(df['Date'].dt.isocalendar().week)['Date'].first()
plt.xticks(ticks=weekly_ticks, labels=weekly_ticks.dt.strftime('%b %d'), rotation=45)

plt.xlabel('Date')
plt.ylabel('Cumulative Profit ($)')
plt.title('Cumulative Profit Over Full Year (Model vs Always Buy)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/Yearly_Profit_Plot.png", dpi=300)
plt.close()
