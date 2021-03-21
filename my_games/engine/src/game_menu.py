import pygame
from src.utility import FPS, WHITE, BLACK, draw_text, reset_keys, blit_screen


class GameMenu():
    def __init__(self, screen, display, WIDTH, HEIGHT, game):
        self.game = game
        self.first_screen_menu = FirstScreenMenu(self, screen, display, WIDTH, HEIGHT)
        self.loading_menu = LoadingMenu(self, screen, display, WIDTH, HEIGHT)
        self.main_menu = MainMenu(self, screen, display, WIDTH, HEIGHT, game)
        self.options_menu = OptionsMenu(self, screen, display, WIDTH, HEIGHT)
        self.credits_menu = CreditsMenu(self, screen, display, WIDTH, HEIGHT)
        self.game_options_menu = GameOptionsMenu(self, screen, display, WIDTH, HEIGHT)
        #Launch game directly
        self.current_menu = self.main_menu
        self.main_menu.run_display = False
        self.main_menu.game.launch(self.main_menu.game_menu)


class Menu():
    def __init__(self, game_menu, screen, display, WIDTH, HEIGHT):
        self.game_menu = game_menu
        self.screen = screen
        self.display = display
        self.w, self.h = WIDTH, HEIGHT
        self.mid_w, self.mid_h = WIDTH / 2, HEIGHT / 2
        self.run_display = False
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.K_ESCAPE = False, False, False, False, False
        self.font_name = pygame.font.get_default_font()
        self.font_size = 20

    def draw_cursor(self):
        draw_text(self.display, '*', self.font_name, 15, WHITE,
                  self.cursor_rect.x, self.cursor_rect.y)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run_display = False
                pygame.Resume()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.K_ESCAPE = True


class FirstScreenMenu(Menu):
    def __init__(self, game_menu, screen, display, WIDTH, HEIGHT):
        Menu.__init__(self, game_menu, screen, display, WIDTH, HEIGHT)
        self.state = "FirstScreen"
        self.startx, self.starty = self.mid_w, self.mid_h + 30

    def display_menu(self):
        print(self.state)
        self.run_display = True
        self.game_menu.current_menu = self
        self.display.fill((255, 0, 0))
        blit_screen(self)
        pygame.display.update()
        pygame.time.delay(300)
        self.run_display = False
        self.game_menu.loading_menu.display_menu()


class LoadingMenu(Menu):
    def __init__(self, game_menu, screen, display, WIDTH, HEIGHT):
        Menu.__init__(self, game_menu, screen, display, WIDTH, HEIGHT)
        self.state = "LoadingMenu"
        self.startx, self.starty = self.mid_w, self.mid_h + 30

    def display_menu(self):
        print(self.state)
        self.run_display = True
        self.game_menu.current_menu = self
        self.display.fill((0, 255, 0))
        blit_screen(self)
        pygame.display.update()
        pygame.time.delay(300)
        self.run_display = False
        self.game_menu.main_menu.display_menu()


class MainMenu(Menu):
    def __init__(self, game_menu, screen, display, WIDTH, HEIGHT, game):
        Menu.__init__(self, game_menu, screen, display, WIDTH, HEIGHT)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 60
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.game = game

    def display_menu(self):
        reset_keys(self)
        print(self.state)
        self.run_display = True
        while self.run_display:
            self.display.fill((0, 0, 0))
            draw_text(self.display, 'Main Menu', self.font_name,
                      self.font_size, WHITE, self.mid_w, self.mid_h - 20)
            draw_text(self.display, "Start Game", self.font_name,
                      self.font_size,  WHITE, self.startx, self.starty)
            draw_text(self.display, "Options", self.font_name,
                      self.font_size,  WHITE, self.optionsx, self.optionsy)
            draw_text(self.display, "Credits", self.font_name,
                      self.font_size,  WHITE, self.creditsx, self.creditsy)
            self.check_events()
            self.check_input()
            self.draw_cursor()
            blit_screen(self)
            pygame.display.update()

    def move_cursor(self):
        if self.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.START_KEY:
            if self.state == 'Start':
                self.run_display = False
                self.game.launch(self.game_menu)
            elif self.state == 'Options':
                self.run_display = False
                self.game_menu.options_menu.display_menu()
            elif self.state == 'Credits':
                self.run_display = False
                self.game_menu.credits_menu.display_menu()


