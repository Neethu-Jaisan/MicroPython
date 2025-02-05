from machine import Pin, PWM
import time

# Initialize PWM on GPIO15 at 50Hz (standard for servos)
servo = PWM(Pin(15), freq=50)

def set_servo_angle(angle):
    """
    Set the servo to the given angle (0 to 180 degrees).
    Most servos expect a pulse width between 0.5ms (0°) and 2.5ms (180°) out of a 20ms period.
    In this example with ESP32 PWM (duty range 0-1023):
      - 0.5ms corresponds roughly to a duty of ~25
      - 2.5ms corresponds roughly to a duty of ~128
    The formula maps the angle (0-180) to this duty range.
    """
    duty = int((angle / 180) * (128 - 25) + 25)
    servo.duty(duty)

while True:
    # Sweep from 0° to 180°
    for angle in range(0, 181, 10):
        set_servo_angle(angle)
        print("Angle:", angle)
        time.sleep(0.5)
    # Sweep back from 180° to 0°
    for angle in range(180, -1, -10):
        set_servo_angle(angle)
        print("Angle:", angle)
        time.sleep(0.5)
