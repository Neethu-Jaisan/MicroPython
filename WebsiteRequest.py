#This MicroPython script connects an ESP32 to a Wi-Fi network, scans for available networks, and makes an HTTP request if connected successfully. Below is an explanation with comments:

import network  # Import the network module to handle Wi-Fi connections
import time     # Import the time module for delays
import urequests  # Import urequests to make HTTP requests

timeout = 0  # Initialize a timeout counter

# Create a Wi-Fi station interface
wifi = network.WLAN(network.STA_IF)  
wifi.active(True)  # Activate Wi-Fi in station mode

# Scan for available Wi-Fi networks
networks = wifi.scan()  
print(networks)  # Print the list of networks found

# Connect to a specified Wi-Fi network
wifi.connect('SSID', 'PASS')  # Replace 'SSID' and 'PASS' with your Wi-Fi credentials

# Check if the connection is successful
if not wifi.isconnected():
    print('connecting..')
    
    # Try connecting for a maximum of 5 seconds
    while (not wifi.isconnected() and timeout < 5):  
        print(5 - timeout)  # Print countdown
        timeout = timeout + 1
        time.sleep(1)  # Wait for 1 second before retrying

# If connected, proceed to make an HTTP request
if wifi.isconnected():
    print('Connected')  
    req = urequests.get('https://www.example.com')  # Make a GET request to example.com
    print(req.status_code)  # Print the HTTP response status code (e.g., 200 for success)
    print(req.text)  # Print the response content
else:
    print('Time Out')  # Print timeout message if not connected
    print('Not Connected')  # Indicate connection failure
