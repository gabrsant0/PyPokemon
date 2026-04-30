import pygame
import config
import tile_manager

class Map_Editor():
    def __init__(self, screen):
        self.screen = screen

        self.cx = 5
        self.cy = 5

        self.tile_size = 32
        self.x_line = int(config.SCREEN_WIDTH / self.tile_size)
        self.y_line = int(config.SCREEN_HEIGHT / self.tile_size)

        self.tile_map = []

        self.rect = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.map = 'grid/maptest.txt'
        self.selected_sprite = 'G'

        self.cam_x = int(self.x_line / 2)
        self.cam_y = int((self.y_line / 2) - 4)

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

    def update_map(self):
        with open(self.map, 'r') as map_file:
            for y in range(self.y_line + self.cam_y):
                lines = map_file.readline()
                if len(lines) < self.x_line:
                    current_y = len(self.tile_map)
                    new_tile_x = []
                    self.tile_map.append(new_tile_x)
                    for x in range(self.x_line + 1):
                        if self.x_line + 1 == x + 1:
                            self.tile_map[current_y].append('E')
                            continue
                        self.tile_map[current_y].append('N')
        print("cam y", self.cam_y, "tile map len", len(self.tile_map))
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

        #draw tiles
        for y in range(len(self.tile_map)):
            for x in range(len(self.tile_map[y])):
                if self.tile_map[y][x] in map_tile_set:
                    self.screen.blit(map_tile_set[self.tile_map[y][x]], (x * 32, (y * 32) - (self.cam_y * 32)))
                else:
                    pass
                    #pygame.draw.rect(self.screen, (255, 255, 255), (x * 32, (y * 32) - (self.cam_y * 32), 32, 32), 1)

        #draw squares
        #for y in range(self.y_line):
            #for x in range(self.x_line):
                #pygame.draw.rect(self.screen, (255, 255, 255), (self.tile_size * x, self.tile_size * y, 32, 32), 1)

        self.screen.blit(map_tile_set[self.selected_sprite], (self.cx * 32, (self.cy * 32) - (self.cam_y * 32)))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.cx * 32, (self.cy * 32) - (self.cam_y * 32), 32, 32), 1)


        self.screen.blit(self.rect, (0, 0))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
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
                    self.update_map()
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
    tile_manager.GRASS_TILE1: pygame.transform.scale(pygame.image.load("assets/tileset/grass1.png"), (32, 32)),
    tile_manager.GRASS_TILE2: pygame.transform.scale(pygame.image.load("assets/tileset/grass2.jpg"), (32, 32)),
    tile_manager.GRASS_TILE3: pygame.transform.scale(pygame.image.load("assets/tileset/grass3.jpg"), (32, 32)),
    tile_manager.GRASS_TILE4: pygame.transform.scale(pygame.image.load("assets/tileset/grass4.jpg"), (32, 32)),
    tile_manager.GRASS_TILE5: pygame.transform.scale(pygame.image.load("assets/tileset/grass5.jpg"), (32, 32))
}