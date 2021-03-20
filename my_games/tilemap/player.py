import pygame
from spritesheet import Spritesheet

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

   def init_player :
       self.load_player_data_from_json()
       self.image = pygame.Surface((resolution[0]*self.scale, resolution[1]*self.scale))
       self.rect = self.image.get_rect()
       self.image.set_colorkey(colorkey)
       self.current_state = self.prev_state = self.first_frame
       self.playersheet_img = pygame.image.load(playersheet_name).convert_alpha()
       #self.playersheet_img_flip = self


    def reset_velocity() :
        self.velocity_x,self.velocity_y = 0,0

    def move() :
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y + self.velocity_z

    def check_event() :
        if self.K_SPACE:
            self.reset_velocity()
        else :
            if self.K_LEFT:
                self.velocity = -2
            elif self.K_RIGHT:
                self.velocity = 2
            if self.KEYUP:
                self.velocity = -2
            elif self.K_DOWN:
                self.velocity = 2


    def set_state(self):
        self.state = ' idle'
        if self.velocity > 0:
            self.state = 'moving right'
        elif self.velocity < 0:
            self.state = 'moving left'

    def get_frame(self,state,frame) :
        frame = self.frames_data[state][frame+1]
        return frame

    def animate(self):
        now = pygame.time.get_ticks()
        frame_rate = get_frame(self.current_state,self.current_frame)['frame_rate']
        if now - self.last_updated > 200:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames_left)

        if self.current_frame = 0 :
            if self.isAttacking or self.isJumping or self.isHurt :
                self.last_updated = now
                self.current_state = self.prev_state


    def update(self):
        self.reset_velocity()
        self.check_event()
        self.move()
        self.check_state()
        self.animate()


    def load_frames(self):
        my_spritesheet = Spritesheet('poppy_sheet.png')
        #pygame.image.load('MY_IMAGE_NAME.png').convert()
        self.idle_frames_left = [my_spritesheet.parse_sprite("poppy_idle1.png"),
                                 my_spritesheet.parse_sprite("poppy_idle2.png")]
        self.walking_frames_left = [my_spritesheet.parse_sprite("poppywalk1.png"), my_spritesheet.parse_sprite("poppywalk2.png"),
                           my_spritesheet.parse_sprite("poppywalk3.png"), my_spritesheet.parse_sprite("poppywalk4.png"),
                           my_spritesheet.parse_sprite("poppywalk5.png"), my_spritesheet.parse_sprite("poppywalk6.png"),
                           my_spritesheet.parse_sprite("poppywalk7.png"), my_spritesheet.parse_sprite("poppywalk8.png")]
        self.idle_frames_right = []
        for frame in self.idle_frames_left:
            self.idle_frames_right.append( pygame.transform.flip(frame,True, False) )
        self.walking_frames_right = []
        for frame in self.walking_frames_left:
            self.walking_frames_right.append(pygame.transform.flip(frame, True, False))
