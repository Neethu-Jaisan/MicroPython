from machine import Timer, Pin

# Initialize LED on GPIO 2
led = Pin(2, Pin.OUT)

# Initialize Button on GPIO 0
but = Pin(0, Pin.IN, Pin.PULL_UP)

# Create a global Timer instance
timer = Timer(0)

# Interrupt handler function
def buttons_irq(pin):
    print("Triggered")
    # Toggle the LED periodically
    timer.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: led.value(not led.value()))

# Attach interrupt to button (falling edge = button press)
but.irq(trigger=Pin.IRQ_FALLING, handler=buttons_irq)

