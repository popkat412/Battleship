import pygame
from typedefs import Color, Pos
import random
import config


def random_color() -> Color:
    return (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))


def sub_pos(r1: Pos, r2: Pos) -> Pos:
    return (r1[0] - r2[0], r1[1] - r2[1])


def add_pos(r1: Pos, r2: Pos) -> Pos:
    return (r1[0] + r2[0], r1[1] + r2[1])


def rect_to_pos(r: pygame.Rect) -> Pos:
    return (r.x, r.y)


def dist_board_window(axis: str) -> float:
    if axis == "X":
        return (config.HEIGHT - config.GRID_Y * config.GRID_SIZE) / 2
    else:
        return (config.WIDTH - config.GRID_X * config.GRID_SIZE) / 2


def draw_title_text(s: pygame.Surface, subhead: str) -> None:
    """Draw title at the top of the screen in the center"""

    text_surface, text_rect = config.TITLE_FONT.render(
        f"BATTLESHIP: {subhead}", config.FOREGROUND_COLOR)
    s.blit(text_surface, (int(config.WIDTH / 2 -
                              text_rect.width / 2),
                          int(dist_board_window("X") / 2)))


def draw_info_text(s: pygame.Surface, text: str, pos: Pos) -> None:
    """Draw text at the position, pos[0] is the X of the center"""

    text_surface, text_rect = config.INFO_FONT.render(
        text, config.FOREGROUND_COLOR)
    s.blit(text_surface, (int(pos[0] - text_rect.width / 2), pos[1]))


def lerp_color(a: Color, b: Color, t: float) -> Color:
    return (int(a[0] + (b[0] - a[0]) * t),
            int(a[1] + (b[1] - a[1]) * t),
            int(a[2] + (b[2] - a[2]) * t))
