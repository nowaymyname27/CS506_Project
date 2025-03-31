import pandas as pd
import matplotlib.pyplot as plt

# Load the data from CSV
df = pd.read_csv('TSLA_Dif_LOOCV_Ridge.csv')

# Convert the 'date' column to datetime format for proper plotting
df['date'] = pd.to_datetime(df['date'])

# Create a plot
plt.figure(figsize=(10, 6))

# Plot the actual and predicted close prices
plt.plot(df['date'], df['actual_close'], label='Actual Close', color='blue', linestyle='-', marker='o')
plt.plot(df['date'], df['predicted_close'], label='Predicted Close', color='red', linestyle='--', marker='x')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.title('Actual vs Predicted Close Prices')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Display grid for better readability
plt.grid(True)

# Set reasonable y-axis limits based on the min and max values of actual and predicted close
min_value = min(df['actual_close'].min(), df['predicted_close'].min())
max_value = max(df['actual_close'].max(), df['predicted_close'].max())
buffer = (max_value - min_value) * 0.1  # Add 10% buffer to top and bottom for better visibility
plt.ylim(min_value - buffer, max_value + buffer)

# Display legend
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()