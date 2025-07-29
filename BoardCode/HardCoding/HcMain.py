import wiringpi as w
import logging
import sys

startbutton = 14

motorspeed = 100

leftIR = 24 ##Confirmed
rightIR = 20 ##Confirmed
frontLeftIR = 23 ##Confirmed
frontRightIR = 21 ##Confirmed

colorLeft = 26 ##Confirmed
colorRight = 25 ##Confirmed

# Motor pins
m1a = 17
m1b = 19
m2a = 18
m2b = 16

turnTimerLeft = 0
turnTimerRight = 0
turningTime = 25

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
w.pinMode(m1a, w.GPIO.PWM_OUTPUT)     # Set to OUTPUT
w.pinMode(m1b, w.GPIO.PWM_OUTPUT)     # Set to OUTPUT
w.pinMode(m2a, w.GPIO.PWM_OUTPUT)     # Set to OUTPUT
w.pinMode(m2b, w.GPIO.PWM_OUTPUT)     # Set to OUTPUT

def getSensorData():
    p_leftIR = not w.digitalRead(leftIR)
    p_rightIR = not w.digitalRead(rightIR)
    p_frontLeftIR = not w.digitalRead(frontLeftIR)
    p_frontRightIR = not w.digitalRead(frontRightIR)
    p_colorLeft = not w.digitalRead(colorLeft)
    p_colorRight = not w.digitalRead(colorRight)
    return p_leftIR, p_rightIR, p_frontLeftIR, p_frontRightIR, p_colorLeft, p_colorRight

def moveForward():
    w.pwmWrite(m1a, motorspeed)
    w.pwmWrite(m1b, 0)
    w.pwmWrite(m2a, motorspeed)
    w.pwmWrite(m2b, 0)

def moveBackward():
    w.pwmWrite(m1a, 0)
    w.pwmWrite(m1b, motorspeed)
    w.pwmWrite(m2a, 0)
    w.pwmWrite(m2b, motorspeed)

def turnLeft():
    w.pwmWrite(m1a, 0)
    w.pwmWrite(m1b, motorspeed)
    w.pwmWrite(m2a, motorspeed)
    w.pwmWrite(m2b, 0)

def turnRight():
    w.pwmWrite(m1a, motorspeed)
    w.pwmWrite(m1b, 0)
    w.pwmWrite(m2a, 0)
    w.pwmWrite(m2b, motorspeed)

def stopMotors():
    w.pwmWrite(m1a, 0)
    w.pwmWrite(m1b, 0)
    w.pwmWrite(m2a, 0)
    w.pwmWrite(m2b, 0)

while True:
    if(w.digitalRead(startbutton)):
        p_leftIR, p_rightIR, p_frontLeftIR, p_frontRightIR, p_colorLeft, p_colorRight = getSensorData()
        
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
    else:
        stopMotors()