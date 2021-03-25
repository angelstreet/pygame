import pygame
from src.utility import *
from types import MethodType
from src.gamesprite import GameSprite


class Text(pygame.sprite.Sprite):
    def __init__(self, text, font_name, size, color, bg_color, x, y, layer, sprite=None, behind=False):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.layer = layer
        self.text = text
        self.font_name = font_name
        self.size = size
        self.color = color
        self.bg_color = bg_color
        self.sprite = sprite
        self.behind = behind
        self.image = pygame.Surface((100, 50), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()
        self.init_text()
        self.draw()

    def init_text(self):
        if self.sprite:
            self.x += self.sprite.x
            self.y += self.sprite.y
        if self.behind:
            # TODO: Find sprite position in layer then ad font before sprite [sort]
            pass
        else:
            self.layer.add(self)

    def draw_text(self, text, font_name, size, color):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(str(text), True, color)
        return text_surface

    def draw(self):
        font = self.draw_text(self.text, self.font_name, self.size, self.color)
        font_rect = font.get_rect()
        self.image = pygame.transform.scale(self.image, font_rect.size)
        if self.bg_color:
            self.image.fill(self.bg_color)
        else:
            self.image.fill((0, 0, 0, 0))
        self.image.blit(font, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class DynamicText(Text):
    def __init__(self, text, font_name, size, color, bg_color, x, y, layer, sprite=None, behind=False):
        Text.__init__(self, text, font_name, size, color, bg_color, x, y, layer, sprite, behind)

    def update(self):
        self.draw()
