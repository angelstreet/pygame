import pygame as pg
from engine.src.utility import move_sprite


class Button(pg.sprite.Sprite):
    def __init__(self,  w, h, text, font_name, font_size, font_color, bg_color):
        pg.sprite.Sprite.__init__(self)
        self.w, self.h = w, h
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.font_color = font_color
        self.bg_color = bg_color
        self._init_button()

    def _init_button(self):
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA, 32).convert_alpha()
        self.button = pg.Rect(0, 0, self.w, self.h)
        pg.draw.rect(self.image, self.bg_color, self.button)
        self.rect = self.image.get_rect()
        font = pg.font.Font(self.font_name, self.font_size)
        text_surface = font.render(str(self.text), True, self.font_color)
        centerx = (self.w-text_surface.get_rect().width)/2
        centery = (self.h-text_surface.get_rect().height)/2
        self.image.blit(text_surface, (centerx, centery))
        self.rect = self.image.get_rect()

    def rollover(self):
        self.x, self.y = self.rect.x, self.rect.y
        w = int(self.rect.width*1.3)
        h = int(self.rect.height*1.3)
        offsetx = (w-self.rect.width) /2
        offsety = (h-self.rect.height) /2
        self.image = pg.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        move_sprite(self, self.x-offsetx, self.y-offsety)

    def rollout(self):
        self.image = pg.transform.scale(self.image, (self.w, self.h))
        self.rect = self.image.get_rect()
        move_sprite(self, self.x, self.y)
