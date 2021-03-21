import pygame
from utility import FPS,WHITE,BLACK,draw_text,reset_keys,resize_screen,blit_screen
clock = pygame.time.Clock()

class Game():
    def __init__(self,screen,display,WIDTH,HEIGHT,isplaying=True):
        self.screen = screen
        self.display = display
        self.w, self.h = WIDTH,HEIGHT
        self.mid_w, self.mid_h = WIDTH / 2, HEIGHT / 2
        self.playing = False
        self.game_menu = None
        self.screen = screen
        self.current_game_menu = "game_menu_world"
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.K_ESCAPE = False, False, False, False,False
        self.font_name = pygame.font.get_default_font()
        self.font_size = 20

    def launch(self,game_menu,resume=False):
        reset_keys(self)
        self.screen,self.display = resize_screen(self.w, self.h)
        self.game_menu = game_menu
        self.playing = True
        if resume:
            print("Game Resume")
        else:
            print("Game Start")
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing= False
            if self.K_ESCAPE :
                self.playing= False
                self.screen,self.display = resize_screen(self.game_menu.current_menu.w, self.game_menu.current_menu.h)
                self.game_menu.game_options_menu.display_menu()
            self.display.fill(WHITE)
            draw_text(self.display,'Thanks for Playing', self.font_name,self.font_size, BLACK,self.mid_w, self.mid_h)
            blit_screen(self)
            pygame.display.update()
            clock.tick(FPS)

    def resume(self):
        self.launch(self.game_menu,True)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                pygame.quit()
            if event.type == pygame.VIDEORESIZE :
                self.w,self.h=event.w,event.h
                self.mid_w,self.mid_h= self.w / 2, self.h / 2
                self.screen,self.display = resize_screen(event.w, event.h,True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.K_ESCAPE = True
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
