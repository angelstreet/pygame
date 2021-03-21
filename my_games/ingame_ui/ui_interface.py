#AngelStreet @2021
####################################################
import pygame
#from utility import load_json,move_sprite
DEFAULT_COLOR = (255, 0, 0)
DEFAULT_BORDER = {'color': (0, 0, 0), 'size': 1, 'radius': 0}

class GameBar(pygame.sprite.Sprite):
    def __init__(self, value, total, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.value = value
        self.total = total
        self.x = x
        self.y = y

    def update(self):
        self.draw_bar


class ColorGameBar(GameBar):
    def __init__(self, value, total, x, y, w, h, color=None, border=None):
        GameBar.__init__(self,value, total, x, y)
        self.w = w
        self.h=h
        self.color = color or DEFAULT_COLOR
        self.border = border or DEFAULT_BORDER
        self.init_bar()
        self.draw_bar()


    def init_bar(self):
        self.border_color =self.border['color']
        self.border_size =self.border['size']
        self.border_radius =self.border['radius']
        self.bg_rect_w = self.w+2*self.border_size
        self.bg_rect_h = self.h+2*self.border_size
        self.image = pygame.Surface((self.bg_rect_w, self.bg_rect_h))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def draw_bar(self) :
        pygame.draw.rect(self.image, self.border_color, (0,0,self.bg_rect_w, self.bg_rect_w), self.border_radius)
        self.bar_percentage = self.value/self.total
        self.fill_rect_w = self.w*self.bar_percentage
        self.fill_rect_h = self.h
        pygame.draw.rect(self.image, self.color, (self.border_size,self.border_size,self.fill_rect_w, self.fill_rect_h), self.border_radius)


class ImageGameBar(GameBar):
    def __init__(self, value, total, x, y, bg_image, bar_image, colorkey=(0,0,0), alpha=True):
        GameBar.__init__(self,value, total, x, y)
        self.bg_image = bg_image
        self.bar_image = bar_image
        self.colorkey = colorkey
        self.init_bar()
        self.draw_bar()

    def init_bar(self):
        if alpha :
            self.bg_sprite = pygame.image.load(self.bg_image).convert_alpha()
            self.bar_sprite = pygame.image.load(self.bar_image).convert_alpha()
        else :
            self.bg_sprite = pygame.image.load(self.bg_image).convert()
            self.bar_sprite = pygame.image.load(self.bar_image).convert()
        self.w = self.bg_sprite.rect.height
        self.h = self.bg_sprite.rect.width
        self.image = pygame.Surface((self.w, self.h))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def draw_bar(self) :
        self.image.blit(self.bg_sprite.image,(self.w,self.h))
        self.bar_percentage = self.value/self.total
        self.image.blit(self.bar_sprite.image,(self.bar_percentage,self.h))
