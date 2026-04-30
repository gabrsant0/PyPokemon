import pygame
import config
import tile_manager
from player import Player
from game_state import gameState

class Map1():
    def __init__(self, screen, game):
        self.screen = screen        

        self.tile_map = []

        self.load() 
        self.game = game
         
        self.cam_x = int((config.SCREEN_WIDTH / config.TS) / 2)
        self.cam_y = int(((config.SCREEN_WIDTH / config.TS) / 2) - 4)
        self.player = Player(screen, self.cam_x, self.cam_y)

    def load(self):
        self.tile_map_group = []
        self.tile_map = []
        self.tile_map_group.append(self.tile_map)

        tile_map_count = 0

        with open('grid/map1.txt') as map_file:
            content = map_file.read()
            step = 2
            for tile in content:
                if step % 2 == 0:
                    if tile == 'E':
                        self.tile_map_2 = []
                        self.tile_map_group.append(self.tile_map_2)
                        tile_map_count += 1
                    else:
                        self.tile_map_group[tile_map_count].append(tile)
                step += 1

    def update(self):
        pass

    def render(self):
        self.screen.fill((0, 0, 0))
        
        for y in range(len(self.tile_map_group) - 1):
            for x in range(len(self.tile_map_group[y]) - 1):
                if self.tile_map_group[y][x] in map_tile_set:
                    self.screen.blit(map_tile_set[self.tile_map_group[y][x]], 
                ((config.TS * x) - (self.cam_x * config.TS), 
                (config.TS * y) - (self.cam_y) * config.TS, 
                config.TS, config.TS))

        self.player.render()
      
    def set_camera(self):
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.game_state = gameState.NONE
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player.player_mov(0, -1)
                    self.cam_y -= 1
                elif event.key == pygame.K_s:
                    self.player.player_mov(0, 1)
                    self.cam_y += 1
                elif event.key == pygame.K_d:
                    self.player.player_mov(1, 0)
                    self.cam_x += 1
                elif event.key == pygame.K_a:
                    self.player.player_mov(-1, 0)
                    self.cam_x -= 1

map_tile_set = {
    tile_manager.GRASS_TILE1: pygame.transform.scale(pygame.image.load("assets/tileset/grass1.png"), (config.TS, config.TS)),
    tile_manager.GRASS_TILE2: pygame.transform.scale(pygame.image.load("assets/tileset/grass2.jpg"), (config.TS, config.TS)),
    tile_manager.GRASS_TILE3: pygame.transform.scale(pygame.image.load("assets/tileset/grass3.jpg"), (config.TS, config.TS)),
    tile_manager.GRASS_TILE4: pygame.transform.scale(pygame.image.load("assets/tileset/grass4.jpg"), (config.TS, config.TS)),
    tile_manager.GRASS_TILE5: pygame.transform.scale(pygame.image.load("assets/tileset/grass5.jpg"), (config.TS, config.TS)),
}
