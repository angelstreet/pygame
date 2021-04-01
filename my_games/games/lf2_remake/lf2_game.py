import pygame as pg
from engine.src.game import Game
from engine.src.utility import scale_img


class LF2_Game(Game):
    def __init__(self, display, w, h):
        Game.__init__(self, display, w, h)

    def add_imagegamebar(self, layer, x, y, value, total, avatar, bg_img, hp_bar, mp_bar, offset, scale=1):
        imagegamebar = Lf2GameBar(value, total, avatar, bg_img, hp_bar, mp_bar, offset, scale)
        self.move_sprite(imagegamebar, x, y)
        self.add_sprite(layer, x, y, imagegamebar)


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
