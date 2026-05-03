import pygame

player_sprite_settings = {
    'sprite_left':'player_src/player_left.png',
    'sprite_right':'player_src/player_right.png',
    'sprite_top':'player_src/player_top.png',
    'sprite_bottom':'player_src/player_bottom.png',

    'size_x': 96,
    'size_y': 54,
    'number_of_animations': 3
}

sprite_sheet = {
    'bottom':pygame.transform.scale(pygame.image.load(player_sprite_settings['sprite_bottom']), (96, 54)),
    'top':pygame.transform.scale(pygame.image.load(player_sprite_settings['sprite_top']), (96, 54)),
    'left':pygame.transform.scale(pygame.image.load(player_sprite_settings['sprite_left']), (96, 54)),
    'right':pygame.transform.scale(pygame.image.load(player_sprite_settings['sprite_right']), (96, 54))
}