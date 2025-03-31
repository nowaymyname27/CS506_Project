import requests
import time
from datetime import datetime, timedelta
import csv

# Replace with your actual API key
API_KEY = ""
url = "https://api.marketaux.com/v1/news/all"


# Define search parameters
params = {
    "api_token": API_KEY,
    "symbols": "TSLA",  # Tesla stock ticker
    "published_after": "2025-02-01",
    "published_before": "2025-03-01",
    "must_have_entities": True,
    "filter_entities": True,
    "limit": 3,  # Max allowed per request based on plan
    "page": 1
}

# File to store previously found articles
csv_filename = "found_articles.csv"

# Load existing articles to avoid duplicates
found_articles = set()
try:
    with open(csv_filename, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            found_articles.add(row[4])  # Store URLs to check for duplicates
except FileNotFoundError:
    pass  # No previous data, start fresh

# Open CSV file to store new results
with open(csv_filename, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # If file was empty, add header
    if not found_articles:
        writer.writerow(["Title", "Source", "Published Date", "Sentiment Score", "URL"])

    # Make up to 100 requests
    for request_num in range(1, 101):  # 100 requests max per day
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("data", [])

            new_articles_found = 0
            for article in articles:
                title = article.get("title", "N/A")
                source = article.get("source", "N/A")
                published = article.get("published_at", "N/A")
                url = article.get("url", "N/A")
                sentiment_score = "N/A"

                # Extract sentiment for Tesla
                for entity in article.get("entities", []):
                    if entity["symbol"] == "TSLA":
                        sentiment_score = entity.get("sentiment_score", "N/A")

                # Check if article is new
                if url not in found_articles:
                    writer.writerow([title, source, published, sentiment_score, url])
                    found_articles.add(url)
                    new_articles_found += 1

            # Stop if no new articles are found
            if new_articles_found == 0:
                print("No new articles found. Adjusting parameters...")
                break  # Stop wasting requests if only duplicates are coming

            print(f"Request {request_num}: Found {new_articles_found} new articles.")

            # Wait a bit to avoid hitting rate limits
            time.sleep(1)

        else:
            print(f"Error {response.status_code}: {response.text}")
            break  # Stop on error

print(f"Saved Tesla news data to {csv_filename}")
