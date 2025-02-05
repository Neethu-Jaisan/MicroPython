from machine import Pin, Timer  # Import Pin and Timer modules from the machine library
from time import sleep_ms       # Import sleep_ms for delay functions
import ubluetooth               # Import ubluetooth for BLE functionality

message = ""  # Variable to store received messages

class ESP32_BLE():
    def __init__(self, name):
        # Onboard LED configuration (blinks when disconnected, stays on when connected)
        self.led = Pin(2, Pin.OUT)  
        self.timer = Timer(0)  # Timer for LED blinking
        
        self.name = name
        self.ble = ubluetooth.BLE()  # Create BLE instance
        self.ble.active(True)        # Activate BLE module
        self.disconnected()           # Start in disconnected state
        self.ble.irq(self.ble_irq)    # Set BLE interrupt handler
        self.register()               # Register BLE services
        self.advertiser()              # Start advertising BLE

    def connected(self):
        """Function to handle BLE connection event"""
        self.led.value(1)  # Turn LED on when connected
        self.timer.deinit()  # Stop blinking timer

    def disconnected(self):
        """Function to handle BLE disconnection event"""
        # Start blinking LED every 100ms
        self.timer.init(period=100, mode=Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))

    def ble_irq(self, event, data):
        """Handles BLE events like connection, disconnection, and message reception"""
        global message
        
        if event == 1:  # _IRQ_CENTRAL_CONNECT: A device connected
            self.connected()

        elif event == 2:  # _IRQ_CENTRAL_DISCONNECT: Device disconnected
            self.advertiser()  # Restart advertising BLE
            self.disconnected()

        elif event == 3:  # _IRQ_GATTS_WRITE: A message was received
            buffer = self.ble.gatts_read(self.rx)  # Read incoming BLE message
            message = buffer.decode('UTF-8').strip()  # Decode and clean message
            print(message)  # Print received message
            
    def register(self):        
        """Registers the Nordic UART Service (NUS) for BLE communication"""
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'  # Main BLE service UUID
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'   # Receiving UUID (write from app)
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'   # Transmitting UUID (notify app)
            
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)  # Client writes to RX
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY) # ESP32 notifies TX
            
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART, )
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)  # Register services

    def send(self, data):
        """Send data via BLE notification"""
        self.ble.gatts_notify(0, self.tx, data + '\n')  

    def advertiser(self):
        """Advertise BLE device to make it discoverable"""
        name = bytes(self.name, 'UTF-8')  # Convert name to bytes
        adv_data = bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)  # Start advertising BLE
        print(adv_data)  
        print("\r\n")

# Pin configuration for LED, button, and relay
led = Pin(2, Pin.OUT)      # LED on GPIO2
but = Pin(0, Pin.IN)       # Push button on GPIO0
relay = Pin(15, Pin.OUT)   # Relay on GPIO15

ble = ESP32_BLE("ESP32")  # Initialize BLE with device name "ESP32"

def buttons_irq(pin):
    """Handles button press interrupts"""
    led.value(not led.value())  # Toggle LED
    ble.send('LED state will be toggled.')  # Send BLE notification
    print('LED state will be toggled.')   

but.irq(trigger=Pin.IRQ_FALLING, handler=buttons_irq)  # Attach interrupt to button

# Main loop to handle received BLE messages
while True:
    if message == "Relay_ON":
        relay.value(1)  # Turn relay on
        print("Relay Turned On")
        message = ""  # Clear message buffer

    elif message == "Relay_OFF":
        relay.value(0)  # Turn relay off
        print("Relay Turned Off")
        message = ""  # Clear message buffer

    sleep_ms(100)  # Delay to reduce CPU load
