from typing import List, Tuple
import random
import config
from coord import Coord


class Ship:
    def __init__(self, length: int) -> None:
        self.segments: List[Coord] = []
        self.length: int = length

    @staticmethod
    def generateBoard(*sizes) -> List[Coord]:
        for ship_size in sizes:
            # Pick a orientation
            orientation = random.choice(("vertical", "horizontal"))

            segments: List[Coord] = []
            if orientation == "vertical":
                # Pick a random starting point
                starting = Coord(random.randint(0, config.GRID_X - 1),
                                 random.randint(0, config.GRID_Y - ship_size))
