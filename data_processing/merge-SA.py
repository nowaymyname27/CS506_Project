import pandas as pd

# Import the files
tsla_df = pd.read_csv("tsla_daily_2024.csv")
reddit_df = pd.read_csv("reddit_sentiment_processed.csv")
news_df = pd.read_csv("news_sentiment_processed.csv")
reddit_DET_df = pd.read_csv("reddit_sentiment_processed_DET.csv")
news_DET_df = pd.read_csv("news_sentiment_processed.csv")

# Average all the sentiments on each day
reddit_avg = reddit_df.groupby('date')['sentiment'].mean().reset_index()
news_avg = news_df.groupby('date')['sentiment'].mean().reset_index()
reddit_DET_avg = reddit_DET_df.groupby('date')['sentiment'].mean().reset_index()
news_DET_avg = news_DET_df.groupby('date')['sentiment'].mean().reset_index()

# Rename for merging
reddit_avg.rename(columns={'sentiment': 'sentiment_reddit'}, inplace=True)
news_avg.rename(columns={'sentiment': 'sentiment_news'}, inplace=True)
reddit_DET_avg.rename(columns={'sentiment': 'sentiment_reddit_det'}, inplace=True)
news_DET_avg.rename(columns={'sentiment': 'sentiment_news_det'}, inplace=True)

# Merge
merged_sentiment_df = pd.merge(reddit_avg, news_avg[['date', 'sentiment_news']], on='date', how='outer')
merged_sentiment_df = pd.merge(merged_sentiment_df, reddit_DET_avg[['date', 'sentiment_reddit_det']], on='date', how='outer')
merged_sentiment_df = pd.merge(merged_sentiment_df, news_DET_avg[['date', 'sentiment_news_det']], on='date', how='outer')

# Save the averaged and merged files
merged_sentiment_df.to_csv("sentiment_merged.csv", index=False)
print(f"✅ The merged data has been saved to sentiment_merged.csv")