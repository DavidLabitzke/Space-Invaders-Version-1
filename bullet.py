import pygame


class Bullet:
    def __init__(self, x, y, img):
        self.x: int = x
        self.y: int = y
        self.image: pygame.Surface | pygame.SurfaceType = img
        self.image_rect = self.image.get_rect()
        self.vel: int = 5
        self.mask: pygame.Mask = pygame.mask.from_surface(self.image.convert_alpha())

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self, move_up: bool):
        if move_up:
            self.y -= self.vel * 2
        else:
            self.y += self.vel

    def is_off_screen(self, height) -> bool:
        return not (height >= self.y >= 0)

    def collide(self, obj):
        offset_x = obj.x - self.x
        offset_y = obj.y - self.y
        return self.mask.overlap(obj.mask, (offset_x, offset_y)) is not None

    def collision(self, obj):
        return self.collide(obj)
