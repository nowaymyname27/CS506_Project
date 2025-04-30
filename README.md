# Sentiment Analysis and Stock Price Predictions

[Midterm Presentation](https://www.youtube.com/watch?v=Z3ZaY0fRCl0&ab_channel=JoseRamirez)

[Final Presentation]()

## Running Instructions

INSTRUCTIONS TO RUN THE CODE

## Final Project Detailing

### Initial Project Description and Goals

This project investigates the impact of public sentiment from social media and financial news about a certain company on its stock price movements. By analyzing the quantity and quality of comments on platforms such as X and Reddit, along with financial news headlines (Financial Times), we aim to build a model which will predict the movements in stock price of a particular company based on the public opinion.

#### Goals
- **Analyze** the correlation between public sentiment and stock price movements.
- **Develop** a predictive model to forecast stock price changes based on sentiment data.
- **Identify** which social media and financial news sources have the most significant impact on stock prices.

### Revised Project Description and Goals

After diving deeper into the project, we faced several challenges and asked ourselves various questions, leading to a slightly modified project description and goals.

In the past month, we asked ourselves a question: what if the companies we choose to analyze (randomly) are very stable in the market, and for them, even major discussions on social media do not result in stock price movements? After talking to several financial experts who confirmed our concern, we decided to start our project by building a model that predicts stock price movements of a company based on public sentiment expressed in social media and news articles for a company that is 1) widely discussed, and 2) significantly affected by public opinion. For such purposes, we chose Tesla.

Our ultimate goal by the end of the semester is to repeat the procedure we describe below for different companies from various sectors and conclude which types of companies the correlation we are researching actually exists. Below, we describe the work done so far and further goals for the rest of the semester.

### Data Extraction

#### Reddit Data Extraction

At the start of the project we wanted to extract Reddit data related to specific dates - the January 2025. However, we faced several issues collecting this data:

1. Reddit does nt give you opportunity to easily search comments by their dates;
2. Free version of API that allows extracting Reddit data did not let us have comments past three days from today (for example, we tried it on March 18th, but were able to get data from March 18th to March 15th, or from March 21st to March 18th);
3. Datasets that were collected and uploaded for free from the Internet were only up to December 2024;
4. First attempts took Days to process and filter this data.

Finally, we decided to switch our vector to work on December 2024 because it was the most recent data made by other enthusiasts and uploaded on **[AcademicTorrents.com](academictorrents.com)**. We collected 33 gb of Reddit data for December 2024, and used filtering code to extract specific lines that we were interested in.

After that, we needed to polish this data:
1. We removed all non-relevant comments that were too small or didn't contain discussions regarding Tesla or Elon Musk;
2. We sampled 3000 random comments (from about 100000) for our project needs.

#### Financial News Data Extraction

Initially, our goal was to extract financial news articles from the **Financial Times**, given its reputation and relevance. However, we encountered two significant obstacles: the site’s content is **behind a paywall**, and their **API access requires paid plans and business credentials** that were beyond our scope for this project.

