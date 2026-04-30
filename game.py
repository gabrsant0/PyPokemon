import pygame
import config
from game_state import gameState
from game_state import State
from menu import Menu
from map_1 import Map1
from map_editor import Map_Editor

class Game():
    def __init__(self, screen):
        self.screen = screen
        self.game_state = gameState.MAIN_MENU

        self.main_menu = Menu(screen)
        self.map_1 = Map1(screen)
        self.map_editor = Map_Editor(screen)
        

    def render(self):
        if self.game_state == gameState.MAP_1:
            self.map_1.render()
        elif self.game_state == gameState.MAIN_MENU:
            self.main_menu.render()
        elif self.game_state == gameState.MAP_EDITOR:
            self.map_editor.render()
        self.handle_Events()

    def load_map_editor(self):
        map_file = input("Please write the directory of the map \n")
        try:
            with open(map_file) as map_f:
                print('Map loaded')
                self.map_editor.load(map_file)
                self.game_state = gameState.MAP_EDITOR
        except:
            print("Error, this map directory does not exist.")

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
                    if event.key == pygame.K_e:
                        self.load_map_editor()
        elif self.game_state == gameState.MAP_EDITOR:
            self.map_editor.handle_events()
            
        elif self.game_state == gameState.MAP_1:
            self.map_1.handle_events()