import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# Find the latest CSV file in the directory
csv_files = glob.glob('D:\Transferencias\sensor_data_with_month (11).csv')  
latest_csv = max(csv_files, key=os.path.getctime)

# Load the CSV file
df = pd.read_csv(latest_csv)

# Convert timestamp to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(df['timestamp'], df['temperature'], label='Temperature (°C)', marker='o')
plt.plot(df['timestamp'], df['humidity'], label='Humidity (%)', marker='o')

plt.title('Temperature and Humidity Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Values')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save the plot to an image file
plt.savefig('temperature_humidity_plot.png')

# Show the plot (optional)
plt.show()

