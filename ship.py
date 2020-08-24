from typing import List, Tuple
import sys
import random
import config
from typedefs import Color
from coord import Coord
import utilities as utils
from enum import Enum, auto


class ShipOrientation(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()


class Ship:
    def __init__(self, segments: List[Coord]) -> None:
        self.segments: List[Coord] = segments
        self.size = len(self.segments)
        self.color: Color = utils.random_color()

    def __str__(self) -> str:
        return f"<Ship>{self.segments}"

    def __repr__(self) -> str:
        return self.__str__()

    def is_overlapping(self, o) -> bool:
        for self_seg in self.segments:
            for other_seg in o.segments:
                if self_seg == other_seg:
                    return True

        return False


def generate_ships(*sizes) -> List[Ship]:
    ships: List[Ship] = []

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
        orientation = random.choice(list(ShipOrientation))

        segments: List[Coord] = []
        generateCount = 0
        while generateCount < 100:
            generateCount += 1

            if orientation == ShipOrientation.VERTICAL:
                segments = generate_segments(Coord(random.randint(0, config.GRID_X - 1),
                                                   random.randint(0, config.GRID_Y - 1 - (ship_size - 1))), ship_size, orientation)
            elif orientation == ShipOrientation.HORIZONTAL:
                segments = generate_segments(Coord(
                    random.randint(0, config.GRID_X - 1 - (ship_size - 1)),
                    random.randint(0, config.GRID_Y - 1)), ship_size, orientation)

            s = Ship(segments)

            if not check_overlap(s):
                ships.append(Ship(segments))
                break

        if generateCount >= 100:
            sys.exit("Error: Infinite loop while generating ships")

    return ships


def generate_segments(starting_coord: Coord, ship_size: int, orientation: ShipOrientation) -> List[Coord]:

    segments: List[Coord] = []
    if orientation == ShipOrientation.VERTICAL:
        # Pick a random starting point
        for i in range(ship_size):
            segments.append(Coord(starting_coord.x, starting_coord.y + i))
    elif orientation == ShipOrientation.HORIZONTAL:
        for i in range(ship_size):
            segments.append(Coord(starting_coord.x + i, starting_coord.y))
    return segments
