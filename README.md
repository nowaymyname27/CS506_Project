# Sentiment Analysis and Stock Price Predictions

[Midterm Presentation](https://www.youtube.com/watch?v=Z3ZaY0fRCl0&ab_channel=JoseRamirez)

[Final Presentation](https://youtu.be/wpLwfAlvnOg?feature=shared)

## Running Instructions

These instructions assume that the Reddit and news data are already given, as these files take a long time to generate (multiple days). These files can still be created (if wanted) using the code in this repo, but this code will not be included in the pipeline (as allowed). 

#### Requirements:

- ✅ Python 3.13
- ✅ pip (comes with Python)
- ✅ make (used to run automated steps)

📁 To install all necessary packages, run `make install`

▶️ To run the pipeline (this also generates the final graph and every intermediate csv for future modularity), run `make run_pipeline`

🧹 To clean, simply run `make clean`

## Final Project Detailing

### Project Description and Goals

The goals of this project were slightly modified throughout the semester, due to several challenges we faced. The goal of our project is to identify the correlation between the public sentiment about Tesla expressed on social media and news headlines and Tesla's stock prices. After identifying the correlation between these, we aimed to create a trading strategy which outperforms the always-buy strategy. 
### Data Extraction

#### Reddit Data Extraction

At the start of the project we wanted to extract Reddit data related to specific dates. However, we faced several issues collecting this data:

1. Reddit does not give you opportunity to easily search comments by their dates;
2. Free version of API that allows extracting Reddit data did not let us have comments past three days from today (for example, we tried it on March 18th, but were able to get data from March 18th to March 15th, or from March 21st to March 18th);
3. Datasets that were collected and uploaded for free from the Internet were only up to December 2024;
4. First attempts took Days to process and filter this data.

At the end, we decided to process the whole year 2024 worth of Reddit data. We collected 460 gb of Reddit data for, and used filtering code to extract specific lines that contained word "tesla".

After that, we needed to polish this data:
1. We removed all comments that were broken or removed;
2. We removed all comments that were too short (less than 10 words), or too long (more than 150 words);
3. We removed all comments that included names of other popular companies (such as Apple or Google) to ease the sentiment analysis in a way that it analyses only Tesla related comments;
2. Finally, we sampled 36500 random comments from the whole year (expecting about 100 comments per day) for our project.


#### Financial News Data Extraction

Initially, our goal was to extract financial news articles from the Financial Times, given its reputation and relevance. However, we encountered two significant obstacles: the site’s content is behind a paywall, and their API access requires paid plans and business credentials that were beyond our scope for this project.

To address these limitations, we adopted a new two-step approach:

1. **News Article Discovery via API:**  
   `web_scraper.py`: We used a Google news API that searches for articles with "Tesla" in the title and returns both the article titles and their corresponding links. This allowed us to efficiently identify relevant news stories across a wide range of sources, ensuring that our dataset focused specifically on Tesla-related news.

2. **Content Extraction via Web Scraping:**  
   `csv_cleaner.py`: For each article link obtained from the API, we developed a web scraper to extract the full content of the article. This step enabled us to gather the actual text for sentiment analysis, rather than relying solely on headlines or summaries.

After collecting the raw article content, we performed an additional cleaning step:  
We filtered the text to retain only the sentences that explicitly mention "Tesla." This ensured that our sentiment analysis remained tightly focused on content directly relevant to the company, improving the quality and relevance of our sentiment signals.

The resulting cleaned CSV file, containing only Tesla-specific sentences from each article, was then used as input for our sentiment analysis pipeline.


#### Stocks Data Extraction

For this step, we used the yfinance library, which is a very convenient way to extract stock data from Yahoo Finance. This library is completely free and goes back many years in daily stock prices (including open and close, which were the main metrics for this project). After finding this library, we did not run into any issues - we simply used the library and then cleaned the data that it produced. 

**Relevant file regarding stock extraction is:**

- `stock-extract.py`: extracts stock data using yfinance and removes unnecessary columns. 

### Sentiment Analysis

Before our midterm report, we experimented with various sentiment analysis models and concluded that the most accurate was the transformer-based **RoBERTa** model.

We found a study that achieved **93.6% accuracy** on sentiment classification of Reddit and Twitter comments after additional training on 200,000 sentiment-labeled examples:  
[Kaggle Notebook – Sentiment Analysis 93.6% Test Accuracy](https://www.kaggle.com/code/farneetsingh24/sentiment-analysis-93-6-test-accuracy)

We reproduced this fine-tuning process using the same datasets (limited to 100,000 labeled comments from Twitter and Reddit), and saved the resulting model to Hugging Face as:

[`alika21/roberta-sentiment-trained`](https://huggingface.co/alika21/roberta-sentiment-trained)

#### Fine-Tuning Script

The training process is implemented in:

- `finetuningRoberta.py` – fine-tunes and saves the RoBERTa model.

#### Sentiment Analysis Scripts

After fine-tuning, we used the model to perform sentiment analysis on data collected from Reddit and Google News. The following scripts perform inference using our custom model:

- `SA_news.py` – sentiment analysis on Google News data  
- `SA_reddit.py` – sentiment analysis on Reddit comments

#### Data Processing

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

A little more about the last step - we decided that the most useful yet unbiased way to test our model, given certain API limitations, was to find the total profit given our trading strategy. Since sentiment happens during the day, it would be unreasonable the use the time frame from close to open, so instead we decided that the model should decide whether or not to buy each day at close, and sell (if bought) immediately at open. For the purposes of this model, assume we are always buying exactly one share, and we always have enough money to buy that one share (meaning if the price of the stock goes up during the day, we can still buy effortlessly at close). The benchmark strategy was to buy every single day at close. After eliminating all the randomness in this model, we found that we actually outperformed the default strategy by 41.83% or $91.35, and even outperformed the total buy-and-hold strategy (meaning buy first day at open, sell last day at close)! This was a very exciting result for us. Profits have been made, and our hypothesis was proven true - the model works. 

**Relevant file regarding building the model is:**

- `FINAL-model.py` - the model that we ended up going with (described in this section). 

### Visualizations

![IMAGE 1](https://github.com/nowaymyname27/CS506_Project/blob/main/modeling/plots/Yearly_Profit_Plot.png)

This is the main final result of the project - a graph that depicts the cumulative profits for the model each day, compared to the always buy strategy. We can see from this graph that the model outpferms always buying at all times of the year, and never dips below the baseline. At the end of the year, it even manages to catch only the positive days out of a series of alternations. As stated in the modeling section, we can confidently say that the generated model works well for Tesla. 

![IMAGE 2](https://github.com/nowaymyname27/CS506_Project/blob/main/modeling/plots/Monthly_Profit_Comparison.png)

This image shows a comparison of monthly profits between the model and the always buy strategy. It can be seen from this graph that the model never loses any significant amount of money over the course of a month. In the begining of the year, we can see that the model successfully mitigates the losses incurred by the baseline model. In the middle of the year, neither model experiences any signifcant change, showing that the model dos not sabotage neutral times by buying incorrectly. Towards the end of the year, we can see that Tesla experiences high profits, and the model recognizes that. Overall, the model performs well during positive, negative, and neutral times. 

![IMAGE 3](https://github.com/nowaymyname27/CS506_Project/blob/main/modeling/plots/Buy_Signal_Timeline.png)

This image shows when exactly the stock was bought by the model (1 - bought). This is simply an expansion of the green dots from the cumulative profit graph. 

![IMAGE 4](https://github.com/nowaymyname27/CS506_Project/blob/main/modeling/plots/Buy_Frequency_Smoothed.png)

This model shows trends in how freqently the model bought a share of Tesla (1 - a lot of buying near that time, 0 - very little buying near that time). This shows the general buying trends of the model, and when the model identified down/up times. 

![IMAGE 5](https://github.com/nowaymyname27/CS506_Project/blob/main/modeling/plots/Sentiment_vs_Price.png)

This model shows the comparion between the sentiment scores and stock price on each day. This model shows clearly that there is not an obvious pattern between stock prices and sentiment analysis that can be seen with the naked eye, proving that the model is actually necessary to achieve the results shown in Graph 1. 

**Relevant files regarding visualizations are:**

- `plot-model.py` - plots the cumulative profit graph
- `Yearly_Profit_Plot.png` - shows the graph that was generated as a final result (cumulative profit difference)
- `Monthly_Profit_Comparison.png` - shows the differences in monthly profit between model and always buy strategy (non-cumulative)
- `Buy_Signal_Timeline.png` - shows when the stock was bought by the model (1 - bought)
- `Buy_Frequency_Smoothed.png` - shows trends in how freqently the model bought (1 - a lot of buying)
- `Sentiment_vs_Price.png` - shows the comparion between the sentiment scores and stock price on each day

### Issues and Moving Forward:

Obviously, our model was not perfect - as stated before, we managed to get better results utilizing the randomness, and we did not try absolutely everything that there is to try for financial modeling. However, ultimately, we created a model that works and generates a pretty serious profit - in both negtaive and positive times for Tesla. 

In the future, it would be interesting to see this model applied to current data (scrape the internet for sentiment during the day, run the model near close, and trade accordingly), or even to try expanding this model to other companies. This would be significantly outside the scope of the project, but is plausible and could potentially lead to positive results based on the success of this model. 


## <a id="credits">Team Members</a>

The work is done by a group of students at Boston University for the *CAS CS 506 - Data Science Tools and Applications* course:
- **Aleksei Glebov** - aglebov@bu.edu
- **Alika Grigorova** - alika21@bu.edu
- **Andrey Mukhin** - amukhin@bu.edu
- **Jose Ramirez** - galock@bu.edu
