import network
import time
from umqtt.simple import MQTTClient

# Wi-Fi credentials
ssid = 'your_SSID'
password = 'your_PASSWORD'

# MQTT broker details
mqtt_broker = 'mqtt_broker_address'  # e.g., 'test.mosquitto.org'
mqtt_port = 1883

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

while not wifi.isconnected():
    time.sleep(1)
    print("Connecting to WiFi...")

print("Connected to WiFi")

# MQTT Client setup
client = MQTTClient("ESP32", mqtt_broker)
client.connect()
