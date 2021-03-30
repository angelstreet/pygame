import pygame
import json
from pygame.locals import Color
FPS = 60
BLACK, WHITE, RED = Color('black'), Color('white'), Color('red')
GREEN, YELLOW, BLUE = Color('green'), Color('yellow'), Color('blue')


def draw_image(display, image, scale=1):
    rect = display.get_rect()
    dimension = rect.width*scale, rect.height*scale
    if rect.size != dimension:
        display = pygame.transform.scale(image, dimension)
    else:
        display.blit(image, (0, 0))


def load_json(json_file):
    with open(json_file) as f:
        data = json.load(f)
    f.close()
    return data


def cartesian_to_iso(i, j, w, h):
    iso_x = int((i - j) * w/2)
    iso_y = int((i + j) * h/2)
    return iso_x, iso_y

def cartesian_to_iso2(x,y):
    iso_x = int((x - y))
    iso_y = int((x + y)/2)
    return iso_x, iso_y


def iso_to_cartesian(isox, isoy):
    x = int((2*isoy + isox)/2)
    y = int((2*isoy-isox)/2)
    return x, y


def move_sprite(sprite, x, y):
    sprite.rect.x = x
    sprite.rect.y = y
