from typing import Tuple, List
from gomoku_enum import Player
import itertools
import random
import logging
import sys

logger = logging.getLogger("Brain")
#logger.setLevel("DEBUG")

DEFAULT_NB_LAYER = 1

class Brain:
    def __init__(self, board, path=None, machine_learning_mode=False):
        self.board = board  # type: Board
        # if machine_learning_mode:
        #     self.network = (NeuralNetwork.unserialize(path) if path is not None
        #                     else NeuralNetwork(self.board.size * self.board.size, DEFAULT_NB_LAYER, 2, (self.board.size + 1) ** 2))

    def begin(self):
        """
        Returns:
            Tuple[int, int]: the x and y coordonate for put a piece
        """
        v = self.board.size // 2
        return (v, v)

    def play(self):
        """
        Returns:
            Tuple[int, int]: the x and y coordonate for put a piece
        """
        d = self.get_euristic_tab()
        logger.debug('\n'.join([f"{k} : {v}" for k, v in sorted(d.items(), key=lambda x: x[1], reverse=True) if v]))
        r = max(d.items(), key=lambda x: x[1])
        return r[0]
        #return self.put_rock_randomly()

    def get_euristic_tab(self):
        """
        Returns:
            Dict[Tuple[int, int], int]: A dict with coordinate as key and euristic board value as value
        """
        d = {i: 0 for i in ((x,y) for x, y, v in self.board.enumerate() if not v)}
        for ls in self.board.enumerate_comp():
            for x, y, pl in ls:
                if (x, y) not in d:
                    continue
                l = [v for _, _, v in ls]
                nb_none, nb_ally, nb_enemy = (sum(v == p for x, y, v in ls) for p in (Player.NONE, Player.ALLY, Player.ENEMY))
                if nb_ally and nb_enemy:  # This chunck can't won
                    continue
                if nb_ally == 4:
                    d[(x, y)] = 10000000
                    continue
                if nb_enemy == 4:
                    d[(x, y)] = 1000000
                    continue
                d[(x, y)] += self.no_border_pattern_bonus(l)
                d[(x, y)] += (max(nb_ally, nb_enemy) ** 3) * nb_none
        return d

    def no_border_pattern_bonus(self, ls):
        """
        Args:
            ls (List[Tuple[int, int, Player]]):
        Returns:
            int
        """
        for pl in (1, 2):
            if ls == [0, pl, pl, pl, 0]:
                return 100
        return 0


    def play_machine_learning(self):
        output = list(self.network.get_output([player.value for _, _, player in self.board.enumerate()]))
        logger.debug(f"Ai result is {output}")
        return tuple(int(val * 19) for val in output)

    def put_rock_randomly(self):
        coords = [(i, j) for i, j, v in self.board.enumerate() if not v]
        return random.choice(coords)
