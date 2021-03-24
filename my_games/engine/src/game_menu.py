import pygame
from src.utility import FPS, WHITE, BLACK


class GameMenu(pygame.sprite.Sprite):
    def __init__(self, w, h, game):
        pygame.sprite.Sprite.__init__(self)
        self.w = w
        self.h = h
        self.game = game
        self.init_game_menu()

    def init_game_menu(self):
        self.image = pygame.Surface((self.w, self.h))
        self.rect = self.image.get_rect()

    def update(self):
        self.current_menu.update()

class Menu():
    def __init__(self, game_menu):
        self.game_menu = game_menu
        self.w = game_menu.w
        self.h = game_menu.h
        self.display = self.game_menu.image
        self.mid_w = self.w/2-70
        self.mid_h = self.h/2
        self.center =  self.mid_w,self.mid_h
        self.run_display = False
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 80
        self.font_name = pygame.font.get_default_font()
        self.font_size = 20

    def show(self):
        print(self.state)
        self.run_display = True
        self.game_menu.current_menu = self

    def move_cursor_up(self):
        pass
    def move_cursor_down(self):
        pass

    def go_back(self):
        pass

    def press_enter(self):
        pass

    def draw_text(self,display, text, font_name, size, color, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(str(text), True, color)
        self.display.blit(text_surface,(x,y))

    def draw_cursor(self):
        self.draw_text(self.display, '*', self.font_name, 20, WHITE,self.cursor_rect.x, self.cursor_rect.y)

class FirstScreenMenu(Menu):
    def __init__(self, game_menu, image):
        Menu.__init__(self,  game_menu)
        self.state = "FirstScreen"
        self.image = image

    def show(self):
        print(self.state)
        self.run_display = True
        self.last_updated = pygame.time.get_ticks()
        self.game_menu.current_menu = self
        sprite = pygame.image.load(self.image).convert()
        rect = sprite.get_rect()
        center = (self.w-rect.width)/2,(self.h-rect.height)/2
        self.display.fill((255,255, 255))
        self.display.blit(sprite,center)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_updated > 10000 :
            self.run_display = False
            self.game_menu.loading_menu.show()


class LoadingMenu(Menu):
    def __init__(self, game_menu, image, sound):
        Menu.__init__(self, game_menu)
        self.state = "LoadingMenu"
        self.image = image
        self.sound = sound

    def show(self):
        print(self.state)
        self.run_display = True
        self.last_updated = pygame.time.get_ticks()
        self.game_menu.current_menu = self
        self.sprite = pygame.image.load(self.image).convert()
        rect = self.sprite.get_rect()
        self.display.fill((255,255, 255))
        self.display.blit(self.sprite,(0,0))
        pygame.mixer.music.load(self.sound)
        pygame.mixer.music.play()
        self.draw_text(self.display, 'Loading...', self.font_name,30, WHITE, 1050,640)
        self.percentage = 1

    def update(self):
        now = pygame.time.get_ticks()
        self.display.fill((255,255, 255))
        self.display.blit(self.sprite,(0,0))
        self.draw_text(self.display, 'Loading...', self.font_name,30, WHITE, 990,640)
        self.draw_text(self.display, self.percentage, self.font_name,30, WHITE, 1140,640)
        if self.percentage < 100 :
            self.percentage +=1
            pygame.time.delay(100)
        else:
            pygame.time.delay(300)
            self.run_display = False
            pygame.mixer.music.stop()
            self.game_menu.main_menu.show()


class MainMenu(Menu):
    def __init__(self, game_menu):
        Menu.__init__(self, game_menu)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 60
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.game = game_menu.game

    def update(self):
        self.display.fill((0, 0, 0))
        self.draw_text(self.display, 'Main Menu', self.font_name,self.font_size, WHITE, self.mid_w, self.mid_h - 20)
        self.draw_text(self.display, "Start Game", self.font_name,self.font_size,  WHITE, self.startx, self.starty)
        self.draw_text(self.display, "Options", self.font_name,self.font_size,  WHITE, self.optionsx, self.optionsy)
        self.draw_text(self.display, "Credits", self.font_name, self.font_size,  WHITE, self.creditsx, self.creditsy)
        self.draw_cursor()

    def move_cursor_up(self):
        if self.state == 'Start':
            self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
            self.state = 'Credits'
        elif self.state == 'Options':
            self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
            self.state = 'Start'
        elif self.state == 'Credits':
            self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
            self.state = 'Options'
        pygame.time.delay(100)

    def move_cursor_down(self):
        if self.state == 'Start':
            self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
            self.state = 'Options'
        elif self.state == 'Options':
            self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
            self.state = 'Credits'
        elif self.state == 'Credits':
            self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
            self.state = 'Start'
        pygame.time.delay(100)

    def press_enter(self):
        if self.state == 'Start':
            self.run_display = False
            self.game.hide_game_menu()
            print("Launch game")
            self.game.resume()
        elif self.state == 'Options':
            self.run_display = False
            self.game_menu.options_menu.show()
        elif self.state == 'Credits':
            self.run_display = False
            self.game_menu.credits_menu.show()
        pygame.time.delay(100)


class OptionsMenu(Menu):
    def __init__(self, game_menu):
        Menu.__init__(self, game_menu)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)


    def update(self):
        self.display.fill((0, 0, 0))
        self.draw_text(self.display, 'Options', self.font_name, self.font_size, WHITE, self.mid_w, self.mid_h - 30)
        self.draw_text(self.display, 'Volume', self.font_name, self.font_size, WHITE, self.volx, self.voly)
        self.draw_text(self.display, 'Controls', self.font_name, self.font_size, WHITE, self.controlsx, self.controlsy)
        self.draw_cursor()


    def move_cursor_down(self):
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def move_cursor_up(self):
        self.move_cursor_down()

    def go_back(self):
        self.run_display = False
        self.game_menu.main_menu.show()
        pygame.time.delay(100)


