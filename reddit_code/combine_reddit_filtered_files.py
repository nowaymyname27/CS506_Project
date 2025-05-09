# This short script combines 12 filtered files together,
# making 1 file with all the data for 12 months (year 2024).

import pandas as pd

combined_df = pd.DataFrame()
for i in range(1, 13):
    file_name = f"filtered_output_{i}.csv"
    temp_df = pd.read_csv(file_name, header=None)
    combined_df = pd.concat([combined_df, temp_df], ignore_index=True)

combined_df.to_csv("combined_filtered.csv", index=False, header=False)
