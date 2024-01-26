import os
import logging
import paho.mqtt.client as mqtt
import time
import json
import random  

# Environment variables and MQTT configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
SENSOR_TYPE = os.getenv("SENSOR_TYPE", "DHT22").upper()
SENSOR_PIN = int(os.getenv('SENSOR_PIN', '4'))
SENSOR_CHECK_INTERVAL = int(os.getenv('SENSOR_CHECK_INTERVAL', 30))
DECIMAL_POINTS = int(os.getenv("SENSOR_DECIMAL_POINTS", 2))

MQTT_HOSTNAME = os.getenv("MQTT_HOSTNAME", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TIMEOUT = int(os.getenv("MQTT_TIMEOUT", 60))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", 'sensor/value')
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "dht-sensor-mqtt")
MQTT_CLEAN_SESSION = os.getenv("CLIENT_CLEAN_SESSION", False)
MQTT_TLS_INSECURE = os.getenv("CLIENT_TLS_INSECURE", True)
MQTT_CLIENT_QOS = int(os.getenv("CLIENT_QOS", 0))
MQTT_USERNAME = os.getenv('MQTT_USERNAME', None)
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', None)

# Logging configuration
def configure_logging():
    level_map = {
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'WARN': logging.WARNING,
        'ERROR': logging.ERROR
    }

    log_level = level_map.get(LOG_LEVEL, "Unsupported log level provided!")
    logging.basicConfig(level=log_level)

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    logging.info("Connected to the MQTT broker!")

def on_disconnect(client, userdata, flags, rc):
    logging.warn(f"Disconnected from the MQTT broker. End state - '{rc}'")

# Main execution
if __name__ == '__main__':
    configure_logging()

    if MQTT_HOSTNAME is None or MQTT_PORT is None:
        logging.error("Could not acquire MQTT broker connection parameters...")
        exit(1)

    client = mqtt.Client(MQTT_CLIENT_ID, MQTT_CLEAN_SESSION)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(MQTT_HOSTNAME, MQTT_PORT, MQTT_TIMEOUT)
    client.loop_start()

    logging.info("Successfully initialized application! Starting simulation...")

    while True:
        try:
            # Simulate sensor readings
            temperature = random.uniform(31, 33)
            humidity = random.uniform(31, 33)

            # Log and publish the simulated data
            logging.debug(f"Simulated sensor values - temperature '{temperature}', humidity '{humidity}'")
            data = {
                'temperature': round(temperature, DECIMAL_POINTS),
                'humidity_percentage': round(humidity, DECIMAL_POINTS)
            }

            logging.debug(f"Publishing data to topic - '{MQTT_TOPIC}'")
            client.publish(MQTT_TOPIC, json.dumps(data))
        except Exception as e:
            logging.error(f"Error in simulation: {e}")
        finally:
            time.sleep(SENSOR_CHECK_INTERVAL)
    
            a = "test"
            print(a)
