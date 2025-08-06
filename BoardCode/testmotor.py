import wiringpi as w
import time

w.wiringPiSetup()  # For GPIO pin numbering


# Motor pins
m1a = 20 ##Confirmed
m1b = 21 ##Confirmed
m2a = 23 ##Confirmed
m2b = 22 ##Confirmed

# Motor Speed Forward (MSF) and Backward (MSB) and full speed (FS)
fs = 100
msf = 60
msb = 50

# Setup motor output pins (Possibly not needed)
w.pinMode(m1a, 4)     # Set to SOFT PWM OUTPUT
w.pinMode(m1b, 4)     # Set to SOFT PWM OUTPUT
w.pinMode(m2a, 4)     # Set to SOFT PWM OUTPUT
w.pinMode(m2b, 4)     # Set to SOFT PWM OUTPUT

# Create Software Driven PWM Pins
w.softPwmCreate(m1a, 0, fs)
w.softPwmCreate(m1b, 0, fs)
w.softPwmCreate(m2a, 0, fs)
w.softPwmCreate(m2b, 0, fs)

#w.pwmSetMode(w.PWM_MODE_MS) # Set PWM Type

def moveForward():
    print("Moving forward")
    w.softPwmWrite(m1a, msf)
    w.softPwmWrite(m1b, 0)
    w.softPwmWrite(m2a, msf)
    w.softPwmWrite(m2b, 0)

def moveBackward():
    print("Moving backward")
    w.softPwmWrite(m1a, 0)
    w.softPwmWrite(m1b, msb)
    w.softPwmWrite(m2a, 0)
    w.softPwmWrite(m2b, msb)

def sprint():
    print("Sprinting")
    w.softPwmWrite(m1a, fs)
    w.softPwmWrite(m1b, 0)
    w.softPwmWrite(m2a, fs)
    w.softPwmWrite(m2b, 0)

def turnLeft():
    print("Turning left")
    w.softPwmWrite(m1a, 0)
    w.softPwmWrite(m1b, msb)
    w.softPwmWrite(m2a, msb)
    w.softPwmWrite(m2b, 0)

def turnRight():
    print("Turning right")
    w.softPwmWrite(m1a, msb)
    w.softPwmWrite(m1b, 0)
    w.softPwmWrite(m2a, 0)
    w.softPwmWrite(m2b, msb)

def stopMotors():
    print("Stopping motors")
    w.softPwmWrite(m1a, 0)
    w.softPwmWrite(m1b, 0)
    w.softPwmWrite(m2a, 0)
    w.softPwmWrite(m2b, 0)
try:
    while True:
        moveForward()
        time.sleep(4)  # Run motors forward for 1 second
        moveBackward()
        time.sleep(4)  # Run motors in reverse for 1 second
        turnLeft()
        time.sleep(4) # Turn left for 1 second
        turnRight()
        time.sleep(4) # Turn right for 1 second
        stopMotors()
        time.sleep(4) # Stop motors for 1 second
        
        
except KeyboardInterrupt:
    w.softPwmStop(m1a)
    w.softPwmStop(m1b)
    w.softPwmStop(m2a)
    w.softPwmStop(m2b)
    print("I SHALL DIE IN HONOR OF MY CREATORS")

