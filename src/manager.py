#!/usr/bin/env python3

from sys import exit, argv
from Manager.exc import ProgramKO, ProgramCrashed
from Manager.Manager import Manager
import logging
import asyncio

logging.basicConfig(level="INFO")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        manager = Manager(argv[1], argv[2])
        winner = manager.run()
    except ProgramCrashed as e:
        print(f"CRASHED: Program {e.who} has crashed (Program {e.who ^ 0b11} won) !")
        print(f"Reason: {e}")
    except ProgramKO as e:
        print(f"FAIL: Program {e.who} returned wrong output (Program {e.who ^ 0b11} won) !")
        print(f"Reason: {e}")
    else:
        print(f"OK: The program {winner} won !")
        print(manager.board)
        exit(winner)

