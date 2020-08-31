from director import Director
from GameScene import GameScene
from ship import generate_segments
from typedefs import Pos
from coord import Coord
import pygame
from draggable_ship import DraggableShip
from typing import List
from scene import Scene
import config
import utilities as utils


class PlaceShipsScene(Scene):
    """Place ships scene, scene where user drags ships onto the grid"""

    def __init__(self, director: Director):
        super().__init__(director)

        self.director = director

        # Draggable ships
        self.draggable_ships: List[DraggableShip] = []

        for i, size in enumerate(config.SHIP_SIZES):
            pos = (int(config.WIDTH / 8),
                   int((config.HEIGHT - utils.dist_board_window("Y")) + i * config.GRID_SIZE))
            self.draggable_ships.append(DraggableShip(size, pos))

        # All ships placed
        self.all_ships_placed: bool = False

        # Start button
        self.start_button = pygame.Surface(
            (config.GRID_SIZE * 3, config.GRID_SIZE))
        self.start_button.fill(config.BUTTON_COLOR)
        text_surface, text_rect = config.INFO_FONT.render(
            "Start", config.FOREGROUND_COLOR)
        self.start_button.blit(text_surface, (
            int(self.start_button.get_rect().width / 2 - text_rect.width / 2),
            int(self.start_button.get_rect().height / 2 - text_rect.height / 2)
        ))

        # Grid surface
        self.grid_surface: pygame.Surface = pygame.Surface(
            (config.GRID_X * config.GRID_SIZE, config.GRID_Y * config.GRID_SIZE))

    def on_update(self):
        pass

    def on_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            # sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Pressed space
                for s in self.draggable_ships:
                    if s.rel_mouse_pos is not None:
                        # This ship is being dragged
                        print("Toggling orientation...")
                        s.toggle_orientation()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Mouse button down
            print(f"INFO: Mouse down: {pygame.mouse.get_pos()}")

            # Check ships
            for s in self.draggable_ships:
                if s.get_screen_pos_rect().collidepoint(pygame.mouse.get_pos()):
                    print("INFO: Clicked on ship")
                    mousePos: Pos = pygame.mouse.get_pos()
                    s.rel_mouse_pos = utils.sub_pos(
                        mousePos, utils.rect_to_pos(s.get_screen_pos_rect()))

        elif event.type == pygame.MOUSEBUTTONUP:
            # MOUSE BUTTON UP

            # Check button
            if self.all_ships_placed:
                if self.start_button.get_rect().move(
                    config.WIDTH - self.start_button.get_rect().width,
                    config.HEIGHT - self.start_button.get_rect().height
                ).collidepoint(pygame.mouse.get_pos()):
                    print("INFO: Clicked on start button")
                    self.director.change_scene(
                        GameScene(self.director, [s.ship for s in self.draggable_ships]))

            # Ship placement
            for s in self.draggable_ships:
                # If ship is being dragged
                if s.rel_mouse_pos is not None:
                    # If released inside board
                    if self.grid_surface.get_rect().move(*config.GRID_DISP_LOCATION).collidepoint(pygame.mouse.get_pos()):

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
                        for s2 in self.draggable_ships:
                            if s2 is not s and s2.grid_pos is not None and s2.ship.is_overlapping(s.ship):
                                # Oops: overlapping, not allowed
                                print("INFO: Overlapping ship")
                                s.reset()

                    else:
                        s.reset()

                s.rel_mouse_pos = None

    def on_draw(self, window: pygame.Surface):
        self.all_ships_placed = True
        for s in self.draggable_ships:
            if s.grid_pos is None:
                self.all_ships_placed = False

        # Title
        utils.draw_title_text(window, "Place your Ships")

        # Grid
        for i in range(config.GRID_X):
            for j in range(config.GRID_Y):
                pygame.draw.rect(self.grid_surface, config.FOREGROUND_COLOR,
                                 pygame.Rect(i * config.GRID_SIZE, j * config.GRID_SIZE, config.GRID_SIZE, config.GRID_SIZE), 3)

        window.blit(self.grid_surface, config.GRID_DISP_LOCATION)

        # Draggable ships
        for s in sorted(self.draggable_ships, key=lambda s: 0 if s.grid_pos is not None else 1):
            if s.rel_mouse_pos is not None:
                mousePos = pygame.mouse.get_pos()
                window.blit(
                    s.surface, utils.sub_pos(mousePos, s.rel_mouse_pos))
            elif s.grid_pos is not None:
                window.blit(s.surface, s.grid_pos)
            else:
                window.blit(s.surface, s.default_pos)

        # Start game button
        if self.all_ships_placed:
            window.blit(self.start_button, (
                config.WIDTH - self.start_button.get_rect().width,
                config.HEIGHT - self.start_button.get_rect().height
            ))
