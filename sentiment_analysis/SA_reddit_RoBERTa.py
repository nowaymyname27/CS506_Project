import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

df = pd.read_csv("final_output.csv", header=None)
df.columns = ['score', 'date', 'user', 'url', 'comment']

model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, truncation=True, max_length=512)

def analyze_sentiment(text):
    try:
        result = sentiment_pipeline(str(text))[0]
        if result['label'] == "LABEL_2":
            label = "positive"
        if result['label'] == "LABEL_0":
            label = "negative"
        if result['label'] == "LABEL_1":
            label = "neutral"

        confidence = round(result['score'] * 100, 2) 
        return pd.Series([label, confidence])
    except:
        return pd.Series([None, None])
df[['sentiment_label', 'confidence']] = df['comment'].apply(analyze_sentiment)
df.to_csv("SA_reddit_roberta.csv", index=False)


