from coord import Coord
from typing import Optional
from ship import Ship, ShipOrientation
import pygame
import config
from typedefs import Pos


class DraggableShip:
    def __init__(self, size: int, default_pos: Pos) -> None:
        self.ship: Ship = Ship([Coord(-1, -1) for _ in range(size)])

        # All ships are horizontal
        self.surface: pygame.Surface = pygame.Surface(
            (config.GRID_SIZE * size, config.GRID_SIZE))

        # This is the relative mouse pos from top right
        # This is also an indicator whether the ship is being dragged
        # If this is not None, indicates that the ship is being dragged
        self.rel_mouse_pos: Optional[Pos] = None

        self.default_pos: Pos = default_pos

        # Position of the ship when on the grid, used when user drags ships onto the grid
        # If this is not None, indicates that the ship is placed on the grid
        self.grid_pos: Optional[Pos] = None

        self.orientation = ShipOrientation.HORIZONTAL

    def get_screen_pos_rect(self) -> pygame.Rect:
        r = self.surface.get_rect()

        if self.rel_mouse_pos is not None:
            r = r.move(*self.rel_mouse_pos)
        elif self.grid_pos is not None:
            r = r.move(*self.grid_pos)
        else:
            r = r.move(*self.default_pos)

        return r
