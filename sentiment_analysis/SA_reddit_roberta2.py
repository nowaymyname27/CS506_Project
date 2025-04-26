import pandas as pd
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification
model_id = "alika21/roberta-sentiment-trained"
tokenizer = RobertaTokenizer.from_pretrained(model_id)
model = RobertaForSequenceClassification.from_pretrained(model_id)
model.eval()
id2label = {0: "negative", 1: "neutral", 2: "positive"}
df = pd.read_csv("../final_output.csv")
print("Columns detected:", df.columns)
comment_column = "comment"  
if comment_column not in df.columns:
    raise ValueError(f"Expected column '{comment_column}' not found in CSV.")
def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)
        predicted_class = torch.argmax(probs, dim=1).item()
        confidence = probs[0][predicted_class].item()
    return id2label[predicted_class], round(confidence, 3)

df["predicted_sentiment"], df["confidence"] = zip(*df[comment_column].map(predict_sentiment))
output_path = "fine-tuned_Roberta_reddit.csv"
df.to_csv(output_path, index=False)