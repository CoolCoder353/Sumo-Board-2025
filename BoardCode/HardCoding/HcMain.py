import wiringpi as w
import logging
import sys

startbutton = 0

leftIR = 0
rightIR = 0
frontLeftIR = 0
frontRightIR = 0

colorLeft = 0
colorRight = 0

leftMotor = 0
rightMotor = 0


turnTimerleft = 0
turnTimerRight = 0
turningTime = 25

w.wiringPiSetupGpio()  # For GPIO pin numbering

w.pinMode(leftIR, 0)       # Set pin 6 to 0 ( INPUT )
w.pinMode(rightIR, 0)       # Set pin 6 to 0 ( INPUT )
w.pinMode(colorLeft, 0)       # Set pin 6 to 0 ( INPUT )
w.pinMode(colorRight, 0)       # Set pin 6 to 0 ( INPUT )
w.pinMode(frontLeftIR, 0)
w.pinMode(frontRightIR, 0)
w.pinMode(startbutton, 0)  # Set pin 8 to 0 ( INPUT )

w.pinMode(leftMotor, 1)     # Set pin 17 to 1 ( OUTPUT )
w.pinMode(rightMotor, 1)    # Set pin 18 to 1 ( OUTPUT )

def getSensorData ():
    p_leftIR = w.digitalRead(leftIR)
    p_rightIR = w.digitalRead(rightIR)
    p_frontLeftIR = w.digitalRead(frontLeftIR)
    p_frontRightIR = w.digitalRead(frontRightIR)
    p_colorLeft = w.digitalRead(colorLeft)
    p_colorRight = w.digitalRead(colorRight)
    return p_leftIR,p_rightIR,p_frontLeftIR,p_frontRightIR,p_colorLeft,p_colorRight

while True:
    if(w.digitalread(startbutton)):
        p_leftIR,p_rightIR,p_frontLeftIR,p_frontRightIR,p_colorLeft,p_colorRight = getSensorData()
        if(p_colorLeft == 1 or p_colorRight == 1 or turnTimerLeft > 0 or turnTimerRight > 0):
            #SHIT THERES A LINE... GO BACK
            if(p_colorLeft == 1 or turnTimerLeft > 0):
                #LEFT LINE
                if(p_colorLeft == 1):
                    turnTimerLeft = turningTime
                elif turnTimerLeft > 0:
                    turnTimerLeft -= 1
                w.digitalWrite(leftMotor, 1)
                w.digitalWrite(rightMotor, 0)
              
            elif(p_colorRight == 1 or turnTimerRight > 0):
                #RIGHT LINE
                if(p_colorRight == 1):
                    turnTimerRight = turningTime
                elif turnTimerRight > 0:
                    turnTimerRight -= 1
                
                w.digitalWrite(leftMotor, 0)
                w.digitalWrite(rightMotor, 1)

        elif(p_frontLeftIR == 1 or p_frontRightIR == 1):

            #SHIT WE FOUND THE FUCKER, GET HIM!!!!
            if(p_frontLeftIR == 1):
                #LEFT FRONT IR
                w.digitalWrite(leftMotor, 0)
                w.digitalWrite(rightMotor, 1)
            elif(p_frontRightIR == 1):
                #RIGHT FRONT IR
                w.digitalWrite(leftMotor, 1)
                w.digitalWrite(rightMotor, 0)
          
        else:
            #NO LINE, NO PEOPLE, GO FORWARD LONELY BOT
            w.digitalWrite(leftMotor, 1)
            w.digitalWrite(rightMotor, 1)
