from enum import Enum

class State(Enum):
    NONE = 0
    RUNNING = 1
    pass

class gameState(Enum):
    NONE = 10
    MAIN_MENU = 0
    MAP_EDITOR =1
    MAP_1 = 2
    MAP_1_BATTLE = 3
    MAP_2 = 4
    MAP_2_BATTLE = 5