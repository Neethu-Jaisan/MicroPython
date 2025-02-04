from machine import Pin  # Import the Pin class from the machine module to control GPIO pins
import time  # Import the time module to add delays if needed

led = Pin(2, Pin.OUT)  # Create a Pin object for GPIO pin 2 and set it as an output pin (for controlling the LED)
Button = Pin(0, Pin.IN)  # Create a Pin object for GPIO pin 0 and set it as an input pin (for the button)

while True:  # Infinite loop to continuously check the button status and control the LED
    Button_Status = Button.value()  # Read the status of the button
    if Button_Status == False:  # If the button is pressed (typically low when pressed)
        led.value(1)  # Turn the LED on by setting the pin to HIGH (1)
    else:  # If the button is not pressed (high when not pressed)
        led.value(0)  # Turn the LED off by setting the pin to LOW (0)
