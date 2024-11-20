from enum import Enum
class Move(Enum):
    HIT = 1
    STAND = 2
    DOUBLE = 3
    SPLIT = 4
    INSURANCE = 5
    EVEN_MONEY = 6
    SURRENDER = 7

    @staticmethod
    def getAllOptions():
        return [(move.value, move.name) for move in Move]