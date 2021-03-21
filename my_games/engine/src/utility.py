import pygame, json

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def draw_text(display, text, font_name, size, color, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(str(text), True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    display.blit(text_surface, text_rect)


def resize_screen(w, h, resizable=False):
    # print(w,h,resizable)
    if resizable:
        screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
    else:
        screen = pygame.display.set_mode((w, h))
    display = pygame.Surface((w, h))
    return screen, display


def load_json(json_file):
    with open(json_file) as f:
        data = json.load(f)
    f.close()
    return data

def get_sprite(sprite_sheet, x, y, w, h,colorkey):
    sprite = pygame.Surface((w, h))
    sprite.set_colorkey(colorkey)
    sprite.blit(sprite_sheet, (0, 0), (x, y, w, h))
    return sprite

def cartesian_to_iso(x, y, w, h):
    iso_x = round((x - y) * w/2)
    iso_y = round((x + y) * h/2)
    return iso_x, iso_y

def move_sprite(self, x, y) :
    self.rect.x += x
    self.rect.y += y