from math import exp
import random
import time
import pickle
import logging


logger = logging.getLogger("NeuralNetwork")


class Neuron:
    def __init__(self, w, b):
        self.weights = w.copy()
        self.bias = b

    def __str__(self):
        return f"Neuron: bias {self.bias}, weights {self.weights}"

    @staticmethod
    def activator(x):
        return 1 / (1 + exp(-x))

    def get_result(self, inputs):
        return self.activator(sum(self.weights[i] * inp for i, inp in enumerate(inputs)) + self.bias)


class NeuralLayer:
    def __init__(self, size, nb_inputs):
        logger.debug(f"Creating neural layer: {nb_inputs} inputs and {size} neurons")
        self.neurons = [
            Neuron(
                [random.uniform(-1, 1) for _ in range(nb_inputs)],
                random.uniform(-0.2, 0.2)
            ) for _ in range(size)
        ]

    def get_output(self, inputs):
        return (neuron.get_result(inputs) for neuron in self.neurons)


class NeuralNetwork:
    def __init__(self, nb_inputs, nb_hidden_layers, nb_outputs, layer_size):
        random.seed(time.time())
        self.nb_inputs = nb_inputs
        self.nb_hidden_layers = nb_hidden_layers
        self.nb_outputs = nb_outputs
        self.layer_size = layer_size
        self.layers = [
            NeuralLayer(layer_size, nb_inputs),
            *(NeuralLayer(layer_size, layer_size) for _ in range(0, nb_hidden_layers)),
            NeuralLayer(nb_outputs, layer_size)
        ]
        logger.debug([str(n) for n in self.layers[-1].neurons])

    def get_layer_output(self, inputs, index):
        inputs = tuple(inputs)
        logger.debug(f"Layer inputs: {inputs}")
        if index == len(self.layers) - 1:
            return self.layers[index].get_output(inputs)
        return self.get_layer_output(self.layers[index].get_output(inputs), index + 1)

    def get_output(self, inputs):
        return self.get_layer_output(tuple(inputs), 0)

    def serialize(self, file):
        with open(file, "wb") as fd:
            pickle.dump(self, fd)

    @classmethod
    def unserialize(cls, file):
        with open(file, "rb") as fd:
            return pickle.load(fd)
