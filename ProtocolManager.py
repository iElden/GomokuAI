import logging
from gomoku_enum import Player, Order

ABOUT = {
    "name": "My name is nobody",
    "version": "0.1",
    "author": "Etienne BERTRAND",
    "country": "France"
}

logger = logging.getLogger("Protocol")

class Protocol:
    def __init__(self, board):
        self.FUNC = {
            "START": lambda size: self.cmd_start(int(size)),
            "TURN": lambda x, y: self.cmd_turn(int(x), int(y)),
            "BEGIN": lambda: self.cmd_begin(),
            "BOARD": lambda: self.cmd_board(),
            "INFO": lambda key, value: self.cmd_info(key, value),
            "END": lambda: self.cmd_end(),
            "ABOUT": lambda: self.cmd_about(),
            "RECTSTART": lambda x, y: self.cmd_rectstart(int(x), int(y)),
            "RESTART": lambda: self.cmd_restart(),
            "TAKEBACK": lambda x, y: self.cmd_traceback(int(x), int(y)),
            "PLAY": lambda x, y: self.cmd_play(int(x), int(y)),
        }
        self.board = board  #type: Board

    def send(self, *data, sep=','):
        logger.debug(f"SENDING *{data}")
        print(*data, sep=sep)

    def send_error(self, exception):
        logger.error(f"ERROR {type(exception).__name__} {exception}")
        print(f"ERROR {type(exception).__name__} {exception}")

    def send_unknow(self, method_name):
        print(f"UNKNOWN The command {method_name} was unknown")

    def _recv(self):
        return input().strip()

    def recv_packet(self):
        logger.debug("Waiting for Manager input")
        text = self._recv()
        logger.info(f"Recieve: {text}")
        cmd, *args = text.split(' ')
        try:
            return self.FUNC[cmd](*args)
        except KeyError:
            self.send_unknow(cmd)
        except Exception as exception:
            self.send_error(exception)
        return Order.NONE

    def cmd_start(self, size):
        if size < 5:
            raise InvalidInput("Size can't be < at 5")
        self.board.reset(size)
        self.send("OK")
        return Order.NONE

    def cmd_turn(self, x, y):
        self.board.put(x, y, Player.ENEMY)
        return Order.PLAY

    def cmd_begin(self):
        return Order.PLAY

    def cmd_board(self):
        self.board.reset(self.board.size)
        while True:
            text = self._recv()
            if text == "DONE":
                break
            x, y, player_id = [int(i) for i in text.split()]
            self.board.put(x, y, Player(player_id))
        return Order.PLAY

    def cmd_info(self, key, value):
        logger.warning("Command info ignored")
        return Order.NONE

    def cmd_end(self):
        return Order.EXIT

    def cmd_about(self):
        self.send(*[f"{k}={repr(v)}" for k, v in ABOUT.items()], sep=', ')
        return Order.NONE

    def cmd_rectstart(self, x, y):
        raise InvalidInput("The rectangle shape is not supported")

    def cmd_restart(self):
        self.board.reset()
        self.send("OK")
        return Order.NONE

    def cmd_traceback(self, x, y):
        self.board.put(x, y, Player.NONE)
        self.send("OK")
        return Order.NONE

    def cmd_play(self, x, y):
        self.board.put(x, y, Player.ALLY)
        self.send("OK")
        return Order.NONE



class InvalidInput(Exception):
    """Exception raised in case of invalid input"""
