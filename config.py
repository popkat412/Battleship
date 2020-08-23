from typing import Tuple

# Type aliases
Pos = Tuple[int, int]
Color = Tuple[int, int, int]

# Sizes
WIDTH, HEIGHT = 750, 750
GRID_X = 10
GRID_Y = 10
GRID_SIZE = 50

# Display
SHIP_DISP_PADDING = 5
GRID_DISP_LOCATION = (int((HEIGHT - GRID_SIZE * GRID_X) / 2),
                      int((WIDTH - GRID_SIZE * GRID_Y) / 2))  # This is the location of the board's top-left corner
BACKGROUND_COLOR: Color = (0, 0, 0)

# Text
FONT_NAME = "assets/Verdana.ttf"
FONT_SIZE = 20
TITLE_FONT_SIZE = 28

# Gameplay
SHIP_SIZES = (2, 3, 3, 5)
