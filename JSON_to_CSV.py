import json
import csv

# Input and output filenames
json_filename = "newsapi_tesla_20250320.json"  # Replace with your actual JSON filename
csv_filename = "newsapi_tesla.csv"

# Load JSON data
with open(json_filename, "r", encoding="utf-8") as json_file:
    articles = json.load(json_file)

# Open CSV file for writing
with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)

    # Write header row
    writer.writerow(["Source", "Author", "Title", "Description", "URL", "Published At"])

    # Write article data
    for article in articles:
        source = article.get("source", {}).get("name", "N/A")
        author = article.get("author", "N/A")
        title = article.get("title", "N/A")
        description = article.get("description", "N/A")
        url = article.get("url", "N/A")
        published_at = article.get("publishedAt", "N/A")

        writer.writerow([source, author, title, description, url, published_at])

print(f"Converted JSON to CSV: {csv_filename}")
