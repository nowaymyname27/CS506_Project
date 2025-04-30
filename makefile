.PHONY: install clean

# Set up a virtual environment and install all packages
install:
	python3.13 -m venv venv
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install pandas holidays xgboost scikit-learn matplotlib numpy

# Step 2: Run the full data and model pipeline
run_pipeline:
	# Run sentiment analysis scripts
	. venv/bin/activate && python SA_news.py
	. venv/bin/activate && python SA_reddit.py
	
	# Move sentiment CSVs to data_processing folder
	cp sentiment_analysis/news_sentiment.csv data_processing/
	cp sentiment_analysis/reddit_sentiment.csv data_processing/

	# Run data processing scripts
	. venv/bin/activate && python filter-SA.py
	. venv/bin/activate && python adjust-sentiment.py
	. venv/bin/activate && python merge-SA.py
	. venv/bin/activate && python factor-weekends.py

	# Move model input to modeling folder
	cp data_processing/model_input.csv modeling/

	# Run modeling and plotting
	. venv/bin/activate && python FINAL-model.py
	. venv/bin/activate && python plot-model.py

# Remove the virtual environment
clean:
	rm -rf venv
