import pygame
import config
from map.editor import Map_Editor

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

pygame.display.set_caption("Map Editor")

clock = pygame.time.Clock()

editor = Map_Editor(screen)
editor.load('map/map1.txt')


while editor.running == True:
    editor.render()
    editor.handle_events()

    clock.tick(config.FPS)
    
    pygame.display.flip()
