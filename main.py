from typing import Union
from ship import Ship
from pygame import Surface
from game_state import GameState
import pygame
import pygame.freetype
from player import Player
import config

pygame.init()

WIN = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
INFO_FONT = pygame.freetype.Font(config.FONT_NAME, config.FONT_SIZE)
TITLE_FONT = pygame.freetype.Font(config.FONT_NAME, config.TITLE_FONT_SIZE)
pygame.display.set_caption("Battleship")


def main():
    run = True
    FPS = 30
    clock = pygame.time.Clock()

    # Game data
    players = (Player("Human", []), Player("Computer"))
    currentPlayer = players[0]
    currentState = GameState.PLACE_SHIPS

    def dist_board_window(axis: str) -> float:
        if axis == "X":
            return (config.HEIGHT - config.GRID_Y * config.GRID_SIZE) / 2
        else:
            return (config.WIDTH - config.GRID_X * config.GRID_SIZE) / 2

    def draw_title_text(s: Surface, subhead: str) -> None:
        text_surface, text_rect = TITLE_FONT.render(
            f"BATTLESHIP: {subhead}", (255, 255, 255))
        s.blit(text_surface, (config.WIDTH / 2 -
                              text_rect.width / 2,
                              dist_board_window("X") / 2))

    def place_ships_screen() -> None:
        nonlocal run

        # TODO: 2 rows of ships at the bottom for player to drag
        ship_surfaces = []
        for size in config.SHIP_SIZES:
            ship_surfaces.append((Ship([]), pygame.Surface(
                (config.GRID_SIZE * size, config.GRID_SIZE))))  # Ships are all horizontal

            for i in range(size):
                pygame.draw.circle(
                    ship_surfaces[-1][1], ship_surfaces[-1][0].color, (config.GRID_SIZE / 2 + i * config.GRID_SIZE, config.GRID_SIZE / 2), (config.GRID_SIZE - config.SHIP_DISP_PADDING) / 2)

        while run:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Title
            draw_title_text(WIN, "Place your Ships")

            grid_surface = pygame.Surface(
                (config.GRID_X * config.GRID_SIZE, config.GRID_Y * config.GRID_SIZE))

            # Grid
            for i in range(config.GRID_X):
                for j in range(config.GRID_Y):
                    pygame.draw.rect(grid_surface, (255, 255, 255),
                                     pygame.Rect(i * config.GRID_SIZE, j * config.GRID_SIZE, config.GRID_SIZE, config.GRID_SIZE), 3)

            # Ships
            for ship in players[0].ships:
                for segment in ship.segments:
                    pygame.draw.circle(grid_surface, ship.color,
                                       (segment.x * config.GRID_SIZE + config.GRID_SIZE / 2,
                                        segment.y * config.GRID_SIZE + config.GRID_SIZE / 2),
                                       config.GRID_SIZE / 2 - config.SHIP_DISP_PADDING)

            WIN.blit(grid_surface, config.GRID_DISP_LOCATION)

            # Draggable ships at the bottom
            for i, s in enumerate(ship_surfaces):
                # NOTE: Maybe find some better way to automatically arrange the ships...
                # ! This only works if there are 4 ships
                if i < 2:  # Put first 2 in first column
                    WIN.blit(s[1], (config.WIDTH / 4,
                                    (config.HEIGHT - dist_board_window("Y")) + i * config.GRID_SIZE + config.SHIP_DISP_PADDING))
                else:  # Put next 2 in 3rd column
                    WIN.blit(s[1], (config.WIDTH / 2, (config.HEIGHT -
                                                       dist_board_window("Y")) + (i - 2) * config.GRID_SIZE + config.SHIP_DISP_PADDING))

            pygame.display.update()

    def game_screen():
        nonlocal run
        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Player text
            # text_surface, text_rect = TITLE_FONT.render(
            #     "BATTLESHIP", (255, 255, 255))
            # WIN.blit(text_surface, (config.WIDTH / 2 -
            #                         text_rect.width / 2, (config.HEIGHT - config.GRID_Y * config.GRID_SIZE) / 4))

    def redraw_window():
        # Background
        WIN.fill((0, 0, 0))

        if (currentState == GameState.PLACE_SHIPS):
            place_ships_screen()
        elif (currentState == GameState.GAME_SCREEN):
            game_screen()

    while run:
        clock.tick(FPS)
        # Current Player Text

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        redraw_window()


if __name__ == "__main__":
    main()
