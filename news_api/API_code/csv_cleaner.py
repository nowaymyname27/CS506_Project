import pandas as pd
import re

# Split on whitespace after ., ! or ?
SENT_SPLIT_RE = re.compile(r'(?<=[.!?])\s+')
# Match “tesla” (any case) or “Elon Musk”
MATCH_RE = re.compile(r'\btesla\b|elon musk', re.IGNORECASE)

def split_sentences(text: str) -> list[str]:
    if not isinstance(text, str):
        return []
    return SENT_SPLIT_RE.split(text)

def clean_content(text: str) -> str:
    # Keep only sentences matching our pattern
    sentences = split_sentences(text)
    filtered = [s for s in sentences if MATCH_RE.search(s)]
    return ' '.join(filtered).strip()

def main():
    df = pd.read_csv('tesla_2024_raw.csv')      # your raw file
    df['Content'] = df['Content'].apply(clean_content)
    df.to_csv('tesla_2024_clean.csv', index=False)

if __name__ == '__main__':
    main()

