import pandas as pd

def process_file(input_file, columns_to_keep, output_file):
    df = pd.read_csv(input_file)
    filtered_df = df[columns_to_keep]
    filtered_df.to_csv(output_file, index=False)
    print(f"The filtered data has been saved to {output_file}")

files_info = [
    ("SA_reddit_google.csv", ["date", "gcloud_sentiment_score", "gcloud_sentiment_magnitude"], "SAR_GO_Filtered.csv"),
    ("SA_news_titles_google.csv", ["publishedAt", "title_sentiment_score", "title_sentiment_magnitude"], "SANT_GO_Filtered.csv"),
    ("SA_reddit_RoBERTa.csv", ["date", "sentiment_label", "confidence"], "SAR_RO_Filtered.csv"),
    ("SA_reddit_Vader.csv", ["date", "vader_compound", "vader_label"], "SAR_VA_Filtered.csv")
]

for input_file, columns_to_keep, output_file in files_info:
    process_file(input_file, columns_to_keep, output_file)