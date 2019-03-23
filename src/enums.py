from enum import Enum, auto

__all__ = ['Screens', 'Weapons', 'Zoom']


class Screens(Enum):
    map = 0
    inventory = 1
    play = 2


class Weapons(Enum):
    primary = 0
    secondary = 1
    other = 2


class Zoom(Enum):
    x1 = 0
    x2 = 1
    x3 = 2
    x4 = 3
    x6 = 4
    xx = -1
