import pygame


class Wall:
    def __init__(self, x, y, wall_img):
        self.x = x
        self.y = y
        self.img = wall_img
        self.health = 30
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
