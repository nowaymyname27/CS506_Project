import pandas as pd

def modify_date_column(input_file, output_file):
    df = pd.read_csv(input_file)

    if 'publishedAt' in df.columns:
        df = df.rename(columns={'publishedAt': 'date'})
    else:
        print(f"'publishedAt' column not found in {input_file}. Skipping...")
        return
    
    df['date'] = df['date'].astype(str).str[:10]
    df.to_csv(output_file, index=False)
    print(f"The modified data has been saved to {output_file}")

input_file = "SANT_GO_Filtered.csv"
output_file = "SANT_GO_Filtered.csv"
modify_date_column(input_file, output_file)