import pandas as pd

# Create single sentiment column for numerical news sentiment
df1 = pd.read_csv("news_sentiment_filtered.csv")
if 'predicted_sentiment' in df1.columns and 'confidence' in df1.columns:
    df1['sentiment'] = df1['predicted_sentiment'].apply(lambda x: 0 if x == 'neutral'
                                                              else 1 if x == 'positive'
                                                              else -1 if x == 'negative'
                                                              else 0)
    df1['sentiment'] = df1['confidence'] * df1['sentiment'] 
    df1['sentiment'] = df1['sentiment'].round(3)
    df1[['date', 'sentiment']].to_csv("news_sentiment_processed.csv", index=False)
    print("✅ Operation 1: Processed news_sentiment_filtered.csv and saved to news_sentiment_processed.csv")

# Create single sentiment column for numerical reddit sentiment
df2 = pd.read_csv("reddit_sentiment_filtered.csv")
if 'predicted_sentiment' in df2.columns and 'confidence' in df2.columns:
    df2['sentiment'] = df2['predicted_sentiment'].apply(lambda x: 0 if x == 'neutral'
                                                              else 1 if x == 'positive'
                                                              else -1 if x == 'negative'
                                                              else 0)
    df2['sentiment'] = df2['confidence'] * df2['sentiment'] 
    df2['sentiment'] = df2['sentiment'].round(3)
    df2[['date', 'sentiment']].to_csv("reddit_sentiment_processed.csv", index=False)
    print("✅ Operation 2: Processed reddit_sentiment_filtered.csv and saved to reddit_sentiment_processed.csv")

# Create single sentiment column for deterministic news sentiment
df3 = pd.read_csv("news_sentiment_filtered.csv")
if 'predicted_sentiment' in df3.columns and 'confidence' in df3.columns:
    df3['sentiment'] = df3['predicted_sentiment'].apply(lambda x: 0 if x == 'neutral'
                                                              else 1 if x == 'positive'
                                                              else -1 if x == 'negative'
                                                              else 0)
    df3['sentiment'] = df3['sentiment'].round(3)
    df3[['date', 'sentiment']].to_csv("news_sentiment_processed_DET.csv", index=False)
    print("✅ Operation 3: Processed news_sentiment_filtered.csv and saved to news_sentiment_processed_DET.csv")

# Create single sentiment column for deterministic reddit sentiment
df4 = pd.read_csv("reddit_sentiment_filtered.csv")
if 'predicted_sentiment' in df4.columns and 'confidence' in df4.columns:
    df4['sentiment'] = df4['predicted_sentiment'].apply(lambda x: 0 if x == 'neutral'
                                                              else 1 if x == 'positive'
                                                              else -1 if x == 'negative'
                                                              else 0)
    df4[['date', 'sentiment']].to_csv("reddit_sentiment_processed_DET.csv", index=False)
    df4['sentiment'] = df4['sentiment'].round(3)
    print("✅ Operation 4: Processed reddit_sentiment_filtered.csv and saved to reddit_sentiment_processed_DET.csv")