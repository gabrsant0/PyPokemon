import pygame
import config
import tile_manager
from player import Player
from game_state import gameState

class Map1():
    def __init__(self, screen, game):
        self.screen = screen        
        self.load() 
        self.game = game
        self.clock = pygame.time.Clock()


        self.tile_map = []
         
        self.center_x = int((config.SCREEN_HEIGHT / 32) / 2)
        self.center_x = int((config.SCREEN_WIDTH / 32) / 2)
        self.camera_speed = 5.3
        self.camera_is_mov_x = False
        self.camera_is_mov_y = False
        self.cam_x = 0
        self.cam_y = 0
        
        self.player = Player(screen, self.center_x, self.center_x)

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

        self.player.render(self.cam_x, self.cam_y)

        self.dt = self.clock.tick(config.FPS) / 1000


        self.set_camera()


    def set_camera(self):
        #print(eventkey)
        #print('pos x', self.player.pos_x, 'pos y', self.player.pos_y, 'camx', self.cam_x, 'camy', self.cam_y)
        
        if self.player.pos_x - self.cam_x > 20:
            self.cam_x += self.camera_speed * self.dt
        elif self.player.pos_x - self.cam_x < 4:
            self.cam_x -= self.camera_speed * self.dt

        if self.player.pos_y - self.cam_y < 4:
            self.cam_y -= self.camera_speed * self.dt
        elif self.player.pos_y - self.cam_y > 13:
            self.cam_y += self.camera_speed * self.dt


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.game_state = gameState.NONE

        #player mov
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.player_mov(0, (self.player.speed - (self.player.speed * 2)) * self.dt, 'top')
            self.set_camera()
        elif keys[pygame.K_s]:
            self.player.player_mov(0, self.player.speed * self.dt, 'bottom')
            self.set_camera()
        elif keys[pygame.K_d]:
            self.player.player_mov(self.player.speed * self.dt, 0, 'right')
            self.set_camera()
        elif keys[pygame.K_a]:
            self.player.player_mov((self.player.speed - (self.player.speed * 2)) * self.dt, 0, 'left')
            self.set_camera()


map_tile_set = {
    tile_manager.GRASS_TILE1: pygame.transform.scale(pygame.image.load("assets/tileset/grass1.png"), (config.TS, config.TS)),
    tile_manager.GRASS_TILE2: pygame.transform.scale(pygame.image.load("assets/tileset/grass2.jpg"), (config.TS, config.TS)),
    tile_manager.GRASS_TILE3: pygame.transform.scale(pygame.image.load("assets/tileset/grass3.jpg"), (config.TS, config.TS)),
    tile_manager.GRASS_TILE4: pygame.transform.scale(pygame.image.load("assets/tileset/grass4.jpg"), (config.TS, config.TS)),
    tile_manager.GRASS_TILE5: pygame.transform.scale(pygame.image.load("assets/tileset/grass5.jpg"), (config.TS, config.TS)),
}
