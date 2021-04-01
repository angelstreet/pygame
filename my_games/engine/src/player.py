# AngelStreet @2021
####################################################
import pygame
from engine.src.gamesprite import GameSprite
from engine.src.utility import load_json, move_sprite, cartesian_to_iso, iso_to_cartesian


class _Player(GameSprite):
    def __init__(self, layer, json,  scale=1):
        GameSprite.__init__(self)
        self.json, self.layer = json, layer
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
        self._init_player()

    def _load_player_data_from_json(self):
        data = load_json(self.json)
        self.w = data['player']['sprite_w']
        self.h = data['player']['sprite_h']
        self.spritesheet_data = data['player']['spritesheet_list']
        self.colorkey = data['player']['colorkey']
        self.attributes = data['player']['attributes']
        self.first_frame = data['player']['first_frame']
        self.frames_data = data['player']['frames']
        if 'sound' in data['player']:
            self.sound_data = data['player']['sound']
        self.collision_losange = data['player']['collision_losange']

    def _get_frame_sprite_data(self, frame):
        return frame['x'], frame['y'], frame['offsetx'], frame['offsety']

    def _load_player_frames(self):
        # Create spritesheets
        self.spritesheet_list = {}
        for key, spritesheet in self.spritesheet_data.items():
            if spritesheet['colorkey']:
                self.spritesheet_list[key] = pygame.image.load(spritesheet['path']).convert()
                self.spritesheet_list[key].set_colorkey(spritesheet['colorkey'])
            else:
                self.spritesheet_list[key] = pygame.image.load(spritesheet['path']).convert_alpha()
            rect = self.spritesheet_list[key].get_rect()
            dimension = int(rect.width*self.scale), int(rect.height*self.scale)
            self.spritesheet_list[key] = pygame.transform.scale(
                self.spritesheet_list[key], dimension)
        # Create sprite for all animation frames
        dimension = int(self.w*self.scale), int(self.h*self.scale)
        for key, value in self.frames_data.items():
            for i, frame in enumerate(value):
                if i > 0 and isinstance(frame, dict):
                    spritesheet_id = str(frame['spritesheet'])
                    x, y, offsetx, offsety = [int(elt*self.scale)
                                              for elt in self._get_frame_sprite_data(frame)]
                    sprite = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32).convert_alpha()
                    sprite.blit(self.spritesheet_list[spritesheet_id],
                                (0, 0), (x, y, self.w, self.h))
                    sprite_flip = pygame.transform.flip(sprite, True, False)
                    frame['sprite'] = sprite
                    frame['sprite_flip'] = sprite_flip

    def _set_current_frame(self, frame):
        if self.current_frame != frame:
            self.prev_frame = self.current_frame
            self.current_frame = frame
            self.current_frame_id = 0

    def _set_state(self, state=False):
        if not self.current_state == state:
            if state:
                if self.current_state:
                    self.prev_state = self.current_state
                self.current_state = state
            else:
                states = ['idle', 'walk', 'run' 'attack', 'jump', 'fall', 'hurt']
                for state in states:
                    if state in self.current_frame:
                        if self.current_state:
                            self.prev_state = self.current_state
                        self.current_state = state
        self._set_frame()

    def _init_direction_from_frame(self):
        if "down" in self.current_frame:
            self.direction_v = "down"
        else:
            self.direction_v = "up"
        if "right" in self.current_frame:
            self.direction_h = "right"
        else:
            self.direction_h = "left"

    def _init_player(self):
        self._load_player_data_from_json()
        self.w = int(self.w*self.scale)
        self.h = int(self.h*self.scale)
        self.create_surface(self.w, self.h)
        if self.colorkey:
            self.image.set_colorkey(self.colorkey)
        self.prev_frame = None
        self.current_frame = self.first_frame
        self.last_collision_list = []
        self._init_direction_from_frame()
        self._init_collision_losange()
        self._set_state()
        self._set_frame()
        self._load_player_frames()
        self.get_collision_sprite()

    def _init_collision_losange(self):
        self.collision_losange_w = self.collision_losange["w"]*self.scale
        self.collision_losange_h = self.collision_losange["h"]*self.scale
        self.collision_losange_offsetx = self.collision_losange["offsetx"]*self.scale
        self.collision_losange_offsety = self.collision_losange["offsety"]*self.scale

    def _reset_velocity(self):
        self.velocity_x, self.velocity_y = 0, 0

    def move(self, x, y):
        move_sprite(self, self.rect.x + x, self.rect.y + y)

    def vsort_collision_list(self, sprite):
        if 'z' in dir(sprite):
            return sprite.z
        return 0

    def check_collision(self):
        if self.debug:
            self.blit_rear(self.collision_sprite.image,
                           (self.collision_sprite.x, self.collision_sprite.y))
        for c_sprite in self.last_collision_list:
            c_sprite.parent.remove_blend()
        self.last_collision_list = []
        c_left, c_right, c_up, c_down, c_top, c_bottom = 0, 0, 0, 0, 0, 0
        if len(self.collision_list) > 0:
            self.collision_list.sort(key=self.vsort_collision_list)
            for c_sprite in self.collision_list:
                if self.debug:
                    c_sprite.parent.blend((255, 0, 0))
                    self.last_collision_list.append(c_sprite)
                if self.current_state == 'fall' and abs(self.z-c_sprite.parent.z-c_sprite.parent.rect.height) < 4:
                    c_bottom = -1
                    self.velocity_x, self.velocity_y, self.velocity_z = 0, 0, 0
                    self._set_state("idle")
                    break
                if self.collision_sprite.rect.x < c_sprite.rect.x+c_sprite.rect.width/2:
                    c_right = -1
                else:
                    c_left = 1
                if self.collision_sprite.rect.y < c_sprite.rect.y+c_sprite.rect.height/2:
                    c_down = -1
                else:
                    c_up = 1
        self.collision_list = []
        return c_left, c_right, c_up, c_down, 0, 0

    def _move_player(self):
        c_left, c_right, c_up, c_down, c_top, c_bottom = self.check_collision()
        vx = self.velocity_x+(c_left+c_right)*self.velocity
        vy = self.velocity_y+(c_up+c_down)*self.velocity
        vz = self.velocity_z
        if vx != 0 and vy != 0:
            vx *= 0.8
        self.move(vx, vy+vz)
        if (self.current_state == 'jump' and self.velocity_z < 0):
            self.velocity_z = min(0, self.velocity_z+self.gravity)
            self.z += self.velocity_z
        elif(self.current_state == 'jump' and self.velocity_z == 0):
            self._set_state("fall")
        elif(self.current_state == 'fall'):
            self.velocity_z = max(self.jump_force, self.velocity_z+self.gravity)
            self.z += self.velocity_z
            if(self.velocity_z == -1*self.jump_force+self.gravity):
                self._set_state("idle")
                self.velocity_z = 0
                self.z = 0
                self._reset_velocity()

    def _attack(self):
        if 'attack' in self.sound_data:
            attack_sound = self.sound_data['attack']
            pygame.mixer.music.load(attack_sound)
            pygame.mixer.music.play()

    def _jump(self):
        self.z = 0
        self.velocity_z = self.jump_force
        if 'jump' in self.sound_data:
            jump_sound = self.sound_data['jump']
            pygame.mixer.music.load(jump_sound)
            pygame.mixer.music.play()

    def _fall(self):
        pass

    def _check_event(self):
        if self.K_RETURN:
            if not self.current_state in ('attack'):
                self._reset_velocity()
                self._set_state('attack')
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

    def _get_frame_rate(self):
        frame_rate = self.frames_data[self.current_frame][self.current_frame_id+1]['frame_rate']
        return frame_rate

    def _get_nb_frame(self):
        nb_frames = len(self.frames_data[self.current_frame])-1  # less midbottom and sprite
        return nb_frames

    def _animate(self):
        frame_rate = self._get_frame_rate()
        nb_frames = self._get_nb_frame()
        now = pygame.time.get_ticks()
        if now - self.last_updated > 100*frame_rate:
            self.last_updated = now
            self.current_frame_id += 1
            if self.current_frame_id == nb_frames:
                self.current_frame_id = 0
                if self.current_state in ('attack', 'hurt'):
                    self.last_updated = now
                    self._set_state('idle')
        self._display_current_sprite()

    # Public --------------------------------------------
    def update(self):
        self._check_event()  # check key press event
        self._move_player()
        self._animate()  # animate player by updating frame
        self.blits()

    def zsort(self):
        offsetx = (self.w-self.tile_w)/2
        offsety = (self.h-self.tile_h)/2
        isox = self.rect.x+offsetx+self.rect.width/2-self.map_x
        isoy = self.rect.y+offsety+self.rect.height-self.map_y
        x, y = iso_to_cartesian(isox, isoy)
        x = x - 60
        y = y - 10
        i = round(2*x/self.tile_w)
        j = round(y/(2*self.tile_h-self.tile_w))
        depth = int(200+i*100+1000*j-self.z-self.tile_h)
        return depth

    def is_moving(self):
        if self.velocity_x != 0 or self.velocity_y != 0 or self.velocity_z != 0:
            return True
        return False

    def center(self):
        self.get_collision_sprite()
        centerx = self.collision_sprite.rect.x + self.collision_sprite.rect.width/2
        centery = self.collision_sprite.rect.y + self.collision_sprite.rect.height/2
        return centerx, centery

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
        self.collision_sprite.y = self.rect.height-self.collision_sprite.rect.height+offsety
        self.collision_sprite.rect.x = self.rect.x+self.collision_sprite.x
        self.collision_sprite.rect.y = self.rect.y+self.rect.height-self.collision_sprite.y
        self.collision_sprite.parent = self
        return self.collision_sprite


