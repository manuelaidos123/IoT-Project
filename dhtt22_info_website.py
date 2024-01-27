from flask import Flask, render_template
from flask import jsonify, send_from_directory
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)
socketio = SocketIO(app)

# MQTT Configuration
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_TOPIC = "weather_conditions"

# Initial sensor data
sensor_data = {"temp": 0, "humidity": 0}

# MQTT Callback
def on_message(client, userdata, message):
    global sensor_data

    topic = message.topic
    payload = message.payload.decode("utf-8")

    if topic == MQTT_TOPIC:
        try:
            data = json.loads(payload)
            sensor_data = data
            print("Received MQTT message:", sensor_data)
            socketio.emit("sensor_update", sensor_data, namespace="/sensor")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

# MQTT Client Setup
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.connect(MQTT_BROKER)
client.subscribe(MQTT_TOPIC)
client.on_message = on_message
client.loop_start()

# Web server route to render the HTML page with sensor data
@app.route("/")
def home():
    return render_template("index.html", temp_range=get_temperature_range(sensor_data["temp"]),
                           humidity_range=get_humidity_range(sensor_data["humidity"]))

@socketio.on("connect", namespace="/sensor")
def handle_connect():
    print("Client connected")
    
def get_temperature_range(temp):
    if 20 <= temp <= 25:
        return "20-25 ºC"
    else:
        return "Unknown range"  

def get_humidity_range(humidity):
    if 60 <= humidity <= 70:
        return "60-70%"
    else:
        return "Unknown range"
        
@app.route("/download_csv")
def download_csv():
    # ... (your existing code to generate CSV)

    # Save the CSV file on the server
    csv_path = "static/sensor_data.csv"
    with open(csv_path, "w") as csv_file:
        csv_file.write(csv_content)

    return send_from_directory("static", "sensor_data.csv", as_attachment=True)

@app.route("/train_model")
def train_model():
    # Load the CSV file
    df = pd.read_csv('static/sensor_data.csv')

    # Preprocess the data (assuming timestamp is in a valid datetime format)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['timestamp'] = df['timestamp'].astype(int) // 10**9  # Convert timestamp to seconds for simplicity

    # Assuming you have 'timestamp' and 'temperature' columns for this example
    X = df[['timestamp']]
    y = df['temperature']

    # Train a simple linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Save the trained model (you might want to store it for future use)
    joblib.dump(model, 'static/temperature_model.joblib')

    return jsonify({"message": "Model trained successfully."})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

