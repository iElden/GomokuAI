class ProgramCrashed(Exception):
    """Raised when a program crashed"""
    def __init__(self, who, msg):
        self.who = who
        Exception.__init__(self, msg)

class ProgramKO(Exception):
    """Raised when receive wrong output"""
    def __init__(self, who, msg):
        self.who = who
        Exception.__init__(self, msg)