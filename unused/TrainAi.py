#!/usr/bin/env python3
import sys
from NeuralNetwork import NeuralNetwork


def train_ais():
    pass


def get_best_ai():
    return ais[0]


try:
    network = NeuralNetwork.unserialize("data/brain.dat")
except Exception:
    ais = (NeuralNetwork(*[int(arg) for arg in sys.argv]) for i in range(500))

while True:
    try:
        train_ais()
    except KeyboardInterrupt:
        break

get_best_ai().serialize("data/brain.dat")