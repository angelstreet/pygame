import pygame
from utility import FPS,WHITE,BLACK,draw_text,reset_keys

class Game():
    def __init__(self,screen,display,WIDTH,HEIGHT):
        self.screen = screen
        self.display = display
        self.w, self.h = WIDTH,HEIGHT
        self.mid_w, self.mid_h = WIDTH / 2, HEIGHT / 2
        self.running, self.playing = True, False
        self.game_menu = None
        self.screen = screen
        self.current_game_menu = "game_menu_world"
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.K_ESCAPE = False, False, False, False,False
        self.font_name = pygame.font.get_default_font()
        self.font_size = 20

    def blit_screen(self):
        self.screen.blit(self.display, (0, 0))
        reset_keys(self)

    def launch(self,game_menu):
        self.game_menu = game_menu
        self.playing = True
        print("Game Start")
        displayInfo = pygame.display.Info()
        #pygame.display.set_mode((displayInfo.current_w, displayInfo.current_h))
        #pygame.display.set_mode((self.w,self.h), pygame.FULLSCREEN)
        clock = pygame.time.Clock()
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing= False
            if self.K_ESCAPE :
                self.playing= False
                self.game_menu.game_options_menu.display_menu()
            self.display.fill(WHITE)
            draw_text(self.display,'Thanks for Playing', self.font_name,self.font_size, BLACK,self.mid_w, self.mid_h)
            self.blit_screen()
            pygame.display.update()
            clock.tick(FPS)

    def resume(self):
        self.playing = True
        print("Game Resume")
        #displayInfo = pygame.display.Info()
        #pygame.display.set_mode((displayInfo.current_w, displayInfo.current_h))
        #pygame.display.set_mode((self.w,self.h), pygame.FULLSCREEN)
        clock = pygame.time.Clock()
        return
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing= False
            if self.K_ESCAPE :
                self.playing= False
                self.game_menu.game_options_menu.display_menu()
            self.display.fill(WHITE)
            draw_text(self.display,'Resume Playing', self.font_name,self.font_size, BLACK,self.mid_w, self.mid_h)
            self.blit_screen()
            pygame.display.update()
            clock.tick(FPS)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                pygame.quit()
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

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
