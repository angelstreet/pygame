#AngelStreet @2021
####################################################
from src.utility import load_json, get_sprite, move_sprite
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, json, scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.json = json
        self.scale = scale
        self.K_LEFT, self.K_RIGHT, self.K_DOWN, self.K_UP, self.K_SPACE, self.K_RETURN = False, False, False, False, False, False
        self.current_frame_id = 0
        self.last_updated = 0
        self.velocity = 2
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity_z = 0
        self.gravity = 1
        self.jump_force = -10
        self.z = 0
        self.current_state = None
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.1)
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

    def set_current_frame(self,frame):
        if self.current_frame != frame:
            self.prev_frame = self.current_frame
            self.current_frame = frame
            self.current_frame_id=0

    def set_frame(self):
        self.set_current_frame("%s_right_%s" % (self.current_state, self.direction_v))


    def set_state(self,state=False):
        if not self.current_state==state :
            if state :
                if self.current_state :
                    self.prev_state = self.current_state
                self.current_state = state
            else :
                states = ['idle', 'walk', 'attack', 'jump','fall', 'hurt']
                for state in states:
                    if state in self.current_frame:
                        if self.current_state :
                            self.prev_state = self.current_state
                        self.current_state = state
        self.set_frame()

    def init_direction_from_frame(self):
        if "down" in self.current_frame :
            self.direction_v = "down"
        else : self.direction_v = "up"
        if "right" in self.current_frame :
            self.direction_h = "right"
        else  : self.direction_h = "left"

    def init_player(self):
        self.load_player_data_from_json()
        self.image = pygame.Surface(
            (self.resolution['max_w']*self.scale*2, self.resolution['max_h']*self.scale))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(self.colorkey)
        self.prev_frame = None
        self.current_frame = self.first_frame
        self.init_direction_from_frame()
        self.set_state()
        self.set_frame()
        self.load_player_frames()

    def reset_velocity(self):
        self.velocity_x, self.velocity_y = 0, 0

    def move(self, x, y):
        move_sprite(self, x, y)

    def move_player(self,):
        self.move(self.velocity_x, self.velocity_y + self.velocity_z)
        if (self.current_state == 'jump' and self.velocity_z<0) :
            self.velocity_z = min(0,self.velocity_z+self.gravity)
            self.z+=self.velocity_z
        elif(self.current_state == 'jump' and self.velocity_z==0) :
            self.set_state("fall")
        elif(self.current_state == 'fall') :
            self.velocity_z = max(self.jump_force,self.velocity_z+self.gravity)
            self.z+=self.velocity_z
            if(self.velocity_z==-1*self.jump_force+self.gravity) :
                self.set_state("idle")
                self.velocity_z = 0
                self.z=0
                self.reset_velocity()

    def attack(self):
        pygame.mixer.music.load('sword.mp3')
        pygame.mixer.music.play()

    def jump(self):
        self.z = 0
        self.velocity_z = self.jump_force
        pygame.mixer.music.load('jump.mp3')
        pygame.mixer.music.play()

    def fall(self):
        pass

    def check_event(self):
        if self.K_RETURN:
            if not self.current_state in ('attack'):
                self.reset_velocity()
                self.set_state('attack')
                self.attack()
        elif self.K_SPACE:
            if not self.current_state in ('jump','fall') :#need to be abuse for double jumps
                self.set_state('jump')
                self.jump()
        elif not (self.current_state == 'attack' or self.current_state == 'jump' or self.current_state == 'fall' or self.current_state == 'hurt'):
            if self.K_LEFT:
                self.velocity_x = -self.velocity
                if self.direction_h != 'left':
                    self.direction_h = 'left'
                    self.current_frame_id = 0
                self.set_state('walk')
            elif self.K_RIGHT:
                self.velocity_x = self.velocity
                if self.direction_h != 'right':
                    self.direction_h = 'right'
                    self.current_frame_id = 0
                self.set_state('walk')
            if self.K_UP:
                self.velocity_y = -self.velocity
                if self.direction_v != 'up':
                    self.direction_v = 'up'
                    self.current_frame_id = 0
                self.set_state('walk')
            elif self.K_DOWN:
                self.velocity_y = self.velocity
                if self.direction_v != 'down':
                    self.direction_v = 'down'
                    self.current_frame_id = 0
                self.set_state('walk')
            if not (self.K_LEFT or self.K_RIGHT) :
                self.velocity_x = 0
            if not (self.K_UP or self.K_DOWN) :
                self.velocity_y = 0
            if not (self.K_LEFT or self.K_RIGHT or self.K_UP or self.K_DOWN) :
                self.set_state('idle')

    def get_frame_rate(self):
        # +1 to skip midbottm
        frame_rate = self.frames_data[self.current_frame][self.current_frame_id+1]['frame_rate']
        return frame_rate

    def get_nb_frame(self):
        nb_frames = len(self.frames_data[self.current_frame])-1  # less midbottom and sprite
        return nb_frames

    def display_current_sprite(self):
        if self.direction_h =='right' :
            self.image = self.frames_data[self.current_frame][self.current_frame_id+1]['sprite']
        else:
            self.image = self.frames_data[self.current_frame][self.current_frame_id+1]['sprite_flip']

    def animate(self):
        frame_rate = self.get_frame_rate()
        nb_frames = self.get_nb_frame()
        now = pygame.time.get_ticks()
        if now - self.last_updated > 100*frame_rate:
            self.last_updated = now
            self.current_frame_id += 1
            if self.current_frame_id == nb_frames :
                self.current_frame_id = 0
                if self.current_state in ('attack', 'hurt'):
                    self.last_updated = now
                    self.set_state('idle')
        self.display_current_sprite()

    def update(self):
        self.check_event()  # check key press event
        self.move_player()
        #self.set_frame()  # attack_right_down_1, hurt_right_up_1, etc..
        #self.set_state()  # idle, move or attack
        self.animate()  # animate player by updating frame

    def zsort(self):
        depth = round(self.rect.y+self.rect.h-self.z+54)
        return depth
