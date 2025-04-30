import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

# ------------------ Prepare Data ------------------

# Load data
df = pd.read_csv("model_input.csv")
df['date'] = pd.to_datetime(df['date'])
df = df[df['date'].dt.month <= 10]

# Create additional features
df['previous_close'] = df['close'].shift(1)
df['price_movement'] = df['open'] - df['previous_close']
df['price_pct_change'] = (df['close'] - df['previous_close']) / df['previous_close'] * 100
df['reddit_sentiment_rolling3'] = df['sentiment_reddit'].rolling(window=3, min_periods=1).mean()
df['news_sentiment_rolling3'] = df['sentiment_news'].rolling(window=3, min_periods=1).mean()

# Drop NaNs
df.dropna(subset=['price_movement', 'previous_close', 'sentiment_reddit', 'sentiment_news'], inplace=True)

# Label: up = 1, down = 0
def categorize_movement(x, threshold=0.5):
    if x < -threshold:
        return 0
    else:
        return 1

df['movement_category'] = df['price_movement'].apply(categorize_movement)

# Features
feature_cols = ['previous_close', 'open', 'sentiment_reddit', 'sentiment_news',
                'price_pct_change', 'reddit_sentiment_rolling3', 'news_sentiment_rolling3']

X_all = df[feature_cols].values
y_all = df['movement_category'].values

# ------------------ Create Sequences ------------------

window_size = 10  # <-- Changed to 10 days memory
X_seq = []
y_seq = []

for i in range(window_size, len(X_all)):
    X_seq.append(X_all[i-window_size:i])
    y_seq.append(y_all[i])

X_seq = np.array(X_seq)
y_seq = np.array(y_seq)

# Train/Test split
split_idx = int(0.8 * len(X_seq))
X_train = X_seq[:split_idx]
y_train = y_seq[:split_idx]
X_test = X_seq[split_idx:]
y_test = y_seq[split_idx:]

# Convert to PyTorch tensors
X_train_torch = torch.tensor(X_train, dtype=torch.float32)
y_train_torch = torch.tensor(y_train, dtype=torch.float32)
X_test_torch = torch.tensor(X_test, dtype=torch.float32)
y_test_torch = torch.tensor(y_test, dtype=torch.float32)

# ------------------ Define LSTM Model ------------------

class LSTMClassifier(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super(LSTMClassifier, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 1)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        out, (h_n, c_n) = self.lstm(x)
        out = h_n[-1]  # Last hidden state
        out = self.fc(out)
        out = self.sigmoid(out)
        return out

input_dim = X_train.shape[2]  # number of features
hidden_dim = 64

model = LSTMClassifier(input_dim, hidden_dim)

# Loss and optimizer
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# ------------------ Train Model ------------------

n_epochs = 100  # <-- Upgraded to 100 epochs

for epoch in range(n_epochs):
    model.train()
    optimizer.zero_grad()
    output = model(X_train_torch).squeeze()
    loss = criterion(output, y_train_torch)
    loss.backward()
    optimizer.step()
    
    if (epoch+1) % 10 == 0:
        print(f"Epoch {epoch+1}/{n_epochs}, Loss: {loss.item():.4f}")

# ------------------ Evaluate Model with Confidence Threshold ------------------

model.eval()
with torch.no_grad():
    y_pred_prob = model(X_test_torch).squeeze()
    
# Apply confidence threshold
confidence_threshold = 0.6
y_pred = (y_pred_prob >= confidence_threshold).int()

print(f"\n📊 Classification Report (threshold {confidence_threshold}):")
print(classification_report(y_test_torch.numpy(), y_pred.numpy(), target_names=['down', 'up']))

# ------------------ Simulate Trading ------------------

# Load close and open prices for test period
close_prices = df['close'].values[-len(y_seq):]
open_prices = df['open'].values[-len(y_seq):]
dates = df['date'].values[-len(y_seq):]

close_test = close_prices[split_idx:]
open_test = open_prices[split_idx:]
dates_test = dates[split_idx:]

profits_model = []
profits_always_buy = []

for i in range(len(y_pred) - 1):
    today_close = close_test[i]
    tomorrow_open = open_test[i + 1]
    
    # Model strategy
    if y_pred[i] == 1:
        profit = tomorrow_open - today_close
    else:
        profit = 0
    profits_model.append(profit)
    
    # Always-buy strategy
    profit_always = tomorrow_open - today_close
    profits_always_buy.append(profit_always)

# Total profits
total_profit_model = sum(profits_model)
total_profit_always = sum(profits_always_buy)

print(f"\n💰 Profit following MODEL strategy: ${total_profit_model:.2f}")
print(f"💰 Profit following ALWAYS BUY strategy: ${total_profit_always:.2f}")

# Save trading results
import pandas as pd
trading_results = pd.DataFrame({
    'Date': dates_test[:-1],
    'Model Prediction (1=buy, 0=skip)': y_pred[:-1].numpy(),
    'Profit Model Strategy': profits_model,
    'Profit Always Buy Strategy': profits_always_buy
})
trading_results.to_csv("Trading_Strategy_LSTM_Comparison.csv", index=False)
print("Trading strategy results saved to Trading_Strategy_LSTM_Comparison.csv")

# ------------------ Plot Cumulative Profits ------------------

trading_results['Cumulative Model Profit'] = np.cumsum(trading_results['Profit Model Strategy'])
trading_results['Cumulative Always Buy Profit'] = np.cumsum(trading_results['Profit Always Buy Strategy'])

plt.figure(figsize=(14, 7))
plt.plot(trading_results['Date'], trading_results['Cumulative Model Profit'], label='Model Strategy', linewidth=2)
plt.plot(trading_results['Date'], trading_results['Cumulative Always Buy Profit'], label='Always Buy Strategy', linestyle='--', linewidth=2)
plt.xlabel('Date')
plt.ylabel('Cumulative Profit ($)')
plt.title('Cumulative Profit Over Time (PyTorch LSTM, Improved)')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()