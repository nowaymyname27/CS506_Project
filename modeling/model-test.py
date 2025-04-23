import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import LeaveOneOut
from sklearn.preprocessing import StandardScaler
import numpy as np

#Load
df = pd.read_csv('TSLA_Merged.csv')

#Define
df['previous_close'] = df['close'].shift(1)
df.dropna(subset=['previous_close'], inplace=True)
features = ['sentiment_sar_go', 'previous_close']
target = 'open'
X = df[features]
y = df[target]

loo = LeaveOneOut()
predictions = []
actual_values = []
dates = []

#Model
ridge_model = Ridge(alpha=0.2) 
scaler = StandardScaler()

#Perform LOO-CV
for train_idx, test_idx in loo.split(X):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    date_test = df.iloc[test_idx]['date'].values[0] 
    #Scale the features 
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    #Train and predict
    ridge_model.fit(X_train_scaled, y_train)
    #Assume the model starts with true value
    if len(predictions) == 0:
        y_pred = y_test.values[0] 
    else:
        y_pred = ridge_model.predict(X_test_scaled)
    predictions.append(y_pred if isinstance(y_pred, (float, np.float64)) else y_pred[0]) 
    actual_values.append(y_test.values[0]) 
    dates.append(date_test)

#Calculate the MSE
mse = mean_squared_error(actual_values, predictions)
print(f'Mean Squared Error (MSE): {mse}')

#Output
results_df = pd.DataFrame({
    'date': dates,
    'actual_close': actual_values,
    'predicted_close': predictions,
})
results_df.to_csv('TSLA_TEST.csv', index=False)
print("LOO-CV results saved to 'TSLA_TEST.csv'")