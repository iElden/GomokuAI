from sys import stderr, exit
import logging

from Board import Board
from ProtocolManager import Protocol
from gomoku_enum import Order

logging.basicConfig(level="INFO")
logger = logging.getLogger("Main")

class GomokuAI:
    def __init__(self, size, print_board=False):
        self.board = Board(size)  # type: Board
        self.protocol = Protocol(self.board)  # type: Protocol
        self.print_board = print_board  # type: bool

    def run(self):
        logger.info("Now running")
        while True:
            order = self.protocol.recv_packet()
            if self.print_board and self.board.has_been_edited:
                logger.info(f"Board state:\n{self.board.dump()}")
            if order == Order.NONE:
                continue
            elif order == Order.EXIT:
                print("EXIT !")
                exit(0)
            elif order == Order.PLAY:
                self.protocol.send(0, 0)


ai = GomokuAI(19, print_board=True)
ai.run()