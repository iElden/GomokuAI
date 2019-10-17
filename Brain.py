from typing import Tuple
from NeuralNetwork import NeuralNetwork
from gomoku_enum import Player
import random
import logging


logger = logging.getLogger("Brain")

DEFAULT_BOARD_SIZE = 20
DEFAULT_NB_LAYER = 1
DEFAULT_LAYER_SIZE = (DEFAULT_BOARD_SIZE + 1) ** 2


class Brain:
    def __init__(self, board, path=None, machine_learning_mode=False):
        self.board = board
        if machine_learning_mode:
            self.network = (NeuralNetwork.unserialize(path) if path is not None
                            else NeuralNetwork(DEFAULT_BOARD_SIZE * DEFAULT_BOARD_SIZE, DEFAULT_NB_LAYER, 2, DEFAULT_LAYER_SIZE))

    def play(self):
        """
        Returns:
            Tuple[int, int]: the x and y coordonate for put a piece
        """
        return self.put_rock_randomly()

    def play_machine_learning(self):
        output = list(self.network.get_output([player.value for _, _, player in self.board.enumerate()]))
        logger.debug(f"Ai result is {output}")
        return tuple(int(val * 19) for val in output)

    def put_rock_randomly(self):
        coords = [(i, j) for i, j, v in self.board.enumerate() if not v]
        return random.choice(coords)
