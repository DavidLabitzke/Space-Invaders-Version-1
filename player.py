import pygame

from ship import Ship


class Player(Ship):
    def __init__(self, x, y, ship_img, bullet_img, death_img, death_img_str):
        super().__init__(x, y)
        self.ship_img = ship_img
        self.ship_img_rect = self.ship_img.get_rect()
        self.bullet_img = bullet_img

        self.death_img = death_img
        self.death_img_str = death_img_str
        self.mask = pygame.mask.from_surface(self.ship_img.convert_alpha())
        self.score = 0
        self.lives = 3
        self.is_dying = False
        self.death_animation_cooldown: int = 0
        self.shoot_possible = True

    def handle_player_inputs(self, keys, width, screen_margin):
        """Listens for inputs from the user, and performs corresponding method calls for moving and shooting"""
        if keys[pygame.K_LEFT] and self.x > screen_margin:
            self.move_left()
        if keys[pygame.K_RIGHT] and self.x < width - screen_margin - self.ship_img.get_width():
            self.move_right()
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move_bullets(self, move_up: bool, height, enemy_master_list, spaceship_enemy_list, wall_list):
        """Moves player bullets after they have been fired"""
        self.bullet_cooldown()
        for bullet in self.bullets:
            if bullet.is_off_screen(height):
                self.bullets.remove(bullet)
            else:
                self.handle_bullet_collision(bullet, enemy_master_list, spaceship_enemy_list, wall_list)
            bullet.move(move_up)

    def handle_bullet_collision(self, bullet, enemy_master_list, spaceship_enemy_list, wall_list):
        """Checks if a player bullet has collided with an enemy object"""
        for spaceship_enemy in spaceship_enemy_list:
            if bullet.collide(spaceship_enemy):
                self.score += spaceship_enemy.points
                spaceship_enemy.hit = True
                if bullet in self.bullets:
                    self.bullets.remove(bullet)

        for enemy_list in enemy_master_list:
            for enemy in enemy_list:
                if bullet.collide(enemy):
                    self.score += enemy.points
                    enemy.hit = True
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

        for wall in wall_list:
            if bullet.collide(wall):
                wall.health -= 1
                if bullet in self.bullets:
                    self.bullets.remove(bullet)

    def reset_player_position(self, x, y):
        """Resets the player's position to the default starting position"""
        self.x, self.y = x, y
