from typing import List
from ship import Ship
import config


class Player:
    def __init__(self, name: str, ships: List[Ship] = None) -> None:
        if ships is not None:
            self.ships: List[Ship] = ships
        else:
            self.ships = Ship.generate_ships(*config.SHIP_SIZES)

        self.name: str = name
