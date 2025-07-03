import Model
import wiringpi
import logging
import sys

class LoggerWriter:
    def __init__(self, level):
        self.level = level

    def write(self, message):
        if message != '\n':
            self.level(message)

    def flush(self):
        pass  # Needed for file-like interface

# Configure logging to write to a file and flush on each write
logging.basicConfig(
    filename='output.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    filemode='a'
)

# Redirect print statements to logging
sys.stdout = LoggerWriter(logging.info)

print("Starting Sumo Robot Controller...")

#ports
leftIR = 1
rightIR = 3
frontleftIR = 4
frontrightIR = 5
colorLeft = 6
colorRight = 7

startbutton = 8

leftMotor = 17
rightMotor = 18


# Constants
debugMode = True


# #Private var setup
# p_leftIR = 0
# p_rightIR = 0
# p_colorLeft = 0
# p_colorRight = 0
# p_frontleft = 0
# p_frontright = 0

wiringpi.wiringPiSetupGpio()  # For GPIO pin numbering

wiringpi.pinMode(leftIR, 0)       # Set pin 6 to 0 ( INPUT )
wiringpi.pinMode(rightIR, 0)       # Set pin 6 to 0 ( INPUT )
wiringpi.pinMode(colorLeft, 0)       # Set pin 6 to 0 ( INPUT )
wiringpi.pinMode(colorRight, 0)       # Set pin 6 to 0 ( INPUT )
wiringpi.pinMode(frontleftIR, 0)
wiringpi.pinMode(frontrightIR, 0)
wiringpi.pinMode(startbutton, 0)  # Set pin 8 to 0 ( INPUT )

wiringpi.pinMode(leftMotor, 1)     # Set pin 17 to 1 ( OUTPUT )
wiringpi.pinMode(rightMotor, 1)    # Set pin 18 to 1 ( OUTPUT )

def GenerateRandomInput(rows):
    import random
    # Generate a random input for the model
    input_data = [random.uniform(0, 1) for _ in range(rows)]
    return input_data

def getSensorData():
    p_frontleftIR = wiringpi.digitalRead(frontleftIR)
    p_leftIR = wiringpi.digitalRead(leftIR)
    p_frontrightIR = wiringpi.digitalRead(frontrightIR)
    p_rightIR = wiringpi.digitalRead(rightIR)
    p_colorLeft = wiringpi.digitalRead(colorLeft)
    p_colorRight = wiringpi.digitalRead(colorRight)

    return [p_frontleftIR, p_frontrightIR, p_leftIR, p_rightIR, p_colorLeft, p_colorRight]


# Load model
model = Model.Model('BoardCode\\SumoAgent.onnx')
whitelineCounterLeft = 0;
whitelineCounterRight = 0;
sensorData = []
while True:
    if(wiringpi.digitalRead(startbutton) != 1): ##NEeed to calibrate
        print("Waiting for start button...")
        continue

    # Read sensor data
    ##For just RNG that bitch
    # sensorData = GenerateRandomInput(6)
    sensorData = getSensorData();

    print(f'Sensor Data: {sensorData}')


    ##Whiteline check
    if(sensorData[4] == 1 or sensorData[5] == 1 or whitelineCounterLeft > 0 or whitelineCounterRight > 0):
        print("Whiteline detected, turning around...")
        if sensorData[4] == 1 or sensorData[5] == 1:
            if sensorData[4] == 1:
                whitelineCounterLeft = 10 ##TODO: CALIBRATE
            if sensorData[5] == 1:
                whitelineCounterRight = 10##TODO: CALIBRATE
        else:
            whitelineCounterLeft = max(0, whitelineCounterLeft - 1)
            whitelineCounterRight = max(0, whitelineCounterRight - 1)
        # Turn around logic
        if(whitelineCounterLeft > 0):
            wiringpi.digitalWrite(leftMotor, 0)  # Stop left motor
            wiringpi.digitalWrite(rightMotor, 1)  # Turn right ##TODO: CALIBRATE
            print("Turning right due to left white line detection")
        elif(whitelineCounterRight > 0):
            wiringpi.digitalWrite(leftMotor, 1) ##TODO: CALIBRATE
            wiringpi.digitalWrite(rightMotor, 0)  # Turn left 
            print("Turning left due to right white line detection")
        continue

 


    predictions = model.run(sensorData)

    # Control motors based on predictions
    leftMotorOn = predictions[0] > 0.5
    rightMotorOn = predictions[1] > 0.5
    
    print(f'Left Motor: {"ON" if leftMotorOn else "OFF"}, Right Motor: {"ON" if rightMotorOn else "OFF"}')

    if(not debugMode):
        wiringpi.digitalWrite(leftMotor, 1 if leftMotorOn else 0)
        wiringpi.digitalWrite(rightMotor, 1 if rightMotorOn else 0)
print("Exiting Sumo Robot Controller...")