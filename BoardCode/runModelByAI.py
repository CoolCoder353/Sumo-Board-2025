import onnxruntime as rt
import numpy as np

# Load the ONNX model
model_path = 'BoardCode\\SumoAgent.onnx'
session = rt.InferenceSession(model_path)

# Prepare your input data
# Ensure the shape and type match what the model expects
input_data = np.array([[0.5, 0.3, 0.2, 0.8, 0.1]], dtype=np.float32)

# Get the name of the input layer
input_name = session.get_inputs()[0].name

# Make predictions
predictions = session.run(None, {input_name: input_data})

# Output predictions
print(predictions[2])