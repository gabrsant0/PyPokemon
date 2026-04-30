import pygame
import math
import random
from dataclasses import dataclass

pygame.init()

WIDTH, HEIGHT = 960, 640
HALF_H = HEIGHT // 2
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fake 3D Dungeon Crawler - Raycast Demo")
clock = pygame.time.Clock()

# Colors
BLACK = (5, 5, 8)
WHITE = (235, 235, 235)
GRAY = (90, 90, 100)
DARK_GRAY = (35, 35, 45)
RED = (220, 70, 70)
GREEN = (80, 220, 120)
BLUE = (80, 160, 255)
YELLOW = (240, 210, 80)
PURPLE = (170, 90, 220)
BROWN = (115, 78, 46)
FLOOR = (42, 36, 34)
CEILING = (16, 17, 28)

font_big = pygame.font.SysFont(None, 74)
font_med = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 24)

TILE = 64
FOV = math.radians(66)
NUM_RAYS = 240
MAX_DEPTH = 900
DELTA_ANGLE = FOV / NUM_RAYS
PROJ_DIST = (WIDTH / 2) / math.tan(FOV / 2)
SCALE = WIDTH // NUM_RAYS

# Map legend:
# # = wall
# . = floor
# D = closed door
# E = exit stairs
# P = player start
# M = monster
# T = treasure
DUNGEON_MAP = [
    "################",
    "#P....#........#",
    "#.##..#..####..#",
    "#..#.....#..#..#",
    "##.#####.#..#..#",
    "#......#.#..#..#",
    "#..T...D....#..#",
    "#......###..#..#",
    "####.#......#..#",
    "#....#.####.#..#",
    "#.####.#....#..#",
    "#......#..M....#",
    "#..######.######",
    "#..M...........#",
    "#.......T...E..#",
    "################",
]

MAP_H = len(DUNGEON_MAP)
MAP_W = len(DUNGEON_MAP[0])


@dataclass
class Monster:
    x: float
    y: float
    hp: int = 3
    cooldown: int = 0


@dataclass
class Treasure:
    x: float
    y: float
    taken: bool = False


