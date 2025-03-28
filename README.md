# Sentiment Analysis and Stock Price Predictions



## <a id="about">Project Description</a>

This project investigates the impact of public sentiment from social media and financial news about a certain company on its stock price movements. By analyzing the quantity and quality of comments on platforms such as X and Reddit, along with financial news headlines (Financial Times), we aim to build a model which will predict the movements in stock price of a particular company based on the public opinion.

## <a id="goals">Goals</a>

- **Analyze** the correlation between public sentiment and stock price movements.
- **Develop** a predictive model to forecast stock price changes based on sentiment data.
- **Identify** which social media and financial news sources have the most significant impact on stock prices.

## Midterm Update

### Revised Project Description and Goals

After diving deeper into the project, we faced several challenges and asked ourselves various questions, leading to a slightly modified project description and goals.

In the past month, we asked ourselves a question: what if the companies we choose to analyze (randomly) are very stable in the market, and for them, even major discussions on social media do not result in stock price movements? After talking to several financial experts who confirmed our concern, we decided to start our project by building a model that predicts stock price movements of a company based on public sentiment expressed in social media and news articles for a company that is 1) widely discussed, and 2) significantly affected by public opinion. For such purposes, we chose Tesla.

Our ultimate goal by the end of the semester is to repeat the procedure we describe below for different companies from various sectors and conclude which types of companies the correlation we are researching actually exists. Below, we describe the work done so far and further goals for the rest of the semester.

### Data Extraction

We describe sources found, methods used, and challenges met (e.g., too expensive, limits in terms of comments you can extract).

Further plans regarding data extraction are also described.

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
- `SA_news_google.py`: Code for running the Google Cloud NLP API on news article titles.

### Data Modeling

[Add your data modeling section here]


## <a id="credits">Team Members</a>

The work is done by a group of students at Boston University for the *CS 506 - Data Science Tools and Applications* course:
- **Alika Grigorova** - alika21@bu.edu
- **Aleksei Glebov** - aglebov@bu.edu
- **Andrey Mukhin** - amukhin@bu.edu
- **Jose Ramirez** - galock@bu.edu
