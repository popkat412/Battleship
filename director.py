import sys
from typing import Optional
from scene import Scene
import pygame
import config


class Director:
    """Represents the main object of the game.

    The Director object keeps the game on, and takes care of updating it,
    drawing it and propagate events.

    This object must be used with Scene objects that are defined later."""

    def __init__(self) -> None:
        self.window: pygame.Surface = pygame.display.set_mode(
            (config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("Battleship")
        self.scene: Optional[Scene] = None
        self.quit_flag: bool = False
        self.clock = pygame.time.Clock()

    def loop(self) -> None:
        """Main game loop."""

        while not self.quit_flag:
            self.clock.tick(60)

            # Exit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                # Detect events
                if self.scene is not None:
                    self.scene.on_event(event)

            if self.scene is not None:
                # Update scene
                self.scene.on_update()

                # Draw the screen
                self.window.fill(config.BACKGROUND_COLOR)
                self.scene.on_draw(self.window)
                pygame.display.update()

    def change_scene(self, scene) -> None:
        """Changes the current scene."""
        self.scene = scene

    def quit(self) -> None:
        self.quit_flag = True
        pygame.quit()
        sys.exit()