class HorizontalPlayer(_Player):
    def __init__(self, layer, json, scale=1, force_right=False):
        self.force_right = force_right
        _Player.__init__(self, layer, json, scale)

    def _set_frame(self):
        self._set_current_frame("%s_right" % self.current_state)

    def _display_current_sprite(self):
        if self.direction_h == 'right':
            self.blit(self.frames_data[self.current_frame][self.current_frame_id + 1]['sprite'])
        elif not self.force_right:
            self.blit(self.frames_data[self.current_frame]
                      [self.current_frame_id + 1]['sprite_flip'])

    def _display_current_sprite(self):
        if self.direction_h == 'right' or self.force_right:
            self.blit(self.frames_data[self.current_frame][self.current_frame_id+1]['sprite'])
        else:
            self.blit(self.frames_data[self.current_frame][self.current_frame_id+1]['sprite_flip'])


class VerticalPlayer(_Player):
    def __init__(self, layer, json,  scale=1, force_up=False):
        self.force_up = force_up
        _Player.__init__(self, layer, json, scale)

    def _set_frame(self):
        if self.force_up:
            self._set_current_frame("%s_up" % self.current_state)
        else:
            self._set_current_frame("%s_%s" % (self.current_state, self.direction_v))

    def _display_current_sprite(self):
        if self.direction_h == 'right':
            self.blit(self.frames_data[self.current_frame][self.current_frame_id+1]['sprite'])
        else:
            self.blit(self.frames_data[self.current_frame][self.current_frame_id+1]['sprite_flip'])


