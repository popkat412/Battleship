from typedefs import Pos
from coord import Coord
from typing import List
from ship import Ship, ShipOrientation
import pygame
import config


class GridAnnotation:
    """Grid annotations can be added to grids to draw extra info in the grid squares"""

    def __init__(self, surface: pygame.Surface, coord: Coord):
        self.surface = surface
        self.coord = coord


class Grid:
    """Grid class for storing and drawing grid and grid annotations to avoid repeated code"""

    def __init__(self, disp_pos: Pos):
        self.surface: pygame.Surface = pygame.Surface((config.GRID_X * config.GRID_SIZE,
                                                       config.GRID_Y * config.GRID_SIZE))
        self.annotations: List[GridAnnotation] = []
        self.disp_pos = disp_pos

    def add_ships(self, ships: List[Ship]):
        for s in ships:
            ship_surface = pygame.Surface(
                (s.size * config.GRID_SIZE, config.GRID_SIZE)
                if s.orientation == ShipOrientation.VERTICAL else
                (config.GRID_SIZE, s.size * config.GRID_SIZE))
            for i, seg in enumerate(s.segments):
                pygame.draw.circle(ship_surface, s.color, (
                    config.GRID_SIZE / 2,
                    i * config.GRID_SIZE + config.GRID_SIZE / 2),
                    (config.GRID_SIZE - config.SHIP_DISP_PADDING) / 2)
                self.add_annotations([GridAnnotation(ship_surface, seg)])

    def add_annotations(self, annotations: List[GridAnnotation]):
        self.annotations.extend(annotations)

    def draw(self, screen: pygame.Surface):

        for i in range(config.GRID_X):
            for j in range(config.GRID_Y):
                pygame.draw.rect(
                    self.surface,
                    config.FOREGROUND_COLOR,
                    pygame.Rect(
                        i * config.GRID_SIZE,
                        j * config.GRID_SIZE,
                        config.GRID_SIZE,
                        config.GRID_SIZE), 3)

        for a in self.annotations:
            self.surface.blit(a.surface, (a.coord.x * config.GRID_SIZE,
                                          a.coord.y * config.GRID_SIZE))

        screen.blit(self.surface, self.disp_pos)

    def compensated_grid_loc(self):
        return self.surface.get_rect().move(*config.GRID_DISP_LOCATION)
