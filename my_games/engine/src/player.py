#AngelStreet @2021
####################################################
from src.utility import load_json, move_sprite
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
        self.rigid = True
        self.collision_list = []
        self.current_state = None
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.1)
        self.init_player()
        self.debug = True


    def load_player_data_from_json(self):
        data = load_json(self.json)
        self.playersheet_name = data['player']['playersheet_name']
        self.colorkey = data['player']['colorkey']
        self.attributes = data['player']['attributes']
        self.first_frame = data['player']['first_frame']
        self.resolution = data['player']['resolution']
        self.frames_data = data['player']['frames']
        self.sound_data = data['player']['sound']

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
            midbottom = value[0]['midbottom']
            flip = value[-1]
            for i, frame in enumerate(value):
                if i > 0 and isinstance(frame, dict):
                    frame_name = frame['name']
                    x, y, w, h, offsetx, offsety = [int(elt*self.scale) for elt in self.get_frame_sprite_data(frame)]
                    sprite = pygame.Surface((w, h),pygame.SRCALPHA, 32).convert_alpha()
                    sprite.blit(self.playersheet_img , (0, 0), (x, y, w, h))
                    sprite_flip =  pygame.transform.flip(sprite, True, False)
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
        move_sprite(self.rect,x, y)

    def check_collision(self):
        c_left,c_right,c_up,c_down,c_top,c_bottom = False,False,False,False,False,False
        if len(self.collision_list)>0:
            for c_sprite in self.collision_list:
                if self.collision_sprite.rect.x< c_sprite.rect.x :
                    print("1")
                    c_right,c_left=0,-1
                else :
                    print("2")
                    c_right,c_left=1,0
                if self.collision_sprite.rect.y< c_sprite.rect.y :
                    print("3")
                    c_down,c_up=0,-1
                else:
                    print("4")
                    c_down,c_up=1,0
            print(self.collision_sprite.rect,c_sprite.rect)
        self.collision_list = []
        #print(c_left,c_right,c_up,c_down)
        return c_left,c_right,c_up,c_down,0,0

    def move_player(self):
        c_left,c_right,c_up,c_down,c_top,c_bottom = self.check_collision()
        vx = self.velocity_x+(c_left+c_right)*self.velocity
        vy = self.velocity_y+(c_up+c_down)*self.velocity
        vz = self.velocity_z
        if vx!=0 and vy!=0 :
            vx*=0.8

        self.move(vx,vy+vz)
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
        if 'attack' in self.sound_data :
            attack_sound = self.sound_data['attack']
            pygame.mixer.music.load(attack_sound)
            pygame.mixer.music.play()

    def jump(self):
        self.z = 0
        self.velocity_z = self.jump_force
        if 'jump' in self.sound_data :
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
        if self.debug :
            self.displayCollisionLosange()
            self.displayRadius()

    def displayCollisionLosange(self):
        self.image.blit(self.get_collision_sprite().image,(0,0))

    def displayRadius(self):
        pass

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
        self.animate()  # animate player by updating frame

    def zsort(self):
        depth = round(self.rect.y+self.rect.h-self.z+50)
        return depth

    def is_moving(self) :
        if self.velocity_x!=0 or self.velocity_y!=0 or self.velocity_z!=0:
            return True
        return False

    def get_collision_sprite(self) :
        self.collision_sprite = pygame.sprite.Sprite()
        self.collision_sprite.image = pygame.Surface((self.rect.size),pygame.SRCALPHA, 32).convert_alpha()
        w,h = int(100*0.43),int(60*0.43)
        x,y,z=40,54,40
        polygon_b=[(w/2+x, y), (w+x, h/2+y), (w/2+x, h+y),(x, h/2+y)]
        pygame.draw.polygon(self.collision_sprite.image,(0,0,255),polygon_b)
        self.collision_sprite.mask = pygame.mask.from_surface(self.collision_sprite.image)
        self.collision_sprite.rect = self.image.get_rect()
        self.collision_sprite.rect.x=self.rect.x
        self.collision_sprite.rect.y=self.rect.y
        #polygon_t=[(w/2+x, y-z), (w+x, h/2+y-z), (w/2+x, h+y-z),(x, h/2+y-z)]
        #pygame.draw.polygon(collision_sprite,(255,0,0),polygon_t)
        #pygame.draw.line(collision_sprite,(0,0,255),polygon_t[1],polygon_b[1] )
        #pygame.draw.line(collision_sprite,(0,0,255),polygon_t[3],polygon_b[3])
        self.collision_sprite.parent = self
        return self.collision_sprite
