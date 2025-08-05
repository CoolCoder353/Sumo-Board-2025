import wiringpi as w
import time

# Motor pins
m1a = 21 ##Confirmed
m1b = 19 ##Confirmed
m2a = 22 ##Confirmed
m2b = 23 ##Confirmed

# Motor Speed Forward (MSF) and Backward (MSB) and full speed (FS)
fs = 100
msf = 60
msb = 50

w.wiringPiSetup()  # For GPIO pin numbering

# Setup motor output pins
w.pinMode(m1a, w.GPIO.OUTPUT)
w.pinMode(m1b, w.GPIO.OUTPUT)
w.pinMode(m2a, w.GPIO.OUTPUT)
w.pinMode(m2b, w.GPIO.OUTPUT)

def moveForward():
    #print("Moving forward")
    w.digitalWrite(m1a, 1)
    w.digitalWrite(m1b, 0)
    w.digitalWrite(m2a, 1)
    w.digitalWrite(m2b, 0)

def moveBackward():
    #print("Moving backward")
    w.digitalWrite(m1a, 0)
    w.digitalWrite(m1b, 1)
    w.digitalWrite(m2a, 0)
    w.digitalWrite(m2b, 1)

def turnLeft():
    #print("Turning left")
    w.digitalWrite(m1a, 0)
    w.digitalWrite(m1b, 1)
    w.digitalWrite(m2a, 1)
    w.digitalWrite(m2b, 0)

def turnRight():
    #print("Turning right")
    w.digitalWrite(m1a, 1)
    w.digitalWrite(m1b, 0)
    w.digitalWrite(m2a, 0)
    w.digitalWrite(m2b, 1)

def stopMotors():
    #print("Stopping motors")
    w.digitalWrite(m1a, 0)
    w.digitalWrite(m1b, 0)
    w.digitalWrite(m2a, 0)
    w.digitalWrite(m2b, 0)

try:
    while True:
        moveForward()
        time.sleep(1)  # Run motors forward for 1 second
        moveBackward()
        time.sleep(1)  # Run motors in reverse for 1 second
        turnLeft()
        time.sleep(1) # Turn left for 1 second
        turnRight()
        time.sleep(1) # Turn right for 1 second
        stopMotors()
        time.sleep(1) # Stop motors for 1 second
        
        
except KeyboardInterrupt:
    print("I SHALL DIE IN HONOR OF MY CREATORS")

