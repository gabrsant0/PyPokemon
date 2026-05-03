import pygame
import config
from game_state import gameState
from game_state import State
from scenes.menu import Menu
from scenes.map_1 import Map1
from player_src.player import Player

class Game():
    def __init__(self, screen):
        self.screen = screen
        self.game_state = gameState.MAIN_MENU

        self.main_menu = Menu(screen)
        self.map_1 = Map1(screen, self, Player)        

    def render(self):
        if self.game_state == gameState.MAP_1:
            self.map_1.render()
        elif self.game_state == gameState.MAIN_MENU:
            self.main_menu.render()
        elif self.game_state == gameState.MAP_EDITOR:
            self.map_editor.render()
        self.handle_Events()

    def handle_Events(self):
        if self.game_state == gameState.MAIN_MENU:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = gameState.NONE
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.game_state = gameState.NONE
                    if event.key == pygame.K_m:
                        self.game_state = gameState.MAIN_MENU
                    if event.key == pygame.K_RETURN:
                        self.game_state = gameState.MAP_1
        elif self.game_state == gameState.MAP_1:
            self.map_1.handle_events()