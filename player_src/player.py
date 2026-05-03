import pygame
import config
import player_src.player_sprite as sprite
from utilities.timer import Timer

class Player():
    def __init__(self, screen, x, y):
        #self.player_command = {        }

        self.sprite_states = [ 0,
            sprite.player_sprite_settings['size_x'] / 3,
            sprite.player_sprite_settings['size_x'] - (sprite.player_sprite_settings['size_x'] / 3)
        ] #sequence between the first, the second and the third sprite of the sprite sheet
        print(self.sprite_states)
        self.current_anim = 0

        self.walking = False

        self.sprite = sprite.sprite_sheet['bottom'].subsurface((0, 0), (32, sprite.player_sprite_settings['size_y']))
        self.sprite.convert_alpha()
        self.update_animation()
        

        self.speed = 15.3
        self.pos_x = x
        self.pos_y = y
        self.screen = screen

        self.timer = Timer()

    def render(self, cam_x, cam_y):
        self.screen.blit(self.sprite, ((self.pos_x * config.TS) - (cam_x * config.TS), (self.pos_y * config.TS) - (cam_y * config.TS), 
        config.TS, config.TS))
        
        self.timer.update()

    def update_animation(self):
        if self.current_anim >= 2:
                self.current_anim = 0
        else:
            self.current_anim += 1

        self.directions = {
            'left':sprite.sprite_sheet['left'].subsurface((self.sprite_states[self.current_anim], 0), (32, sprite.player_sprite_settings['size_y'])),
            'right':sprite.sprite_sheet['right'].subsurface((self.sprite_states[self.current_anim], 0), (32, sprite.player_sprite_settings['size_y'])),
            'top':sprite.sprite_sheet['top'].subsurface((self.sprite_states[self.current_anim], 0), (32, sprite.player_sprite_settings['size_y'])),
            'bottom':sprite.sprite_sheet['bottom'].subsurface((self.sprite_states[self.current_anim], 0), (32, sprite.player_sprite_settings['size_y']))
        }

    def walking_anim(self):
        self.walking = False

    def player_mov(self, x, y, set_direction):
        if self.walking == False:
            self.walking = True 

            self.timer.start(100, self.walking_anim)

            self.update_animation()
            
            self.sprite = self.directions[set_direction]
            self.pos_x += x
            self.pos_y += y
    