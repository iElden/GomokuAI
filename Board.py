from typing import List
from gomoku_enum import Player

class Board:
    def __init__(self, size):
        self.size = size  #type: int
        self.raw = [[0] * size for _ in range(size)]  # type: List[List[Player]]

    def get(self, x, y):
        """
        Args:
            x (int): x coordinate
            y (int): y coordinate
        Returns:
            Player: Returns an int according to the stone placed on the square (0: None, 1: Ally, 2: Enemy)
        """
        return self.raw[y][x]

    def put(self, x, y, player):
        """
        Args:
            x (int): x coordinate
            y (int): y coordinate
            player (Player): Player who put the rock
        Returns:
            None: None
        """
        self.raw[y][x] = player