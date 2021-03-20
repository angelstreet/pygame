#AngelStreet @2021
####################################################
from utility import load_json, get_sprite, move_sprite
import sys
import os
import pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Player(pygame.sprite.Sprite):
    def __init__(self, json, scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.json = json
        self.scale = scale
        self.K_LEFT, self.K_RIGHT, self.K_DOWN, self.K_UP, self.K_SPACE = False, False, False, False, False
        self.current_frame = 0
        self.last_updated = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity_z = 0
        self.init_player()

    def load_player_data_from_json(self):
        data = load_json(self.json)
        self.playersheet_name = data['player']['playersheet_name']
        self.colorkey = data['player']['colorkey']
        self.attributes = data['player']['attributes']
        self.first_frame = data['player']['first_frame']
        self.resolution = data['player']['resolution']
        self.frames_data = data['player']['frames']

    def get_frame_sprite_data(self, frame):
        return frame['x'], frame['y'], frame['w'], frame['h'], frame['offsetx'], frame['offsety']

    def load_player_frames(self):
        flip_frames = []
        for key, value in self.frames_data.items():
            flip_frame_name = key.replace('right', 'left')
            flip_value = value.copy()
            value.append('False')  # identify frame to flip
            flip_value.append('True')
            flip_frames.append((flip_frame_name, flip_value))
        # Populate the dictionnary with flipped frames
        for flip_frame_name, flip_value in flip_frames:
            self.frames_data[flip_frame_name] = flip_value
        # Create spritesheets
        self.playersheet_img = pygame.image.load(self.playersheet_name).convert_alpha()
        self.playersheet_img_flip = pygame.transform.flip(self.playersheet_img.copy(), True, False)
        # Create sprite for all aimation frames
        for key, value in self.frames_data.items():
            midbottom = value[0]['midbottom']
            flip = value[-1]
            for i, frame in enumerate(value):
                if i > 0 and isinstance(frame, dict):
                    frame_name = frame['name']
                    x, y, w, h, offsetx, offsety = self.get_frame_sprite_data(frame)
                    if not flip:
                        sprite = get_sprite(self.playersheet_img_flip, x, y, w, h, self.colorkey)
                    else:
                        sprite = get_sprite(self.playersheet_img, x, y, w, h, self.colorkey)
                    sprite = pygame.transform.scale(sprite, (w*self.scale, h*self.scale))
                    frame['sprite'] = sprite

    def set_state(self):
        states = ['idle', 'walk', 'attack', 'jump', 'hurt']
        for state in states:
            if state in self.current_state:
                self.state = state

    def set_direction(self):
        if 'right' in self.current_state:
            self.direction_h = 'right'
        else:
            self.direction_h = 'left'
        if 'up' in self.current_state:
            self.direction_v = 'up'
        else:
            self.direction_v = 'down'

    def init_player(self):
        self.load_player_data_from_json()
        self.image = pygame.Surface(
            (self.resolution['max_w']*self.scale*2, self.resolution['max_h']*self.scale))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(self.colorkey)
        self.current_state = self.prev_state = self.first_frame
        self.load_player_frames()
        self.set_state()
        self.set_direction()

    def reset_velocity(self):
        self.velocity_x, self.velocity_y = 0, 0

    def move(self, x, y):
        move_sprite(self, x, y)

    def move_player(self,):
        self.move(self.velocity_x, self.velocity_y + self.velocity_z)

    def check_event(self):
        if self.K_SPACE:
            self.reset_velocity()
        else:
            if self.K_LEFT:
                self.velocity_x = -2
                self.direction_h = 'left'
            elif self.K_RIGHT:
                self.velocity_x = 2
                self.direction_h = 'right'
            if self.K_UP:
                self.velocity_y = -2
                self.direction_v = 'up'
            elif self.K_DOWN:
                self.velocity_y = 2
                self.direction_v = 'down'

    def set_frame(self):
        if self.velocity_x != 0:
            self.current_state = "walk_%s_%s" % (self.direction_h,self.direction_v)
        elif self.velocity_y != 0:
            self.current_state = "walk_%s_%s" % (self.direction_h,self.direction_v)
        elif self.state!='idle' and self.velocity_x==0 and self.velocity_x==0 and self.velocity_z == 0 :
            self.current_state = "idle_%s_%s" % (self.direction_h,self.direction_v)

    def get_frame_rate(self):
        # +1 to skip midbottm
        frame_rate = self.frames_data[self.current_state][self.current_frame+1]
        return frame_rate

    def get_nb_frame(self):
        nb_frame = len(self.frames_data[self.current_state])-2  # less midbottom and flip
        return nb_frame

    def display_current_sprite(self):
        # print(self.frames_data[self.current_state][self.current_frame+1])
        # +1 to skip midbottom
        self.image = self.frames_data[self.current_state][self.current_frame+1]['sprite']

    def animate(self):
        frame_rate = self.get_frame_rate()['frame_rate']
        nb_frames = self.get_nb_frame()
        now = pygame.time.get_ticks()
        if now - self.last_updated > 100*frame_rate:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1) % nb_frames

        if self.current_frame == 0:
            if self.state in ('attack', 'jump', 'hurt'):
                self.last_updated = now
                self.current_state = self.prev_state

        self.display_current_sprite()

    def update(self):
        self.reset_velocity()
        self.check_event()  # check key press event
        self.move_player()
        self.set_frame()  # attack_right_down_1, hurt_right_up_1, etc..
        self.set_state()  # idle, move or attack
        self.set_direction()  # left or right
        self.animate()  # animate player by updating frame
