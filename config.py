import pygame.freetype
from typedefs import Pos, Color

pygame.init()

# Sizes
WIDTH, HEIGHT = 1500, 750
GRID_X = 10
GRID_Y = 10
GRID_SIZE = 50

# Display
SHIP_DISP_PADDING = 5
# This is the location of the board's top-left corner
GRID_DISP_LOCATION: Pos = (int((WIDTH - GRID_SIZE * GRID_X) / 2),
                           int((HEIGHT - GRID_SIZE * GRID_Y) / 2))
PLAYER_GRID_LOCATION: Pos = (int((WIDTH - 2 * GRID_SIZE * GRID_X) / 3),
                             int((HEIGHT - GRID_SIZE * GRID_Y) / 2))
OPPONENT_GRID_LOCATION: Pos = (int((WIDTH - 2 * GRID_SIZE * GRID_X) / 3*2 + GRID_SIZE * GRID_X),
                               int((HEIGHT - GRID_SIZE * GRID_Y) / 2))

# Colors
BACKGROUND_COLOR: Color = (0, 0, 0)
FOREGROUND_COLOR: Color = (255, 255, 255)
BUTTON_COLOR: Color = (30, 30, 30)

# Text
FONT_NAME = "assets/Verdana.ttf"
FONT_SIZE = 20
TITLE_FONT_SIZE = 28
INFO_FONT = pygame.freetype.Font(FONT_NAME, FONT_SIZE)
TITLE_FONT = pygame.freetype.Font(FONT_NAME, TITLE_FONT_SIZE)

# Gameplay
SHIP_SIZES = (2, 3, 3, 5)
