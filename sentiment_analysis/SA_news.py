import pandas as pd
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification

# Load model and tokenizer from Hugging Face
model_id = "alika21/roberta-sentiment-trained"
tokenizer = RobertaTokenizer.from_pretrained(model_id)
model = RobertaForSequenceClassification.from_pretrained(model_id)
model.eval()

# Label map (adjust if needed)
id2label = {0: "negative", 1: "neutral", 2: "positive"}

# Load headlines from file
df = pd.read_csv("news_api/Data/tesla_2024_clean.csv")

# Predict sentiment for each headline
def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)
        predicted_class = torch.argmax(probs, dim=1).item()
        confidence = probs[0][predicted_class].item()
    return id2label[predicted_class], round(confidence, 3)

# Apply prediction
df["predicted_sentiment"], df["confidence"] = zip(*df["Title"].map(predict_sentiment))

# Save to CSV
output_path = "sentiment_analysis/news_sentiment.csv"
df.to_csv(output_path, index=False)

print(f"Saved predictions to: {output_path}")

