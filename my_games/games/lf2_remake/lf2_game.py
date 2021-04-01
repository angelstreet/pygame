import pygame as pg
from engine.src.game import Game
from engine.src.player import HorizontalPlayer
from engine.src.utility import scale_img


class LF2_Game(Game):
    def __init__(self, display, w, h):
        Game.__init__(self, display, w, h)

    def add_imagegamebar(self, layer, x, y, value, total, avatar, bg_img, hp_bar, mp_bar, offset, scale=1):
        imagegamebar = Lf2GameBar(value, total, avatar, bg_img, hp_bar, mp_bar, offset, scale)
        self.move_sprite(imagegamebar, x, y)
        self.add_sprite(layer, x, y, imagegamebar)

    def add_player(self, layer, x, y, json, scale=1, force_right=False):
        player = Lf2Player(layer+2, json, scale, force_right)
        player.move(x, y)
        self.game_sprites.add(player)
        return player


class Lf2Player(HorizontalPlayer):
    def __init__(self, layer, json, scale=1, force_right=False):
        HorizontalPlayer.__init__(self, layer, json, scale,force_right)

    def _check_event(self):
        if self.K_RETURN:
            print(self.current_state,self.current_state in ('attack'), self._is_last_frame())
            if not self.current_state in ('attack','attack2'):
                self._reset_velocity()
                self._set_state('attack')
                self._attack()
            elif self.current_state in ('attack') and self._is_last_frame():
                self._set_state('attack2')
                self._attack()
        elif self.K_SPACE:
            if not self.current_state in ('jump', 'fall'):
                self._set_state('jump')
                self._jump()
        elif not (self.current_state == 'attack' or self.current_state == 'jump' or self.current_state == 'fall' or self.current_state == 'hurt'):
            if self.K_LEFT:
                self.velocity_x = -self.velocity
                if self.direction_h != 'left':
                    self.direction_h = 'left'
                    self.current_frame_id = 0
                self._set_state('walk')
            elif self.K_RIGHT:
                self.velocity_x = self.velocity
                if self.direction_h != 'right':
                    self.direction_h = 'right'
                    self.current_frame_id = 0
                self._set_state('walk')
            if self.K_UP:
                self.velocity_y = -self.velocity
                if self.direction_v != 'up':
                    self.direction_v = 'up'
                    self.current_frame_id = 0
                self._set_state('walk')
            elif self.K_DOWN:
                self.velocity_y = self.velocity
                if self.direction_v != 'down':
                    self.direction_v = 'down'
                    self.current_frame_id = 0
                self._set_state('walk')
            if not (self.K_LEFT or self.K_RIGHT):
                self.velocity_x = 0
            if not (self.K_UP or self.K_DOWN):
                self.velocity_y = 0
            if not (self.K_LEFT or self.K_RIGHT or self.K_UP or self.K_DOWN):
                self._set_state('idle')

class Lf2GameBar(pg.sprite.Sprite):
    def __init__(self, max_hp, max_mp, av_path, bg_path, hp_path, mp_path, offset, scale=1):
        pg.sprite.Sprite.__init__(self)
        self.max_hp = self.hp = max_hp
        self.max_mp = self.mp = max_mp
        self.av_path = av_path
        self.bg_path = bg_path
        self.hp_path = hp_path
        self.mp_path = mp_path
        self.offset = offset
        self.scale = scale
        self._load_img()
        self._scale_img()
        self._init_bar()

    def _load_img(self):
        self.av_img = pg.image.load(self.av_path).convert_alpha()
        self.bg_img = pg.image.load(self.bg_path).convert_alpha()
        self.hp_img = pg.image.load(self.hp_path).convert_alpha()
        self.mp_img = pg.image.load(self.mp_path).convert_alpha()

    def _scale_img(self):
        if self.scale != 1:
            self.av_img = scale_img(self.av_img, self.scale)
            self.bg_img = scale_img(self.bg_img, self.scale)
            self.hp_img = scale_img(self.hp_img, self.scale)
            self.mp_img = scale_img(self.mp_img, self.scale)

    def _init_bar(self):
        rect = self.bg_img.get_rect()
        self.image = pg.Surface(rect.size, pg.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()
        self.hp_bar_w, self.hp_bar_h = self.hp_img.get_rect().size
        self.mp_bar_w, self.mp_bar_h = self.mp_img.get_rect().size
        self.offset = int(self.offset*self.scale)

    def _draw(self):
        hp_percentage = self.hp/self.max_hp
        mp_percentage = self.hp/self.max_mp
        self.hp_w = round(hp_percentage*self.hp_bar_w)
        self.mp_w = round(mp_percentage*self.mp_bar_w)
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.hp_img, (self.offset, 0),
                        (0, 0, self.hp_bar_w, self.hp_bar_h))
        self.image.blit(self.mp_img, (self.offset, 0),
                        (0, 0, self.mp_bar_w, self.mp_bar_h))
        self.image.blit(self.av_img, (0, 0))
        self.image.blit(self.bg_img, (0, 0))

    # Public
    def update(self):
        self._draw()
