import pygame, json

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def draw_image(display, image,scale=1):
        rect = display.get_rect()
        dimension = rect.width*scale,rect.height*scale
        if rect.size != dimension :
            display = pygame.transform.scale(image, dimension)
        else :
            display.blit(image, (0,0))


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

def cartesian_to_iso(x, y, w, h):
    iso_x = int((x - y) * w/2)
    iso_y = int((x + y) * h/2)
    return iso_x, iso_y

def iso_to_cartesian(isox, isoy):
    x = int((2*isoy + isox)/2)
    y = int((2*isoy-isox)/2)
    return x, y


def move_sprite(rect, x, y) :
    rect.x += x
    rect.y += y
