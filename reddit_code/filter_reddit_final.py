import pandas as pd

df = pd.read_csv("combined_filtered.csv", header=None)

sampled_df = df.sample(n=36500, random_state=42) if len(df) >= 36500 else df

sampled_df.to_csv("final_output.csv", index=False, header=False)
