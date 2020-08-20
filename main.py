import pygame
from ship import Ship

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battleship")


def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()

    # Game data
    ships = []
    miss_coord = []
    hit_coord = []

    def redraw_window():
        # Background
        pygame.draw.rect(WIN, (0, 0, 0), (0, 0, WIDTH, HEIGHT))

        # Grid

        pygame.display.update()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        redraw_window()


if __name__ == "__main__":
    main()
