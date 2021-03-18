import pygame

FPS = 60
BLACK = (0,0,0)
WHITE = (255,255,255)

def draw_text(display, text,font_name, size,color, x, y ):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x,y)
    display.blit(text_surface,text_rect)

def reset_keys(self):
    self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.K_ESCAPE = False, False, False, False, False
    return self
