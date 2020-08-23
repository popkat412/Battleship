from typing import List
from config import Pos
from draggable_ship import DraggableShip
from game_state import GameState
import pygame
import pygame.freetype
from player import Player
import config
import utilities as utils

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

    def draw_title_text(s: pygame.Surface, subhead: str) -> None:
        text_surface, text_rect = TITLE_FONT.render(
            f"BATTLESHIP: {subhead}", config.FOREGROUND_COLOR)
        s.blit(text_surface, (int(config.WIDTH / 2 -
                                  text_rect.width / 2),
                              int(dist_board_window("X") / 2)))

    def place_ships_screen() -> None:
        nonlocal run

        # TODO: 2 rows of ships at the bottom for player to drag
        draggable_ships: List[DraggableShip] = []

        for i, size in enumerate(config.SHIP_SIZES):
            # NOTE: Maybe find some better way to automatically arrange the ships...
            # ! This only works if there are 4 ships
            pos = (int(config.WIDTH / 4),
                   int((config.HEIGHT - dist_board_window("Y")) + i * config.GRID_SIZE +
                       config.SHIP_DISP_PADDING))  # Put first 2 in first column
            if i >= 2:  # Put next 2 in 2nd column
                pos = (int(config.WIDTH / 2), int((config.HEIGHT -
                                                   dist_board_window("Y")) + (i - 2) * config.GRID_SIZE + config.SHIP_DISP_PADDING))
            draggable_ships.append(DraggableShip(size, pos))

            for i in range(size):
                pygame.draw.circle(
                    draggable_ships[-1].surface, draggable_ships[-1].ship.color, (int(config.GRID_SIZE / 2 + i * config.GRID_SIZE), int(config.GRID_SIZE / 2)), int((config.GRID_SIZE - config.SHIP_DISP_PADDING) / 2))

        while run:
            clock.tick(FPS)

            grid_surface = pygame.Surface(
                (config.GRID_X * config.GRID_SIZE, config.GRID_Y * config.GRID_SIZE))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Mouse button down
                    print(f"Mouse down: {pygame.mouse.get_pos()}")
                    for s in draggable_ships:
                        if s.get_screen_pos_rect().collidepoint(pygame.mouse.get_pos()):
                            print("Clicked on ship")
                            mousePos: Pos = pygame.mouse.get_pos()
                            s.rel_mouse_pos = utils.sub_pos(
                                mousePos, utils.rect_to_pos(s.get_screen_pos_rect()))

                elif event.type == pygame.MOUSEBUTTONUP:
                    # Mouse button up
                    for s in draggable_ships:
                        # If ship is being dragged
                        if s.rel_mouse_pos is not None:
                            # If released inside board
                            if grid_surface.get_rect().move(*config.GRID_DISP_LOCATION).collidepoint(pygame.mouse.get_pos()):

                                print("Released on grid!")
                                s.grid_pos = utils.sub_pos(
                                    pygame.mouse.get_pos(), s.rel_mouse_pos)

                        s.rel_mouse_pos = None

            # Background
            WIN.fill(config.BACKGROUND_COLOR)

            # Title
            draw_title_text(WIN, "Place your Ships")

            # Grid
            for i in range(config.GRID_X):
                for j in range(config.GRID_Y):
                    pygame.draw.rect(grid_surface, config.FOREGROUND_COLOR,
                                     pygame.Rect(i * config.GRID_SIZE, j * config.GRID_SIZE, config.GRID_SIZE, config.GRID_SIZE), 3)

            # Ships (may not be necessary)
            for ship in players[0].ships:
                for segment in ship.segments:
                    pygame.draw.circle(grid_surface, ship.color,
                                       (segment.x * config.GRID_SIZE + config.GRID_SIZE / 2,
                                        segment.y * config.GRID_SIZE + config.GRID_SIZE / 2),
                                       config.GRID_SIZE / 2 - config.SHIP_DISP_PADDING)

            WIN.blit(grid_surface, config.GRID_DISP_LOCATION)

            # Draggable ships at the bottom
            for s in draggable_ships:
                if s.rel_mouse_pos is not None:
                    mousePos = pygame.mouse.get_pos()
                    WIN.blit(
                        s.surface, utils.sub_pos(mousePos, s.rel_mouse_pos))
                elif s.grid_pos is not None:
                    WIN.blit(s.surface, s.grid_pos)
                else:
                    WIN.blit(s.surface, s.default_pos)

            pygame.display.update()

    def game_screen():
        nonlocal run

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Player text
            # text_surface, text_rect = TITLE_FONT.render(
            #     "BATTLESHIP", config.FOREGROUND_COLOR)
            # WIN.blit(text_surface, (config.WIDTH / 2 -
            #                         text_rect.width / 2, (config.HEIGHT - config.GRID_Y * config.GRID_SIZE) / 4))

    def redraw_window():
        # Background
        WIN.fill(config.BACKGROUND_COLOR)

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

    pygame.quit()


if __name__ == "__main__":
    main()
