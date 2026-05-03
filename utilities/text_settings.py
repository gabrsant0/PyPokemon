import pygame

class NewLabel():
    def __init__(self, text=str):
        self.color = (0, 0, 0)
        self.count = 0
        self.max_count = 0
        self.alphapersec = 9
        self.font_size = 22
        self.input_text = text
        self.font = pygame.font.SysFont("Arial", self.font_size)
        self.text = self.font.render(text, True, self.color)
        self.text = self.text.convert_alpha()
        self.alpha = 255
        self.visible = True
        self.blinking_anim = False
        self.fade_out_anim = False
        self.fade_in_anim = False
        self.duration_set = False

    def set_color(self, color):
        self.color = color
        self.text = self.font.render(self.input_text, True, self.color)

    def set_size(self, size):
        self.font_size = size
        self.font = pygame.font.SysFont("Arial", size)
        self.text = self.font.render(self.input_text, True, self.color)

    def set_text(self, text):
        self.visible = True
        self.input_text = text
        self.text = self.font.render(self.input_text, True, self.color)

    def alpha_anim(self):
        if self.fade_in_anim == True:
            if self.alpha < 255:
                self.alpha += self.alphapersec
                self.text.set_alpha(self.alpha)
            elif self.alpha >= 255:
                self.fade_in_anim = False
        elif self.fade_out_anim == True:
            if self.alpha > 0:
                self.alpha -= self.alphapersec
                self.text.set_alpha(self.alpha)
            elif self.alpha <= 0:
                self.visible = False
        elif self.blinking_anim == True:
            if self.count < self.max_count and self.alpha < 255:
                self.alpha += self.alphapersec
                self.text.set_alpha(self.alpha)
            elif self.count < self.max_count and self.alpha >= 255:
                self.alpha = 0
                self.text.set_alpha(self.alpha)
                self.count += 1
            elif self.count >= self.max_count:
                if self.alpha < 255:
                    self.alpha += self.alphapersec
                    self.text.set_alpha(self.alpha)
                else:
                    self.blinking_anim = False

    def blink_anim(self, aps, count):
        self.count = 0
        self.max_count = count
        self.alphapersec = aps
        self.blinking_anim = True

    def blink_fade(self, count, aps):
        self.alphapersec = aps
        self.count = count
        self.alpha = 0

    def fade_out(self, aps):
        self.fade_out_anim = True
        self.alphapersec = aps

    def fade_in(self, aps):
        self.fade_in_anim = True
        self.alpha = 0
        self.alphapersec = aps

    def duration(self, milisseconds, aps):
        self.last_update_time = self.current_time
        self.duration_set = True
        self.milisseconds = milisseconds
        self.alphapersec = aps

    def draw(self, screen, rect):
        self.current_time = pygame.time.get_ticks()
        self.text.set_alpha(self.alpha)
        screen.blit(self.text, rect)
        if self.fade_in_anim:
            self.alpha_anim()
        elif self.fade_out_anim:
            self.alpha_anim()
        elif self.blinking_anim:
            self.alpha_anim()
        elif self.duration_set == True:
            if self.current_time - self.last_update_time > self.milisseconds:
                self.fade_out(self.alphapersec)
            
    