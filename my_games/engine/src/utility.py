import pygame as pg
from pygame.locals import Color
import json
FPS = 60
BLACK, WHITE, RED = Color('black'), Color('white'), Color('red')
GREEN, YELLOW, BLUE = Color('green'), Color('yellow'), Color('blue')


def load_image(path, alpha=False, colorkey=None, scale=1):
    sprite = pg.sprite.Sprite()
    if alpha:
        load_img = pg.image.load(path).convert_alpha()
    else:
        load_img = pg.image.load(path).convert()
        if colorkey:
            load_img.set_colorkey(colorkey)
    rect = load_img.get_rect()
    dimension = rect.width*scale, rect.height*scale
    if rect.size != dimension:
        load_img = pg.transform.scale(load_img, dimension)
    sprite.image = load_img
    sprite.rect = load_img.get_rect()
    sprite.w = sprite.rect.width
    sprite.h = sprite.rect.height
    return sprite


def draw_image(display, image, scale=1):
    rect = display.get_rect()
    dimension = rect.width*scale, rect.height*scale
    if rect.size != dimension:
        display = pg.transform.scale(image, dimension)
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


def iso_to_cartesian(isox, isoy):
    x = int((2*isoy + isox)/2)
    y = int((2*isoy-isox)/2)
    return x, y


def move_sprite(sprite, x, y, displace=False):
    if displace:
        sprite.rect.x += x
        sprite.rect.y += y
    else:
        sprite.rect.x = x
        sprite.rect.y = y


def setIcon(iconfile):
    gameicon = pg.image.load(iconfile)
    pg.display.set_icon(gameicon)


def scale_img(img, scale):
    rect = img.get_rect()
    dimension = round(rect.width*scale), round(rect.height*scale)
    return pg.transform.scale(img, dimension)
