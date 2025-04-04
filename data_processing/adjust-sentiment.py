import pandas as pd
import random

df1 = pd.read_csv("SAR_GO_Filtered.csv")
if 'gcloud_sentiment_score' in df1.columns and 'gcloud_sentiment_magnitude' in df1.columns:
    df1['sentiment'] = df1['gcloud_sentiment_score'] * df1['gcloud_sentiment_magnitude']
    df1[['date', 'sentiment']].to_csv("SAR_GO_Processed.csv", index=False)
    print("Operation 1: Processed SAR_GO_Filtered.csv and saved to SAR_GO_Processed.csv")

df2 = pd.read_csv("SANT_GO_Filtered.csv")
if 'title_sentiment_score' in df2.columns:
    df2 = df2.rename(columns={'title_sentiment_score': 'sentiment'})
    df2 = df2.drop(columns=['title_sentiment_magnitude'])
    df2[['date', 'sentiment']].to_csv("SANT_GO_Processed.csv", index=False)
    print("Operation 2: Processed SANT_GO_Filtered.csv and saved to SANT_GO_Processed.csv")

df3 = pd.read_csv("SAR_RO_Filtered.csv")
if 'sentiment_label' in df3.columns and 'confidence' in df3.columns:
    df3['sentiment'] = df3['sentiment_label'].apply(lambda x: random.choice([1000, -1000]) if x == 'neutral'
                                                              else 100 if x == 'positive'
                                                              else -100 if x == 'negative'
                                                              else 0)
    df3['sentiment'] = df3['confidence'] / df3['sentiment'] 
    df3[['date', 'sentiment']].to_csv("SAR_RO_Processed.csv", index=False)
    print("Operation 3: Processed SAR_RO_Filtered.csv and saved to SAR_RO_Processed.csv")

df4 = pd.read_csv("SAR_VA_Filtered.csv")
if 'vader_compound' in df4.columns:
    df4 = df4.rename(columns={'vader_compound': 'sentiment'})
    df4 = df4.drop(columns=['vader_label'])
    df4[['date', 'sentiment']].to_csv("SAR_VA_Processed.csv", index=False)
    print("Operation 4: Processed SAR_VA_Filtered.csv and saved to SAR_VA_Processed.csv")