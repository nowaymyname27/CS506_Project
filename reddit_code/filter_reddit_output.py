import pandas as pd

df = pd.read_csv("output.csv", header=None)

df = df[df[4] != '[removed]']

df = df[df[4].str.split().str.len() >= 5]

df = df[~df[4].str.match(r'(?i)^hello\s+u/')]

df.to_csv("filtered_output.csv", index=False)
