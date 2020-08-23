import pygame
from typedefs import Color, Pos
import random


def random_color() -> Color:
    return (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))


def sub_pos(r1: Pos, r2: Pos) -> Pos:
    return (r1[0] - r2[0], r1[1] - r2[1])


def rect_to_pos(r: pygame.Rect) -> Pos:
    return (r.x, r.y)
