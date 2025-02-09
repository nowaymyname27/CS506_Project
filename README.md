# Sentiment Analysis and Stock Price Predictions

### Table of content

- [*Project Description*](#about)
- [*Goals*](#goals)
- [*Data Collection*](#data_collection)
- [*Companies and Time Period*](#companies_and_time)
- [*Data Processing*](#data_processing)
- [*Modeling Approach*](#modeling_approach)
- [*Data Visualization*](#data_visualization)
- [*Testing Plan*](#testing_plan)
- [*Credits*](#credits)
  
## <a id="about">Project Description</a>
This project investigates the impact of public sentiment from social media and financial news about a certain company on its stock price movements. By analyzing the quantity and quality of comments on platforms such as X and Reddit, along with financial news headlines (Financial Times), we aim to build a model which will predict the movements in stock price of a particular company based on the public opinion.

## <a id="goals">Goals</a>
- **Analyze** the correlation between public sentiment and stock price movements.
- **Develop** a predictive model to forecast stock price changes based on sentiment data.
- **Identify** which social media and financial news sources have the most significant impact on stock prices.

## <a id="data_collection">Data Collection</a>

### Sources
- **Social Media**: X, Reddit (r/investing, r/stocks, etc.).
- **Financial News**:Financial Times.
- **Stock Market Data**: Yahoo Finance API, Alpha Vantage, Google Finance, Bloomberg.

### Methods
- **Social Media Scraping**: We will use APIs such as the X API and Pushshift API (for Reddit) to collect posts and comments about specific companies.
- **Financial News Scraping**: News headlines will be gathered using BeautifulSoup and Scrapy.
- **Stock Price Data**: APIs like Yahoo Finance or Alpha Vantage will be used to obtain historical stock price data.
- **Sentiment Analysis**: We will apply NLP techniques to classify sentiment (positive, negative, neutral) using pre-trained models (VADER, TextBlob, or FinBERT).
- **Real-Time Sentiment Analysis**: We will integrate Bytewax's NLP streaming framework to process live Twitter data and analyze immediate sentiment trends.

## <a id="companies_and_time">Companies and Time Period</a>
To build a robust model, we will analyze approximately 20-30 companies, which will be randomly chosen from S&P 500. For the time period, we will collect sentiment data over a rolling window of the past 6 to 12 months to capture both short-term fluctuations and broader trends. Predictions will be made using different time frames:
- **Short-Term Predictions**: Based on sentiment from today, predicting stock price movement for the next day.
- **Medium-Term Trends**: Analyzing sentiment over a week and predicting stock price shifts over the next 7 days.
- **Long-Term Trends**: Assessing sentiment trends over a month to predict broader stock movements.

## <a id="data_processing">Data Processing & Feature Engineering</a>
### Data Cleaning
- Removing irrelevant posts, duplicate content, and non-English text.

### Feature Extraction
- Sentiment scores (positive/negative/neutral).
- Volume of mentions per company per day.
- Weighted sentiment scores based on user engagement (likes, retweets, comments).

### Time Alignment
- Synchronizing sentiment data with stock price movements.

## <a id="modeling_approach">Modeling Approach</a>
### Base Models
- Simple regression models to test initial correlations between the sentiment data collected and stock prices movements.

### Advanced Models (Rough Plan)
- Random Forest, XGBoost for feature importance evaluation.
- LSTM or GRU-based neural networks for time-series prediction.
- Transformer-based sentiment analysis (e.g., FinBERT for financial sentiment classification).

## <a id="data_visualization">Data Visualization (Rough Plan)</a>
- **Stock Price vs. Sentiment**: Plots which show correlation.
- **Feature Importance**: Bar charts illustrating which sentiment features contribute most to predictions.

## <a id="testing_plan">Testing Plan</a>
- **Train/Test Split**: 80% training, 20% testing.
- **Time-Based Validation**: Train on historical data (during Feb-March), test on recent data (during April).

## <a id="credits">Team Members</a>
The work is done by a group of students at Boston University for the *CS 506 - Data Science Tools and Applications* course:
- **Alika Grigorova** - alika21@bu.edu
- **Aleksei Glebov** - aglebov@bu.edu
- **Andrey Mukhin** - amukhin@bu.edu
- **Jose Ramirez** - galock@bu.edu
