import network
import time

ssid = "mywifi"
password = "password"

sta = network.WLAN(network.STA_IF)  # Create a station interface
sta.active(True)  # Activate Wi-Fi
sta.connect(ssid, password)  # Connect to Wi-Fi

# Wait for connection
while not sta.isconnected():
    print("Connecting...")
    time.sleep(1)

print("Connected! IP Address:", sta.ifconfig()[0])  # Print IP address

print("Wi-Fi Signal Strength:", sta.status('rssi'), "dBm")
while True:
    if not sta.isconnected():
        print("Reconnecting...")
        sta.connect(ssid, password)
    time.sleep(5)

