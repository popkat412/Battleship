from typing import List, Tuple
import random
import config
from coord import Coord


class Ship:
    def __init__(self, segments: List[Coord]) -> None:
        self.segments: List[Coord] = segments

    def __str__(self) -> str:
        return str(self.segments)

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def generateShips(*sizes) -> list:
        ships = []
        for ship_size in sizes:
            if ship_size <= 0:
                raise Exception("Ship size must be > 0")

            # Pick a orientation
            orientation = random.choice(("vertical", "horizontal"))

            segments: List[Coord] = []
            if orientation == "vertical":
                # Pick a random starting point
                starting = Coord(random.randint(0, config.GRID_X - 1),
                                 random.randint(0, config.GRID_Y - 1 - (ship_size - 1)))
                for i in range(ship_size):
                    segments.append(Coord(starting.x, starting.y + i))
            else:
                starting = Coord(random.randint(0, config.GRID_X - 1 - (ship_size - 1)),
                                 random.randint(0, config.GRID_Y - 1))
                for i in range(ship_size):
                    segments.append(Coord(starting.x + i, starting.y))

            ships.append(Ship(segments))

        return ships
