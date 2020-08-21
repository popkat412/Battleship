import pygame
from typing import List
from config import GRID_SIZE
from ship import Ship
import config

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battleship")


def main():
    run = True
    FPS = 30
    clock = pygame.time.Clock()

    # Game data
    ships: List[Ship] = Ship.generate_ships(*config.SHIP_SEGMENTS)
    miss_coord = []
    hit_coord = []

    def redraw_window():
        # Background
        WIN.fill((0, 0, 0))

        # Grid
        for i in range(config.GRID_X):
            for j in range(config.GRID_Y):
                pygame.draw.rect(WIN, (255, 255, 255),
                                 pygame.Rect(i * config.GRID_SIZE, j * config.GRID_SIZE, config.GRID_SIZE, config.GRID_SIZE), 3)

        # Ships
        for ship in ships:
            for segment in ship.segments:
                pygame.draw.circle(WIN, ship.color,
                                   (segment.x * config.GRID_SIZE + config.GRID_SIZE / 2,
                                    segment.y * config.GRID_SIZE + config.GRID_SIZE / 2),
                                   config.GRID_SIZE / 2 - config.SHIP_PADDING)

        pygame.display.update()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        redraw_window()


if __name__ == "__main__":
    main()
