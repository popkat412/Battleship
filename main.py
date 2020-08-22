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
    players = (Player("Human"), Player("Computer"))
    currentPlayer = players[0]

    def redraw_window():
        # Background
        WIN.fill((0, 0, 0))

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

        # Current Player Text
        text_surface, text_rect = INFO_FONT.render(
            f"Current Player: {currentPlayer.name}", (255, 255, 255))
        WIN.blit(text_surface, (config.WIDTH / 2 -
                                text_rect.width / 2, config.HEIGHT - (config.HEIGHT - config.GRID_Y * config.GRID_SIZE) / 4))
        text_surface, text_rect = TITLE_FONT.render(
            "BATTLESHIP", (255, 255, 255))
        WIN.blit(text_surface, (config.WIDTH / 2 -
                                text_rect.width / 2, (config.HEIGHT - config.GRID_Y * config.GRID_SIZE) / 4))

        pygame.display.update()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        redraw_window()


if __name__ == "__main__":
    main()
