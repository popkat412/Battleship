from grid import Grid
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

        self.player_grid = Grid(config.PLAYER_GRID_LOCATION)
        self.opponent_grid = Grid(config.OPPONENT_GRID_LOCATION)

        self.player_grid.add_ships(ships)

    def on_update(self):
        pass

    def on_event(self, event):
        pass

    def on_draw(self, window):
        # Title
        utils.draw_title_text(window, "Game Scene")

        # Grid
        self.player_grid.draw(window)
        self.opponent_grid.draw(window)

        # Player status text
        utils.draw_info_text(
            window,
            f"Current player: {self.current_player.name}",
            # (10, 10))
            (int(config.WIDTH / 2),
             int((utils.dist_board_window("X") * 1.5) + (config.GRID_SIZE * config.GRID_Y))))
