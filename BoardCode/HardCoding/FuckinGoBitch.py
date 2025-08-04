import wiringpi as w
import logging
import sys
import time

startbutton = 27  # Confirmed

# Sensor pins
leftIR = 24 ##Confirmed
rightIR = 16 ##Confirmed
frontLeftIR = 15 ##Confirmed
frontRightIR = 13 ##Confirmed

colorLeft = 26 ##Confirmed
colorRight = 25 ##Confirmed

# Motor pins
m1a = 21 ##Confirmed
m1b = 20 ##Confirmed
m2a = 22 ##Confirmed
m2b = 23 ##Confirmed

turnTimerLeft = 0
turnTimerRight = 0
turningTime = 25


w.wiringPiSetup()  # For GPIO pin numbering

# Setup sensor input pins
w.pinMode(leftIR, w.GPIO.INPUT)
w.pinMode(rightIR, w.GPIO.INPUT)
w.pinMode(colorLeft, w.GPIO.INPUT)
w.pinMode(colorRight, w.GPIO.INPUT)
w.pinMode(frontLeftIR, w.GPIO.INPUT)
w.pinMode(frontRightIR, w.GPIO.INPUT)

# Setup Start Button
w.pinMode(startbutton, w.GPIO.INPUT)
w.pullUpDnControl(startbutton, w.PUD_DOWN) # Sets internal pull up resistor function


# Setup motor output pins
w.pinMode(m1a, w.GPIO.OUTPUT)
w.pinMode(m1b, w.GPIO.OUTPUT)
w.pinMode(m2a, w.GPIO.OUTPUT)
w.pinMode(m2b, w.GPIO.OUTPUT)

def getSensorData():
    p_leftIR = not w.digitalRead(leftIR)
    p_rightIR = not w.digitalRead(rightIR)
    p_frontLeftIR = not w.digitalRead(frontLeftIR)
    p_frontRightIR = not w.digitalRead(frontRightIR)
    p_colorLeft = not w.digitalRead(colorLeft)
    p_colorRight = not w.digitalRead(colorRight)
    return p_leftIR, p_rightIR, p_frontLeftIR, p_frontRightIR, p_colorLeft, p_colorRight

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

    print("Starting Hardcoded Main Loop...")
    print("May god have mercy on our souls...")
    while True:
        time.sleep(0.1)
        if(w.digitalRead(startbutton) == 0):
            print("Waiting for button press...")
            turnTimerLeft = 0
            turnTimerRight = 0
            stopMotors()
            
        if(w.digitalRead(startbutton) == 1):

            p_leftIR, p_rightIR, p_frontLeftIR, p_frontRightIR, p_colorLeft, p_colorRight = getSensorData()
            
            print("Sensor Data - Left IR: {}, Right IR: {}, Front Left IR: {}, Front Right IR: {}, Color Left: {}, Color Right: {}".format(p_leftIR, p_rightIR, p_frontLeftIR, p_frontRightIR, p_colorLeft, p_colorRight))
            if(p_colorLeft == 1 or p_colorRight == 1 or turnTimerLeft > 0 or turnTimerRight > 0):
                #SHIT THERES A LINE... GO BACK
                if(p_colorLeft == 1 or turnTimerLeft > 0):
                    #LEFT LINE
                    if(p_colorLeft == 1):
                        turnTimerLeft = turningTime
                    elif turnTimerLeft > 0:
                        turnTimerLeft -= 1
                    turnRight()
                
                elif(p_colorRight == 1 or turnTimerRight > 0):
                    #RIGHT LINE
                    if(p_colorRight == 1):
                        turnTimerRight = turningTime
                    elif turnTimerRight > 0:
                        turnTimerRight -= 1
                    turnLeft()

            elif(p_frontLeftIR == 1 or p_frontRightIR == 1):
                #SHIT WE FOUND THE FUCKER, GET HIM!!!!
                if(p_frontLeftIR == 1):
                    #LEFT FRONT IR
                    turnRight()
                elif(p_frontRightIR == 1):
                    #RIGHT FRONT IR
                    turnLeft()
            
            else:
                #NO LINE, NO PEOPLE, GO FORWARD LONELY BOT
                moveForward()
except KeyboardInterrupt:
    print("I SHALL DIE IN HONOR OF MY CREATORS")