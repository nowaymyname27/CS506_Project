import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

import yfinance as yf

tsla = yf.Ticker("TSLA")
tsla_historical = tsla.history(start="2025-02-21", end="2025-03-21", interval="5m")
tsla_historical
tsla_historical.to_csv('tsla.csv')