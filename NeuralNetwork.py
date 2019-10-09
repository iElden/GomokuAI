from Neuron import Neuron
import random


class NeuralLayer:
    def __init__(self, size, nb_inputs):
        self.neurons = [
            Neuron(
                (random.random() for _ in range(nb_inputs)),
                random.random()
            ) for _ in range(size)
        ]

    def get_output(self, inputs):
        return (neuron.get_result(inputs) for neuron in self.neurons)


class NeuralNetwork:
    def __init__(self, nb_inputs, nb_hidden_layers, nb_outputs, layer_size):
        self.layers = [
            NeuralLayer(layer_size, nb_inputs),
            *(NeuralLayer(layer_size, layer_size) for _ in range(0, nb_hidden_layers)),
            NeuralLayer(nb_outputs, layer_size)
        ]

    def get_layer_output(self, inputs, index):
        if index == len(self.layers) - 1:
            return self.layers[index].get_output(inputs)
        return self.get_layer_output(self.layers[index].get_output(inputs), index + 1)

    def get_output(self, inputs):
        return self.get_layer_output(inputs, 0)
