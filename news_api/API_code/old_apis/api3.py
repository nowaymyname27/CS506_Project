import requests
import json
import time
import re
from datetime import datetime, timezone

API_KEY = ""
url = "https://newsapi.org/v2/everything"

params = {
    "q": "Tesla",
    "from": "2025-02-27",
    "to": "2025-02-28",
    "sortBy": "relevancy",
    "language": "en",
    "apiKey": API_KEY,
    "pageSize": 99,
    "page": 1
}

json_filename = f"tesla_mentions_{datetime.now(timezone.utc).strftime('%Y%m%d')}.json"
tesla_mentions = []

def extract_tesla_sentences(text):
    if not text:
        return []
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [s for s in sentences if "tesla" in s.lower()]

while True:
    response = requests.get(url, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            print("JSON decoding failed.")
            break

        articles = data.get("articles", [])
        if not articles:
            print("No more articles found.")
            break

        for article in articles:
            content = article.get("content", "")
            description = article.get("description", "")

            tesla_bits = extract_tesla_sentences(description) + extract_tesla_sentences(content)
            if tesla_bits:
                tesla_mentions.append({
                    "title": article.get("title"),
                    "publishedAt": article.get("publishedAt"),
                    "source": article.get("source", {}).get("name"),
                    "url": article.get("url"),
                    "tesla_sentences": tesla_bits
                })

        print(f"Page {params['page']}: Processed {len(articles)} articles.")
        params["page"] += 1
        time.sleep(1)

        if len(tesla_mentions) >= 500:
            print("Reached extraction limit.")
            break
    else:
        print(f"Error {response.status_code}: {response.text}")
        break

with open(json_filename, "w", encoding="utf-8") as file:
    json.dump(tesla_mentions, file, indent=4)

print(f"Saved extracted Tesla mentions to {json_filename}")
