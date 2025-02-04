from machine import Pin, I2C
import dht
import ssd1306
import time

# Initialize the I2C bus
i2c = I2C(scl=Pin(22), sda=Pin(21))  # SCL on GPIO 22, SDA on GPIO 21

# Create the OLED display object (128x64 resolution)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Initialize the DHT11 sensor (GPIO 15)
sensor = dht.DHT11(Pin(15))

# Function to clear the OLED screen and display data
def display_data(temp, humidity):
    oled.fill(0)  # Clear the screen
    oled.text("Temp: {}C".format(temp), 0, 0)
    oled.text("Humidity: {}%".format(humidity), 0, 20)
    oled.show()  # Display the updated text

while True:
        sensor.measure()  # Take a reading from the sensor
        temperature = sensor.temperature()  # Get the temperature in Celsius
        humidity = sensor.humidity()  # Get the humidity in percentage

        # Display the data on OLED
        display_data(temperature, humidity)
        oled.show()
        time.sleep(2)  # Wait for 2 seconds before updating

