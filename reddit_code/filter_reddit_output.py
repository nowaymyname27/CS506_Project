import pandas as pd

banned_companies = ['apple', 'microsoft', 'google', 'amazon', 'meta', 'huawei', 'yandex']

for i in range(1,13):
    df = pd.read_csv(f"output_{i}.csv", header=None)

    df = df[df[4] != '[removed]']

    df = df[df[4].str.split().str.len() >= 10]
    
    df = df[df[4].str.split().str.len() <= 150]

    df = df[~df[4].str.match(r'(?i)^hello\s+u/')]
    
    df = df[df[4].str.contains(r'(?i)(?<!\S)(tesla)(?!\S)', na=False)]
    
    banned_pattern = r'(?i)(?<!\S)(' + '|'.join(banned_companies) + r')(?!\S)'
    banned_mask = ~df[4].str.contains(banned_pattern, na=False)
    df = df[banned_mask]

    df.to_csv(f"filtered_output_{i}.csv", index=False)
