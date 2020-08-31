from typing import List
from ship import Ship
from player import Player
import pygame
import config
from director import Director
from scene import Scene
import utilities as utils


class GameScene(Scene):
    """Game scene, scene where player actually plays the game"""

    def __init__(self, director: Director, ships: List[Ship]):
        super().__init__(director)

        self.director = director
        self.human_player = Player("Human", ships)
        self.computer_player = Player("Computer")
        self.current_player = self.human_player

    def on_update(self):
        pass

    def on_event(self, event):
        pass

    def on_draw(self, window):
        # Title
        utils.draw_title_text(window, "Game Scene")

        # Grid
        player_grid_surface = pygame.Surface(
            (config.GRID_X * config.GRID_SIZE, config.GRID_X * config.GRID_SIZE))
        opponent_grid_surface = pygame.Surface(
            (config.GRID_X * config.GRID_SIZE, config.GRID_X * config.GRID_SIZE))

        for i in range(config.GRID_X):
            for j in range(config.GRID_Y):
                pygame.draw.rect(player_grid_surface, config.FOREGROUND_COLOR,
                                 pygame.Rect(i * config.GRID_SIZE, j * config.GRID_SIZE, config.GRID_SIZE, config.GRID_SIZE), 3)
                pygame.draw.rect(opponent_grid_surface, config.FOREGROUND_COLOR,
                                 pygame.Rect(i * config.GRID_SIZE, j * config.GRID_SIZE, config.GRID_SIZE, config.GRID_SIZE), 3)

        for ship in self.human_player.ships:
            for seg in ship.segments:
                pygame.draw.circle(player_grid_surface, utils.lerp_color(ship.color, config.BACKGROUND_COLOR, 0.5), (
                    seg.x * config.GRID_SIZE + config.GRID_SIZE / 2, seg.y * config.GRID_SIZE + config.GRID_SIZE / 2), (config.GRID_SIZE - config.SHIP_DISP_PADDING) / 2)

        window.blit(player_grid_surface, config.PLAYER_GRID_LOCATION)
        window.blit(opponent_grid_surface, config.OPPONENT_GRID_LOCATION)

        # Player status text
        utils.draw_info_text(
            window,
            f"Current player: {self.current_player.name}",
            # (10, 10))
            (int(config.WIDTH / 2),
             int((utils.dist_board_window("X") * 1.5) + (config.GRID_SIZE * config.GRID_Y))))
