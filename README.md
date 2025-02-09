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
- **Social Media:** X, Reddit, Facebook, Stocktwits (more if needed)
  - This will be used for the collection of public sentiment
- **Financial News:** Bloomberg, Financial Times, MarketWatch (more if needed)
  - This will be used for the collection of more concrete financial data and more professional sentiment
- **Stock Market Data:** Yahoo Finance API, Alpha Vantage, Google Finance, Bloomberg.
  - This will be used for the collection of the actual stock market data (preference to Yahoo Finance)

### Methods
- **Social Media and Financial Scraping:** The data will be collected from these sources via their own API’s (such as X API for Twitter, Pushshift API for Reddit, Scrapy for news headlines, etc.) or libraries such as Hugging Face. 
- **Stock Price Data:** APIs like Yahoo Finance or Alpha Vantage will be used to obtain historical stock price data.
- **Sentiment Analysis:** We will apply NLP techniques to classify sentiment (positive, negative, neutral) partially through our own analysis and partially using pre-trained models (such as VADER, TextBlob, or FinBERT)
- **Real-Time Sentiment Analysis:** We will integrate Bytewax's NLP streaming framework to process live Twitter data and analyze immediate sentiment trends.
- **LLMs:** Use built LLMs (such as ChatGPT) to guide data scraping from Social Media (hashtag generation given a company name)

## <a id="companies_and_time">Selection of Companies and Time Period:</a>
- **Company Selection:** we will select 20-30 companies from the S&P500 based on their popularity to make sure that there is enough data available from social media.
- **Time Period:** Total predictions will be made using a set time frame based on the stock tick increments available to us, with a preference given to a smaller time window (such as day/week, maybe/unlikely month). There will be multiple assessments throughout the day for all of these methods. 

## <a id="data_processing">Data Processing & Feature Engineering</a>
### Data Cleaning
- Removing irrelevant posts, duplicate content, and non-English text, removal of URLs, etc.

### Feature Extraction
- The volume of mentions per company per day.
- Weighted sentiment scores based on user engagement (likes, retweets, comments)
- Other extraction techniques will become increasingly obvious when we start collecting data

### Time Alignment
- Synchronizing sentiment data with stock price movements.

## <a id="modeling_approach">Modeling Approach</a>
### Base Models
- Simple regression models to test initial correlations between the sentiment data collected and stock prices movements.

### Advanced Models (Rough Plan)
- Random Forest, XGBoost for feature importance evaluation.
- Transformer-based sentiment analysis (e.g., FinBERT for financial sentiment classification).
- LLM-based approaches that will allow us to convert textual data to numerical vector embeddings
  - This will be used as an input to various models together with the financial time series data to predict stock movement
- Possibly use neural networks and deep learning (more details expected to be learned from this class)
  - This could be LSTM or GRU-based neural networks

## <a id="data_visualization">Data Visualization (Rough Plan)</a>
- **Stock Price vs. Sentiment**: Plots which show correlation.
- **Feature Importance**: Bar charts illustrating which sentiment features contribute most to predictions.

## <a id="testing_plan">Testing Plan</a>
- **Train/Test Split**: 80% training, 20% testing.
- **Time-Based Validation**: Train on historical data (during Feb-March), test on recent data (during April).
- **Benchmark strategy:** Beat a “buy-and-hold” user and/or beat S&P500 return over the same period

## <a id="credits">Team Members</a>
The work is done by a group of students at Boston University for the *CS 506 - Data Science Tools and Applications* course:
- **Alika Grigorova** - alika21@bu.edu
- **Aleksei Glebov** - aglebov@bu.edu
- **Andrey Mukhin** - amukhin@bu.edu
- **Jose Ramirez** - galock@bu.edu
