from enum import IntEnum

class Player(IntEnum):
    NONE = 0
    ALLY = 1
    ENEMY = 2

class Order(IntEnum):
    NONE = 0
    PLAY = 1
    BEGIN = 2
    EXIT = 3