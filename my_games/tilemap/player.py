#AngelStreet @2021
####################################################
import sys,os,pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utility import load_json,get_sprite
class Player(pygame.sprite.Sprite):
    def __init__(self,json,scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.json = json
        self.scale = scale
        self.K_LEFT, self.K_RIGHT, self.K_DOWN, self.K_UP, self.K_SPACE = False, False, False,False, False
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

    def get_frame_sprite_data(self,frame) :
        return frame['x'],frame['y'],frame['w'],frame['h'], frame['offsetx'],frame['offsety']

    def load_player_frames(self):
        flip_frames = []
        for key,value in self.frames_data.items() :
            flip_frame_name = key.replace('right','left')
            flip_value = value.copy()
            value.append('False') #identify frame to flip
            flip_value.append('True')
            flip_frames.append((flip_frame_name,flip_value))
        #Populate the dictionnary with flipped frames
        for flip_frame_name,flip_value in flip_frames :
            self.frames_data[flip_frame_name] = flip_value
        #Create spritesheets
        self.playersheet_img = pygame.image.load(self.playersheet_name).convert_alpha()
        self.playersheet_img_flip = pygame.transform.flip(self.playersheet_img.copy(),True, False)
        #Create sprite for all aimation frames
        for key, value in self.frames_data.items() :
            midbottom = value[0]['midbottom']
            flip  = value[-1]
            for i, frame in enumerate(value) :
                if i>0:
                    frame_name = frame['name']
                    x,y,w,h,offsetx,offsety = self.get_frame_sprite_data(frame)
                    if flip :
                        sprite = get_sprite(self.playersheet_img_flip, x, y, w, h,self.colorkey)
                    else :
                        sprite = get_sprite(self.playersheet_img, x, y, w, h,self.colorkey)
                    pygame.transform.scale(sprite, (w*self.scale, h*self.scale))
                    frame['sprite'] = sprite
                    #print(value)

    def init_player(self) :
       self.load_player_data_from_json()
       self.image = pygame.Surface((self.resolution['max_w']*self.scale*2, self.resolution['max_h']*self.scale))
       self.rect = self.image.get_rect()
       self.image.set_colorkey(self.colorkey)
       self.current_state = self.prev_state = self.first_frame
       self.load_player_frames()


    def reset_velocity(self) :
        self.velocity_x,self.velocity_y = 0,0

    def move(self) :
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y + self.velocity_z

    def check_event(self) :
        if self.K_SPACE:
            self.reset_velocity()
        else :
            if self.K_LEFT:
                self.velocity = -2
            elif self.K_RIGHT:
                self.velocity = 2
            if self.K_UP:
                self.velocity = -2
            elif self.K_DOWN:
                self.velocity = 2

    def set_state(self):
        states = ['idle','walk','attack','jump','hurt']
        for state in states :
            if state in self.current_state :
                self.state = state

    def set_direction(self):
      if 'right' in self.current_state :
          self.direction = 'right'
      else:  self.direction = 'left'

    def get_frame_rate(self) :
        frame_rate = self.frames_data[self.current_state][self.current_frame+1] #+1 to skip midbottm
        return frame_rate

    def get_nb_frame(self) :
        nb_frame = len(self.frames_data[self.current_state])-2 #less midbottom and flip
        return nb_frame

    def get_current_sprite(self) :
        sprite = self.frames_data[self.current_state][self.current_frame+1]['sprite'] #+1 to skip midbottom
        return sprite

    def animate(self):
        now = pygame.time.get_ticks()
        frame_rate = self.get_frame_rate()['frame_rate']
        nb_frames = self.get_nb_frame()
        if now - self.last_updated > 100*frame_rate:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1) % len(nb_frames)

        if self.current_frame == 0 :
            if 'attack'or 'jump'or 'hurt' in self.state :
                self.last_updated = now
                self.current_state = self.prev_state

        self.image =self.get_current_sprite()

    def update(self):
        self.reset_velocity()
        self.check_event() #check key press event
        self.move()
        self.set_state() #idle, move or attack
        self.set_direction() #left or right
        self.animate() #animate player by updating frame
