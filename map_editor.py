import pygame
import config
import tile_manager
from game_state import gameState

class Map_Editor():
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game

        self.cx = 5
        self.cy = 5

        self.x_line = int(config.SCREEN_WIDTH / config.TS)
        self.y_line = int(config.SCREEN_HEIGHT / config.TS)

        self.tile_map = []

        self.rect = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.map = 'grid/maptest.txt'
        self.selected_sprite = 'G'

        self.cam_x = 0
        self.cam_y = 0

        self.debug_sprite = True

    def check_valid_map(self, map):
        with open(self.map, 'r') as map_file:
            step = 2
            for line in map_file:
                print('line', line)
                for char in line:
                    if step % 2 == 0 and char == ' ':
                        return False, print("The Map is invalid. Please select one valid or create a new txt file.") 
                    else:
                        step += 1
            return True


    def load(self, map_to_load):
        self.map = map_to_load
        with open(self.map, 'r') as map_file:
            for y in range(self.y_line):
                tile_map_1 = []
                self.tile_map.append(tile_map_1)
                lines = map_file.readline()
                if len(lines) < (self.x_line * 2) - 1: #check if the map has enough characters for the whole grid, if not, rewrite the map
                    print("error, there's less map tiles than should on the screen")
                    for x in range(self.x_line + 1): #append the new map into the array
                        if self.x_line + 1 == x + 1:
                            self.tile_map[y].append("E")
                            continue
                        self.tile_map[y].append('N')
                else: #if the map is valid append it to the array
                    step = 2
                    for char in lines:
                        if step % 2 == 0:
                            self.tile_map[y].append(char)
                            step += 1
                        else:
                            step += 1
        self.write_map()

    def rndm(self):
        pass

    def update_map_x(self):
        for y in range(len(self.tile_map)):
            print("array len", len(self.tile_map[y]), 'self x line', self.x_line, 'self cam', self.cam_x)
            if len(self.tile_map[y]) < self.x_line + self.cam_x:
                self.tile_map[y][len(self.tile_map[y]) - 1] = 'N'
                self.tile_map[y].append('E')
        for y in range(self.y_line + self.cam_y):
            if len(self.tile_map) < self.y_line + self.cam_y and y >= len(self.tile_map):
                new_tile_x = []
                self.tile_map.append(new_tile_x)
                for x in range(self.x_line + self.cam_x + 1):
                    if self.x_line + self.cam_x == x:
                        self.tile_map[y].append('E')
                        continue
                    self.tile_map[y].append('N')

        self.write_map()

    def update_map(self): #the open map is unecessary, the map itself is one array, the map is already loaded. Is easier to predict the map size 
        #with array than opening the map and reading it again and trying to modify it.
        with open(self.map, 'r') as map_file:
            for y in range(self.y_line + self.cam_y): #range(self.cam_y, self.y_line + self.cam_y, 1
                lines = map_file.readline()
                if len(lines) < self.x_line:
                    new_tile_x = []
                    self.tile_map.append(new_tile_x)
                    for x in range(self.x_line + 1):
                        if self.x_line + 1 == x + 1:
                            self.tile_map[y].append('E')
                            continue
                        self.tile_map[y].append('N')
        self.write_map()


    def write_map(self):
        with open(self.map, 'w') as map_file: #write the tilme map array into the txt file
            for y in range(len(self.tile_map)):
                string_line = ''
                for x in self.tile_map[y]:
                    string_line += x
                    if x != 'E':
                        string_line += " "
                map_file.write(string_line + '\n')

    def render(self):
        self.screen.fill(config.BLACK)

        self.cam_rect = [self.cam_x * config.TS, self.cam_y * config.TS]

        #draw tiles
        for y in range(len(self.tile_map)):
            for x in range(len(self.tile_map[y])):
                if self.tile_map[y][x] in map_tile_set:
                    self.screen.blit(map_tile_set[self.tile_map[y][x]], ((x * config.TS) - self.cam_rect[0], (y * config.TS) - self.cam_rect[1]))
                elif self.debug_sprite == True:
                    pygame.draw.rect(self.screen, (255, 255, 255), ((x * config.TS) - self.cam_rect[0], (y * config.TS) - self.cam_rect[1], 
                    config.TS, config.TS), 1)

        #main control
        self.screen.blit(map_tile_set[self.selected_sprite], ((self.cx * config.TS) - self.cam_rect[0], (self.cy * config.TS) - self.cam_rect[1]))

        pygame.draw.rect(self.screen, (255, 255, 255), ((self.cx * config.TS) - self.cam_rect[0], (self.cy * config.TS) - self.cam_rect[1], 
        config.TS, config.TS), 1)


        self.screen.blit(self.rect, (0, 0))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.game_state = gameState.NONE
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if self.cy - 1 < self.cam_y:
                        return
                    self.cy -= 1
                elif event.key == pygame.K_s:
                    if self.cy + 1 > self.cam_y + self.y_line:
                        return
                    self.cy += 1
                elif event.key == pygame.K_d:
                    self.cx += 1
                elif event.key == pygame.K_a:
                    self.cx -= 1


                #camera mov
                elif event.key == pygame.K_UP:
                    print(self.cy, self.cam_y)
                    if self.cam_y - 1 < 0:
                        return
                    elif self.cy - self.cam_y > self.y_line - 1:
                        return
                    self.cam_y -= 1
                elif event.key == pygame.K_DOWN:
                    if self.cy - self.cam_y - 1 < 0:
                        return
                    self.cam_y += 1
                    self.update_map_x()
                elif event.key == pygame.K_RIGHT:
                    self.cam_x += 1
                    self.update_map_x()
                elif event.key == pygame.K_LEFT:
                    if self.cam_x - 1 < 0:
                        return
                    self.cam_x -= 1


                #place sprite
                elif event.key == pygame.K_RETURN:
                    self.tile_map[self.cy][self.cx] = self.selected_sprite
                    self.write_map()
                elif event.key == pygame.K_e:
                    self.tile_map[self.cy][self.cx] = "N"
                    self.write_map()


                #chgange sprites
                elif event.key == pygame.K_1:
                    self.selected_sprite = 'G'
                elif event.key == pygame.K_2:
                    self.selected_sprite = '2'
                elif event.key == pygame.K_3:
                    self.selected_sprite = '3'

map_tile_set = { 
    tile_manager.GRASS_TILE1: pygame.transform.scale(pygame.image.load("assets/tileset/grass1.png"), (config.TS, config.TS)),
    tile_manager.GRASS_TILE2: pygame.transform.scale(pygame.image.load("assets/tileset/grass2.jpg"), (config.TS, config.TS)),
    tile_manager.GRASS_TILE3: pygame.transform.scale(pygame.image.load("assets/tileset/grass3.jpg"), (config.TS, config.TS)),
    tile_manager.GRASS_TILE4: pygame.transform.scale(pygame.image.load("assets/tileset/grass4.jpg"), (config.TS, config.TS)),
    tile_manager.GRASS_TILE5: pygame.transform.scale(pygame.image.load("assets/tileset/grass5.jpg"), (config.TS, config.TS))
}