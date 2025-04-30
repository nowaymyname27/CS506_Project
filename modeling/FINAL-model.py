import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report

# Floating point range generator
def frange(start, stop, step):
    while start <= stop:
        yield start
        start += step

# Load and preprocess data
df = pd.read_csv("model_input.csv")
df['date'] = pd.to_datetime(df['date'])
df['price_movement'] = df['open'].shift(-1) - df['close']
df['previous_close'] = df['close'].shift(1)
df.dropna(subset=['price_movement', 'previous_close', 'sentiment_reddit', 'sentiment_news'], inplace=True)

def categorize_movement(x, threshold=0.5):
    return "down" if x < -threshold else "up"

df['movement_category'] = df['price_movement'].apply(categorize_movement)
label_mapping = {'down': 0, 'up': 1}

# Storage for outputs
classified_rows = []
strategy_rows = []

# Loop through each month
for test_month in range(1, 13):
    print(f"\n📅 Processing month {test_month:02d}...")

    test_df = df[df['date'].dt.month == test_month].copy()
    train_df = df[(df['date'].dt.month != test_month) & (df['date'].dt.month < 11)].copy()

    X_train = train_df[['previous_close', 'open', 'sentiment_reddit', 'sentiment_news']]
    y_train = train_df['movement_category'].map(label_mapping)

    X_test = test_df[['previous_close', 'open', 'sentiment_reddit', 'sentiment_news']]
    y_test = test_df['movement_category'].map(label_mapping)

    close_test = test_df['close'].values
    open_test = test_df['open'].values
    dates_test = test_df['date'].values

    # Grid search
    model = XGBClassifier(random_state=42, eval_metric='logloss')
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
        verbose=0,
        n_jobs=-1
    )

    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    print(f"✅ Best hyperparameters found for month {test_month:02d}: {grid_search.best_params_}")

    # Optimize confidence threshold
    thresholds = [round(x, 2) for x in list(frange(0.50, 0.81, 0.05))]
    best_threshold = None
    best_profit = -float('inf')

    def simulate_profit(y_pred, close_test, open_test):
        return sum(
            (open_test[i + 1] - close_test[i]) if y_pred[i] == 1 else 0
            for i in range(len(y_pred) - 1)
        )

    for threshold in thresholds:
        y_pred_proba = best_model.predict_proba(X_test)[:, 1]
        y_pred = (y_pred_proba >= threshold).astype(int)
        profit = simulate_profit(y_pred, close_test, open_test)
        if profit > best_profit:
            best_profit = profit
            best_threshold = threshold

    y_pred_proba = best_model.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_proba >= best_threshold).astype(int)

    print(f"✅ Best threshold for month {test_month:02d}: {best_threshold}")

    # Save classification
    for d, yt, yp in zip(dates_test, y_test, y_pred):
        classified_rows.append({
            'Date': d,
            'True Movement': yt,
            'Predicted Movement': yp
        })

    # Simulate trading
    profits_model = []
    profits_always_buy = []

    for i in range(len(y_pred) - 1):
        today_close = close_test[i]
        tomorrow_open = open_test[i + 1]
        profit_model = (tomorrow_open - today_close) if y_pred[i] == 1 else 0
        profit_always = tomorrow_open - today_close
        profits_model.append(profit_model)
        profits_always_buy.append(profit_always)

        strategy_rows.append({
            'Date': dates_test[i],
            'Model Prediction (1=buy, 0=skip)': y_pred[i],
            'Profit Model Strategy': profit_model,
            'Profit Always Buy Strategy': profit_always
        })

    # Evaluate trades
    good_trades_caught = 0
    good_trades_missed = 0
    bad_trades_avoided = 0
    bad_trades_taken = 0
    total_profitable_opportunities = 0
    total_unprofitable_opportunities = 0

    profit_threshold = 0  # Can be adjusted if needed

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

    total_profit_model = sum(profits_model)
    total_profit_always = sum(profits_always_buy)

    print(f"\n💰 Profit following MODEL strategy (month {test_month:02d}): ${total_profit_model:.2f}")
    print(f"💰 Profit following ALWAYS BUY strategy: ${total_profit_always:.2f}")

    print(f"\n📊 Good trades: Caught {good_trades_caught} / {total_profitable_opportunities}")
    print(f"🚫 Good trades missed: {good_trades_missed}")

    print(f"\n✅ Bad trades avoided: {bad_trades_avoided} / {total_unprofitable_opportunities}")
    print(f"❌ Bad trades taken: {bad_trades_taken}")

# Save final yearly CSVs
pd.DataFrame(classified_rows).to_csv("TSLA_Yearly_Classified.csv", index=False)
pd.DataFrame(strategy_rows).to_csv("Trading_Strategy_Yearly.csv", index=False)

print("\n✅ All months complete. Files saved:")
print("- TSLA_Yearly_Classified.csv")
print("- Trading_Strategy_Yearly.csv")