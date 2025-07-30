import wiringpi as w
import logging
import sys
import time

startbutton = 27  # Confirmed

toggle = False

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

# Motor Speed Forward and Backward
fs = 100
msf = 60
msb = 50

turnTimerLeft = 0
turnTimerRight = 0
turningTime = 25

readyToSwitch = True

w.wiringPiSetup()  # For GPIO pin numbering

# Setup input pins
w.pinMode(leftIR, w.GPIO.INPUT)       # Set to INPUT
w.pinMode(rightIR, w.GPIO.INPUT)      # Set to INPUT
w.pinMode(colorLeft, w.GPIO.INPUT)    # Set to INPUT
w.pinMode(colorRight, w.GPIO.INPUT)   # Set to INPUT
w.pinMode(frontLeftIR, w.GPIO.INPUT)  # Set to INPUT
w.pinMode(frontRightIR, w.GPIO.INPUT) # Set to INPUT
w.pinMode(startbutton, w.GPIO.INPUT)  # Set to INPUT

# Setup motor output pins
w.pinMode(m1a, 4)     # Set to SOFT PWM OUTPUT
w.pinMode(m1b, 4)     # Set to SOFT PWM OUTPUT
w.pinMode(m2a, 4)     # Set to SOFT PWM OUTPUT
w.pinMode(m2b, 4)     # Set to SOFT PWM OUTPUT

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


print("Starting Hardcoded Main Loop...")
print("May god have mercy on our souls...")
while True:
    time.sleep(0.1)  # Sleep to prevent busy waiting
    #print(w.digitalRead(startbutton))

    # Toggle functionality for the button
    if(w.digitalRead(startbutton) == 0 and readyToSwitch):
        toggle = not toggle
        readyToSwitch = False
        # 3 second wait time as per regulation
        print("Toggle state changed to:", toggle)
        time.sleep(3)
    else:
        readyToSwitch = True

    if(toggle == False):
        #print("Waiting for button press...")
        turnTimerLeft = 0
        turnTimerRight = 0
        stopMotors()
        
    if(toggle == True):
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
    # else:
    #     stopMotors()