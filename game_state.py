from enum import Enum, auto


class GameState(Enum):
    START_SCREEN = auto()  # Note not needed yet
    PLACE_SHIPS = auto()
    GAME_SCREEN = auto()
