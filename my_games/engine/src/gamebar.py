#AngelStreet @2021
####################################################
import pygame
from src.utility import load_json,draw_image
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
        self.draw()


class ColorGameBar(GameBar):
    def __init__(self, value, total, x, y, w, h, color=None, border=None):
        GameBar.__init__(self,value, total, x, y)
        self.w = w
        self.h=h
        self.color = color or DEFAULT_COLOR
        self.border = border or DEFAULT_BORDER
        self.init_bar()
        self.draw()


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

    def draw(self) :
        pygame.draw.rect(self.image, self.border_color, (0,0,self.bg_rect_w, self.bg_rect_w), self.border_radius)
        self.bar_percentage = self.value/self.total
        self.fill_rect_w = self.w*self.bar_percentage
        self.fill_rect_h = self.h
        pygame.draw.rect(self.image, self.color, (self.border_size,self.border_size,self.fill_rect_w, self.fill_rect_h), self.border_radius)


class ImageGameBar(GameBar):
    def __init__(self, value, total, x, y, bg_image, fill_image,fill_offset,scale, alpha=True, colorkey=None):
        GameBar.__init__(self,value, total, x, y)
        self.bg_image = bg_image
        self.fill_image = fill_image
        self.fill_offset = fill_offset
        self.scale = scale
        self.alpha = alpha
        self.colorkey = colorkey
        self.init_bar()
        self.draw()

    def init_bar(self):
        if self.alpha :
            self.bg_sprite = pygame.image.load(self.bg_image).convert_alpha()
            self.fill_sprite = pygame.image.load(self.fill_image).convert_alpha()
        else :
            self.bg_sprite = pygame.image.load(self.bg_image).convert()
            self.fill_sprite = pygame.image.load(self.fill_image).convert()

        if self.colorkey :
            self.bg_sprite.set_colorkey(self.colorkey)
            self.fill_sprite.set_colorkey(self.colorkey)

        rect = self.fill_sprite.get_rect()
        dimension = round(rect.width*self.scale),round(rect.height*self.scale)
        self.fill_sprite = pygame.transform.scale(self.fill_sprite,dimension)
        self.fill_sprite_rect = self.fill_sprite.get_rect()

        rect = self.bg_sprite.get_rect()
        dimension = round(rect.width*self.scale),round(rect.height*self.scale)
        self.bg_sprite = pygame.transform.scale(self.bg_sprite,dimension)

        if self.alpha :
            self.image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        else :
            self.image = pygame.Surface(rect.size)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self) :
        bar_percentage = self.value/self.total
        self.bar_w= round(bar_percentage*self.fill_sprite_rect.width)
        offset = int(self.fill_offset*self.scale)
        self.image.fill((0,0,0,0))
        self.image.blit(self.fill_sprite,(offset,0), (0,0,self.bar_w,self.fill_sprite_rect.height))
        self.image.blit(self.bg_sprite,(0,0))


class HeartGameBar(ImageGameBar):
    def __init__(self, value, total, x, y, json,scale=1,offset=0):
        GameBar.__init__(self,value, total, x, y)
        self.json = json
        self.scale = scale
        self.offset = offset
        self.init_bar()
        self.draw()

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
        self.spritesheet = pygame.image.load(self.sprite_name).convert_alpha()
        rect = self.spritesheet.get_rect()
        dimension = round(rect.width*self.scale), round(rect.height*self.scale)
        self.spritesheet = pygame.transform.scale(self.spritesheet, dimension)
        rect = self.spritesheet.get_rect()
        self.image = pygame.Surface((rect.width*self.max_heart, rect.height), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.w *= self.scale
        self.h*=self.scale

    def draw_heart(self,i,sprite_id) :
        dest = i*self.w+i*self.offset,0
        area = (sprite_id-1)*self.w,0,self.w,self.h
        self.image.blit(self.spritesheet,(dest),area)

    def draw(self) :
        nb_hearts = int(self.total/2)
        for i in range(0,nb_hearts) :
            if i*2+2<=round(self.value) :
                self.draw_heart(i,self.full_id)
            elif i*2+1<=round(self.value) :
                self.draw_heart(i,self.half_id)
            else :
                self.draw_heart(i,self.empty_id)
