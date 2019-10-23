from typing import Tuple
import asyncio
import logging

from Board import Board
from gomoku_enum import Player
from .Program import Program
from .exc import ProgramCrashed, ProgramKO

logger = logging.getLogger("Manager")


class Manager:
    def __init__(self, program1, program2, size=20):
        self.loop = asyncio.get_event_loop()
        self.program1, self.program2 = self.loop.run_until_complete(self._create_programs(program1, program2))  # type: Program
        self.programs = (self.program1, self.program2)  # type: Tuple[Program, Program]
        self.size = size  # type: int
        self.board = Board(size)  # type: Board

    async def _create_programs(self, program1, program2):
        try:
            p1 = await Program.create(program1, nb=1)  # type: Program
        except Exception as exception:
            raise ProgramCrashed(1, f"Failed to init: {type(exception).__name__} {exception}")
        try:
            p2 = await Program.create(program2, nb=2)  # type: Program
        except Exception as exception:
            raise ProgramCrashed(1, f"Failed to init: {type(exception).__name__} {exception}")
        return p1, p2

    async def send_end_to_programs(self):
        for program in self.programs:
            await program.end()

    async def kill_programs(self):
        for program in self.programs:
            await program.kill()

    async def send_starts_to_programs(self):
        for program in self.programs:
            await program.send(f"START {self.size}")
            opt = await program.recv()
            if opt != "OK":
                raise ProgramKO(program.nb, f"The program must be return 'OK' after a START but it was {opt}")

    async def run_game(self):
        current_turn = 2

        await self.send_starts_to_programs()
        x, y = await self.program1.communicate_coords("BEGIN")
        self.board.put(x, y, Player(1))
        while True:
            program = self.programs[current_turn - 1]
            x, y = await program.communicate_coords(f"TURN {x},{y}")
            try:
                if self.board.get(x, y):
                    raise ProgramKO(program.nb, "The program put a rock in not empty slot")
            except ValueError:
                raise ProgramKO(program.nb, f"The program put rock out of board range: tried ({x}, {y}) but size was {self.size}")
            self.board.put(x, y, Player(current_turn))
            if self.board.get_winner():
                await self.send_end_to_programs()
                return current_turn
            logger.info(f"Board State:\n{self.board}")
            current_turn ^= 0b11

    def run(self):
        try:
            return self.loop.run_until_complete(self.run_game())
        except Exception as e:
            self.loop.run_until_complete(self.send_end_to_programs())
            raise e



