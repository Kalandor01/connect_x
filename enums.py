from enum import Enum


class Win_types(Enum):
    NO_WIN = 0
    WIN = 1
    DRAW = 2


class Play_modes(Enum):
    P_P = 0
    P_PC = 1
    PC_P = 2
    PC_PC = 3