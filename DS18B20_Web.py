import network
import socket
import time
import machine
import onewire
import ds18x20

# Wi-Fi credentials
SSID = 'SSID'  # Replace with your Wi-Fi SSID
PASSWORD = 'password'  # Replace with your Wi-Fi password

# Initialize the Wi-Fi connection
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    # Wait for connection
    for _ in range(10):
        if wlan.isconnected():
            print('Connected to Wi-Fi:', wlan.ifconfig())
            return wlan.ifconfig()  # Return IP configuration
        time.sleep(1)

    raise Exception("Failed to connect to Wi-Fi")

# Read temperature from DS18B20 sensor
def read_temperature():
    ow_pin = machine.Pin(14)  # GPIO14 (change according to your setup)
    ow = onewire.OneWire(ow_pin)  # Initialize the OneWire bus
    sensor = ds18x20.DS18X20(ow)

    devices = ow.scan()  # Scan for DS18B20 devices on the bus
    print('Found devices:', devices)
    
    if devices:
        sensor.convert_temp()  # Start temperature conversion
        time.sleep(1)  # Wait for conversion to complete
        for device in devices:
            temp = sensor.read_temp(device)  # Read the temperature from each device
            print('Temperature: {}C'.format(temp))
            return temp  # Return the temperature value

    return None  # Return None if no sensor is found

# Set up the web server
def create_web_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]  # Listen on port 80
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Listening on', addr)

    while True:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024)
        print('Request:', request)

        # Read the temperature from the sensor
        temperature = read_temperature()

        # HTML response
        if temperature is not None:
            response = """
            <html>
                <head><title>ESP32 Web Server</title></head>
                <body>
                    <h1>Temperature Data</h1>
                    <p>Current Temperature: {:.2f}°C</p>
                </body>
            </html>
            """.format(temperature)
        else:
            response = """
            <html>
                <head><title>ESP32 Web Server</title></head>
                <body>
                    <h1>Temperature Sensor Not Found</h1>
                    <p>Please check your sensor connections.</p>
                </body>
            </html>
            """

        # Send the response to the client
        cl.send('HTTP/1.1 200 OK\r\n')
        cl.send('Content-Type: text/html\r\n')
        cl.send('\r\n')
        cl.send(response)
        cl.close()

# Main Program
if __name__ == '__main__':
    # Connect to Wi-Fi
    try:
        ip_config = connect_wifi()
    except Exception as e:
        print(e)
        while True:
            time.sleep(1)  # Wait for Wi-Fi connection

    # Start the web server
    create_web_server()

