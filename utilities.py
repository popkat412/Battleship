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
    text_surface, text_rect = config.TITLE_FONT.render(
        f"BATTLESHIP: {subhead}", config.FOREGROUND_COLOR)
    s.blit(text_surface, (int(config.WIDTH / 2 -
                              text_rect.width / 2),
                          int(dist_board_window("X") / 2)))
