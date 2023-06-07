import pygame
import random
from ship import Ship
from bullet import Bullet


class Enemy(Ship):
    def __init__(self, x, y, ship_img, img_str, points, bullet_img=None, death_img=None, death_img_str=None,
                 should_move_left=None):
        super().__init__(x, y)
        self.ship_img: pygame.Surface | pygame.SurfaceType = ship_img
        self.ship_img_rect = self.ship_img.get_rect()
        self.ship_img_str: str = img_str

        self.bullet_img: pygame.Surface | pygame.SurfaceType | None = bullet_img
        self.death_img: pygame.Surface | pygame.SurfaceType | None = death_img
        self.death_img_str: str = death_img_str
        self.mask: pygame.Mask = pygame.mask.from_surface(self.ship_img.convert_alpha())
        self.vel: int = 10
        self.points: int = points
        self.shoot_probability: int = 1000
        self.spaceship_death_animation_counter = 0
        self.spaceship_animation_playing = False
        self.should_move_left = should_move_left
        self.hit: bool = False

    def shoot(self):
        if self.bullet_cooldown_counter == 0:
            rng_shoot = random.randint(0, self.shoot_probability)
            if rng_shoot == 1:
                bullet = Bullet(self.x + self.ship_img.get_width()/2 - self.bullet_img.get_width()/2,
                                self.y + self.ship_img.get_height(), self.bullet_img)
                self.bullets.append(bullet)
                self.bullet_cooldown_counter = 1

    def move_bullets(self, move_up, height, player, wall_list):
        self.bullet_cooldown()
        for bullet in self.bullets:
            if bullet.is_off_screen(height):
                self.bullets.remove(bullet)
            else:
                if bullet.collide(player):
                    player.is_dying = True
                    self.bullets.remove(bullet)
                for wall in wall_list:
                    if bullet.collide(wall):
                        wall.health -= 1
                        self.bullets.remove(bullet)
                bullet.move(move_up)

    def move_spaceship_enemy(self, should_move_left: bool):
        if should_move_left:
            self.x -= 2
        else:
            self.x += 2
