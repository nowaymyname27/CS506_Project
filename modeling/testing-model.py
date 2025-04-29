import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score

# Helper function for floating point ranges
def frange(start, stop, step):
    while start <= stop:
        yield start
        start += step

# ------------------ Load and Preprocess ------------------

# Load data
df = pd.read_csv("model_input.csv")

# Only use data up to October 31
df['date'] = pd.to_datetime(df['date'])  # Ensure datetime type
df = df[df['date'].dt.month <= 10]       # Keep only January–October

# No shift needed for sentiment
df['price_movement'] = df['open'].shift(-1) - df['close']  # Predict tomorrow's open minus today's close

df['previous_close'] = df['close'].shift(1)

# Drop rows with NaN
df.dropna(subset=['price_movement', 'previous_close', 'sentiment_reddit', 'sentiment_news'], inplace=True)

# ------------------ Create Labels ------------------

def categorize_movement(x, threshold=0.5):
    if x < -threshold:
        return "down"
    else:
        return "up"

df['movement_category'] = df['price_movement'].apply(categorize_movement)

label_mapping = {'down': 0, 'up': 1}
y = df['movement_category'].map(label_mapping)

# Prepare features
X = df[['previous_close', 'open', 'sentiment_reddit', 'sentiment_news']]

# Save prices and dates for trading simulation
close_prices = df['close'].values
open_prices = df['open'].values
dates = df['date'].values

# ------------------ Train/Test Split ------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, shuffle=False
)

split_index = len(X_train)

close_train = close_prices[:split_index]
close_test = close_prices[split_index:]

open_train = open_prices[:split_index]
open_test = open_prices[split_index:]

dates_train = dates[:split_index]
dates_test = dates[split_index:]

# ------------------ Train with GridSearchCV ------------------

model = XGBClassifier(
    random_state=42,
    eval_metric='logloss'
)

param_grid = {
    'n_estimators': [100, 300, 500],
    'learning_rate': [0.01, 0.03, 0.05, 0.1],
    'max_depth': [3, 4, 5, 6],
    'subsample': [0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.7, 0.8, 0.9, 1.0]
}

grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=5,
    scoring='accuracy',
    verbose=2,
    n_jobs=-1
)

grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_

print(f"\n✅ Best hyperparameters found: {grid_search.best_params_}")

# ------------------ Optimize Confidence Threshold ------------------

thresholds = [round(x, 2) for x in list(frange(0.50, 0.81, 0.05))]  # 0.50 to 0.80 in steps of 0.05

best_threshold = None
best_profit = -float('inf')  # initialize very low

def simulate_profit(y_pred, close_test, open_test):
    profits = []
    for i in range(len(y_pred) - 1):  # stop early to avoid index error
        if y_pred[i] == 1:
            profit = open_test[i + 1] - close_test[i]
        else:
            profit = 0
        profits.append(profit)
    return sum(profits)

for threshold in thresholds:
    y_pred_proba = best_model.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_proba >= threshold).astype(int)
    
    profit = simulate_profit(y_pred, close_test, open_test)
    
    print(f"Threshold {threshold}: Total Profit = ${profit:.2f}")
    
    if profit > best_profit:
        best_profit = profit
        best_threshold = threshold

print("\n✅ Best threshold found:", best_threshold)
print(f"✅ Best total profit: ${best_profit:.2f}")

# ------------------ Evaluate Model with Best Confidence Threshold ------------------

# Predict probabilities
y_pred_proba = best_model.predict_proba(X_test)[:, 1]

# USE best_threshold FOUND above
confidence_threshold = best_threshold
y_pred = (y_pred_proba >= confidence_threshold).astype(int)

# Classification report
print(f"\n📊 Classification Report (after optimized threshold {confidence_threshold}):")
print(classification_report(y_test, y_pred, target_names=['down', 'up']))

# Save model predictions
test_results = pd.DataFrame({
    'Date': dates_test,
    'True Movement': y_test.values,
    'Predicted Movement': y_pred
})
test_results.to_csv("TSLA_New_Test_Classified.csv", index=False)
print("Predictions saved to TSLA_New_Test_Classified.csv")

# ------------------ Simulate Trading ------------------

profits_model = []
profits_always_buy = []

for i in range(len(y_pred) - 1):  # stop early because we need tomorrow's open
    today_close = close_test[i]
    tomorrow_open = open_test[i + 1]
    
    # Strategy 1: Model-based
    if y_pred[i] == 1:  # 'up'
        profit = tomorrow_open - today_close
    else:
        profit = 0
    profits_model.append(profit)
    
    # Strategy 2: Always buy
    profit_always = tomorrow_open - today_close
    profits_always_buy.append(profit_always)

# Final profits
total_profit_model = sum(profits_model)
total_profit_always = sum(profits_always_buy)

print(f"\n💰 Profit following MODEL strategy: ${total_profit_model:.2f}")
print(f"💰 Profit following ALWAYS BUY strategy: ${total_profit_always:.2f}")

# Save trading history
trading_results = pd.DataFrame({
    'Date': dates_test[:-1],
    'Model Prediction (1=buy, 0=skip)': y_pred[:-1],
    'Profit Model Strategy': profits_model,
    'Profit Always Buy Strategy': profits_always_buy
})
trading_results.to_csv("Trading_Strategy_Comparison.csv", index=False)
print("Trading strategy results saved to Trading_Strategy_Comparison.csv")

# ------------------ Check Trades Caught/Missed/Blocked ------------------

good_trades_caught = 0
good_trades_missed = 0
bad_trades_avoided = 0
bad_trades_taken = 0
total_profitable_opportunities = 0
total_unprofitable_opportunities = 0

profit_threshold = 0  # or raise to $2 or $5 if you want stricter definition

for i in range(len(profits_always_buy)):
    expected_profit = profits_always_buy[i]
    model_action = profits_model[i] != 0
    
    if expected_profit > profit_threshold:
        total_profitable_opportunities += 1
        if model_action:
            good_trades_caught += 1
        else:
            good_trades_missed += 1
    else:
        total_unprofitable_opportunities += 1
        if not model_action:
            bad_trades_avoided += 1
        else:
            bad_trades_taken += 1

print(f"\n📊 Good trades: Caught {good_trades_caught} / {total_profitable_opportunities}")
print(f"🚫 Good trades missed: {good_trades_missed}")

print(f"\n✅ Bad trades avoided: {bad_trades_avoided} / {total_unprofitable_opportunities}")
print(f"❌ Bad trades taken: {bad_trades_taken}")