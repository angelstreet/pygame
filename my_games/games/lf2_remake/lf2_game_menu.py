import pygame as pg
from engine.src.utility import WHITE, BLACK
LAUNCH_GAME = pg.USEREVENT + 1


class GameMenu(pg.sprite.Sprite):
    def __init__(self, w, h, game):
        pg.sprite.Sprite.__init__(self)
        self.w = w
        self.h = h
        self.game = game
        self.menu_list = {}
        self.image = pg.Surface((self.w, self.h))
        self.rect = self.image.get_rect()
        self.current_menu = None
        self.load_sound()

    def load_sound(self):
        self.ok_sound = pg.mixer.Sound('assets/sound/m_ok.wav')
        self.ok_sound.set_volume(0.5)
        self.back_sound = pg.mixer.Sound('assets/sound/m_cancel.wav')
        self.back_sound.set_volume(0.5)
        self.cursor_sound = pg.mixer.Sound('assets/sound/ff7_cursor.mp3')
        self.cursor_sound.set_volume(0.3)


    def add(self, name, menu):
        self.menu_list[name] = menu

    def update(self):
        if self.current_menu:
            self.current_menu.update()
        else:
            print("Warning : menu_list is empty ! Use .add()")

    def show(self, name):
        self.current_menu = self.menu_list[name]
        self.current_menu.show()


class Menu():
    def __init__(self, game_menu):
        self.game_menu = game_menu
        self.w = game_menu.w
        self.h = game_menu.h
        self.display = self.game_menu.image
        self.mid_w = self.w/2-70
        self.mid_h = self.h/2
        self.center = self.mid_w, self.mid_h
        self.cursor_rect = pg.Rect(0, 0, 20, 20)
        self.offset = - 40
        self.font_name = pg.font.get_default_font()
        self.font_size = 20

    def show(self):
        self.last_updated = pg.time.get_ticks()

    def draw_text(self, display, text, font_name, size, color, x, y):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(str(text), True, color)
        self.display.blit(text_surface, (x, y))

    def draw_cursor(self):
        self.draw_text(self.display, '*', self.font_name, 20, WHITE,
                       self.cursor_rect.x, self.cursor_rect.y+5)

    def go_back(self):
        pass

    def press_enter(self):
        pass

    def move_cursor_up(self):
        pass

    def move_cursor_down(self):
        pass


class FirstScreenMenu(Menu):
    def __init__(self, game_menu, image_path):
        Menu.__init__(self,  game_menu)
        self.image_path = image_path

    def show(self):
        super().show()
        self.display.fill((255, 255, 255))
        image = pg.image.load(self.image_path).convert()
        self.display.blit(image, (0, 0))

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_updated > 3000:
            self.game_menu.show('loading_menu')


class LoadingMenu(Menu):
    def __init__(self, game_menu, image_path, sound_path=None):
        Menu.__init__(self, game_menu)
        self.image_path = image_path
        self.sound_path = sound_path
        self.image, self.sound = None, None

    def show(self):
        super().show()
        self.image = pg.image.load(self.image_path).convert()
        self.display.blit(self.image, (0, 0))
        if(self.sound_path):
            pg.mixer.music.load(self.sound_path)
            pg.mixer.music.play()
        self.percentage = 1

    def update(self):
        self.display.fill((255, 255, 255))
        self.display.blit(self.image, (0, 0))
        self.draw_text(self.display, 'Loading...', self.font_name, 30, WHITE, 990, 550)
        self.draw_text(self.display, self.percentage, self.font_name, 30, WHITE, 1140, 550)
        if self.percentage < 100:
            self.percentage += 1
        else:
            pg.time.delay(1000)
            self.game_menu.show('main_menu')


