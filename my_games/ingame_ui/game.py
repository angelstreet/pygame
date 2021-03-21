import pygame
from utility import FPS, WHITE, BLACK, draw_text, reset_keys, resize_screen, blit_screen
import ui_interface
from ui_interface import ColorGameBar,ImageGameBar,HeartGameBar

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT_NAME = pygame.font.get_default_font()
FONT_SIZE = 14

class Game():
    def __init__(self, screen, display, WIDTH, HEIGHT):
        self.screen = screen
        self.display = display
        self.w, self.h = WIDTH, HEIGHT
        self.mid_w, self.mid_h = WIDTH / 2, HEIGHT / 2
        self.playing = False
        self.game_menu = None
        self.screen = screen
        self.current_game_menu = "game_menu_world"
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.K_ESCAPE = False, False, False, False, False
        self.font_name = pygame.font.get_default_font()
        self.font_size = 20
        self.bg = pygame.Surface((self.w, self.h))
        self.fx = pygame.Surface((self.w, self.h))
        self.ui = pygame.Surface((self.w, self.h))
        self.bg_sprites = pygame.sprite.Group()
        self.game_sprites = pygame.sprite.OrderedUpdates()
        self.fx_sprites = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.OrderedUpdates()
        self.init_healtbar()

    def init_healtbar(self):
        #self.healthbar =ColorGameBar(50, 100, 10, 10, 200, 40)
        #self.healthbar =ImageGameBar(100, 100, 10, 10,'healthbar_bg.png','healthbar_fill.png',84, (0,0,0),True)
        self.healthbar =HeartGameBar(6, 6, 10, 10,'heart.json',0.2,10)

        self.ui_sprites.add(self.healthbar)

    def draw_bg(self, display, bg_sprites):
        display.fill(WHITE)
        bg_sprites.draw(display)

    def zsort(self, sprite):
        return sprite.zsort()

    def sortGameSprite(self, game_sprites):
        tmp = game_sprites.sprites()
        tmp.sort(key=self.zsort)
        return pygame.sprite.OrderedUpdates(tmp)

    def draw_game(self, display, game_sprites):
        game_sprites.update()
        game_sprites = self.sortGameSprite(game_sprites)
        game_sprites.draw(display)

    def display_fps(self, display, clock):
        fps = str(int(clock.get_fps()))+" fps"
        draw_text(display, fps, FONT_NAME, FONT_SIZE, BLACK, self.w-50, 20)

    def draw_fx(self, display, fx_sprites):
        pass

    def draw_ui(self, display, ui_sprites, clock):
        self.display_fps(display, clock)
        ui_sprites.update()
        ui_sprites.draw(display)

    def draw_screen(self, screen, display, bg_sprites, game_sprites, fx_sprites, ui_sprites, clock):
        self.draw_bg(display, bg_sprites)
        self.draw_game(display, game_sprites)
        self.draw_fx(display, fx_sprites)
        self.draw_ui(display, ui_sprites, clock)
        screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
        pygame.display.update()

    def launch(self, game_menu, resume=False):
        reset_keys(self)
        self.screen, self.display = resize_screen(self.w, self.h)
        self.game_menu = game_menu
        self.playing = True
        if resume:
            print("Game Resume")
        else:
            print("Game Start")
        clock = pygame.time.Clock()
        while self.playing:
            self.check_events()
            self.draw_screen(self.screen, self.display, self.bg_sprites,
                             self.game_sprites, self.fx_sprites, self.ui_sprites, clock)
            clock.tick(FPS)

    def resume(self):
        self.launch(self.game_menu, True)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                pygame.quit()
            if event.type == pygame.VIDEORESIZE:
                self.w, self.h = event.w, event.h
                self.mid_w, self.mid_h = self.w / 2, self.h / 2
                self.screen, self.display = resize_screen(event.w, event.h, True)
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
        if self.START_KEY:
            self.playing = False
        if self.K_ESCAPE:
            self.playing = False
            self.screen, self.display = resize_screen(
                self.game_menu.current_menu.w, self.game_menu.current_menu.h)
            self.game_menu.game_options_menu.display_menu()
