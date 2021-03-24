#AngelStreet @2021
####################################################
from src.utility import load_json, move_sprite, iso_to_cartesian
import pygame


class GameSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.z = 0
        self.rigid = False

    def update(self):
        self.blits()

    def zsort(self):
        return 1

    def is_moving(self):
        return False

    def create_surface(self, w, h):
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32).convert_alpha()
        self.source_image = pygame.Surface((w, h), pygame.SRCALPHA, 32).convert_alpha()
        self.rear_image = pygame.Surface((w, h), pygame.SRCALPHA, 32).convert_alpha()
        self.front_image = pygame.Surface((w, h), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()

    def create_mask(self):
        self.mask = pygame.mask.from_surface(self.source_image)

    def blits(self):
        self.clear()
        self.image.blit(self.rear_image, (0, 0))
        self.image.blit(self.source_image, (0, 0))
        self.image.blit(self.front_image, (0, 0))
        self.create_mask()

    def blit(self, source, dest=(0, 0), replace=True):
        if replace:
            self.clear_source()
        self.source_image.blit(source, dest)

    def blit_rear(self, source, dest=(0, 0), replace=True):
        if replace:
            self.clear_rear()
        self.rear_image.blit(source, dest)

    def blit_front(self, source, dest=(0, 0), replace=True):
        if replace:
            self.clear_front()
        self.front_image.blit(source, dest)

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def fill(self, surface, color, rect=None, special_flags=0):
        surface.fill(color, rect=None, special_flags=0)

    def clear(self):
        self.image.fill((0, 0, 0, 0), None, pygame.BLEND_RGBA_MULT)

    def clear_source(self):
        self.source_image.fill((0, 0, 0, 0), None, pygame.BLEND_RGBA_MULT)

    def clear_rear(self):
        self.rear_image.fill((0, 0, 0, 0), None, pygame.BLEND_RGBA_MULT)

    def clear_front(self):
        self.front_image.fill((0, 0, 0, 0), None, pygame.BLEND_RGBA_MULT)

    def blend(self, alpha_color):
        self.blit_front(self.source_image)
        self.front_image.fill(alpha_color, None, pygame.BLEND_RGBA_MULT)

    def remove_blend(self):
        self.clear_front()

    def load_image(self, path, alpha=False, colorkey=None, scale=1):
        if alpha:
            load_img = pygame.image.load(path).convert_alpha()
        else:
            load_img = pygame.image.load(path).convert()
        if colorkey:
            load_img.set_colorkey(colorkey)
            self.colorkey = colorkey
        self.rect = load_img.get_rect()
        self.create_surface(self.rect.width, self.rect.height)
        self.blit(load_img)
