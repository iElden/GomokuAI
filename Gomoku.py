from sys import exit
import logging

from Board import Board
from Brain import Brain
from ProtocolManager import Protocol
from gomoku_enum import Order, Player

logging.basicConfig(level="WARNING")
logger = logging.getLogger("Main")


class GomokuAI:
    def __init__(self, size, print_board=False):
        self.board = Board(size)  # type: Board
        self.protocol = Protocol(self.board)  # type: Protocol
        self.brain = Brain(self.board)  # type: Brain
        self.print_board = print_board  # type: bool

    def run(self):
        logger.info("Now running")
        while True:
            order = self.protocol.recv_packet()
            if order == Order.NONE:
                continue
            elif order == Order.EXIT:
                print("EXIT !")
                exit(0)
            elif order == Order.PLAY:
                coords = self.brain.play()
                self.board.put(*coords, Player.ALLY)
                self.protocol.send(*coords)

            if self.print_board and self.board.has_been_edited:
                logger.info(f"Board state:\n{self.board.dump()}")


ai = GomokuAI(20, print_board=True)
ai.run()