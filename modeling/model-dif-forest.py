import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

#Load
df = pd.read_csv("TSLA_Merged.csv")

#Compute price movement (current day's open - previous day's close)
df['price_movement'] = df['open'] - df['close'].shift(1)

#Drop first row
df.dropna(subset=['price_movement'], inplace=True)

df['previous_close'] = df['close'].shift(1)
df.dropna(subset=['previous_close'], inplace=True)
df.dropna(subset=['sentiment_sar_go', 'sentiment_sar_ro', 'sentiment_sar_va'], inplace=True)
X = df[['previous_close', 'open', 'sentiment_sar_go', 'sentiment_sar_ro', 'sentiment_sar_va']]  # Add sentiment columns
y = df['price_movement']

#Split into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

#Make model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

#Evaluate the model using MSE
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

#Output
test_results = pd.DataFrame({'Date': df['date'].iloc[-len(y_test):], 'True Movement': y_test, 'Predicted Movement': y_pred})
test_results.to_csv("TSLA_Dif_Random_Forest.csv", index=False)
print("Predictions saved to TSLA_Predicted_Movements.csv")