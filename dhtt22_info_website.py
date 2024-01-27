import signal
import time
import json
import random  
import paho.mqtt.client as mqtt
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
import threading
from threading import Event

app = Flask(__name__)
socketio = SocketIO(app)

# MQTT Configuration
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_TOPIC = "weather_conditions"

# Simulated Sensor Data
sensor_data = {}

event = Event()  # Create an instance of the Event class

def clear_cache():
    global sensor_data
    sensor_data = {}

signal.signal(signal.SIGTERM, clear_cache)

clear_cache() # Clear the cache before the loop starts

def on_message(client, userdata, msg):
    global sensor_data
    payload = json.loads(msg.payload.decode())
    sensor_data = payload

    socketio.emit("sensor_update", sensor_data, namespace="/sensor")

client = mqtt.Client()
client.connect("broker.emqx.io", 1883)
client.subscribe("/sensor/data")
client.on_message = on_message

def simulate_sensor_data():
    global sensor_data

    while True:
        # Simulate sensor readings
        temperature = round(random.uniform(31, 33), 2)
        humidity = round(random.uniform(31, 33), 2)

        # Log and publish the simulated data
        print(f"Simulated sensor values - temperature '{temperature}', humidity '{humidity}'")
        data = {
            'temperature': temperature,
            'humidity_percentage': humidity
        }

        # Send sensor data to MQTT broker
        client.publish("/sensor/data", json.dumps(data))

        # Update the sensor data dictionary
        sensor_data["temp"] = temperature
        sensor_data["humidity"] = humidity

        socketio.emit("sensor_update", sensor_data, namespace="/sensor")

        event.set()  # Set event to signal that data is ready

        time.sleep(1)

thread = threading.Thread(target=simulate_sensor_data)
thread.daemon = True
thread.start()

@app.route("/")
def home():
    # Wait for data to be ready
    event.wait()  # Call wait() on the event instance

    # Get sensor data
    temperature = sensor_data["temp"]
    humidity = sensor_data["humidity"]

    # Render the template
    return render_template("index.html", temperature=temperature, humidity=humidity, sensor_data=sensor_data)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

@socketio.on("connect", namespace="/sensor")
def handle_connect():
    print("Client connected")

    # Update the client with the latest sensor data
    socketio.emit("sensor_update", sensor_data, namespace="/sensor")

@app.route("/download_csv")
def download_csv():
    # Assume csv_content is defined and contains CSV data
    csv_path = "static/sensor_data.csv"
    with open(csv_path, "w") as csv_file:
        csv_file.write(csv_content)
    return send_from_directory("static", "sensor_data.csv", as_attachment=True)

#@app.route("/train_model")
#def train_model():
#    df = pd.read_csv('static/sensor_data.csv')
#    df['timestamp'] = pd.to_datetime(df['timestamp'])
#    df['timestamp'] = df['timestamp'].astype(int) // 10**9
#    X = df[['timestamp']]
#    y = df['temperature']
#    model = LinearRegression()
#    model.fit(X, y)
#    joblib.dump(model, 'static/temperature_model.joblib')
#    return jsonify({"message": "Model trained successfully."})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