class MainMenu(Menu):
    def __init__(self, game_menu, image_path, sound_path=None):
        Menu.__init__(self, game_menu)
        self.image_path = image_path
        self.sound_path = sound_path
        self.image, self.sound = None, None
        self.state = "Start"
        self.startx, self.starty = self.mid_w-20, self.mid_h - 40
        self.optionsx, self.optionsy = self.mid_w - 20, self.mid_h + 0
        self.creditsx, self.creditsy = self.mid_w-20, self.mid_h + 40
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def show(self):
        super().show()
        image = pg.image.load(self.image_path).convert()
        self.image = pg.transform.scale(image, (800, 400))
        self.rect = self.image.get_rect()
        self.center = (self.w-self.rect.width)/2, (self.h-self.rect.height)/2
        self.display.blit(self.image, self.center)

    def update(self):
        self.display.fill((0, 0, 40))
        self.center = (self.w-self.rect.width)/2, (self.h-self.rect.height)/2
        self.display.blit(self.image, self.center)
        self.draw_text(self.display, "game start ", self.font_name,
                       20, WHITE, self.startx, self.starty)
        self.draw_text(self.display, "control settings", self.font_name,
                       20, WHITE, self.optionsx, self.optionsy)
        self.draw_text(self.display, "credits", self.font_name,
                       20, WHITE, self.creditsx, self.creditsy)
        self.draw_cursor()

    def move_cursor_up(self):
        self.game_menu.cursor_sound.play()
        pg.time.delay(100)
        if self.state == 'Start':
            self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
            self.state = 'Credits'
        elif self.state == 'Options':
            self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
            self.state = 'Start'
        elif self.state == 'Credits':
            self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
            self.state = 'Options'

    def move_cursor_down(self):
        self.game_menu.cursor_sound.play()
        pg.time.delay(100)
        if self.state == 'Start':
            self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
            self.state = 'Options'
        elif self.state == 'Options':
            self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
            self.state = 'Credits'
        elif self.state == 'Credits':
            self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
            self.state = 'Start'

    def press_enter(self):
        self.game_menu.ok_sound.play()
        if self.state == 'Start':
            self.current_menu = None
            pg.time.delay(300)
            launch_game_event = pg.event.Event(LAUNCH_GAME, message='Launch game')
            pg.event.post(launch_game_event)
        # LISTEN GAME MENU KEY EVENT
        elif self.state == 'Options':
            self.game_menu.show('options_menu')
        elif self.state == 'Credits':
            self.game_menu.show('credits_menu')
        pg.time.delay(100)


class OptionsMenu(Menu):
    def __init__(self, game_menu):
        Menu.__init__(self, game_menu)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def update(self):
        self.display.fill((0, 0, 0))
        self.draw_text(self.display, 'Options', self.font_name,
                       self.font_size, WHITE, self.mid_w, self.mid_h - 30)
        self.draw_text(self.display, 'Volume', self.font_name,
                       self.font_size, WHITE, self.volx, self.voly)
        self.draw_text(self.display, 'Controls', self.font_name,
                       self.font_size, WHITE, self.controlsx, self.controlsy)
        self.draw_cursor()

    def move_cursor_down(self):
        self.game_menu.cursor_sound.play()
        pg.time.delay(100)
        if self.state == 'Volume':
            self.state = 'Controls'
            self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
        elif self.state == 'Controls':
            self.state = 'Volume'
            self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def move_cursor_up(self):
        self.move_cursor_down()

    def go_back(self):
        self.game_menu.back_sound.play()
        self.game_menu.show('main_menu')
        pg.time.delay(100)


class CreditsMenu(Menu):
    def __init__(self, game_menu):
        Menu.__init__(self, game_menu)
        self.state = 'Volume'

    def update(self):
        self.display.fill((0, 0, 0))
        self.draw_text(self.display, 'Credits', self.font_name,
                       self.font_size, WHITE, self.mid_w, self.mid_h - 20)
        self.draw_text(self.display, 'AngelStreet @2021', self.font_name,
                       15, WHITE, self.mid_w, self.mid_h + 10)

    def go_back(self):
        self.game_menu.back_sound.play()
        self.game_menu.show('main_menu')
        pg.time.delay(100)


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
        self.draw_text(self.display, 'Options', self.font_name,
                       self.font_size, WHITE, self.mid_w, self.mid_h - 30)
        self.draw_text(self.display, 'Resume', self.font_name,
                       15, WHITE, self.resumex, self.resumey)
        self.draw_text(self.display, 'Volume', self.font_name, 15, WHITE, self.volx, self.voly)
        self.draw_text(self.display, 'Controls', self.font_name,
                       15, WHITE, self.controlsx, self.controlsy)
        self.draw_cursor()

    def go_back(self):
        self.game_menu.back_sound.play()
        self.state = 'Resume'
        self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
        self.current_menu = None
        print("Go Back")
        pg.time.delay(100)

    def press_enter(self):
        if self.state == 'Resume':
            self.current_menu = None
            print("Resume game")
            self.game_menu.ok_sound.play()

    def move_cursor_down(self):
        self.game_menu.cursor_sound.play()
        pg.time.delay(100)
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
        self.game_menu.cursor_sound.play()
        pg.time.delay(100)
        if self.state == 'Controls':
            self.state = 'Volume'
            self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.state == 'Volume':
            self.state = 'Resume'
            self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
        elif self.state == 'Resume':
            self.state = 'Controls'
            self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
