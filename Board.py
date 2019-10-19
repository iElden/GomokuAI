from typing import List, Tuple, Iterator
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
            Iterator[Tuple[int, int, Player]]: a tuple with x, y, and a player for each case in the board
        """
        for j, ls in enumerate(self.raw):
            for i, v in enumerate(ls):
                yield (i, j, v)
        return

    def enumerate_comp(self):
        """
        Returns:
            Iterator[List[Tuple[int, int, Player]]]: Generator that return a list of all 5 combinaison in boards
        """
        rotated = [*zip(*self.raw)]
        for y in range(self.size - 4):
            for x in range(self.size - 4):
                rx = range(x, x+5)
                ry = range(y, y+5)
                yield [*zip(rx, [y]*5, self.raw[y][x:x+5])]
                yield [*zip([y]*5, rx, rotated[y][x:x+5])]
                yield [*zip(rx, ry, [self.raw[y+i][x+i] for i in range(5)])]
        for y in range(4, self.size):
            for x in range(self.size - 4):
                yield [*zip(range(x, x+5), range(y, y-5, -1), [self.raw[y-i][x+i] for i in range(5)])]
        return

    def reset(self, size=None):
        if size:
            self.size = size
        self.has_been_edited = True
        self.raw = [[Player.NONE] * self.size for _ in range(self.size)]
        #self.raw = [[(i, j) for i in range(self.size)] for j in range(self.size)]

    def get(self, x, y):
        """
        Args:
            x (int): x coordinate
            y (int): y coordinate
        Returns:
            Player: Returns an int according to the stone placed on the square (0: None, 1: Ally, 2: Enemy)
        """
        if x > self.size or y > self.size or x < 0 or y < 0:
            raise ValueError("Value given is out of map")
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

    def get_winner(self):
        """
        Returns:
            Player: Player who won
        """
        for player in (Player.ALLY, Player.ENEMY):
            for ls in self.enumerate_comp():
                if len([p for x, y, p in ls if p == player]) == 5:
                    return player
        return Player.NONE


class EmplacementAlreadyUser(Exception):
    """Exception raised when the emplacement of a stone is already taken"""