from typing import List, Tuple
import random
import config
from coord import Coord

Color = Tuple[int, int, int]


def random_color() -> Color:
    return tuple([random.randint(100, 255) for _ in range(3)])


class Ship:
    def __init__(self, segments: List[Coord]) -> None:
        self.segments: List[Coord] = segments
        self.color: Color = random_color()

    def __str__(self) -> str:
        return str(self.segments)

    def __repr__(self) -> str:
        return self.__str__()

    def is_overlapping(self, o) -> bool:
        for self_seg in self.segments:
            for other_seg in o.segments:
                if self_seg == other_seg:
                    return True

        return False

    @staticmethod
    def generate_ships(*sizes) -> list:
        # FIXME: Check if overlapping ships not working
        ships = []

        def check_overlap(to_check: Ship) -> bool:
            """Returns true if to_check is overlapping with existing ships"""
            for ship in ships:
                if ship.is_overlapping(to_check):
                    return True

            return False

        for ship_size in sizes:
            if ship_size <= 0:
                raise Exception("Ship size must be > 0")

            # Pick a orientation
            orientation = random.choice(("vertical", "horizontal"))

            segments: List[Coord] = []
            while True:
                if orientation == "vertical":
                    segments = []
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

                s = Ship(segments)
                if not check_overlap(s):
                    ships.append(Ship(segments))
                    break

        return ships
