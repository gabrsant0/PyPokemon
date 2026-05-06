import pygame
import config
import map.tile_manager as tile_manager
from game_state import gameState
from utilities.collision import Collision

class Map1():
    def __init__(self, screen, game, Player):
        self.screen = screen        
        self.load() 
        self.game = game
        self.clock = pygame.time.Clock()

        self.tile_map = []
         
        self.camera_speed = 5.3
        self.cam_x = 0
        self.cam_y = 0
        
        self.player = Player(screen, (config.SCREEN_WIDTH / 32) / 2, (config.SCREEN_HEIGHT / 32) / 2)
        self.collision_check = Collision(self.screen, self)
        self.collision_rect_x = 400
        self.collision_rect_y = 200
        self.rect_col1 = pygame.Rect(self.collision_rect_x, self.collision_rect_y, 32, 32) 
        self.rect_shape = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.coliders = [self.rect_col1]
        self.collision_check.check_collision()   

    def load(self):
        self.tile_map_group = []
        self.tile_map = []
        self.tile_map_group.append(self.tile_map)

        tile_map_count = 0

        with open('map/map1.txt') as map_file:
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

    def render(self):
        self.screen.fill((0, 0, 0))
        
        for y in range(len(self.tile_map_group) - 1):
            for x in range(len(self.tile_map_group[y]) - 1):
                rect = pygame.Rect((config.TS * x) - (self.cam_x * config.TS), 
                (config.TS * y) - (self.cam_y) * config.TS, 
                config.TS, config.TS)
                if self.tile_map_group[y][x] in map_tile_set:
                    self.screen.blit(map_tile_set[self.tile_map_group[y][x]], rect)

        for colider in self.coliders:
            colider.x = self.collision_rect_x - (config.TS * self.cam_x)
            colider.y = self.collision_rect_y - (config.TS * self.cam_y)

        self.player.render(self.cam_x, self.cam_y)

        self.dt = self.clock.tick(config.FPS) / 1000

        #collision block
        #pygame.draw.rect(self.screen, (255, 255, 255), self.rect_col2, 1)

        self.collision_check.update()
        self.set_camera()

    def check_coliders(self):
        pass

    def set_camera(self):        
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
            if self.collision_check.check_collision(self.player.rect, 'top', 1) == True:
                self.player.player_mov(0, -1, self.dt, 'top')
            #while col = none if col == true:
        elif keys[pygame.K_s]:
            if self.collision_check.check_collision(self.player.rect, 'down', 1) == True:
                self.player.player_mov(0, 1, self.dt, 'bottom')
        elif keys[pygame.K_d]:
            if self.collision_check.check_collision(self.player.rect, 'right', 1) == True:
                self.player.player_mov(1, 0, self.dt, 'right')
        elif keys[pygame.K_a]:
            if self.collision_check.check_collision(self.player.rect, 'left', 1) == True:
                self.player.player_mov(-1, 0, self.dt, 'left')


map_tile_set = {
    tile_manager.GRASS_TILE1: pygame.transform.scale(pygame.image.load("assets/tileset/grass1.png"), (config.TS, config.TS)),
    tile_manager.GRASS_TILE2: pygame.transform.scale(pygame.image.load("assets/tileset/grass2.jpg"), (config.TS, config.TS)),
    tile_manager.GRASS_TILE3: pygame.transform.scale(pygame.image.load("assets/tileset/grass3.jpg"), (config.TS, config.TS)),
    tile_manager.GRASS_TILE4: pygame.transform.scale(pygame.image.load("assets/tileset/grass4.jpg"), (config.TS, config.TS)),
    tile_manager.GRASS_TILE5: pygame.transform.scale(pygame.image.load("assets/tileset/grass5.jpg"), (config.TS, config.TS)),
}
