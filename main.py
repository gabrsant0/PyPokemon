import pygame
import config
from game import Game
from game_state import State

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

pygame.display.set_caption("Py Poke!")

clock = pygame.time.Clock()

game = Game(screen)

state = State.RUNNING

while state is not State.NONE:
    game.render()
    clock.tick(config.FPS)
    
    pygame.display.flip()

    if game.game_state == game.game_state.NONE:
        state = State.NONE