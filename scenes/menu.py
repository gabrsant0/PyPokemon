import pygame
import config

class Menu():
    def __init__(self, screen):
        self.menu_img = pygame.image.load("assets/menu_assets/menuimg.png")
        self.menu_img_rect = pygame.Rect(1, 1, 1, 2)
        self.menu_img = pygame.transform.scale(self.menu_img, (800, 600))
        self.screen = screen
        print("screen menu", id(self.screen), "screen og", id(self.screen))

    def render(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.menu_img, self.menu_img_rect)
        