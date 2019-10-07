from typing import List
from gomoku_enum import Player

PLAYER_REPR = [" ", "X", "O"]

class Board:
    def __init__(self, size):
        self.size = None  #type: int
        self.raw = None   #type: List[List[Player]]
        self.reset(size)
        self.has_been_edited = False

    def __str__(self):
        return '\n'.join([''.join([PLAYER_REPR[i] for i in ls]) for ls in self.raw])

    def dump(self):
        self.has_been_edited = False
        return self.__str__()

    def reset(self, size=None):
        if size:
            self.size = size
        self.has_been_edited = True
        self.raw = [[0] * size for _ in range(size)]

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
        self.has_been_edited = True
        self.raw[y][x] = player


class EmplacementAlreadyUser(Exception):
    """Exception raised when the emplacement of a stone is already taken"""