As a result, we pivoted to a more accessible solution. After evaluating several general news APIs, we selected **[NewsAPI.org](https://newsapi.org/)** due to its **generous free tier** and minimal restrictions. Although it imposes a **100-request daily limit** and only provides access to articles from the **last 30 days**, it proved suitable for our initial data gathering needs.

We used NewsAPI to extract **50 news articles related to Tesla**, which were then used for sentiment analysis. After the initial data collection, we refined our approach by **filtering the article content to include only the sentences that specifically mentioned Tesla**, ensuring our sentiment analysis remained focused and relevant.

#### Stocks Data Extraction

For this step, we used the yfinance library, which is a very convenient way to extract stock data from Yahoo Finance. This library is completely free and goes back many years in daily stock prices (including open and close, which were the main metrics for this project). After finding this library, we did not run into any issues - we simply used the library and then cleaned the data that it produced. 

**Relevant file regarding stock extraction is:**

- `stock-extract.py`: extracts stock data using yfinance and removes unnecessary columns. 

### Sentiment Analysis

After collecting data from Reddit and various news sources, we performed sentiment analysis using three different models tailored for different types of text. For Reddit comments, we used RoBERTa (cardiffnlp/twitter-roberta-base-sentiment), VADER, and Google Cloud Natural Language API.

- **RoBERTa**: A transformer-based model pre-trained on Twitter data, well-suited for short, informal, and noisy social media comments. It classifies sentiment into three categories: positive, neutral, or negative, and returns both a label and confidence score.
- **VADER**: A rule-based model built specifically for social media, providing a compound score ranging from -1 (most negative) to +1 (most positive), along with discrete sentiment labels.
- **Google Cloud API**: Returns a sentiment score (from -1 to +1) and a magnitude score representing emotional intensity, designed for general-purpose language analysis.

For news data, we focused on the titles of articles, analyzing them using the Google Cloud model, which worked well given its ability to handle formal, headline-style text.

Looking ahead, our goal is to fine-tune the RoBERTa model on a custom dataset composed of Reddit comments about Tesla labeled using ChatGPT. We found that the RoBERTa model can achieve 93.6% accuracy after being fine-tuned on Twitter comments (https://www.kaggle.com/code/farneetsingh24/sentiment-analysis-93-6-test-accuracy). This will help improve the model’s relevance and accuracy when analyzing content specifically related to Tesla and its owners.

**Relevant files regarding sentiment analysis are:**

- `SA_reddit_roberta.csv`: Results of running the RoBERTa model on comments collected from Reddit.
- `SA_reddit_RoBERTa.py`: Code for running RoBERTa model.
- `SA_reddit_Vader.csv`: Results of running the VADER model on comments collected from Reddit.
- `SA_reddit_Vader.py`: Code for running VADER model.
- `SA_reddit_google.csv`: Results of running the Google Cloud NLP API on comments collected from Reddit.
- `SA_reddit_google.py`: Code for running the Google Cloud NLP API.
- `SA_news_titles_google.csv`: Results of running the Google Cloud NLP API on headlines of collected news articles.
- `SA_news_google.csv`: Results of running the Google Cloud NLP API on brief summaries of collected news articles.
- `SA_news_google.py`: Code for running the Google Cloud NLP API on news article titles.

### Data Processing

In order to work with the data effectively, we started by cleaning up the files that the sentiment analysis produced. There were a lot of columns that were not useful for the model, so those were removed. Additionally, the data was adjusted so that it was formatted the same across all csv files. Each sentiment source was split into two parts - the "Deterministic sentiment" and the "Numerical sentiment". The "Deterministic sentiment" took into account only the sentiment prediction, splitting the possible options into 1, 0, or -1. The "Numerical sentiment", on the other hand, also took into account the confidence of the model in its prediction. This was done by multiplying the confidence by the sentiment determined in the previous step. (Previously, this was done by 1 for positive sentiment, -1 for negative sentiment, and either -0.1 or 0.1 for neutral sentiment, however, this was very inconsistent and commonly produced both better and worse results than the non-random process, so randomness was removed for the sake of replicability.) This process produced just one quantitative sentiment column. 

After these pre-processing steps were done, the data needed to be compressed. First, all of the sentiment csv files were added together into one. Next, since the stock data, the Reddit data, and the news data were daily, we decided to compress the Reddit and news sentiment to an average of all daily values. Then, we aggregated the sentiment from the weekends and holidays to the nearest preceding weekday. Finally, we combined the sentiment file and the stock file into one csv file. 

**Relevant files regarding data processing are:**

- `filter-SA.py`: sorts out any unnecessary columns in the sentiment analysis and formats columns properly
- `adjust-sentiment.py`: follows through with the sentiment adjustment described in this section
- `merge-SA.py`: merges the different sentiment files as described in this section
- `factor-weekends.py`: aggregates weekends and holidays as described, and handles edge cases. Also produced the final processed data. 

### Building the Model

For modeling, we tried quite a few approaches, but ended up going with a combination of GridSearchCV, XGBoost, and a few other small techniques. The approaches that we tried and did not use included RandomForest, Leave-One-Out Cross-Validation (LOO-CV), Long Short-Term Memory (LTSM), etc, and the features that we tried and did not use included TF-IDF, derivatives (first, second, and combo), moving averages, etc. After all, we stopped on the following workflow of the model:

- Loop through each month separately - this allows us to test on the whole year without overtraining the model.
- For each month, use the given features to train an XGBoost model.
- For each model, run GridSearchCV to find the best parameters (hyperparameter tuning)
- Find the best confidence threshold for buying stock
- Save the resulting classification
- Simulate trading and evaluate trades

A little more about the last step - we decided that the most useful yet unbiased way to test our model, given certain API limitations, was to find the total profit given our trading strategy. Since sentiment happens during the day, it would be unreasonable the use the time frame from close to open, so instead we decided that the model should decide whether or not to buy each day at close, and sell (if bought) immediately at open. For the purposes of this model, assume we are always buying exactly one share, and we always have enough money to buy that one share (meaning if the price of the stock goes up during the day, we can still buy effortlessly at close). The benchmark strategy was to buy every single day at close. After eliminating all the randomness in this model, we found that we actually outperformed the default strategy by BLANK% or $BLANK, and even outperformed the total buy-and-hold strategy (meaning buy first day at open, sell last day at close) by BLANK% or $BLANK! This was a very exciting result for us. Profits have been made, and our hypothesis was proven true - the model works. 

**Relevant file regarding building the model is:**

- `FINAL-model.py` - the model that we ended up going with (described in this section). 

### Visualizations

ADD HERE

**Relevant files regarding visualizations are:**

- 

### Issues and Moving Forward:

Obviously, our model was not perfect - as stated before, we managed to get better results utilizing the randomness, and we did not try absolutely everything that there is to try for financial modeling. However, ultimately, we created a model that works and generates a pretty serious profit - in both negtaive and positive times for Tesla. 

In the future, it would be interesting to see this model applied to current data (scrape the internet for sentiment during the day, run the model near close, and trade accordingly), or even to try expanding this model to other companies. This would be significantly outside the scope of the project, but is plausible and could potentially lead to positive results based on the success of this model. 


## <a id="credits">Team Members</a>

The work is done by a group of students at Boston University for the *CS 506 - Data Science Tools and Applications* course:
- **Aleksei Glebov** - aglebov@bu.edu
- **Alika Grigorova** - alika21@bu.edu
- **Andrey Mukhin** - amukhin@bu.edu
- **Jose Ramirez** - galock@bu.edu
