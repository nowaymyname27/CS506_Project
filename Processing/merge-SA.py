import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar
import holidays

#import
tsla_df = pd.read_csv("TSLA_Dec_Processed.csv")
sar_go_df = pd.read_csv("SAR_GO_Processed.csv")
sar_ro_df = pd.read_csv("SAR_RO_Processed.csv")
sar_va_df = pd.read_csv("SAR_VA_Processed.csv")

#average everything that happened in a day, then save that
sar_go_avg = sar_go_df.groupby('date')['sentiment'].mean().reset_index()
sar_ro_avg = sar_ro_df.groupby('date')['sentiment'].mean().reset_index()
sar_va_avg = sar_va_df.groupby('date')['sentiment'].mean().reset_index()
sar_go_avg.to_csv("SAR_GO_AVG.csv", index=False)
sar_ro_avg.to_csv("SAR_RO_AVG.csv", index=False)
sar_va_avg.to_csv("SAR_VA_AVG.csv", index=False)

#rename for merging
sar_go_avg.rename(columns={'sentiment': 'sentiment_sar_go'}, inplace=True)
sar_ro_avg.rename(columns={'sentiment': 'sentiment_sar_ro'}, inplace=True)
sar_va_avg.rename(columns={'sentiment': 'sentiment_sar_va'}, inplace=True)

#merge
merged_sentiment_df = pd.merge(sar_go_avg, sar_ro_avg[['date', 'sentiment_sar_ro']], on='date', how='outer')
merged_sentiment_df = pd.merge(merged_sentiment_df, sar_va_avg[['date', 'sentiment_sar_va']], on='date', how='outer')

start_date = merged_sentiment_df['date'].min()
end_date = merged_sentiment_df['date'].max()
us_holidays = holidays.US(years=2025, observed=True)  #Get all federal holidays for 2025
#Filter
federal_holidays = [str(date) for date, name in us_holidays.items() if start_date <= str(date) <= end_date]

#date conversions and specifications
merged_sentiment_df['date'] = pd.to_datetime(merged_sentiment_df['date'])
merged_sentiment_df['weekday'] = merged_sentiment_df['date'].dt.weekday

#remove leading weekends
first_date = merged_sentiment_df['date'].min()
if first_date.weekday() >= 5:  #Weekend
    if first_date.weekday() == 5:  #Saturday
        merged_sentiment_df = merged_sentiment_df[merged_sentiment_df['date'] > first_date + pd.Timedelta(days=1)] 
    else:  #Sunday
        merged_sentiment_df = merged_sentiment_df[merged_sentiment_df['date'] > first_date] 


#find weekend dates and aggregate them to the previous Friday
weekend_dates = merged_sentiment_df[merged_sentiment_df['weekday'].isin([5, 6])]  
for idx, row in weekend_dates.iterrows():
    if row['weekday'] == 5:  #Saturday
        prev_friday_idx = merged_sentiment_df[(merged_sentiment_df['date'] == row['date'] - pd.Timedelta(days=1))].index[0]
        #If Saturday is last, only aggregate Saturday
        if row['date'] == merged_sentiment_df['date'].max(): 
            for col in ['sentiment_sar_go', 'sentiment_sar_ro', 'sentiment_sar_va']:
                merged_sentiment_df.at[prev_friday_idx, col] = (merged_sentiment_df.at[prev_friday_idx, col] + 0.5 * row[col]) / 1.5
        #If Saturday is not last (so there is a Sunday), aggregate all
        else:
            next_sunday_idx = merged_sentiment_df[(merged_sentiment_df['date'] == row['date'] + pd.Timedelta(days=1))].index[0]
            for col in ['sentiment_sar_go', 'sentiment_sar_ro', 'sentiment_sar_va']:
                merged_sentiment_df.at[prev_friday_idx, col] = (merged_sentiment_df.at[prev_friday_idx, col] + 0.5 * row[col]
                                                                 + 0.5 * merged_sentiment_df.at[next_sunday_idx, col]) / 2

#remove leading holiday, if any (there are no consecutive federal holidays in the US)
if str(first_date) in federal_holidays:
    merged_sentiment_df = merged_sentiment_df[merged_sentiment_df['date'] != first_date]

#check for holidays
for holiday in federal_holidays:
    #make the holiday dates
    holiday_date = pd.to_datetime(holiday)
    holiday_idx = merged_sentiment_df[merged_sentiment_df['date'] == holiday_date].index[0]

    #find the previous regular weekday (not a weekend or holiday)
    previous_regular_day = merged_sentiment_df[merged_sentiment_df['date'] < holiday_date]
    previous_regular_day = previous_regular_day[previous_regular_day['weekday'] < 5]  #Weekday
    if previous_regular_day.empty:
        continue 

    #aggregate to that date
    previous_regular_idx = previous_regular_day.index[-1]
    for col in ['sentiment_sar_go', 'sentiment_sar_ro', 'sentiment_sar_va']:
        merged_sentiment_df.at[previous_regular_idx, col] = (merged_sentiment_df.at[previous_regular_idx, col] + 0.5 * merged_sentiment_df.at[holiday_idx, col]) / 1.5
    merged_sentiment_df = merged_sentiment_df.drop(holiday_idx)

#Convert 'date' columns to string format 'YYYY-MM-DD' before merging
merged_sentiment_df['date'] = merged_sentiment_df['date'].dt.strftime('%Y-%m-%d')

final_merged_df = pd.merge(tsla_df, merged_sentiment_df[['date', 'sentiment_sar_go', 'sentiment_sar_ro', 'sentiment_sar_va']], on='date', how='inner')
final_merged_df.to_csv("TSLA_Merged.csv", index=False)
print("Merged data with all sentiment columns saved to TSLA_Merged.csv")