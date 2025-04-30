import pandas as pd
import holidays

# Import the files
merged_sentiment_df = pd.read_csv("sentiment_merged.csv")
tsla_df = pd.read_csv("tsla_daily_2024.csv")

# Find start date, end date, and holidays
start_date = merged_sentiment_df['date'].min()
end_date = merged_sentiment_df['date'].max()
us_holidays = holidays.US(years=2024, observed=True)  

#Filter
federal_holidays = [str(date) for date, name in us_holidays.items() if start_date <= str(date) <= end_date]

# Date conversions and specifications
merged_sentiment_df['date'] = pd.to_datetime(merged_sentiment_df['date'])
merged_sentiment_df['weekday'] = merged_sentiment_df['date'].dt.weekday

# Remove leading weekends
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
if start_date.weekday() >= 5:  #Weekend
    if start_date.weekday() == 5:  #Saturday
        merged_sentiment_df = merged_sentiment_df[merged_sentiment_df['date'] > start_date + pd.Timedelta(days=1)] 
    else:  #Sunday
        merged_sentiment_df = merged_sentiment_df[merged_sentiment_df['date'] > start_date] 


# Find weekend dates and aggregate them to the previous Friday
weekend_dates = merged_sentiment_df[merged_sentiment_df['weekday'].isin([5, 6])]  
for idx, row in weekend_dates.iterrows():
    if row['weekday'] == 5:  #Saturday
        prev_friday_idx = merged_sentiment_df[(merged_sentiment_df['date'] == row['date'] - pd.Timedelta(days=1))].index[0]
        # If Saturday is last, only aggregate Saturday
        if row['date'] == merged_sentiment_df['date'].max(): 
            for col in ['sentiment_reddit', 'sentiment_news', 'sentiment_reddit_det', 'sentiment_news_det']:
                merged_sentiment_df.at[prev_friday_idx, col] = (merged_sentiment_df.at[prev_friday_idx, col] + 0.5 * row[col]) / 1.5
        # If Saturday is not last (so there is a Sunday), aggregate all
        else:
            next_sunday_idx = merged_sentiment_df[(merged_sentiment_df['date'] == row['date'] + pd.Timedelta(days=1))].index[0]
            for col in ['sentiment_reddit', 'sentiment_news', 'sentiment_reddit_det', 'sentiment_news_det']:
                merged_sentiment_df.at[prev_friday_idx, col] = (merged_sentiment_df.at[prev_friday_idx, col] + 0.5 * row[col]
                                                                 + 0.5 * merged_sentiment_df.at[next_sunday_idx, col]) / 2

# Remove leading holiday, if any (there are no consecutive federal holidays in the US)
if str(start_date) in federal_holidays:
    merged_sentiment_df = merged_sentiment_df[merged_sentiment_df['date'] != start_date]

# Check for holidays
for holiday in federal_holidays:
    # Make the holiday dates
    holiday_date = pd.to_datetime(holiday)
    holiday_idx = merged_sentiment_df[merged_sentiment_df['date'] == holiday_date].index[0]

    # Find the previous regular weekday (not a weekend or holiday)
    previous_regular_day = merged_sentiment_df[merged_sentiment_df['date'] < holiday_date]
    previous_regular_day = previous_regular_day[previous_regular_day['weekday'] < 5]  #Weekday
    if previous_regular_day.empty:
        continue 

    # Aggregate to that date
    previous_regular_idx = previous_regular_day.index[-1]
    for col in ['sentiment_reddit', 'sentiment_news', 'sentiment_reddit_det', 'sentiment_news_det']:
        merged_sentiment_df.at[previous_regular_idx, col] = (merged_sentiment_df.at[previous_regular_idx, col] + 0.5 * merged_sentiment_df.at[holiday_idx, col]) / 1.5
    merged_sentiment_df = merged_sentiment_df.drop(holiday_idx)

# Convert 'date' columns to string format 'YYYY-MM-DD' before merging
merged_sentiment_df['date'] = merged_sentiment_df['date'].dt.strftime('%Y-%m-%d')

# Merge
final_merged_df = pd.merge(tsla_df, merged_sentiment_df[['date', 'sentiment_reddit', 'sentiment_news', 'sentiment_reddit_det', 'sentiment_news_det']], on='date', how='inner')
final_merged_df[['sentiment_reddit', 'sentiment_news', 'sentiment_reddit_det', 'sentiment_news_det']] = final_merged_df[['sentiment_reddit', 'sentiment_news', 'sentiment_reddit_det', 'sentiment_news_det']].round(5)

# Save
final_merged_df.to_csv("model_input.csv", index=False)
print("✅ Merged and adjusted data with all sentiment columns saved to model_input.csv")