import sys
from coord import Coord
from typing import List, Optional
from config import Pos
from draggable_ship import DraggableShip
from game_state import GameState
import pygame
import pygame.freetype
from player import Player
import config
from ship import ShipOrientation
from ship import generate_segments
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
    current_player = players[0]
    current_state = GameState.PLACE_SHIPS

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
        nonlocal current_state

        draggable_ships: List[DraggableShip] = []

        for i, size in enumerate(config.SHIP_SIZES):
            # NOTE: Maybe find some better way to automatically arrange the ships...
            # * This only works if there are 4 ships
            pos = (int(config.WIDTH / 4),
                   int((config.HEIGHT - dist_board_window("Y")) + i * config.GRID_SIZE +
                       config.SHIP_DISP_PADDING))  # Put first 2 in first column
            if i >= 2:  # Put next 2 in 2nd column
                pos = (int(config.WIDTH / 2), int((config.HEIGHT -
                                                   dist_board_window("Y")) + (i - 2) * config.GRID_SIZE + config.SHIP_DISP_PADDING))
            draggable_ships.append(DraggableShip(size, pos))

        run_place_ships_screen = True

        while run_place_ships_screen:
            clock.tick(FPS)

            grid_surface: pygame.Surface = pygame.Surface(
                (config.GRID_X * config.GRID_SIZE, config.GRID_Y * config.GRID_SIZE))

            start_button = pygame.Surface(
                (config.GRID_SIZE * 3, config.GRID_SIZE))
            start_button.fill(config.BUTTON_COLOR)
            text_surface, text_rect = INFO_FONT.render(
                "Start", config.FOREGROUND_COLOR)
            start_button.blit(text_surface, (
                int(start_button.get_rect().width / 2 - text_rect.width / 2),
                int(start_button.get_rect().height / 2 - text_rect.height / 2)
            ))

            all_ships_placed = True
            for s in draggable_ships:
                if s.grid_pos is None:
                    all_ships_placed = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_place_ships_screen = False
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Pressed space
                        # TODO: rotate ship orientation
                        for s in draggable_ships:
                            if s.rel_mouse_pos is not None:
                                # This ship is being dragged
                                print("Toggling orientation...")
                                s.toggle_orientation()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Mouse button down
                    print(f"INFO: Mouse down: {pygame.mouse.get_pos()}")

                    # Check ships
                    for s in draggable_ships:
                        if s.get_screen_pos_rect().collidepoint(pygame.mouse.get_pos()):
                            print("INFO: Clicked on ship")
                            mousePos: Pos = pygame.mouse.get_pos()
                            s.rel_mouse_pos = utils.sub_pos(
                                mousePos, utils.rect_to_pos(s.get_screen_pos_rect()))

                elif event.type == pygame.MOUSEBUTTONUP:
                    # MOUSE BUTTON UP

                    # Check button
                    if all_ships_placed:
                        if start_button.get_rect().move(
                            config.WIDTH - start_button.get_rect().width,
                            config.HEIGHT - start_button.get_rect().height
                        ).collidepoint(pygame.mouse.get_pos()):
                            print("INFO: Clicked on start button")
                            current_state = GameState.GAME_SCREEN
                            run_place_ships_screen = False

                    # Ship placement
                    for s in draggable_ships:
                        # If ship is being dragged
                        if s.rel_mouse_pos is not None:
                            # If released inside board
                            if grid_surface.get_rect().move(*config.GRID_DISP_LOCATION).collidepoint(pygame.mouse.get_pos()):

                                print("Released on grid!")

                                # Snap to grid
                                grid_pos = utils.sub_pos(
                                    pygame.mouse.get_pos(), s.rel_mouse_pos)
                                trans_grid_pos = utils.sub_pos(
                                    grid_pos, config.GRID_DISP_LOCATION)
                                amended_for_circle_center = utils.add_pos(
                                    trans_grid_pos,
                                    ((config.GRID_SIZE - config.SHIP_DISP_PADDING) // 2,
                                     (config.GRID_SIZE - config.SHIP_DISP_PADDING) // 2))
                                grid_coord = Coord(
                                    amended_for_circle_center[0] // config.GRID_SIZE,
                                    amended_for_circle_center[1] // config.GRID_SIZE)
                                snapped_pos: Pos = utils.add_pos(
                                    (grid_coord.x * config.GRID_SIZE,
                                     grid_coord.y * config.GRID_SIZE),
                                    config.GRID_DISP_LOCATION)
                                s.grid_pos = snapped_pos
                                # Store coords in ship
                                s.ship.segments = generate_segments(
                                    grid_coord, s.ship.size, s.orientation)

                                # EDGE CASE CHECKING

                                # Is ship sticking outside grid
                                for segment in s.ship.segments:
                                    if segment.x not in range(0, config.GRID_X):
                                        # Sticking out on left / right
                                        print(
                                            "INFO: Ship sticking out on X axis")
                                        s.reset()
                                    if segment.y not in range(0, config.GRID_Y):
                                        # Sticking out on top / bottom
                                        print(
                                            "INFO: Ship sticking out on Y axis")
                                        s.reset()

                                # Check overlap
                                for s2 in draggable_ships:
                                    if s2 is not s and s2.grid_pos is not None and s2.ship.is_overlapping(s.ship):
                                        # Oops: overlapping, not allowed
                                        print("INFO: Overlapping ship")
                                        s.reset()

                            else:
                                s.reset()

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

            WIN.blit(grid_surface, config.GRID_DISP_LOCATION)

            # Draggable ships
            for s in sorted(draggable_ships, key=lambda s: 0 if s.grid_pos is not None else 1):
                if s.rel_mouse_pos is not None:
                    mousePos = pygame.mouse.get_pos()
                    WIN.blit(
                        s.surface, utils.sub_pos(mousePos, s.rel_mouse_pos))
                elif s.grid_pos is not None:
                    WIN.blit(s.surface, s.grid_pos)
                else:
                    WIN.blit(s.surface, s.default_pos)

            # Start game button
            if all_ships_placed:
                WIN.blit(start_button, (
                    config.WIDTH - start_button.get_rect().width,
                    config.HEIGHT - start_button.get_rect().height
                ))

            pygame.display.update()

        print("Finished place_ships_screen()")

    def game_screen():
        run_game_screen = True
        while run_game_screen:
            clock.tick(FPS)
            print("running game screen...")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Background
            WIN.fill(config.BACKGROUND_COLOR)

            draw_title_text(WIN, "Game Screen")

    def redraw_window():
        # Background
        WIN.fill(config.BACKGROUND_COLOR)

        if current_state == GameState.PLACE_SHIPS:
            place_ships_screen()
        elif current_state == GameState.GAME_SCREEN:
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
