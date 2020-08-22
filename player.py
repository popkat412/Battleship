from typing import List
from ship import Ship
import config


class Player:
    def __init__(self, name: str, ships: List[Ship] = None) -> None:
        self.ships = ships or Ship.generate_ships(*config.SHIP_SEGMENTS)
        self.name = name
