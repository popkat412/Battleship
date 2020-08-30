from typing import List
from ship import Ship, generate_ships
import config


class Player:
    """ Keeps track of player info"""

    def __init__(self, name: str, ships: List[Ship] = None) -> None:
        if ships is not None:
            self.ships: List[Ship] = ships
        else:
            self.ships = generate_ships(*config.SHIP_SIZES)

        self.name: str = name
