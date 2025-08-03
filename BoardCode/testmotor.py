import wiringpi as w
import time

w.wiringPiSetup()  # For GPIO pin numbering


# Motor pins
m1a = 21 ##Confirmed
m1b = 20 ##Confirmed
m2a = 22 ##Confirmed
m2b = 23 ##Confirmed

# Motor Speed Forward (MSF) and Backward (MSB) and full speed (FS)
fs = 100
msf = 60
msb = 50

# Setup motor output pins
w.pinMode(m1a, 4)     # Set to SOFT PWM OUTPUT
w.pinMode(m1b, 4)     # Set to SOFT PWM OUTPUT
w.pinMode(m2a, 4)     # Set to SOFT PWM OUTPUT
w.pinMode(m2b, 4)     # Set to SOFT PWM OUTPUT

w.softPwmCreate(m1a, 0, fs) # Create Software Driven PWM Pin
w.softPwmCreate(m1b, 0, fs) # Create Software Driven PWM Pin
w.softPwmCreate(m2a, 0, fs) # Create Software Driven PWM Pin
w.softPwmCreate(m2b, 0, fs) # Create Software Driven PWM Pin

#w.pwmSetMode(w.PWM_MODE_MS) # Set PWM Type (Hard Oscilation)

def moveForward():
    print("Moving forward")
    w.digitalWrite(m1a, msf)
    w.digitalWrite(m1b, 0)
    w.digitalWrite(m2a, msf)
    w.digitalWrite(m2b, 0)

def moveBackward():
    print("Moving backward")
    w.digitalWrite(m1a, 0)
    w.digitalWrite(m1b, msb)
    w.digitalWrite(m2a, 0)
    w.digitalWrite(m2b, msb)
try:
    while True:
        moveForward()
        time.sleep(1)  # Run motors forward for 1 second
        moveBackward()
        time.sleep(1)  # Run motors in reverse for 1 second
        
except KeyboardInterrupt:
    w.softPwmStop(m1a)
    w.softPwmStop(m1b)
    w.softPwmStop(m2a)
    w.softPwmStop(m2b)
    print("I SHALL DIE IN HONOR OF MY CREATORS")

