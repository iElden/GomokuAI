from math import exp


class Neuron:
    def __init__(self, w, b):
        self.weights = w.copy()
        self.bias = b

    @staticmethod
    def activator(x):
        return 1 / (1 + exp(-x))

    def get_result(self, inputs):
        return self.activator(sum(self.weights[i] * inputs[i] for i in range(len(inputs))) + self.bias)
