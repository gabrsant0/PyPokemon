import pygame

timeout = {
    'bool':'bool_timeout'
}

class Timer():
    def __init__(self):
        self.time_running = False
        self.miliseconds = 0
        self.boolTimeout = False
        #self.instance = instance
        self.action = None

    def start(self, miliseconds, action):
        self.last_time_update = self.current_time
        self.time_running = True
        self.miliseconds = miliseconds
        self.action = action
        if type(action) == bool:
            print("is bool")

    def timeout(self):
        self.action()
        self.time_running = False

    def update(self):
        self.current_time = pygame.time.get_ticks()
        if self.time_running == True:
            if self.current_time - self.last_time_update > self.miliseconds:
                self.time_running = False
                self.timeout()
        