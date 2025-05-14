import Model
import csv
import wiringpi

#ports
leftIR = 1
centerIR = 2
rightIR = 3
colorLeft = 4
colorRight = 5
colorBackLeft = 6
colorBackRight = 7

# Constants
debugMode = True


#Private var setup
p_leftIR = 0
p_centerIR = 0
p_rightIR = 0
p_colorLeft = 0
p_colorRight = 0
p_colorBackLeft = 0
p_colorBackRight = 0

wiringpi.wiringPiSetupGpio()  # For GPIO pin numbering

wiringpi.pinMode(leftIR, 0)       # Set pin 6 to 0 ( INPUT )
wiringpi.pinMode(centerIR, 0)       # Set pin 6 to 0 ( INPUT )
wiringpi.pinMode(rightIR, 0)       # Set pin 6 to 0 ( INPUT )
wiringpi.pinMode(colorLeft, 0)       # Set pin 6 to 0 ( INPUT )
wiringpi.pinMode(colorRight, 0)       # Set pin 6 to 0 ( INPUT )
wiringpi.pinMode(colorBackLeft, 0)       # Set pin 6 to 0 ( INPUT )
wiringpi.pinMode(colorBackRight, 0)       # Set pin 6 to 0 ( INPUT )


def GenerateRandomInput():
    import random
    # Generate a random input for the model
    input_data = [random.uniform(0, 1) for _ in range(5)]
    return input_data

def getSensorData():
    p_leftIR = wiringpi.digitalRead(leftIR)
    p_centerIR = wiringpi.digitalRead(centerIR)
    p_rightIR = wiringpi.digitalRead(rightIR)
    p_colorLeft = wiringpi.digitalRead(colorLeft)
    p_colorRight = wiringpi.digitalRead(colorRight)
    p_colorBackLeft = wiringpi.digitalRead(colorBackLeft)
    p_colorBackRight = wiringpi.digitalRead(colorBackRight)

    return [p_leftIR, p_centerIR, p_rightIR, p_colorLeft, p_colorRight, p_colorBackLeft, p_colorBackRight]


# Load model
model = Model.Model('BoardCode\\SumoAgent.onnx')

sensorData = []
for i in range(5):
    # Read sensor data
    ##For just RNG that bitch
    sensorData = getSensorData();

    predictions = model.run(sensorData)

    if debugMode:
        print("Sensor Data: ", sensorData)
        print("Predictions: ", predictions)



