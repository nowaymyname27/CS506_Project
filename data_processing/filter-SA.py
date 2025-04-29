import pandas as pd

df1 = pd.read_csv("news_sentiment.csv")
df2 = pd.read_csv("reddit_sentiment.csv")

df1 = df1.rename(columns={'Published': 'date'})
df1['date'] = df1['date'].str.replace('"', '') 
df1['date'] = pd.to_datetime(df1['date'], format='%a, %d %b %Y %H:%M:%S %Z')
df1['date'] = df1['date'].dt.strftime('%Y-%m-%d')

filtered_df1 = df1[["date", "predicted_sentiment", "confidence"]]
filtered_df1.to_csv("news_sentiment_filtered.csv", index=False)
print(f"The filtered data has been saved to news_sentiment_filtered.csv")

filtered_df2 = df2[["date", "predicted_sentiment", "confidence"]]
filtered_df2.to_csv("reddit_sentiment_filtered.csv", index=False)
print(f"The filtered data has been saved to reddit_sentiment_filtered.csv")