import json
import csv

# Input and output filenames
json_filename = "tesla_mentions_20250326.json"  # Replace with your actual JSON filename
csv_filename = "newsapi_tesla2.csv"

# Load JSON data
with open(json_filename, "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# Write to CSV
with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    
    # Header row
    writer.writerow(["title", "publishedAt", "source", "url", "tesla_sentences"])
    
    # Rows
    for article in data:
        writer.writerow([
            article.get("title", ""),
            article.get("publishedAt", ""),
            article.get("source", ""),
            article.get("url", ""),
            " | ".join(article.get("tesla_sentences", []))  # Join multiple sentences
        ])

print(f"Saved CSV to {csv_filename}")
