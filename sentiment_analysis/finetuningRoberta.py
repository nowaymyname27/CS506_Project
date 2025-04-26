import pandas as pd
import re
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from datasets import Dataset
from transformers import RobertaTokenizer, RobertaForSequenceClassification, Trainer, TrainingArguments

# STEP 1: Load Data
reddit = pd.read_csv("data/Reddit_Data.csv")
twitter = pd.read_csv("data/Twitter_Data.csv")

# STEP 2: Combine the datasets
df = pd.concat([reddit, twitter], ignore_index=True)

# STEP 3: Clean text
def clean_text(text):
    text = re.sub(r'http\S+', '', text)  # remove links
    text = re.sub(r'@\w+', '', text)     # remove mentions
    text = re.sub(r'#\w+', '', text)     # remove hashtags
    text = re.sub(r'\d+', '', text)      # remove numbers
    text = re.sub(r'[^\w\s]', '', text)  # remove punctuation
    text = text.lower().strip()          # to lowercase
    return text

df['clean_text'] = df['clean_text'].astype(str).apply(clean_text)

# STEP 4: Encode labels (assuming 'category' column contains sentiment)
label_encoder = LabelEncoder()
df['label'] = label_encoder.fit_transform(df['category'])  # 0 = negative, 1 = neutral, 2 = positive
df = df.sample(n=100000, random_state=42).reset_index(drop=True)
# STEP 5: Split data
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df['clean_text'], df['label'], test_size=0.1, random_state=42)

# STEP 6: Tokenization
tokenizer = RobertaTokenizer.from_pretrained("roberta-base")

train_encodings = tokenizer(list(train_texts), truncation=True, padding=True)
val_encodings = tokenizer(list(val_texts), truncation=True, padding=True)

# Convert to HuggingFace Dataset
train_dataset = Dataset.from_dict({
    'input_ids': train_encodings['input_ids'],
    'attention_mask': train_encodings['attention_mask'],
    'label': list(train_labels)
})
val_dataset = Dataset.from_dict({
    'input_ids': val_encodings['input_ids'],
    'attention_mask': val_encodings['attention_mask'],
    'label': list(val_labels)
})

# STEP 7: Load model
model = RobertaForSequenceClassification.from_pretrained("roberta-base", num_labels=3)

# STEP 8: Training arguments
training_args = TrainingArguments(
    output_dir="./roberta_tesla_sentiment",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    save_total_limit=2,
    load_best_model_at_end=True
)

# STEP 9: Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer
)

# STEP 10: Train & Save
trainer.train()
trainer.save_model("./roberta_tesla_sentiment_100000")
tokenizer.save_pretrained("./roberta_tesla_sentiment_100000")
