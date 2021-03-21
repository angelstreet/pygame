#AngelStreet @2021
####################################################
import pygame
from utility import load_json
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
        self.draw_bar()


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
    def __init__(self, value, total, x, y, bg_image, fill_image,fill_offset, colorkey=(0,0,0), alpha=True):
        GameBar.__init__(self,value, total, x, y)
        self.bg_image = bg_image
        self.fill_image = fill_image
        self.fill_offset = fill_offset
        self.colorkey = colorkey
        self.alpha = alpha
        self.init_bar()
        self.draw_bar()

    def init_bar(self):
        if self.alpha :
            self.bg_sprite = pygame.image.load(self.bg_image).convert_alpha()
            self.fill_sprite = pygame.image.load(self.fill_image).convert_alpha()
        else :
            self.bg_sprite = pygame.image.load(self.bg_image).convert()
            self.fill_sprite = pygame.image.load(self.fill_image).convert()
            self.bg_sprite.set_colorkey(self.colorkey)
            self.fill_sprite.set_colorkey(self.colorkey)

        self.bg_sprite_w = self.bg_sprite.get_rect().width
        self.bg_sprite_h = self.bg_sprite.get_rect().height
        self.fill_sprite_w = self.fill_sprite.get_rect().width
        self.fill_sprite_h = self.fill_sprite.get_rect().height
        self.image = pygame.Surface((self.bg_sprite_w, self.bg_sprite_h))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        if not self.alpha :
            self.image.set_colorkey(self.colorkey)


    def draw_bar(self) :
        bar_percentage = self.value/self.total
        fill_bar_w = bar_percentage*self.fill_sprite_w
        self.image.fill((255,255,255))
        self.image.blit(self.fill_sprite,(self.fill_offset,0), (0,0,fill_bar_w,self.fill_sprite_h))
        self.image.blit(self.bg_sprite,(0,0))


class HeartGameBar(ImageGameBar):
    def __init__(self, value, total, x, y, json,scale=1,offset=0):
        GameBar.__init__(self,value, total, x, y)
        self.json = json
        self.scale = scale
        self.offset = offset
        self.init_bar()
        self.draw_bar()

    def parse_data(self):
        self.sprite_name = self.data['heart']['sprite_name']
        self.colorkey = tuple(self.data['heart']['colorkey'])
        self.w = self.data['heart']['w']
        self.h = self.data['heart']['h']
        self.max_heart = self.data['heart']['max_heart']
        self.full_id = self.data['heart']['full_id']
        self.empty_id = self.data['heart']['empty_id']
        self.half_id = self.data['heart']['half_id']

    def init_bar(self):
        self.data = load_json(self.json)
        self.parse_data()
        if self.colorkey == (0,0,0) :
            self.spritesheet = pygame.image.load(self.sprite_name).convert_alpha()
        else :
            self.spritesheet = pygame.image.load(self.sprite_name).convert()
            self.spritesheet.set_colorkey(self.colorkey)
        self.image = pygame.Surface((self.w*self.max_heart, self.h))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        dimension = round(self.spritesheet.get_rect().width*self.scale), round(self.spritesheet.get_rect().height*self.scale)
        self.spritesheet = pygame.transform.scale(self.spritesheet, dimension)

        if not self.colorkey == (0,0,0) :
            self.image.set_colorkey(self.colorkey)

    def draw_heart(self,i,sprite_id) :
        dest = (round(i*self.w*self.scale)+i*self.offset,0)
        area = (round((sprite_id-1)*self.w)*self.scale,0,round(sprite_id*self.w*self.scale),round(self.h*self.scale))
        self.image.blit(self.spritesheet,dest,area)

    def draw_bar(self) :
        self.image.fill((255,255,255))
        nb_hearts = int(self.total/2)
        for i in range(0,nb_hearts) :
            if i*2+2<=self.value :
                self.draw_heart(i,self.full_id)
            elif i*2+1<=self.value :
                self.draw_heart(i,self.half_id)
            else :
                self.draw_heart(i,self.empty_id)
        self.value-=0.1
