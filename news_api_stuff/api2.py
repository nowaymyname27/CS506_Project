import requests
import time
from datetime import datetime, timedelta
import csv

# Replace with your actual API key
API_KEY = "dWDOolNleMJFGhsBbGE3Yb7bwJspiMQ5"
# Define the endpoint
url = f"https://financialmodelingprep.com/stable/fmp-articles"

# Define the parameters
params = {
    "apikey": API_KEY,
    "tickers": "TSLA",  # Tesla stock ticker
    "limit": 100,  # Max results per request
    "page": 0  # Pagination starts at 0
}

# File to store articles
csv_filename = f"fmp_tesla_news_{datetime.utcnow().strftime('%Y%m%d')}.csv"

# Open CSV file to store data
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Source", "Published Date", "URL"])

    # Pagination loop
    while True:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()

            if not data:  # Stop if no more articles
                break

            for article in data:
                title = article.get("title", "N/A")
                source = article.get("site", "N/A")  # 'site' is the source
                published = article.get("publishedDate", "N/A")
                url = article.get("url", "N/A")

                writer.writerow([title, source, published, url])

            print(f"Page {params['page']}: Retrieved {len(data)} articles.")
            params["page"] += 1  # Go to the next page

        else:
            print(f"Error {response.status_code}: {response.text}")
            break  # Stop on error

print(f"Saved Tesla news data to {csv_filename}")