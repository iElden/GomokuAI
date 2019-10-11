from typing import List, Tuple
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

    def enumerate(self):
        """
        Returns:
            Tuple[int, int, Player]: a tuple with x, y, and a player for each case in the board
        """
        for j, ls in enumerate(self.raw):
            for i, v in enumerate(ls):
                yield (i, j, v)
        return

    def reset(self, size=None):
        if size:
            self.size = size
        self.has_been_edited = True
        self.raw = [[Player.NONE] * self.size for _ in range(self.size)]

    def get(self, x, y):
        """
        Args:
            x (int): x coordinate
            y (int): y coordinate
        Returns:
            Player: Returns an int according to the stone placed on the square (0: None, 1: Ally, 2: Enemy)
        """
        if x >= self.size or y >= self.size:
            raise ValueError("Value given is >= of the map size")
        return self.raw[y - 1][x - 1]

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
        self.raw[y - 1][x - 1] = player

    def get_winner(self):
        """
        Returns:
            Player: Player who won
        """
        rotated = [*zip(*self.raw)]
        for player in (Player.ALLY, Player.ENEMY):
            for y in range(self.size - 4):
                for x in range(self.size - 4):
                    if sum(i for i in self.raw[x][y:y+5] if i == player) == 5:
                        return player
                    if sum(i for i in rotated[x][y:y+5] if i == player) == 5:
                        return player
                    if sum(i for i in [self.raw[x+j][y+j] for j in range(5)] if i == player) == 5:
                        return player

        return Player.NONE


class EmplacementAlreadyUser(Exception):
    """Exception raised when the emplacement of a stone is already taken"""