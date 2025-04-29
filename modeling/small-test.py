import pandas as pd

# Load data
df = pd.read_csv("model_input.csv")

# Make sure 'date' is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Only keep data up to October
df = df[df['date'].dt.month <= 10]

# Calculate price movement (open - previous close)
df['previous_close'] = df['close'].shift(1)
df['price_movement'] = df['open'] - df['previous_close']

# Drop NA rows
df.dropna(subset=['price_movement', 'sentiment_reddit', 'sentiment_news'], inplace=True)

# Calculate average Reddit sentiment
average_reddit_sentiment = df['sentiment_reddit'].mean()

# Focus only on days where:
#   - news sentiment is negative
#   - reddit sentiment is greater than average
mask = (df['sentiment_reddit'] > average_reddit_sentiment)
conflicting_sentiment = df[mask]

# How often does stock lose value in these cases?
loss_days = (conflicting_sentiment['price_movement'] < 0).sum()
total_conflict_days = len(conflicting_sentiment)

# Print results
print(f"Total days with negative news but above-average Reddit sentiment: {total_conflict_days}")
print(f"Days stock lost value after such conflicting sentiment: {loss_days}")
if total_conflict_days > 0:
    print(f"Percentage: {100 * loss_days / total_conflict_days:.2f}%")
else:
    print("No conflicting sentiment days found.")
