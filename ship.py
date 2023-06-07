import pygame
from bullet import Bullet


class Ship:
    BULLET_COOLDOWN = 30

    def __init__(self, x, y):
        self.x: int = x
        self.y: int = y
        self.ship_img: pygame.Surface | pygame.SurfaceType | None = None
        self.bullet_img: pygame.Surface | pygame.SurfaceType | None = None
        self.vel: int = 5
        self.bullets: list[Bullet] = []
        self.bullet_cooldown_counter: int = 0
        self.death_animation_finished: bool = False
        self.death_img_num: int = 0

    def draw(self, window):
        """Blits all objects to the screen"""
        window.blit(self.ship_img, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(window)

    def move_left(self):
        """Moves object to the left"""
        self.x -= self.vel

    def move_right(self):
        """Moves object to the right"""
        self.x += self.vel

    def shoot(self):
        """Creates a new bullet object if able"""
        if self.bullet_cooldown_counter == 0 and not self.bullets:
            bullet = Bullet(self.x + self.ship_img.get_width()/4, self.y, self.bullet_img)
            self.bullets.append(bullet)
            self.bullet_cooldown_counter = 1

    def bullet_cooldown(self):
        """Increments the bullet_cooldown_counter unless it needs to be reset"""
        if not self.bullets:
            self.bullet_cooldown_counter = 0
        elif self.bullet_cooldown_counter >= 45:
            self.bullet_cooldown_counter = 0
        else:
            self.bullet_cooldown_counter += 1