class Game:
    def __init__(self):
        self.state = "menu"
        self.reset()

    def reset(self):
        self.grid = [list(row) for row in DUNGEON_MAP]
        self.monsters = []
        self.treasures = []
        self.message = "Find the exit stairs. Beware the dungeon beasts."
        self.message_timer = 180
        self.hp = 6
        self.score = 0
        self.attack_cooldown = 0
        self.win = False

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                wx = x * TILE + TILE / 2
                wy = y * TILE + TILE / 2
                if cell == "P":
                    self.player_x = wx
                    self.player_y = wy
                    self.player_angle = 0
                    self.grid[y][x] = "."
                elif cell == "M":
                    self.monsters.append(Monster(wx, wy))
                    self.grid[y][x] = "."
                elif cell == "T":
                    self.treasures.append(Treasure(wx, wy))
                    self.grid[y][x] = "."

    def start(self):
        self.reset()
        self.state = "playing"

    def is_wall(self, x, y):
        mx = int(x // TILE)
        my = int(y // TILE)
        if mx < 0 or my < 0 or mx >= MAP_W or my >= MAP_H:
            return True
        return self.grid[my][mx] in ["#", "D"]

    def cell_at_world(self, x, y):
        mx = int(x // TILE)
        my = int(y // TILE)
        if mx < 0 or my < 0 or mx >= MAP_W or my >= MAP_H:
            return "#"
        return self.grid[my][mx]

    def try_move(self, dx, dy):
        radius = 16
        new_x = self.player_x + dx
        new_y = self.player_y + dy

        if not self.is_wall(new_x + math.copysign(radius, dx), self.player_y):
            self.player_x = new_x
        if not self.is_wall(self.player_x, new_y + math.copysign(radius, dy)):
            self.player_y = new_y

    def update(self):
        if self.state != "playing":
            return

        keys = pygame.key.get_pressed()
        dt = clock.get_time() / 1000

        rot_speed = 2.2 * dt
        move_speed = 145 * dt
        strafe_speed = 105 * dt

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_angle -= rot_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_angle += rot_speed

        forward = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            forward += move_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            forward -= move_speed

        strafe = 0
        if keys[pygame.K_q]:
            strafe -= strafe_speed
        if keys[pygame.K_e]:
            strafe += strafe_speed

        dx = math.cos(self.player_angle) * forward + math.cos(self.player_angle + math.pi / 2) * strafe
        dy = math.sin(self.player_angle) * forward + math.sin(self.player_angle + math.pi / 2) * strafe
        self.try_move(dx, dy)

        if keys[pygame.K_f]:
            self.open_door()

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.update_monsters()
        self.collect_treasures()
        self.check_exit()

        if self.message_timer > 0:
            self.message_timer -= 1

        if self.hp <= 0:
            self.state = "dead"

    def open_door(self):
        front_x = self.player_x + math.cos(self.player_angle) * 70
        front_y = self.player_y + math.sin(self.player_angle) * 70
        mx = int(front_x // TILE)
        my = int(front_y // TILE)
        if 0 <= mx < MAP_W and 0 <= my < MAP_H and self.grid[my][mx] == "D":
            self.grid[my][mx] = "."
            self.set_message("The stone door grinds open.")

    def attack(self):
        if self.attack_cooldown > 0 or self.state != "playing":
            return
        self.attack_cooldown = 28

        hit_any = False
        for monster in self.monsters[:]:
            dx = monster.x - self.player_x
            dy = monster.y - self.player_y
            dist = math.hypot(dx, dy)
            angle_to = math.atan2(dy, dx)
            diff = normalize_angle(angle_to - self.player_angle)

            if dist < 95 and abs(diff) < 0.42 and self.has_line_of_sight(monster.x, monster.y):
                monster.hp -= 1
                hit_any = True
                self.set_message("You strike the beast!")
                if monster.hp <= 0:
                    self.monsters.remove(monster)
                    self.score += 100
                    self.set_message("Monster defeated.")
                break

        if not hit_any:
            self.set_message("Your attack hits only darkness.")

    def update_monsters(self):
        for monster in self.monsters:
            dx = self.player_x - monster.x
            dy = self.player_y - monster.y
            dist = math.hypot(dx, dy)

            if monster.cooldown > 0:
                monster.cooldown -= 1

            if dist < 350 and self.has_line_of_sight(monster.x, monster.y):
                if dist > 42:
                    speed = 0.75
                    nx = dx / dist
                    ny = dy / dist
                    if not self.is_wall(monster.x + nx * speed * 2, monster.y):
                        monster.x += nx * speed
                    if not self.is_wall(monster.x, monster.y + ny * speed * 2):
                        monster.y += ny * speed
                elif monster.cooldown <= 0:
                    monster.cooldown = 70
                    self.hp -= 1
                    self.set_message("The beast claws you!")

    def collect_treasures(self):
        for treasure in self.treasures:
            if not treasure.taken and math.hypot(treasure.x - self.player_x, treasure.y - self.player_y) < 42:
                treasure.taken = True
                self.score += 250
                self.set_message("You found ancient gold.")

    def check_exit(self):
        cell = self.cell_at_world(self.player_x, self.player_y)
        if cell == "E":
            self.state = "win"
            self.win = True

    def has_line_of_sight(self, x, y):
        dx = x - self.player_x
        dy = y - self.player_y
        dist = math.hypot(dx, dy)
        if dist <= 1:
            return True
        steps = int(dist / 12)
        for i in range(1, steps):
            t = i / steps
            px = self.player_x + dx * t
            py = self.player_y + dy * t
            if self.is_wall(px, py):
                return False
        return True

    def set_message(self, text):
        self.message = text
        self.message_timer = 160

    def cast_rays(self):
        rays = []
        start_angle = self.player_angle - FOV / 2

        for ray in range(NUM_RAYS):
            ray_angle = start_angle + ray * DELTA_ANGLE
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            hit_x, hit_y = self.player_x, self.player_y
            hit_cell = "#"
            depth = 1

            while depth < MAX_DEPTH:
                test_x = self.player_x + cos_a * depth
                test_y = self.player_y + sin_a * depth
                mx = int(test_x // TILE)
                my = int(test_y // TILE)

                if mx < 0 or my < 0 or mx >= MAP_W or my >= MAP_H:
                    hit_x, hit_y = test_x, test_y
                    hit_cell = "#"
                    break

                if self.grid[my][mx] in ["#", "D"]:
                    hit_x, hit_y = test_x, test_y
                    hit_cell = self.grid[my][mx]
                    break

                depth += 4

            # Remove fish-eye distortion.
            depth *= math.cos(self.player_angle - ray_angle)
            depth = max(depth, 1)
            wall_height = min(int(TILE * PROJ_DIST / depth), HEIGHT * 2)

            # Simple side shading by checking whether hit is close to vertical or horizontal grid line.
            shade = 1.0
            local_x = hit_x % TILE
            local_y = hit_y % TILE
            if local_x < 5 or local_x > TILE - 5:
                shade = 0.78
            if hit_cell == "D":
                base_color = BROWN
            else:
                base_color = (110, 108, 128)

            fog = max(0.25, 1 - depth / MAX_DEPTH)
            color = tuple(max(0, min(255, int(c * shade * fog))) for c in base_color)
            rays.append((ray, depth, wall_height, color))

        return rays

    def draw(self):
        if self.state == "menu":
            self.draw_menu()
        else:
            self.draw_3d_scene()
            self.draw_sprites()
            self.draw_weapon()
            self.draw_ui()

            if self.state == "dead":
                self.draw_overlay("YOU DIED", "Press R to restart or ESC for menu", RED)
            elif self.state == "win":
                self.draw_overlay("DUNGEON CLEARED", "Press R to play again or ESC for menu", GREEN)

        pygame.display.flip()

    def draw_menu(self):
        screen.fill(BLACK)
        title = font_big.render("DUNGEON CRAWLER", True, WHITE)
        subtitle = font_med.render("Fake 3D raycasting prototype", True, BLUE)
        start = font_med.render("Press ENTER to start", True, YELLOW)
        controls = font_small.render("W/S move  |  A/D turn  |  Q/E strafe  |  F open doors  |  Space attack", True, GRAY)

        screen.blit(title, (WIDTH / 2 - title.get_width() / 2, 180))
        screen.blit(subtitle, (WIDTH / 2 - subtitle.get_width() / 2, 250))
        screen.blit(start, (WIDTH / 2 - start.get_width() / 2, 350))
        screen.blit(controls, (WIDTH / 2 - controls.get_width() / 2, 440))

    def draw_3d_scene(self):
        # Ceiling and floor.
        screen.fill(CEILING)
        pygame.draw.rect(screen, FLOOR, (0, HALF_H, WIDTH, HALF_H))

        # Floor depth lines.
        for y in range(HALF_H, HEIGHT, 18):
            darkness = min(85, int((y - HALF_H) * 0.23))
            color = (FLOOR[0] + darkness // 4, FLOOR[1] + darkness // 5, FLOOR[2] + darkness // 6)
            pygame.draw.line(screen, color, (0, y), (WIDTH, y), 1)

        rays = self.cast_rays()
        self.depth_buffer = [depth for _, depth, _, _ in rays]

        for ray, depth, wall_height, color in rays:
            x = ray * SCALE
            y = HALF_H - wall_height // 2
            pygame.draw.rect(screen, color, (x, y, SCALE + 1, wall_height))

            # Stone brick lines.
            if wall_height > 45:
                line_gap = max(12, wall_height // 5)
                for ly in range(y + line_gap, y + wall_height, line_gap):
                    line_color = tuple(max(0, c - 26) for c in color)
                    pygame.draw.line(screen, line_color, (x, ly), (x + SCALE, ly), 1)

    def draw_sprites(self):
        sprites = []

        for monster in self.monsters:
            sprites.append((monster.x, monster.y, "monster", monster.hp))
        for treasure in self.treasures:
            if not treasure.taken:
                sprites.append((treasure.x, treasure.y, "treasure", 1))

        # Draw far sprites first.
        sprites.sort(key=lambda s: math.hypot(s[0] - self.player_x, s[1] - self.player_y), reverse=True)

        for sx, sy, kind, hp in sprites:
            dx = sx - self.player_x
            dy = sy - self.player_y
            dist = math.hypot(dx, dy)
            if dist < 8:
                continue

            theta = math.atan2(dy, dx)
            gamma = normalize_angle(theta - self.player_angle)

            if abs(gamma) > FOV / 2 + 0.25:
                continue

            if not self.has_line_of_sight(sx, sy):
                continue

            screen_x = WIDTH / 2 + math.tan(gamma) * PROJ_DIST
            size = int((TILE * PROJ_DIST / dist) * (0.75 if kind == "treasure" else 1.0))
            size = max(8, min(size, 250))
            top = HALF_H - size // 2
            left = int(screen_x - size // 2)

            ray_index = int(screen_x / SCALE)
            if 0 <= ray_index < len(self.depth_buffer) and dist > self.depth_buffer[ray_index] + 20:
                continue

            if kind == "monster":
                body = pygame.Rect(left, top, size, size)
                pygame.draw.ellipse(screen, RED, body)
                pygame.draw.circle(screen, YELLOW, (int(screen_x - size * 0.18), int(top + size * 0.35)), max(2, size // 13))
                pygame.draw.circle(screen, YELLOW, (int(screen_x + size * 0.18), int(top + size * 0.35)), max(2, size // 13))
                pygame.draw.rect(screen, BLACK, (left + size * 0.25, top + size * 0.62, size * 0.5, max(2, size // 12)))
            else:
                chest = pygame.Rect(left + size * 0.15, top + size * 0.28, size * 0.7, size * 0.5)
                pygame.draw.rect(screen, BROWN, chest)
                pygame.draw.rect(screen, YELLOW, chest, max(1, size // 18))
                pygame.draw.circle(screen, YELLOW, (int(screen_x), int(top + size * 0.52)), max(2, size // 15))

    def draw_weapon(self):
        # Simple sword animation when attacking.
        swing = 0
        if self.attack_cooldown > 0:
            swing = math.sin((28 - self.attack_cooldown) / 28 * math.pi) * 90

        base_x = WIDTH // 2 + 120
        base_y = HEIGHT - 50
        tip_x = WIDTH // 2 + 40 - swing
        tip_y = HEIGHT - 210 + swing * 0.4

        pygame.draw.line(screen, (185, 185, 200), (base_x, base_y), (tip_x, tip_y), 9)
        pygame.draw.line(screen, WHITE, (base_x, base_y), (tip_x, tip_y), 3)
        pygame.draw.rect(screen, BROWN, (base_x - 20, base_y - 12, 52, 18))

    def draw_ui(self):
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, 76))
        hp_text = font_med.render(f"HP: {self.hp}", True, RED if self.hp <= 2 else WHITE)
        score_text = font_med.render(f"Gold: {self.score}", True, YELLOW)
        map_text = font_small.render("F open doors | Space attack | M minimap", True, GRAY)
        screen.blit(hp_text, (18, 16))
        screen.blit(score_text, (145, 16))
        screen.blit(map_text, (WIDTH - map_text.get_width() - 18, 25))

        if self.message_timer > 0:
            msg = font_small.render(self.message, True, WHITE)
            pygame.draw.rect(screen, (0, 0, 0), (WIDTH / 2 - msg.get_width() / 2 - 12, HEIGHT - 42, msg.get_width() + 24, 30))
            screen.blit(msg, (WIDTH / 2 - msg.get_width() / 2, HEIGHT - 34))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            self.draw_minimap()

    def draw_minimap(self):
        scale = 8
        ox, oy = 18, 92
        pygame.draw.rect(screen, (0, 0, 0), (ox - 6, oy - 6, MAP_W * scale + 12, MAP_H * scale + 12))
        for y in range(MAP_H):
            for x in range(MAP_W):
                cell = self.grid[y][x]
                if cell == "#":
                    color = GRAY
                elif cell == "D":
                    color = BROWN
                elif cell == "E":
                    color = GREEN
                else:
                    color = DARK_GRAY
                pygame.draw.rect(screen, color, (ox + x * scale, oy + y * scale, scale - 1, scale - 1))

        px = ox + int(self.player_x / TILE * scale)
        py = oy + int(self.player_y / TILE * scale)
        pygame.draw.circle(screen, BLUE, (px, py), 3)
        pygame.draw.line(screen, BLUE, (px, py), (px + math.cos(self.player_angle) * 10, py + math.sin(self.player_angle) * 10), 2)

        for monster in self.monsters:
            mx = ox + int(monster.x / TILE * scale)
            my = oy + int(monster.y / TILE * scale)
            pygame.draw.circle(screen, RED, (mx, my), 2)

    def draw_overlay(self, title, subtitle, color):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 165))
        screen.blit(overlay, (0, 0))
        title_text = font_big.render(title, True, color)
        subtitle_text = font_med.render(subtitle, True, WHITE)
        screen.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, HEIGHT / 2 - 70))
        screen.blit(subtitle_text, (WIDTH / 2 - subtitle_text.get_width() / 2, HEIGHT / 2 + 10))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "menu":
                if event.key == pygame.K_RETURN:
                    self.start()
                elif event.key == pygame.K_ESCAPE:
                    return False

            elif self.state == "playing":
                if event.key == pygame.K_SPACE:
                    self.attack()
                elif event.key == pygame.K_ESCAPE:
                    self.state = "menu"

            elif self.state in ["dead", "win"]:
                if event.key == pygame.K_r:
                    self.start()
                elif event.key == pygame.K_ESCAPE:
                    self.state = "menu"

        return True


def normalize_angle(angle):
    while angle > math.pi:
        angle -= math.tau
    while angle < -math.pi:
        angle += math.tau
    return angle


def main():
    game = Game()
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                running = game.handle_event(event)

        game.update()
        game.draw()

    pygame.quit()


if __name__ == "__main__":
    main()
