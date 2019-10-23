import asyncio
from .Program import Program, ProgramKO, ProgramCrashed

class UnitTest:
    def __init__(self, stdin=None, stdout=None, return_code=None, timeout=5):
        self.program = None  # type: Program
        self.stdin = stdin  # type: str
        self.stdout = stdout  # type: str
        self.return_code = return_code  # type: int
        self.timeout = timeout

    async def _run_program(self, program_path):
        self.program = await Program.create(program_path, nb=1)

    async def run_test(self, program_path):
        await self._run_program(program_path)
        if self.stdin:
            await self.program.send(self.stdin)
        await self.program.end()
        output = await self.program.proc.stdout.read()
        output = output.decode('ASCII').rstrip('\n')
        if self.stdout is not None and output != self.stdout:
            raise TestFailed(f"The output of program differ from excepted output.\nExcept: \"{self.stdout}\"\nGot: \"{output}\"")
        if self.return_code is not None and self.program.proc.returncode != self.return_code:
            raise TestFailed(f"Invalid exit code. Excepted {self.program.proc.returncode} but got {self.return_code}")
        return 'OK'

    async def run(self, program_path):
        try:
            return await self.run_test(program_path)
        except ProgramCrashed as e:
            return f"CRASH: {e}"
        except ProgramKO as e:
            return f"KO: {e}"
        except TestFailed as e:
            return f"FAIL: {e}"



class TestFailed(Exception):
    """Raised when a test fail"""