import pygame
import config

class Rigidbody():
    def __init__(self, body, rect):
        self.shape_rect = rect
        self.shape = pygame.Surface((1, 1), pygame.SRCALPHA)
        pass

    def update(self, rect):
        self.shape_rect = rect

    def rigidbody_rect(self):
        pass

    def draw_shape(self, screen):
        pygame.draw.rect(screen, (255), self.shape_rect, 1)

class Collision():
    def __init__(self, screen = None, instance = None):
        self.instance = instance
        self.screen = screen

        self.debug = True
        self.shape_rect = None
        self.shape = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.w = 32
        self.h = 32

        self.next_sprite = config.TS

        self.body_x = -200
        self.body_y = -900
        self.body_y_half = -900
        self.body_y_end = -900
        self.body_x_half = -900
        self.body_x_end = -900

    def draw_shape(self, x, y, w, h):
        self.w = w
        self.h = h
        self.shape_rect = pygame.Rect(x, y, w, h)
        self.shape_rect

    def update(self):
        for colider in self.instance.coliders: #self.valid_coliders (it returns all the coliders that are in the screen)          
            colider_end = colider.y + colider.height  
            pygame.draw.rect(self.screen, (255, 255, 255), (colider.x, colider.y, 32, 2), 1)
            pygame.draw.rect(self.screen, (255, 255, 255), (colider.x, colider_end, 32, 2), 1)

            pygame.draw.rect(self.screen, (255, 255, 255), (self.body_x, self.body_y, 2, 54), 1)
            pygame.draw.rect(self.screen, (255, 255, 255), (self.body_x_half, self.body_y, 2, 54), 1)
            pygame.draw.rect(self.screen, (255, 255, 255), (self.body_x_end, self.body_y, 2, 54), 1)

            pygame.draw.rect(self.screen, (255, 255, 255), (self.body_x, self.body_y, 32, 2), 1)
            pygame.draw.rect(self.screen, (255, 255, 255), (self.body_x, self.body_y_half, 32, 2), 1)
            pygame.draw.rect(self.screen, (255, 255, 255), (self.body_x, self.body_y_end, 32, 2), 1)
        
    def check_collision(self, rect = (0, 0, 0, 0), dir = '', speed = 0, body = None) -> bool: #need to send the rect of player

        direction = dir
        body_rect = pygame.Rect(rect)

        self.body_x = body_rect.x
        self.body_y = body_rect.y
        self.body_x_half = body_rect.x + int(body_rect.w / 2)
        self.body_x_end = body_rect.x + body_rect.w
        self.body_y_half = body_rect.y + int(body_rect.h / 2)
        self.body_y_end = body_rect.y + body_rect.h

        next_pos = 0

        if dir == 'right':
            next_pos = body_rect.x + 32
        elif dir == 'left':
            next_pos = body_rect.x - 32
        elif dir == 'down':
            next_pos = body_rect.y + 54
        else:
            next_pos = body_rect.y - 32

        for colider in self.instance.coliders: #self.valid_coliders (it returns all the coliders that are in the screen)    
            colider_y_end = colider.y + colider.height
            colider_x_end = colider.x + colider.width

            if direction == 'right':                
                if body_rect.x < colider.x and next_pos >= colider.x: #the logic checks which line hits the colider
                    if self.body_y >= colider.y and self.body_y <= colider_y_end:
                        return False
                    elif self.body_y_half >= colider.y and self.body_y <= colider_y_end:
                        return False
                    elif self.body_y_end <= colider_y_end and self.body_y_end >= colider.y:
                        return False
    
            elif direction == 'left': 
                if colider.x < body_rect.x and next_pos <= colider.x:
                    if self.body_y >= colider.y and self.body_y <= colider_y_end:
                        return False
                    elif self.body_y_half >= colider.y and self.body_y_half <= colider_y_end:
                        return False
                    elif self.body_y_end <= colider_y_end and self.body_y_end >= colider.y:
                        return False
                    
            elif direction == 'down':
                if self.body_y <= colider.y and next_pos >= colider.y:
                    if self.body_x >= colider.x and self.body_x <= colider_x_end:
                        return False
                    elif self.body_x_half >= colider.x and self.body_x_half <= colider_x_end:
                        return False
                    elif self.body_x_end >= colider.x and self.body_x_end <= colider_x_end:
                        return False
                    
            else:
                if colider.y <= body_rect.y and next_pos <= colider.y:
                    if self.body_x >= colider.x and self.body_x <= colider_x_end:
                        return False
                    elif self.body_x_half >= colider.x and self.body_x_half <= colider_x_end:
                        return False
                    elif self.body_x_end >= colider.x and self.body_x_end <= colider_x_end:
                        return False
                    
        return True
        