import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# Find the latest CSV file in the directory
csv_files = glob.glob('sensor_data_with_month (12).csv')  
latest_csv = max(csv_files, key=os.path.getctime)

# Load the CSV file
df = pd.read_csv(latest_csv)

# Convert timestamp to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Create subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

# Plot Temperature
ax1.plot(df['timestamp'], df['temperature'], label='Temperature (°C)', marker='o', color='red')
ax1.set_ylabel('Temperature (°C)')
ax1.legend()
ax1.grid(True)

# Plot Humidity
ax2.plot(df['timestamp'], df['humidity'], label='Humidity (%)', marker='o', color='blue')
ax2.set_xlabel('Timestamp')
ax2.set_ylabel('Humidity (%)')
ax2.legend()
ax2.grid(True)

# Title for the entire figure
plt.suptitle('Temperature and Humidity Over Time')

# Adjust layout
plt.tight_layout()

# Save the plots to image files
plt.savefig('temperature_plot.png')
plt.savefig('humidity_plot.png')

# Show the plots (optional)
plt.show()
