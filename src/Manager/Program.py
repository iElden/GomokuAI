import re
from asyncio import subprocess, wait_for, TimeoutError
from typing import Tuple
import logging

from .exc import ProgramKO, ProgramCrashed

EXCEPTED_OUTPUT = r"^(\d+),(\d+)$"

class Program:
    def __init__(self):
        """ASYNCIO CLASS : DON'T CALL THIS, call .create() instead"""
        self.nb = None  # type: int
        self.proc = None # type: subprocess.Process
        self.logger = None # type: logging.Logger

    @classmethod
    async def create(cls, path, *, nb):
        self = cls()
        self.nb = nb
        self.proc = await subprocess.create_subprocess_exec(path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.logger = logging.getLogger("Program")
        self.log("READY")
        return self

    def log(self, msg, level=20):
        self.logger.log(level, f"{self.nb}> {msg}")

    async def send(self, txt : str) -> None:
        self.log(f"Send to program: {txt}")
        self.proc.stdin.write(f"{txt}\n".encode('ASCII'))
        self.log(f"Sent", level=10)

    async def recv(self, timeout=5) -> str:
        r = self.proc.returncode
        if r is not None:
            raise ProgramCrashed(self.nb, f"The manager excepted a output but the program was dead with return code {r}")
        try:
            self.log(f"Waiting for recieve", level=10)
            line = await wait_for(self.proc.stdout.readline(), timeout)
            self.log(f"recieved", level=10)
        except TimeoutError:
            raise ProgramCrashed(self.nb, f"The Program didn't answer within {timeout} seconds")

        if not line:
            raise ProgramCrashed(self.nb, "The manager excepted a output but the program reach EOF")
        return line.decode('ASCII').rstrip('\n')

    async def recv_coord(self) -> Tuple[int, int]:
        coords = await self.recv()
        r = re.findall(EXCEPTED_OUTPUT, coords)
        self.log(f"received coords: {coords}")
        if not r:
            raise ProgramKO(self.nb, f"The output must match regular expression {EXCEPTED_OUTPUT} but it was {coords}")
        return tuple(int(i) for i in r[0])

    async def communicate_coords(self, txt : str) -> Tuple[int, int]:
        await self.send(txt)
        return await self.recv_coord()

    async def end(self):
        await self.send('END')
        try:
            await wait_for(self.proc.wait(), 1)
        except TimeoutError:
            await self.proc.kill()
            raise ProgramCrashed(self.nb, "The program didn't stop in 1 second after a END has been sent")

    async def kill(self):
        if self.proc.returncode is not None:
            await self.proc.kill()