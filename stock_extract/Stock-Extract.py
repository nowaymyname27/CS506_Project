import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

import yfinance as yf

tsla = yf.Ticker("TSLA")
tsla_historical = tsla.history(start="2024-01-01", end="2024-12-31", interval="1d")
tsla_historical = tsla_historical.reset_index()  

tsla_historical.columns = tsla_historical.columns.str.lower()
tsla_historical = tsla_historical[['date', 'open', 'close']]
tsla_historical['date'] = tsla_historical['date'].astype(str).str[:10]
tsla_historical[['open', 'close']] = tsla_historical[['open', 'close']].round(2)

tsla_historical.to_csv("tsla_daily_2024.csv", index=False)
print("The data has been processed and saved to tsla_daily_2024.csv")