class OptionsMenu(Menu):
    def __init__(self, game_menu, screen, display, WIDTH, HEIGHT):
        Menu.__init__(self, game_menu, screen, display, WIDTH, HEIGHT)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        reset_keys(self)
        print(self.state)
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.display.fill((0, 0, 0))
            draw_text(self.display, 'Options', self.font_name,
                      self.font_size, WHITE, self.mid_w, self.mid_h - 30)
            draw_text(self.display, 'Volume', self.font_name, 15, WHITE, self.volx, self.voly)
            draw_text(self.display, 'Controls', self.font_name,
                      15, WHITE, self.controlsx, self.controlsy)
            self.draw_cursor()
            blit_screen(self)
            pygame.display.update()

    def check_input(self):
        if self.BACK_KEY or self.K_ESCAPE:
            self.run_display = False
            self.game_menu.main_menu.display_menu()
        elif self.UP_KEY or self.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.START_KEY:
            # TO-DO: Create a Volume Menu and a Controls Menu
            pass


class CreditsMenu(Menu):
    def __init__(self, game_menu, screen, display, WIDTH, HEIGHT):
        Menu.__init__(self, game_menu, screen, display, WIDTH, HEIGHT)

    def display_menu(self):
        reset_keys(self)
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            self.display.fill(BLACK)
            draw_text(self.display, 'Credits', self.font_name,
                      self.font_size, WHITE, self.mid_w, self.mid_h - 20)
            draw_text(self.display, 'Made by me', self.font_name,
                      15, WHITE, self.mid_w, self.mid_h + 10)
            blit_screen(self)
            pygame.display.update()

    def check_input(self):
        if self.START_KEY or self.BACK_KEY or self.K_ESCAPE:
            self.run_display = False
            self.game_menu.main_menu.display_menu()


class GameOptionsMenu(Menu):
    def __init__(self, game_menu, screen, display, WIDTH, HEIGHT):
        Menu.__init__(self, game_menu, screen, display, WIDTH, HEIGHT)
        self.state = 'Resume'
        self.resumex, self.resumey = self.mid_w, self.mid_h + 20
        self.volx, self.voly = self.mid_w, self.mid_h + 40
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)

    def display_menu(self):
        reset_keys(self)
        print(self.state)
        self.run_display = True

        while self.run_display:
            self.check_events()
            self.check_input()
            self.display.fill((0, 0, 0))
            draw_text(self.display, 'Options', self.font_name,
                      self.font_size, WHITE, self.mid_w, self.mid_h - 30)
            draw_text(self.display, 'Resume', self.font_name, 15, WHITE, self.resumex, self.resumey)
            draw_text(self.display, 'Volume', self.font_name, 15, WHITE, self.volx, self.voly)
            draw_text(self.display, 'Controls', self.font_name,
                      15, WHITE, self.controlsx, self.controlsy)
            self.draw_cursor()
            blit_screen(self)
            pygame.display.update()

    def check_input(self):
        if self.BACK_KEY or self.K_ESCAPE:
            reset_keys(self)
            self.run_display = False
            self.state = 'Resume'
            self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
            self.game_menu.game.resume()
        elif self.DOWN_KEY:
            if self.state == 'Resume':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
            elif self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Resume'
                self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
        elif self.UP_KEY:
            if self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
            elif self.state == 'Volume':
                self.state = 'Resume'
                self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
            elif self.state == 'Resume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
        elif self.START_KEY:
            if self.state == 'Resume':
                self.run_display = False
                self.game_menu.game.resume()
