import pandas as pd
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification

model_id = "alika21/roberta-sentiment-trained"
tokenizer = RobertaTokenizer.from_pretrained(model_id)
model = RobertaForSequenceClassification.from_pretrained(model_id)
model.eval()

id2label = {0: "negative", 1: "neutral", 2: "positive"}

column_names = ["comment", "date"]
df = pd.read_csv("reddit_code/final_output.csv", names=column_names)

print("Data sample:")
print(df.head())

def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)
        predicted_class = torch.argmax(probs, dim=1).item()
        confidence = probs[0][predicted_class].item()
    return id2label[predicted_class], round(confidence, 3)

df["predicted_sentiment"], df["confidence"] = zip(*df["comment"].map(predict_sentiment))

output_path = "sentiment_analysis/fine-tuned_Roberta_reddit.csv"
df.to_csv(output_path, index=False)

print(f"Saved predictions to: {output_path}")
