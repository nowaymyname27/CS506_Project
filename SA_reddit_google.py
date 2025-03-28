import pandas as pd
from google.cloud import language_v1
df = pd.read_csv("final_output.csv", header=None)
df.columns = ['score', 'date', 'user', 'url', 'comment']
client = language_v1.LanguageServiceClient()
def analyze_sentiment(text):
    try:
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.analyze_sentiment(request={'document': document})
        sentiment = response.document_sentiment
        return pd.Series([sentiment.score, sentiment.magnitude])
    except Exception as e:
        print(f"Error: {e}")
        return pd.Series([None, None])
df[['gcloud_sentiment_score', 'gcloud_sentiment_magnitude']] = df['comment'].apply(analyze_sentiment)
df.to_csv("reddit_comments_with_gcloud_sentiment.csv", index=False)

