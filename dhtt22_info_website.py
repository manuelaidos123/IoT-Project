from flask import Flask, render_template, jsonify, send_from_directory
from flask_socketio import SocketIO
import json
import random
import time
import threading
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import httplib2  # Import httplib2

app = Flask(__name__)
socketio = SocketIO(app)

THINGSBOARD_HOST = 'https://thingsboard.cloud'
ACCESS_TOKEN = 'xsHO2Sx2NzGfWebhz70B'

# Simulated Sensor Data
sensor_data = {"temp": 0, "humidity": 0}

def send_to_thingsboard(data):
    url = f'{THINGSBOARD_HOST}/api/v1/{ACCESS_TOKEN}/telemetry'
    headers = {'Content-Type': 'application/json'}
    
    http_obj = httplib2.Http()
    response, content = http_obj.request(
        uri=url,
        method='POST',
        body=json.dumps(data),
        headers=headers
    )

    # Print the response (optional)
    print(f"Response status: {response['status']}")
    print(f"Response content: {content}")

def simulate_sensor_data():
    global sensor_data
    while True:
        sensor_data = {
            "temp": round(random.uniform(31, 33), 2),
            "humidity": round(random.uniform(31, 33), 2)
        }
        socketio.emit("sensor_update", sensor_data, namespace="/sensor")
        send_to_thingsboard(sensor_data)
        time.sleep(1)

thread = threading.Thread(target=simulate_sensor_data)
thread.daemon = True
thread.start()

@app.route("/")
def home():
    return render_template("index.html", sensor_data=sensor_data)

@socketio.on("connect", namespace="/sensor")
def handle_connect():
    print("Client connected")

@app.route("/download_csv")
def download_csv():
    # Assume csv_content is defined and contains CSV data
    csv_path = "static/sensor_data.csv"
    with open(csv_path, "w") as csv_file:
        csv_file.write(csv_content)
    return send_from_directory("static", "sensor_data.csv", as_attachment=True)

@app.route("/train_model")
def train_model():
    df = pd.read_csv('static/sensor_data.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['timestamp'] = df['timestamp'].astype(int) // 10**9
    X = df[['timestamp']]
    y = df['temperature']
    model = LinearRegression()
    model.fit(X, y)
    joblib.dump(model, 'static/temperature_model.joblib')
    return jsonify({"message": "Model trained successfully."})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
