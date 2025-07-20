import wiringpi


m1a = 17
m1b = 19

m2a = 18
m2b = 16

def setup_motor_pins():
    """Setup GPIO pins for motor control."""
    wiringpi.wiringPiSetupGpio()  # Use BCM GPIO numbering
    wiringpi.pinMode(m1a, wiringpi.GPIO.OUTPUT)
    wiringpi.pinMode(m1b, wiringpi.GPIO.OUTPUT)
    wiringpi.pinMode(m2a, wiringpi.GPIO.OUTPUT)
    wiringpi.pinMode(m2b, wiringpi.GPIO.OUTPUT)

def motor_forward():
    """Set motors to move forward."""
    wiringpi.digitalWrite(m1a, wiringpi.GPIO.HIGH)
    wiringpi.digitalWrite(m1b, wiringpi.GPIO.LOW)
    wiringpi.digitalWrite(m2a, wiringpi.GPIO.HIGH)
    wiringpi.digitalWrite(m2b, wiringpi.GPIO.LOW)

def motor_reverse():
    """Set motors to move in reverse."""
    wiringpi.digitalWrite(m1a, wiringpi.GPIO.LOW)
    wiringpi.digitalWrite(m1b, wiringpi.GPIO.HIGH)
    wiringpi.digitalWrite(m2a, wiringpi.GPIO.LOW)
    wiringpi.digitalWrite(m2b, wiringpi.GPIO.HIGH)

while True:
    motor_forward()
    wiringpi.delay(1000)  # Run motors forward for 1 second
    motor_reverse()
    wiringpi.delay(1000)  # Run motors in reverse for 1 second