class CreditsMenu(Menu):
    def __init__(self, game_menu):
        Menu.__init__(self, game_menu)
        self.state = 'Volume'

    def update(self):
        self.display.fill((0, 0, 0))
        self.draw_text(self.display, 'Credits', self.font_name, self.font_size, WHITE, self.mid_w, self.mid_h - 20)
        self.draw_text(self.display, 'AngelStreet @2021', self.font_name,15, WHITE, self.mid_w, self.mid_h + 10)

    def go_back(self):
        self.run_display = False
        self.game_menu.main_menu.show()
        pygame.time.delay(100)

    def press_enter(self):
        self.go_back()


class GameOptionsMenu(Menu):
    def __init__(self, game_menu):
        Menu.__init__(self, game_menu)
        self.state = 'Resume'
        self.resumex, self.resumey = self.mid_w, self.mid_h + 20
        self.volx, self.voly = self.mid_w, self.mid_h + 40
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
        self.game = game_menu.game

    def update(self):
        self.display.fill((0, 0, 0))
        self.draw_text(self.display, 'Options', self.font_name, self.font_size, WHITE, self.mid_w, self.mid_h - 30)
        self.draw_text(self.display, 'Resume', self.font_name, 15, WHITE, self.resumex, self.resumey)
        self.draw_text(self.display, 'Volume', self.font_name, 15, WHITE, self.volx, self.voly)
        self.draw_text(self.display, 'Controls', self.font_name,15, WHITE, self.controlsx, self.controlsy)
        self.draw_cursor()

    def go_back(self):
        self.run_display = False
        self.state = 'Resume'
        self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
        self.game.hide_game_menu()
        self.game.resume()

    def press_enter(self):
        if self.state == 'Resume':
            self.run_display = False
            self.game.hide_game_menu()
            self.game.resume()

    def move_cursor_down(self):
        if self.state == 'Resume':
            self.state = 'Volume'
            self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.state == 'Volume':
            self.state = 'Controls'
            self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
        elif self.state == 'Controls':
            self.state = 'Resume'
            self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)

    def move_cursor_up(self):
        if self.state == 'Controls':
            self.state = 'Volume'
            self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.state == 'Volume':
            self.state = 'Resume'
            self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
        elif self.state == 'Resume':
            self.state = 'Controls'
            self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
