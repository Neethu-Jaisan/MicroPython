import network
import time

ssid = "YourWiFiName"
password = "YourWiFiPassword"

sta = network.WLAN(network.STA_IF)  # Create a station interface
sta.active(True)  # Activate Wi-Fi
sta.connect(ssid, password)  # Connect to Wi-Fi

# Wait for connection
while not sta.isconnected():
    print("Connecting...")
    time.sleep(1)

print("Connected! IP Address:", sta.ifconfig()[0])  # Print IP address
