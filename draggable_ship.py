from coord import Coord
from typing import Optional
from ship import Ship, ShipOrientation
import pygame
import config
from typedefs import Pos


class DraggableShip:
    """ Ship with a surface and helper methods for ships that can be dragged by the user"""

    def __init__(self, size: int, default_pos: Pos) -> None:
        self.ship: Ship = Ship([Coord(-1, -1) for _ in range(size)])

        self.initWithOrientation(ShipOrientation.HORIZONTAL)

        # This is the relative mouse pos from top right
        # This is also an indicator whether the ship is being dragged
        # If this is not None, indicates that the ship is being dragged
        self.rel_mouse_pos: Optional[Pos] = None

        self.default_pos: Pos = default_pos

        # Position of the ship when on the grid, used when user drags ships onto the grid
        # If this is not None, indicates that the ship is placed on the grid
        self.grid_pos: Optional[Pos] = None

        # TODO: Use orientation on ship class instead of defining own
        self.orientation = ShipOrientation.HORIZONTAL

    def initWithOrientation(self, orientation: ShipOrientation):
        print(f"initWithOrientation: {orientation}")
        if orientation == ShipOrientation.VERTICAL:
            self.orientation = ShipOrientation.VERTICAL
            self.surface = pygame.Surface(
                (config.GRID_SIZE, config.GRID_SIZE * self.ship.size))
            for i in range(self.ship.size):
                pygame.draw.circle(
                    self.surface, self.ship.color, (
                        int(config.GRID_SIZE / 2),
                        int(config.GRID_SIZE / 2 + i * config.GRID_SIZE)),
                    int((config.GRID_SIZE - config.SHIP_DISP_PADDING) / 2))
        elif orientation == ShipOrientation.HORIZONTAL:
            self.orientation = ShipOrientation.HORIZONTAL
            self.surface = pygame.Surface(
                (config.GRID_SIZE * self.ship.size, config.GRID_SIZE))
            for i in range(self.ship.size):
                pygame.draw.circle(
                    self.surface, self.ship.color, (
                        int(config.GRID_SIZE / 2 + i * config.GRID_SIZE),
                        int(config.GRID_SIZE / 2)),
                    int((config.GRID_SIZE - config.SHIP_DISP_PADDING) / 2))

    def reset(self):
        self.ship.segments = [
            Coord(-1, -1) for _ in range(self.ship.size)]
        self.grid_pos = None
        self.initWithOrientation(ShipOrientation.HORIZONTAL)

    def toggle_orientation(self):
        if self.orientation == ShipOrientation.HORIZONTAL:
            if self.rel_mouse_pos is not None:
                self.rel_mouse_pos = (
                    self.rel_mouse_pos[1], self.rel_mouse_pos[0])
            self.initWithOrientation(ShipOrientation.VERTICAL)
        elif self.orientation == ShipOrientation.VERTICAL:
            if self.rel_mouse_pos is not None:
                self.rel_mouse_pos = (
                    self.rel_mouse_pos[1], self.rel_mouse_pos[0])
            self.initWithOrientation(ShipOrientation.HORIZONTAL)

    def get_screen_pos_rect(self) -> pygame.Rect:
        r = self.surface.get_rect()

        if self.rel_mouse_pos is not None:
            r = r.move(*self.rel_mouse_pos)
        elif self.grid_pos is not None:
            r = r.move(*self.grid_pos)
        else:
            r = r.move(*self.default_pos)

        return r
