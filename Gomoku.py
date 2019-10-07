from sys import stderr

from Board import Board

class GomokuAI:
    def __init__(self, size):
        self.board = Board(size)
