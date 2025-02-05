#This MicroPython script connects an ESP32 to Wi-Fi and controls a light using Blynk Cloud. The button toggles the light state and sends the status to Blynk. Below is a detailed breakdown with comments:

import network  # Handles Wi-Fi connection
import urequests  # Used to make HTTP requests to Blynk
import time  # Used for delays
from machine import Pin  # Controls GPIO pins

# Global variables to track button state and request status
but_status = 0  # Tracks the button state (pressed or not)
but_flag = 0  # Flag to detect button press
Status = 0  # Stores HTTP response status

# Configure button as an input (GPIO0)
but = Pin(0, Pin.IN)

# Function to connect to Wi-Fi
def connect_wifi():
    wifi = network.WLAN(network.STA_IF)  # Create Wi-Fi station object
    wifi.active(True)  # Activate Wi-Fi in station mode
    wifi.disconnect()  # Ensure no previous connection
    wifi.connect('ss', 'sms123458956')  # Replace with your Wi-Fi SSID and password

    # Wait until connection is established (max 5 seconds)
    if not wifi.isconnected():
        print('connecting..')
        timeout = 0
        while (not wifi.isconnected() and timeout < 5):
            print(5 - timeout)  # Print countdown
            timeout += 1
            time.sleep(1)

    # Connection result
    if wifi.isconnected():
        print('connected')
    else:
        print('not connected')

# Interrupt function for button press
def buttons_irq(pin):
    global but_status
    global but_flag
    but_status = not but_status  # Toggle button status
    but_flag = 1  # Set flag to indicate button press

# Attach interrupt to the button (triggers on falling edge)
but.irq(trigger=Pin.IRQ_FALLING, handler=buttons_irq)

# Connect to Wi-Fi before starting the loop
connect_wifi()

# Main loop to send requests when button is pressed
while True:
    if but_status == True and but_flag == 1:
        # Send HTTP request to turn light OFF via Blynk Cloud
        req = urequests.get('http://blynk-cloud.com/fAdFW1gKTybAqa8S21wUAuIFFMvZGyk8/update/V1?value=1')
        but_flag = 0  # Reset flag after request
        Status = req.status_code  # Get HTTP response code

        if Status == 200:
            print("request successful")
            print("Light Off")
            req.close()  # Close the request

    elif but_status == False and but_flag == 1:
        # Send HTTP request to turn light ON via Blynk Cloud
        req = urequests.get('http://blynk-cloud.com/fAdFW1gKTybAqa8S21wUAuIFFMvZGyk8/update/V1?value=0')
        but_flag = 0  # Reset flag after request
        Status = req.status_code  # Get HTTP response code

        if Status == 200:
            print("request successful")
            print("Light On")
            req.close()  # Close the request
