.PHONY: install clean

# Set up a virtual environment and install all packages
install:
	python3.13 -m venv venv
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install pandas holidays xgboost scikit-learn matplotlib numpy torch transformers

# Step 2: Run the full data and model pipeline
run_pipeline:
	# Run sentiment analysis scripts
	. venv/bin/activate && python sentiment_analysis/SA_news.py
	. venv/bin/activate && python sentiment_analysis/SA_reddit.py
	
	# Move sentiment CSVs to data_processing folder
	cp sentiment_analysis/news_sentiment.csv ./data_processing/
	cp sentiment_analysis/reddit_sentiment.csv ./data_processing/

	# Run data processing scripts
	. venv/bin/activate && cd data_processing && python filter-SA.py
	. venv/bin/activate && cd data_processing && python adjust-sentiment.py
	. venv/bin/activate && cd data_processing && python merge-SA.py
	. venv/bin/activate && cd data_processing && python factor-weekends.py

	# Move model input to modeling folder
	cp data_processing/model_input.csv modeling/

	# Run modeling and plotting
	. venv/bin/activate && cd modeling && python FINAL-model.py
	. venv/bin/activate && cd modeling && python plot-model.py

# Remove the virtual environment
clean:
	rm -rf venv
