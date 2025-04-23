import csv
import time
from datetime import date
from pygooglenews import GoogleNews
from readability import Document
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# --- CONFIG ---
QUERY        = "tesla"
YEAR         = 2024
MAX_ARTICLES = 1200
CSV_OUT      = f"tesla_{YEAR}_full.csv"
LANG, CTY    = "en", "US"

# 1) date windows: each month of YEAR
def month_ranges(year):
    for m in range(1, 13):
        start = date(year, m, 1)
        end   = date(year + (m==12), (m % 12) + 1, 1)
        yield start, end

# 2) collect up to MAX_ARTICLES metadata
gn = GoogleNews(lang=LANG, country=CTY)
seen = set()
entries = []

for frm, to in month_ranges(YEAR):
    if len(entries) >= MAX_ARTICLES:
        break
    print(f"Querying {QUERY} from {frm} to {to} …")
    feed = gn.search(QUERY, from_=frm.isoformat(), to_=to.isoformat())
    for e in feed.get("entries", []):
        if e.link not in seen:
            seen.add(e.link)
            entries.append((e.title, e.link, e.published))
            if len(entries) >= MAX_ARTICLES:
                break

print(f"Collected {len(entries)} metadata entries—now scraping full text…")

# 3) Playwright + Readability extraction
def extract_with_readability(html):
    doc = Document(html)
    summary = doc.summary()
    text = (
        BeautifulSoup(summary, "html.parser")
        .get_text(separator="\n")
        .strip()
    )
    return text or "Could not extract article text."

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    )

    # 4) open CSV and write
    with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["Title", "Link", "Published", "Content"]
        )
        writer.writeheader()

        for idx, (title, link, published) in enumerate(entries, start=1):
            try:
                print(f"[{idx}/{len(entries)}] Rendering {link}")
                page.goto(link, timeout=60000)
                page.wait_for_load_state("networkidle", timeout=60000)
                html = page.content()
                content = extract_with_readability(html)
            except Exception as e:
                content = f"Error: {e}"

            # throttle a bit so you don't hammer any one site
            time.sleep(1)

            writer.writerow({
                "Title":     title,
                "Link":      link,
                "Published": published,
                "Content":   content.replace("\n", " ")[:10000]
            })

    browser.close()

print(f"Done — wrote {len(entries)} rows to {CSV_OUT}")

