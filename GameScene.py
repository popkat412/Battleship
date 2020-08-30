import pygame
from director import Director
from scene import Scene
import utilities as utils


class GameScene(Scene):
    def __init__(self, director: Director):
        super().__init__(director)

        self.director = director

    def on_update(self):
        pass

    def on_event(self, event):
        pass

    def on_draw(self, window):
        utils.draw_title_text(window, "Game Scene")
