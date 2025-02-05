import network
import time
from umqtt.simple import MQTTClient

# Wi-Fi credentials
ssid = 'your_SSID'
password = 'your_PASSWORD'

# MQTT broker details
mqtt_broker = 'test.mosquitto.org'  # Change if necessary
mqtt_port = 1883

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

while not wifi.isconnected():
    time.sleep(1)
    print("Connecting to WiFi...")

print("Connected to WiFi")
print(wifi.ifconfig())  # Print IP address

# MQTT Client setup
client = MQTTClient("ESP32", mqtt_broker)

# Try connecting to the MQTT broker
try:
    client.connect()
    print("Connected to MQTT Broker")
except Exception as e:
    print("Failed to connect to MQTT Broker:", e)

# Function to subscribe to a topic
def sub_cb(topic, msg):
    print("Received message:", msg)

client.set_callback(sub_cb)
client.subscribe('esp32/topic')

# Publish message every 5 seconds
while True:
    client.check_msg()  # Check for incoming messages
    client.publish('esp32/topic', 'Hello, MQTT from ESP32')
    time.sleep(5)

