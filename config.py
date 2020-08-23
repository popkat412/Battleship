from typing import Tuple
from typedefs import Pos, Color


# Sizes
WIDTH, HEIGHT = 750, 750
GRID_X = 10
GRID_Y = 10
GRID_SIZE = 50

# Display
SHIP_DISP_PADDING = 5
GRID_DISP_LOCATION: Pos = (int((HEIGHT - GRID_SIZE * GRID_X) / 2),
                           int((WIDTH - GRID_SIZE * GRID_Y) / 2))  # This is the location of the board's top-left corner

# Colors
BACKGROUND_COLOR: Color = (0, 0, 0)
FOREGROUND_COLOR: Color = (255, 255, 255)

# Text
FONT_NAME = "assets/Verdana.ttf"
FONT_SIZE = 20
TITLE_FONT_SIZE = 28

# Gameplay
SHIP_SIZES = (2, 3, 3, 5)
