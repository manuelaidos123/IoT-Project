import time
import random
import json
import threading
import paho.mqtt.client as mqtt
import os

# LED Configuration
class LED:
    def __init__(self, pin):
        self.pin = pin
        self.pwmval = 1023

    def duty(self, value):
        self.pwmval = value
        print(f"LED Duty: {value}")

led_blue = LED(2)

# MQTT Configuration
MQTT_CLIENT_ID = "zhengzhixin22060540765642"
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "default_topic")

# Count variable
count = 0

# MQTT Callback
def on_message(client, userdata, message):
    global count, led_blue

    topic = message.topic
    msg = message.payload.decode("utf-8")

    if topic == f"ledctl{MQTT_TOPIC.split('/')[1]}":
        print((topic, msg))
        if msg == "on":
            pwmval = 0
            led_blue.duty(pwmval)
        elif msg == "off":
            pwmval = 1023
            led_blue.duty(pwmval)

    elif topic == f"pwmled{MQTT_TOPIC.split('/')[1]}":
        pwmval = int(((100 - int(msg)) / 100) * 1023)
        if pwmval > 1023: pwmval = 1023
        if pwmval < 0: pwmval = 0
        print((topic, pwmval))
        led_blue.duty(pwmval)

# MQTT Client Setup
client = mqtt.Client(MQTT_CLIENT_ID)
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.connect(MQTT_BROKER)
client.subscribe("ledctl2206054076")
client.subscribe("pwmled2206054076")
client.subscribe("ledstatus2206054076")
client.on_message = on_message

# Thread for LED control
def led_thread():
    global count

    while True:
        for i in range(1, 6):
            instance = f"instance{i}"
            print(f"Measuring weather conditions for {instance}... ", end="")
            humidity, temperature = random.uniform(30.1, 31), random.uniform(33.2, 33.7)
            msg_data = {
                "temp": temperature,
                "humidity": humidity,
                "instance": instance
            }
            message = json.dumps(msg_data)
            print("Updated!")
            print(f"Reporting to MQTT topic {MQTT_TOPIC}: {message}")
            client.publish(MQTT_TOPIC, message)
            time.sleep(1)

# Use threading for the common instance
thread = threading.Thread(target=led_thread)
thread.start()

        
# MQTT Message Loop
while True:
    client.loop_start()
    time.sleep(1)

