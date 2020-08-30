from PlaceShipsScene import PlaceShipsScene
from director import Director
import pygame
import pygame.freetype

pygame.init()


def main():
    dir = Director()
    scene = PlaceShipsScene(dir)
    dir.change_scene(scene)
    dir.loop()


if __name__ == "__main__":
    main()
