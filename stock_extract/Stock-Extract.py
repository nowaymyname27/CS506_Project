import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

import yfinance as yf

tsla = yf.Ticker("TSLA")
tsla_historical = tsla.history(start="2024-01-01", end="2024-12-31", interval="1d")
tsla_historical
tsla_historical.to_csv('tsla_daily_2024.csv')