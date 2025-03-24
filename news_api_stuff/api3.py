import requests
import json
import time
from datetime import datetime, timezone  # Import timezone

# Replace with your actual News API key
API_KEY = "4a3d2a0f17b54952908d9f7ce2fb621d"

# Define the endpoint
url = "https://newsapi.org/v2/everything"

# Define the parameters
params = {
    "q": "Tesla",  # Search for Tesla-related news
    "from": "2025-02-20",  # Start date
    "to": "2025-02-28",  # End date
    "sortBy": "relevancy",  # Prioritize relevant articles
    "language": "en",  # English articles only
    "apiKey": API_KEY,
    "pageSize": 100,  # Max articles per request
    "page": 1  # Start at page 1
}

# File to store raw JSON
json_filename = f"newsapi_tesla_{datetime.now(timezone.utc).strftime('%Y%m%d')}.json"

# Store all retrieved data
all_articles = []

while True:
    response = requests.get(url, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            print("JSON decoding failed. Empty response received.")
            break  # Stop execution if response is empty

        articles = data.get("articles", [])
        if not articles:
            print("No more articles found. Stopping pagination.")
            break  # Stop if no more articles

        all_articles.extend(articles)  # Collect all articles
        print(f"Page {params['page']}: Retrieved {len(articles)} articles.")

        params["page"] += 1  # Move to next page
        time.sleep(1)  # Avoid hitting rate limits

        # Stop after 500 articles (News API free tier limit)
        if len(all_articles) >= 500:
            print("Reached News API free tier limit. Stopping.")
            break

    else:
        print(f"Error {response.status_code}: {response.text}")
        break  # Stop on error

# Save JSON file
with open(json_filename, "w", encoding="utf-8") as file:
    json.dump(all_articles, file, indent=4)

print(f"Saved Tesla news data to {json_filename}")
