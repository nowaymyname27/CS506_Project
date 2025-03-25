import pandas as pd

df = pd.read_csv("filtered_output.csv", header=None)

sampled_df = df.sample(n=3000, random_state=42) if len(df) >= 3000 else df

sampled_df.to_csv("final_output.csv", index=False, header=False)