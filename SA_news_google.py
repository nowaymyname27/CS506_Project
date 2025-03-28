import pandas as pd
from google.cloud import language_v1
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "sentiment-analysis-455017-0844dc588737.json"
df = pd.read_csv("newsapi_tesla2.csv")
client = language_v1.LanguageServiceClient()
def analyze_sentiment(text):
    try:
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
            language="en"  # force English to avoid language errors
        )
        response = client.analyze_sentiment(request={'document': document})
        sentiment = response.document_sentiment
        return pd.Series([sentiment.score, sentiment.magnitude])
    except Exception as e:
        print(f"Error processing text: {e}")
        return pd.Series([None, None])
df[['gcloud_sentiment_score', 'gcloud_sentiment_magnitude']] = df['tesla_sentences'].apply(analyze_sentiment)
df.to_csv("tesla_news_with_gcloud_sentiment.csv", index=False)
