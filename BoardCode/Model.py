import onnxruntime as rt
import numpy as np

class Model:
    def __init__(self, path):
        self.path = path
        self.session = rt.InferenceSession(path)
        # Get the name of the input layer
        self.input_name = self.session.get_inputs()[0].name

    def run(self, input_data, returnAllPredictions=False):
        input_data = np.array(input_data, dtype=np.float32)
        # Make predictions
        predictions = self.session.run(None, {self.input_name: [input_data]})

        if returnAllPredictions:
            return predictions
        else:
            return predictions[2]
