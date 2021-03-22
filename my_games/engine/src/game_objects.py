import pygame
from src.utility import FPS, WHITE, BLACK, resize_screen,draw_image
from types import MethodType

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

    def draw_text(self,text, font_name, size, color):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(str(text), True, color)
        return text_surface

    def draw(self):
        font =self.draw_text(self.text, self.font_name, self.size, self.color)
        font_rect = font.get_rect()
        self.image = pygame.transform.scale(self.image, font_rect.size)
        if self.bg_color:
            self.image.fill(self.bg_color)
        else :
            self.image.fill((0,0,0,0))
        self.image.blit(font, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x= self.x
        self.rect.y= self.y


class DynamicText(Text):
    def __init__(self, text, font_name, size, color, bg_color, x, y, layer, sprite=None, behind=False):
        Text.__init__(self,text, font_name, size, color, bg_color, x, y, layer, sprite, behind)
    #Dynamic text is a text than need to be refreshed, redrawn on the sreen
    def update(self):
        self.draw()


class Image(pygame.sprite.Sprite):
    def __init__(self, img_path,alpha,colorkey, x, y, scale, layer, sprite=None, behind=False):
        pygame.sprite.Sprite.__init__(self)
        self.img_path = img_path
        self.x = x
        self.y = y
        self.scale = scale
        self.layer = layer
        self.alpha = alpha
        self.colorkey = colorkey
        self.sprite = sprite
        self.behind = behind
        self.init_img()
        self.draw()

    def init_img(self):
        self.image=None
        if self.sprite:
            print("WARNING : relative position meaning your image could be hided behind the sprite !!!")
            self.x += self.sprite.x
            self.y += self.sprite.y
        if self.behind:
            # TODO: Find sprite position in layer then ad font before sprite [sort]
            pass
        else:
            self.layer.add(self)
        self.sprite = pygame.image.load(self.img_path).convert()
        self.rect = self.sprite.get_rect()
        self.image = pygame.Surface(self.rect.size)

    def draw(self):
        draw_image(self.image, self.sprite,self.scale)
        self.rect = self.image.get_rect()
        if self.colorkey :
            self.image.set_colorkey(self.colorkey)
        self.rect.x= self.x
        self.rect.y= self.y
