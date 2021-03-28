#AngelStreet @2021
####################################################
import pygame
from engine.src.gamesprite import GameSprite
from engine.src.utility import load_json, move_sprite, iso_to_cartesian


class Player(GameSprite):
    def __init__(self, json, map_x, map_y, tile_w, tile_h, scale=1):
        GameSprite.__init__(self)
        self.json = json
        self.map_x = map_x
        self.map_y = map_y
        self.tile_w = tile_w
        self.tile_h = tile_h
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
        self.rigid = True
        self.collision_list = []
        self.current_state = None
        self.debug = False
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
        self.sound_data = data['player']['sound']
        self.collision_losange = data['player']['collision_losange']

    def get_frame_sprite_data(self, frame):
        return frame['x'], frame['y'], frame['w'], frame['h'], frame['offsetx'], frame['offsety']

    def load_player_frames(self):
        # Create spritesheets
        self.playersheet_img = pygame.image.load(self.playersheet_name).convert_alpha()
        rect = self.playersheet_img.get_rect()
        dimension = int(rect.width*self.scale), int(rect.height*self.scale)
        self.playersheet_img = pygame.transform.scale(self.playersheet_img, dimension)
        # Create sprite for all animation frames
        for key, value in self.frames_data.items():
            for i, frame in enumerate(value):
                if i > 0 and isinstance(frame, dict):
                    x, y, w, h, offsetx, offsety = [int(elt*self.scale)
                                                    for elt in self.get_frame_sprite_data(frame)]
                    sprite = pygame.Surface((w, h), pygame.SRCALPHA, 32).convert_alpha()
                    sprite.blit(self.playersheet_img, (0, 0), (x, y, w, h))
                    sprite_flip = pygame.transform.flip(sprite, True, False)
                    frame['sprite'] = sprite
                    frame['sprite_flip'] = sprite_flip

    def set_current_frame(self, frame):
        if self.current_frame != frame:
            self.prev_frame = self.current_frame
            self.current_frame = frame
            self.current_frame_id = 0

    def set_frame(self):
        self.set_current_frame("%s_right_%s" % (self.current_state, self.direction_v))

    def set_state(self, state=False):
        if not self.current_state == state:
            if state:
                if self.current_state:
                    self.prev_state = self.current_state
                self.current_state = state
            else:
                states = ['idle', 'walk', 'attack', 'jump', 'fall', 'hurt']
                for state in states:
                    if state in self.current_frame:
                        if self.current_state:
                            self.prev_state = self.current_state
                        self.current_state = state
        self.set_frame()

    def init_direction_from_frame(self):
        if "down" in self.current_frame:
            self.direction_v = "down"
        else:
            self.direction_v = "up"
        if "right" in self.current_frame:
            self.direction_h = "right"
        else:
            self.direction_h = "left"

    def init_player(self):
        self.create_surface(50, 50)
        self.load_player_data_from_json()
        self.create_surface(self.resolution['max_w']*self.scale *
                            2, self.resolution['max_h']*self.scale)
        if self.colorkey:
            self.image.set_colorkey(self.colorkey)
        self.prev_frame = None
        self.current_frame = self.first_frame
        self.last_collision_list = []
        self.init_direction_from_frame()
        self.init_collision_losange()
        self.set_state()
        self.set_frame()
        self.load_player_frames()
        self.get_collision_sprite()

    def init_collision_losange(self):
        self.collision_losange_w = self.collision_losange["w"]*self.scale
        self.collision_losange_h = self.collision_losange["h"]*self.scale
        self.collision_losange_offsetx = self.collision_losange["offsetx"]*self.scale
        self.collision_losange_offsety = self.collision_losange["offsety"]*self.scale

    def reset_velocity(self):
        self.velocity_x, self.velocity_y = 0, 0

    def move(self, x, y):
        move_sprite(self.rect, x, y)

    def vsort_collision_list(self, sprite):
        if 'z' in dir(sprite):
            return sprite.z
        return 0

    def check_collision(self):
        if self.debug:
            self.blit_rear(self.collision_sprite.image,
                           (self.collision_sprite.x, self.collision_sprite.y))
            #self.blit_rear(self.collision_sprite.image, (0,0))
        for c_sprite in self.last_collision_list:
            c_sprite.parent.clear_front()
        self.last_collision_list = []
        c_left, c_right, c_up, c_down, c_top, c_bottom = 0, 0, 0, 0, 0, 0
        if len(self.collision_list) > 0:
            self.collision_list.sort(key=self.vsort_collision_list)
            for c_sprite in self.collision_list:
                if self.debug:
                    c_sprite.parent.blit_front(c_sprite.image)
                    self.last_collision_list.append(c_sprite)
                if self.current_state == 'fall' and abs(self.z-c_sprite.parent.z-c_sprite.parent.rect.height) < 4:
                    #if self.debug :print("Bottom Collision", self.z,c_sprite.parent.z,c_sprite.parent.rect.height)
                    c_bottom = -1
                    self.velocity_x, self.velocity_y, self.velocity_z = 0, 0, 0
                    self.set_state("idle")
                    break
                if self.collision_sprite.rect.x < c_sprite.rect.x+c_sprite.rect.width/2:
                    #if self.debug :print("Right Collision", self.collision_sprite.rect.x,self.collision_losange_offsetx,c_sprite.rect.x,c_sprite.rect.width/2)
                    c_right = -1
                else:
                    #if self.debug :print("Left Collision",  self.collision_sprite.rect.x,self.collision_losange_offsetx,c_sprite.rect.x,c_sprite.rect.width/2)
                    c_left = 1
                if self.collision_sprite.rect.y < c_sprite.rect.y+c_sprite.rect.height/2:
                    #if self.debug :print("Down Collision", self.collision_sprite.rect.y,self.collision_losange_offsety,c_sprite.rect.y,c_sprite.rect.height/2 )
                    c_down = -1
                else:
                    #if self.debug :print("Up Collision", self.collision_sprite.rect.y,self.collision_losange_offsety,c_sprite.rect.y,c_sprite.rect.height/2 )
                    c_up = 1
            #if self.debug :print(self.collision_sprite.rect,c_sprite.rect)
        self.collision_list = []
        return c_left, c_right, c_up, c_down, 0, 0

    def move_player(self):
        c_left, c_right, c_up, c_down, c_top, c_bottom = self.check_collision()
        vx = self.velocity_x+(c_left+c_right)*self.velocity
        vy = self.velocity_y+(c_up+c_down)*self.velocity
        vz = self.velocity_z
        if vz > 0:
            print(vz, self.z)
        if vx != 0 and vy != 0:
            vx *= 0.8

        self.move(vx, vy+vz)
        if (self.current_state == 'jump' and self.velocity_z < 0):
            self.velocity_z = min(0, self.velocity_z+self.gravity)
            self.z += self.velocity_z
        elif(self.current_state == 'jump' and self.velocity_z == 0):
            self.set_state("fall")
        elif(self.current_state == 'fall'):
            self.velocity_z = max(self.jump_force, self.velocity_z+self.gravity)
            self.z += self.velocity_z
            if(self.velocity_z == -1*self.jump_force+self.gravity):
                self.set_state("idle")
                self.velocity_z = 0
                self.z = 0
                self.reset_velocity()

    def attack(self):
        if 'attack' in self.sound_data:
            attack_sound = self.sound_data['attack']
            pygame.mixer.music.load(attack_sound)
            pygame.mixer.music.play()

    def jump(self):
        self.z = 0
        self.velocity_z = self.jump_force
        if 'jump' in self.sound_data:
            jump_sound = self.sound_data['jump']
            pygame.mixer.music.load(jump_sound)
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
            if not self.current_state in ('jump', 'fall'):  # need to be abuse for double jumps
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
            if not (self.K_LEFT or self.K_RIGHT):
                self.velocity_x = 0
            if not (self.K_UP or self.K_DOWN):
                self.velocity_y = 0
            if not (self.K_LEFT or self.K_RIGHT or self.K_UP or self.K_DOWN):
                self.set_state('idle')

    def get_frame_rate(self):
        frame_rate = self.frames_data[self.current_frame][self.current_frame_id+1]['frame_rate']
        return frame_rate

    def get_nb_frame(self):
        nb_frames = len(self.frames_data[self.current_frame])-1  # less midbottom and sprite
        return nb_frames

    def display_current_sprite(self):
        if self.direction_h == 'right':
            self.blit(self.frames_data[self.current_frame][self.current_frame_id+1]['sprite'])
        else:
            self.blit(self.frames_data[self.current_frame][self.current_frame_id+1]['sprite_flip'])

    def animate(self):
        frame_rate = self.get_frame_rate()
        nb_frames = self.get_nb_frame()
        now = pygame.time.get_ticks()
        if now - self.last_updated > 100*frame_rate:
            self.last_updated = now
            self.current_frame_id += 1
            if self.current_frame_id == nb_frames:
                self.current_frame_id = 0
                if self.current_state in ('attack', 'hurt'):
                    self.last_updated = now
                    self.set_state('idle')
        self.display_current_sprite()

    def update(self):
        self.check_event()  # check key press event
        self.move_player()
        self.animate()  # animate player by updating frame
        self.blits()

    def zsort(self):
        isox, isoy = self.rect.x+self.rect.width/2-self.map_x-600-190, self.rect.y+self.rect.height-self.map_y-80
        x, y = iso_to_cartesian(isox, isoy)
        i = round(x/self.tile_w*self.scale)
        j = round(y/self.tile_h*self.scale)
        depth = int(200+i*100+1000*j-self.z)
        #print("player", i, j, isox,isoy,x,y)
        return depth

    def is_moving(self):
        if self.velocity_x != 0 or self.velocity_y != 0 or self.velocity_z != 0:
            return True
        return False

    def get_collision_sprite_center(self):
        self.get_collision_sprite()
        x = self.collision_sprite.rect.x + self.collision_sprite.rect.width/2
        y = self.collision_sprite.rect.y + self.collision_sprite.rect.height/2
        return x, y

    def get_collision_sprite(self):
        w, h = self.collision_losange_w, self.collision_losange_h
        offsetx, offsety = self.collision_losange_offsetx, self.collision_losange_offsety
        self.collision_sprite = pygame.sprite.Sprite()
        self.collision_sprite.image = pygame.Surface((w, h), pygame.SRCALPHA, 32).convert_alpha()
        polygon_b = [(w/2, 0), (w, h/2), (w/2, h), (0, h/2)]
        pygame.draw.polygon(self.collision_sprite.image, (0, 0, 255), polygon_b)
        self.collision_sprite.mask = pygame.mask.from_surface(self.collision_sprite.image)
        self.collision_sprite.rect = self.collision_sprite.image.get_rect()
        self.collision_sprite.x = offsetx
        self.collision_sprite.y = self.rect.height-self.collision_sprite.rect.height
        self.collision_sprite.rect.x = self.rect.x+self.collision_sprite.x
        self.collision_sprite.rect.y = self.rect.y+self.rect.height-self.collision_sprite.y

        #polygon_t=[(w/2+x, y-z), (w+x, h/2+y-z), (w/2+x, h+y-z),(x, h/2+y-z)]
        # pygame.draw.polygon(collision_sprite,(255,0,0),polygon_t)
        #pygame.draw.line(collision_sprite,(0,0,255),polygon_t[1],polygon_b[1] )
        # pygame.draw.line(collision_sprite,(0,0,255),polygon_t[3],polygon_b[3])
        self.collision_sprite.parent = self
        return self.collision_sprite

class IsoPlayer(Player):
    def __init__(self, json, map_x, map_y, tile_w, tile_h, scale=1):
        Player.__init__(self, json, map_x, map_y, tile_w, tile_h, scale)
