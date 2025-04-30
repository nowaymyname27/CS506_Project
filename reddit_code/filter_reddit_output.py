# This filter file goes through 12 .csv files, cleaning their data,
# by deleting non-relevant comments that we don't wish to use for our sentiment analysis.

import pandas as pd

# Companies to be excluded from comments.
banned_companies = ['apple', 'microsoft', 'google', 'amazon', 'meta', 'huawei', 'yandex']

for i in range(1,13):
    df = pd.read_csv(f"output_{i}.csv", header=None)

    # Delete "broken" (removed) comments.
    df = df[df[4] != '[removed]']

    # Delete too short or too long comments.
    df = df[df[4].str.split().str.len() >= 10]
    df = df[df[4].str.split().str.len() <= 150]

    # Delete comments that start with "Hello".
    df = df[~df[4].str.match(r'(?i)^hello\s+u/')]
    
    # Save only those comments which have separate "tesla" words.
    df = df[df[4].str.contains(r'(?i)(?<!\S)(tesla)(?!\S)', na=False)]
    
    # Delete comments that mention companies that we want to exclude.
    banned_pattern = r'(?i)(?<!\S)(' + '|'.join(banned_companies) + r')(?!\S)'
    banned_mask = ~df[4].str.contains(banned_pattern, na=False)
    df = df[banned_mask]

    df.to_csv(f"filtered_output_{i}.csv", index=False)
