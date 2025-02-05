from machine import Pin  # Import Pin module to control GPIO pins
from machine import Timer  # Import Timer module for LED blinking
from time import sleep_ms  # Import sleep_ms for delays
import ubluetooth  # Import ubluetooth for BLE functionality

# Global variable to store received BLE messages
message = ""

class ESP32_BLE():
    def __init__(self, name):
        """
        Initialize the ESP32 BLE class.
        - Set up the onboard LED to indicate connection status.
        - Initialize the BLE module and start advertising.
        """
        self.led = Pin(2, Pin.OUT)  # Define onboard LED at GPIO2
        self.timer1 = Timer(0)  # Timer for blinking LED
        
        self.name = name  # Store BLE device name
        self.ble = ubluetooth.BLE()  # Initialize BLE module
        self.ble.active(True)  # Activate BLE
        
        self.disconnected()  # Start blinking LED (initial state)
        self.ble.irq(self.ble_irq)  # Set BLE interrupt handler
        self.register()  # Register BLE services and characteristics
        self.advertiser()  # Start advertising BLE services

    def connected(self):
        """Called when a BLE device is connected. Stops LED blinking."""
        self.led.value(1)  # Turn LED ON (stable)
        self.timer1.deinit()  # Stop blinking timer

    def disconnected(self):
        """Called when BLE is disconnected. Starts LED blinking."""
        self.timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))

    def ble_irq(self, event, data):
        """
        BLE interrupt handler that manages:
        - Connection
        - Disconnection
        - Receiving data from the BLE client
        """
        global message
        
        if event == 1:  # _IRQ_CENTRAL_CONNECT: BLE device connected
            self.connected()

        elif event == 2:  # _IRQ_CENTRAL_DISCONNECT: BLE device disconnected
            self.advertiser()  # Restart advertising
            self.disconnected()  # Blink LED again
        
        elif event == 3:  # _IRQ_GATTS_WRITE: Data received from BLE client
            buffer = self.ble.gatts_read(self.rx)  # Read received data
            message = buffer.decode('UTF-8').strip()  # Decode data
            print(message)  # Print received message
            
    def register(self):        
        """
        Register BLE UART (Universal Asynchronous Receiver-Transmitter) service.
        This service allows communication between ESP32 and a BLE client (e.g., phone).
        """
        # Define UUIDs for the Nordic UART Service (NUS)
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'  # Characteristic for receiving data
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'  # Characteristic for sending data
            
        # Create BLE services and characteristics
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)  # RX allows client to write
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)  # TX allows server to send data
            
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))  # Define service with TX & RX
        SERVICES = (BLE_UART, )
        
        # Register services
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        """
        Send data to the connected BLE client.
        """
        self.ble.gatts_notify(0, self.tx, data + '\n')  # Send data via TX characteristic

    def advertiser(self):
        """
        Start BLE advertising so that other BLE devices can discover this ESP32.
        """
        name = self.name.encode()  # Convert name to bytes
        adv_data = b'\x02\x01\x06' + bytes([len(name) + 1, 0x09]) + name  # Format advertising data
        
        self.ble.gap_advertise(500, adv_data)  # Advertise with an interval of 500ms
        print("Advertising started...")
        print(adv_data)


# Define GPIO pins for LED and button
led = Pin(2, Pin.OUT)  # LED connected to GPIO2
but = Pin(0, Pin.IN)  # Button connected to GPIO0

# Create BLE instance with the name "ESP32"
ble = ESP32_BLE("ESP32")

def buttons_irq(pin):
    """
    Interrupt handler for the button press.
    - Toggles LED state.
    - Sends a message over BLE.
    """
    led.value(not led.value())  # Toggle LED state
    ble.send('LED state will be toggled.')  # Send message to BLE client
    print('LED state will be toggled.')  

# Configure button with interrupt on falling edge (button press)
but.irq(trigger=Pin.IRQ_FALLING, handler=buttons_irq)

# Main loop to check for BLE messages
while True:
    if message == "STATUS":  # If BLE client sends "STATUS"
        message = ""  # Clear message
        status_msg = 'LED is ON.' if led.value() else 'LED is OFF'
        print(status_msg)  # Print status
        ble.send(status_msg)  # Send status to BLE client
    sleep_ms(100)  # Small delay to avoid CPU overuse
