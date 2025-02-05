import network

ap = network.WLAN(network.AP_IF)  # Create an access point
ap.active(True)  # Activate AP mode
ap.config(essid="ESP32_AP", password="12345678")  # Set Wi-Fi name & password

print("Access Point Created! IP:", ap.ifconfig()[0])
