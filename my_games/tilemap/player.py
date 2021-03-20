#AngelStreet @2021
####################################################
from utility import load_json, get_sprite, move_sprite

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, json, scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.json = json
        self.scale = scale
        self.K_LEFT, self.K_RIGHT, self.K_DOWN, self.K_UP, self.K_SPACE, self.K_RETURN = False, False, False, False, False, False
        self.current_frame = 0
        self.last_updated = 0
        self.velocity = 2
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity_z = 0
        self.gravity = 1
        self.jump_force = -10
        self.z = 0
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
        # Create spritesheets
        self.playersheet_img = pygame.image.load(self.playersheet_name).convert_alpha()
        #self.playersheet_img_flip = pygame.transform.flip(self.playersheet_img.copy(), True, False)
        # Create sprite for all animation frames
        for key, value in self.frames_data.items():
            midbottom = value[0]['midbottom']
            flip = value[-1]
            for i, frame in enumerate(value):
                if i > 0 and isinstance(frame, dict):
                    frame_name = frame['name']
                    x, y, w, h, offsetx, offsety = self.get_frame_sprite_data(frame)
                    sprite = get_sprite(self.playersheet_img, x, y, w, h, self.colorkey)
                    sprite_flip = get_sprite(self.playersheet_img, x, y, w, h, self.colorkey)
                    sprite_flip = pygame.transform.flip(sprite_flip, True, False)
                    sprite = pygame.transform.scale(sprite, (w*self.scale, h*self.scale))
                    sprite_flip = pygame.transform.scale(sprite_flip, (w*self.scale, h*self.scale))
                    frame['sprite'] = sprite
                    frame['sprite_flip'] = sprite_flip

    def set_current_state(self,state):
        self.prev_state = self.current_state
        self.current_state = state

    def set_state(self):
        states = ['idle', 'walk', 'attack', 'jump', 'hurt']
        for state in states:
            if state in self.current_state:
                self.state = state

    def init_player(self):
        self.load_player_data_from_json()
        self.image = pygame.Surface(
            (self.resolution['max_w']*self.scale*2, self.resolution['max_h']*self.scale))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(self.colorkey)
        self.current_state = self.prev_state = self.first_frame
        self.load_player_frames()
        self.set_state()
        if "down" in self.current_state :
            self.direction_v = "down"
        else : self.direction_v = "up"
        if "right" in self.current_state :
            self.direction_h = "right"
        else  : self.direction_h = "left"

    def reset_velocity(self):
        self.velocity_x, self.velocity_y = 0, 0

    def move(self, x, y):
        move_sprite(self, x, y)

    def move_player(self,):
        self.move(self.velocity_x, self.velocity_y + self.velocity_z)
        if (self.state == 'jump' and self.velocity_z<0) :
            self.velocity_z = min(0,self.velocity_z+self.gravity)
            self.z+=self.velocity_z
        elif(self.state == 'jump' and self.velocity_z==0) :
            self.state="fall"
        elif(self.state == 'fall') :
            self.velocity_z = max(self.jump_force,self.velocity_z+self.gravity)
            self.z+=self.velocity_z
            if(self.velocity_z==-1*self.jump_force+self.gravity) :
                self.state="idle"
                self.velocity_z = 0
                self.z=0
                self.reset_velocity()

    def attack(self):
        pass

    def jump(self):
        self.z = 0
        self.velocity_z = self.jump_force

    def fall(self):
        pass

    def check_event(self):
        if self.K_RETURN:
            self.reset_velocity()
            self.state = 'attack'
            self.attack()
        elif self.K_SPACE:
            if not self.state in ('jump','fall') :#need to be abuse for double jumps
                self.state = 'jump'
                self.jump()
        elif not (self.state == 'attack' or self.state == 'jump' or self.state == 'hurt'):
            if self.K_LEFT:
                self.velocity_x = -self.velocity
                self.direction_h = 'left'
            elif self.K_RIGHT:
                self.velocity_x = self.velocity
                self.direction_h = 'right'
            if self.K_UP:
                self.velocity_y = -self.velocity
                self.direction_v = 'up'
            elif self.K_DOWN:
                self.velocity_y = self.velocity
                self.direction_v = 'down'
            if not (self.K_LEFT or self.K_RIGHT) :
                self.velocity_x = 0
            if not (self.K_UP or self.K_DOWN) :
                self.velocity_y = 0

    def set_frame(self):
        if self.state == 'attack' :
            self.set_current_state("attack_right" % self.direction_v)
        elif self.state == 'jump' :
            self.set_current_state("jump_right_%s" % self.direction_v)
        elif self.state == 'fall' :
            self.set_current_state("fall_right_%s" % self.direction_v)
        else:
            if self.velocity_x != 0:
                self.set_current_state("walk_right_%s" % self.direction_v)
            elif self.velocity_y != 0:
                self.set_current_state("walk_right_%s" % self.direction_v)
            elif self.velocity_x==0 and self.velocity_x==0 and self.velocity_z == 0 :
                self.set_current_state("idle_right_%s" % self.direction_v)

    def get_frame_rate(self):
        # +1 to skip midbottm
        frame_rate = self.frames_data[self.current_state][self.current_frame+1]
        return frame_rate

    def get_nb_frame(self):
        nb_frame = len(self.frames_data[self.current_state])-2  # less midbottom and flip
        return nb_frame

    def display_current_sprite(self):
        if self.direction_h =='right' :
            self.image = self.frames_data[self.current_state][self.current_frame+1]['sprite']
        else:
            self.image = self.frames_data[self.current_state][self.current_frame+1]['sprite_flip']

    def animate(self):
        frame_rate = self.get_frame_rate()['frame_rate']
        nb_frames = self.get_nb_frame()
        now = pygame.time.get_ticks()
        if now - self.last_updated > 100*frame_rate:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1)
            if self.current_frame == nb_frames :
                self.current_frame = 0
                if self.state in ('attack', 'hurt'):
                    self.last_updated = now
                    self.state = 'idle'
        self.display_current_sprite()

    def update(self):
        self.check_event()  # check key press event
        self.move_player()
        self.set_frame()  # attack_right_down_1, hurt_right_up_1, etc..
        self.set_state()  # idle, move or attack
        self.animate()  # animate player by updating frame
