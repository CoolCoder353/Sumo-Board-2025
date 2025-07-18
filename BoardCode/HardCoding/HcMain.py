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
        if(p_colorLeft == 1 or p_colorRight == 1):
            #SHIT THERES A LINE... GO BACK