class FourDirPlayer(_Player):
    def __init__(self, layer, json, scale=1):
        _Player.__init__(self, layer, json, scale)
        self.map_x, self.map_y = 0, 0
        self.tile_w, self.tile_h = 60, 60

    def set_tilemap(self, map_x, map_y, tile_w, tile_h):
        self.map_x, self.map_y = map_x, map_y
        self.tile_w, self.tile_h = tile_w, tile_h

    def _set_frame(self):
        if self.direction_h == 'right':
            self._set_current_frame("%s_right" % self.current_state)
        elif self.direction_v == 'up':
            self._set_current_frame("%s_up" % self.current_state)
        elif self.direction_v == 'down':
            self._set_current_frame("%s_down" % self.current_state)

    def _display_current_sprite(self):
        if self.direction_h == 'left':
            self.blit(self.frames_data[self.current_frame][self.current_frame_id+1]['sprite_flip'])
        else:
            self.blit(self.frames_data[self.current_frame][self.current_frame_id+1]['sprite'])

    def _check_event(self):
        if self.K_RETURN:
            if not self.current_state in ('attack'):
                self._reset_velocity()
                self._set_state('attack')
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
                    self.direction_v = None
                self._set_state('walk')
            elif self.K_RIGHT:
                self.velocity_x = self.velocity
                if self.direction_h != 'right':
                    self.direction_h = 'right'
                    self.current_frame_id = 0
                    self.direction_v = None
                self._set_state('walk')
            if self.K_UP:
                self.velocity_y = -self.velocity
                if self.direction_v != 'up':
                    self.direction_v = 'up'
                    self.current_frame_id = 0
                    self.direction_h = None
                self._set_state('walk')
            elif self.K_DOWN:
                self.velocity_y = self.velocity
                if self.direction_v != 'down':
                    self.direction_v = 'down'
                    self.current_frame_id = 0
                    self.direction_h = None
                self._set_state('walk')
            if not (self.K_LEFT or self.K_RIGHT):
                self.velocity_x = 0
            if not (self.K_UP or self.K_DOWN):
                self.velocity_y = 0
            if not (self.K_LEFT or self.K_RIGHT or self.K_UP or self.K_DOWN):
                self._set_state('idle')

class FourDirIsoPlayer(_Player):
    def __init__(self, layer, json, scale=1):
        _Player.__init__(self, layer, json, scale)
        self.map_x, self.map_y = 0, 0
        self.tile_w, self.tile_h = 60, 60

    def set_tilemap(self, map_x, map_y, tile_w, tile_h):
        self.map_x, self.map_y = map_x, map_y
        self.tile_w, self.tile_h = tile_w, tile_h

    def _set_frame(self):
        self._set_current_frame("%s_right_%s" % (self.current_state, self.direction_v))

    def _display_current_sprite(self):
        if self.direction_h == 'right':
            self.blit(self.frames_data[self.current_frame][self.current_frame_id+1]['sprite'])
        else:
            self.blit(self.frames_data[self.current_frame][self.current_frame_id+1]['sprite_flip'])


class HeightDirPlayer(_Player):
    def __init__(self, layer, json,  scale=1):
        _Player.__init__(self, layer, json, scale)

    def set_tilemap(self, map_x, map_y, tile_w, tile_h):
        self.map_x, self.map_y = map_x, map_y
        self.tile_w, self.tile_h = tile_w, tile_h

    def _set_frame(self):
        self._set_current_frame("%s_%s" % (self.current_state, self.direction_v))

    def _display_current_sprite(self):
        if self.direction_h == 'right':
            self.blit(self.frames_data[self.current_frame][self.current_frame_id+1]['sprite'])
        else:
            self.blit(self.frames_data[self.current_frame][self.current_frame_id+1]['sprite_flip'])
