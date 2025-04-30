.PHONY: install clean

# Set up a virtual environment and install all packages
install:
	python3.13 -m venv venv
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install pandas holidays xgboost scikit-learn matplotlib numpy

# Remove the virtual environment
clean:
	rm -rf venv
