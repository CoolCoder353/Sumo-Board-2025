import wiringpi as w
import logging
import sys
import time

startbutton = 27  ##Confirmed

# Sensor pins
leftIR = 24 ##Confirmed
rightIR = 16 ##Confirmed
frontLeftIR = 15 ##Confirmed
frontRightIR = 13 ##Confirmed

colorLeft = 26 ##Confirmed
colorRight = 25 ##Confirmed

# Motor pins
m1a = 20 ##Confirmed
m1b = 21 ##Confirmed
m2a = 23 ##Confirmed
m2b = 22 ##Confirmed

# Motor Speed Forward (MSF) and Backward (MSB) and full speed (FS)
fs = 100
msf = 60
msb = 50

timerToggle = True

w.wiringPiSetup()  # For GPIO pin numbering

# Setup sensot input pins
w.pinMode(leftIR, w.GPIO.INPUT)
w.pinMode(rightIR, w.GPIO.INPUT)
w.pinMode(colorLeft, w.GPIO.INPUT)
w.pinMode(colorRight, w.GPIO.INPUT)
w.pinMode(frontLeftIR, w.GPIO.INPUT)
w.pinMode(frontRightIR, w.GPIO.INPUT)

# Setup Start Button
w.pinMode(startbutton, w.GPIO.INPUT)
w.pullUpDnControl(startbutton, w.PUD_DOWN) # Sets internal pull up resistor function


# Setup motor output pins (SoftPWM) (--POSSIBLY NOT NEEDED--)
w.pinMode(m1a, 4)
w.pinMode(m1b, 4)
w.pinMode(m2a, 4)
w.pinMode(m2b, 4)

# Create Software Driven PWM Pin
w.softPwmCreate(m1a, 0, fs)
w.softPwmCreate(m1b, 0, fs)
w.softPwmCreate(m2a, 0, fs)
w.softPwmCreate(m2b, 0, fs) 

#w.pwmSetMode(w.PWM_MODE_MS) # Set PWM Type (Hard Oscilation)

def getSensorData():
    p_leftIR = not w.digitalRead(leftIR)
    p_rightIR = not w.digitalRead(rightIR)
    p_frontLeftIR = not w.digitalRead(frontLeftIR)
    p_frontRightIR = not w.digitalRead(frontRightIR)
    p_colorLeft = not w.digitalRead(colorLeft)
    p_colorRight = not w.digitalRead(colorRight)
    return p_leftIR, p_rightIR, p_frontLeftIR, p_frontRightIR, p_colorLeft, p_colorRight

def moveBackward():
    print("Moving backward")
    w.digitalWrite(m1a, msf)
    w.digitalWrite(m1b, 0)
    w.digitalWrite(m2a, msf)
    w.digitalWrite(m2b, 0)

def Sprint():
    print("FULL SPEED AHEAD")
    w.digitalWrite(m1a, 0)
    w.digitalWrite(m1b, fs)
    w.digitalWrite(m2a, 0)
    w.digitalWrite(m2b, fs)

def moveForward():
    print("Moving forward")
    w.digitalWrite(m1a, 0)
    w.digitalWrite(m1b, msb)
    w.digitalWrite(m2a, 0)
    w.digitalWrite(m2b, msb)

def turnLeft():
    print("Turning left")
    w.digitalWrite(m1a, 0)
    w.digitalWrite(m1b, msf)
    w.digitalWrite(m2a, msf)
    w.digitalWrite(m2b, 0)

def turnRight():
    print("Turning right")
    w.digitalWrite(m1a, msf)
    w.digitalWrite(m1b, 0)
    w.digitalWrite(m2a, 0)
    w.digitalWrite(m2b, msf)

def stopMotors():
    print("Stopping motors")
    w.digitalWrite(m1a, 0)
    w.digitalWrite(m1b, 0)
    w.digitalWrite(m2a, 0)
    w.digitalWrite(m2b, 0)

try:

    print("Starting Hardcoded Main Loop...")
    print("May god have mercy on our souls...")
    while True:
        if(w.digitalRead(startbutton) == 0):
            print("Waiting for button press...")
            timerToggle = True
            stopMotors()
            
            
        if(w.digitalRead(startbutton) == 1):
            if timerToggle == True:
                timerToggle = False
                time.sleep(3)
            
            p_leftIR, p_rightIR, p_frontLeftIR, p_frontRightIR, p_colorLeft, p_colorRight = getSensorData()
            
            ##print("Sensor Data - Left IR: {}, Right IR: {}, Front Left IR: {}, Front Right IR: {}, Color Left: {}, Color Right: {}".format(p_leftIR, p_rightIR, p_frontLeftIR, p_frontRightIR, p_colorLeft, p_colorRight))
            if(p_colorLeft == 1 or p_colorRight == 1):
                #SHIT THERES A LINE... GO BACK
                if(p_colorLeft == 1):
                    #LEFT LINE
                    print("Left Color Sensor Detect")
                    # moveBackward()
                    # w.delay(250)
                    turnRight()
                    time.sleep(0.25)
                elif(p_colorRight == 1):
                    #RIGHT LINE
                    print("Right Color Sensor Detect")
                    # moveBackward()
                    # w.delay(250)
                    turnLeft()
                    time.sleep(0.25) 

            elif(p_frontLeftIR == 1 or p_frontRightIR == 1):
                #SHIT WE FOUND THE FUCKER, GET HIM!!!!
                if(p_frontLeftIR == 1):
                    #LEFT FRONT IR
                    turnLeft()
                    w.delay(250)
                elif(p_frontRightIR == 1):
                    #RIGHT FRONT IR
                    turnRight()
                    w.delay(250)
            else:
                #NO LINE, NO PEOPLE, GO FORWARD LONELY BOT
                moveForward()
except KeyboardInterrupt:
    w.softPwmStop(m1a)
    w.softPwmStop(m1b)
    w.softPwmStop(m2a)
    w.softPwmStop(m2b)
    print("I SHALL DIE IN HONOR OF MY CREATORS")