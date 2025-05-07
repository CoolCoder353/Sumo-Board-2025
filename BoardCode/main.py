import Model
import csv

# Constants
debugMode = True

def GenerateRandomInput():
    import random
    # Generate a random input for the model
    input_data = [random.uniform(0, 1) for _ in range(5)]
    return input_data


# Load model
model = Model.Model('BoardCode\\SumoAgent.onnx')

sensorData = []
for i in range(5):
    # Read sensor data
    ##For just RNG that bitch
    sensorData = GenerateRandomInput()

    predictions = model.run(sensorData)

    if debugMode:
        print("Sensor Data: ", sensorData)
        print("Predictions: ", predictions)



