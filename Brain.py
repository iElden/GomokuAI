from typing import Tuple
import random

from gomoku_enum import Player

class Brain:
    def __init__(self, board):
        self.board = board

    def play(self):
        """
        Returns:
            Tuple[int, int]: the x and y coordonate for put a piece
        """
        return self.put_rock_randomly()

    def put_rock_randomly(self):
        coords = [(i, j) for i, j, v in self.board.enumerate() if not v]
        return random.choice(coords)