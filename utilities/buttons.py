import pygame

class Button():
    def __init__(self, button_color, hover_color, rect):
        self.font = pygame.font.SysFont("Arial", 10)
        self.button_color = button_color
        self.hover_color = hover_color
        self.visible = True
        self.text = "text"
        self.text_color = (100, 100, 100)
        self.text_surface = self.font.render("text", True, self.text_color)

        self.button_rect = rect
        self.text_rect = self.text_surface.get_rect(center=self.button_rect.center)
        self.hover_text = False

    def set_hover_text(self, mode, hover_color=None):
        if mode == True:
            self.hover_text = True
            self.hovered_text = pygame.font.SysFont("Arial", self.font_size)
            self.text_hover = hover_color
            self.hovered_text_surface = self.font.render(self.text, True, self.text_hover)
        else: self.hover_text = False

    def set_text(self, text, text_color, font_size):
        self.font = pygame.font.SysFont("Arial", font_size)
        self.font_size = font_size
        self.text = text
        self.text_color = text_color
        self.text_surface = self.font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.button_rect.center)

    def draw(self, screen):
        if self.hover_text == False:
            color = self.hover_color if self.hovered else self.button_color
            pygame.draw.rect(screen, color, self.button_rect, border_radius=8)
            screen.blit(self.text_surface, self.text_rect)
        else:
            if self.hovered:
                screen.blit(self.hovered_text_surface, self.text_rect)
            else:
                screen.blit(self.text_surface, self.text_rect)

    def update(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.button_rect.collidepoint(mouse_pos)
        if self.visible:
            self.draw(screen)


