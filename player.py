import pygame
import config

class Player():
    def __init__(self, screen, x, y):
        self.sprite = pygame.transform.scale(pygame.image.load("assets/menu_assets/menuimgv2.png"), (config.TS, config.TS))
        self.pos_x = x
        self.pos_y = y
        self.rect = pygame.Rect(self.pos_x * config.TS, self.pos_y * config.TS, config.TS, config.TS)
        self.screen = screen

    def render(self):
        self.screen.blit(self.sprite, self.rect)

    def player_mov(self, x, y):
        print(x, y)
        print(self.pos_x)
    