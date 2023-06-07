import pygame


class ImageManager:

    def __init__(self):
        # All colors used in game
        self.BLACK = (0, 0, 0)
        self.GREEN = (88, 255, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)

        # Current Level
        self.current_level = 1

        # All sprite's widths and heights
        self.player_width, self.player_height = 50, 40
        self.enemy_width, self.enemy_height = 32, 32
        self.player_bullet_width, self.player_bullet_height = 32, 30
        self.enemy_bullet_width, self.enemy_bullet_height = 32, 30
        self.spaceship_enemy_width, self.spaceship_enemy_height = 50, 32
        self.wall_width, self.wall_height = 100, 100

        # image number used for animating player and enemy sprites
        self.image_num = 0
        self.enemy_death_image_num = 0
        self.player_death_image_num = 0

        self.player_img_str = "Sprites/player/player.png"
        self.player_img = pygame.transform.scale(
            pygame.image.load(self.player_img_str),
            (self.player_width, self.player_height))

        self.enemy1_img_str = f"Sprites/enemy1/enemy1_{self.image_num}.png"
        self.enemy1_img = pygame.transform.scale(
            pygame.image.load(self.enemy1_img_str),
            (self.enemy_width, self.enemy_height))

        self.enemy2_img_str = f"Sprites/enemy2/enemy2_{self.image_num}.png"
        self.enemy2_img = pygame.transform.scale(
            pygame.image.load(self.enemy2_img_str),
            (self.enemy_width, self.enemy_height))

        self.enemy3_img_str = f"Sprites/enemy3/enemy3_{self.image_num}.png"
        self.enemy3_img = pygame.transform.scale(
            pygame.image.load(self.enemy3_img_str),
            (self.enemy_width, self.enemy_height))

        self.spaceship_img_str = f"Sprites/spaceship/spaceship_{self.image_num}.png"
        self.spaceship_img = pygame.transform.scale(
            pygame.image.load(self.spaceship_img_str),
            (self.spaceship_enemy_width, self.spaceship_enemy_height))

        self.player_bullet_img_str = "Sprites/bullets/player_bullet.png"
        self.player_bullet_img = pygame.transform.scale(
            pygame.image.load(self.player_bullet_img_str),
            (self.player_bullet_width, self.player_bullet_height))

        self.enemy_bullet_img_str = "Sprites/bullets/enemy_bullet.png"
        self.enemy_bullet_img = pygame.transform.scale(
            pygame.image.load(self.enemy_bullet_img_str),
            (self.enemy_bullet_width, self.enemy_bullet_height))

        self.enemy_death_animation_img_str = f"Sprites/enemy-death/enemy-death_{self.enemy_death_image_num}.png"
        self.enemy_death_animation_img = pygame.transform.scale(
            pygame.image.load(self.enemy_death_animation_img_str),
            (self.enemy_width, self.enemy_height))

        self.spaceship_death_x, self.spaceship_death_y = 0, 0

        self.player_death_animation_img_str = f"Sprites/player-death/player-death_img.png"
        self.player_death_animation_img = pygame.transform.scale(
            pygame.image.load(self.player_death_animation_img_str),
            (self.player_width, self.player_height))

        self.wall_img_str = "Sprites/wall/wall.png"
        self.wall_img = pygame.transform.scale(
            pygame.image.load(self.wall_img_str),
            (self.wall_width, self.wall_height))

        self.game_over_animation_timer = 0

    def switch_image_num(self):
        if self.image_num == 0:
            self.image_num = 1
        elif self.image_num == 1:
            self.image_num = 0

    def change_enemy_drawings(self, enemies_master_list, spaceship_enemy_list):
        self.switch_image_num()
        for spaceship_enemy in spaceship_enemy_list:
            spaceship_enemy.ship_img_str = f"{spaceship_enemy.ship_img_str.split('_')[0]}_{self.image_num}.png"
            spaceship_enemy.ship_img = pygame.transform.scale(
                pygame.image.load(spaceship_enemy.ship_img_str),
                (self.spaceship_enemy_width, self.spaceship_enemy_height))
        for enemy_list in enemies_master_list:
            for enemy in enemy_list:
                enemy.ship_img_str = f"{enemy.ship_img_str.split('_')[0]}_{self.image_num}.png"
                enemy.ship_img = pygame.transform.scale(
                    pygame.image.load(enemy.ship_img_str),
                    (self.enemy_width, self.enemy_height))

    def animate_enemy_death(self, enemies_master_list):
        for enemy_list in enemies_master_list:
            for enemy in enemy_list:
                if enemy.hit:
                    if enemy.death_img_num == 5:
                        enemy.death_img_num = 0
                        enemy.death_animation_finished = True
                    if enemy.death_animation_finished:
                        enemy_list.remove(enemy)
                    else:
                        enemy.death_img_str = f"{enemy.death_img_str.split('_')[0]}_{enemy.death_img_num}.png"
                        enemy.ship_img_str = enemy.death_img_str
                        enemy.ship_img = pygame.transform.scale(
                            pygame.image.load(enemy.ship_img_str),
                            (self.enemy_width, self.enemy_height))
                        enemy.death_img_num += 1

    @staticmethod
    def animate_spaceship_death(spaceship_enemy_list):
        for spaceship_enemy in spaceship_enemy_list:
            if spaceship_enemy.hit:
                spaceship_enemy.spaceship_animation_playing = True
                if spaceship_enemy.spaceship_death_animation_counter == 60:
                    spaceship_enemy.spaceship_death_animation_counter = 0
                    spaceship_enemy_list.remove(spaceship_enemy)
                else:
                    spaceship_enemy.spaceship_death_animation_counter += 1

    def animate_player_death(self):
        return self.player_death_animation_img

    def write_walls_health(self, window, main_font, wall_list):
        for wall in wall_list:
            wall_health_label = main_font.render(f"{wall.health}", True, self.WHITE)
            window.blit(wall_health_label,
                        (wall.x + self.wall_img.get_width() / 2, wall.y + self.wall_img.get_height()))

    @staticmethod
    def get_current_high_score():
        with open("high_score.csv", "r") as high_score:
            return high_score.read()

    @staticmethod
    def is_new_high_score(player_score: int) -> bool:
        with open("high_score.csv", "r") as high_score:
            current_high_score = int(high_score.read())
            if player_score > current_high_score:
                return True
        return False

    @staticmethod
    def write_new_high_score(player_score: int):
        with open("high_score.csv", "w") as high_score:
            high_score.write(str(player_score))

    def redraw_window(self, window, player, enemies_master_list, spaceship_list,
                      wall_list, main_font, small_font, width):
        window.fill(self.BLACK)
        current_score_label = main_font.render(f"Score: {player.score}", True, self.WHITE)
        high_score_label = main_font.render(f"High Score: {self.get_current_high_score()}", True, self.WHITE)
        lives_label = small_font.render(f"Lives: {player.lives}", True, self.WHITE)
        level_label = small_font.render(f"Level: {self.current_level}", True, self.WHITE)

        window.blit(current_score_label, (width / 2 - current_score_label.get_width() - 10, 10))
        window.blit(high_score_label, (width - high_score_label.get_width() - 10, 10))
        window.blit(lives_label, (10, 10))
        window.blit(level_label, (10, 10 + level_label.get_height()))

        player.draw(window)
        for enemy_list in enemies_master_list:
            for enemy in enemy_list:
                enemy.draw(window)
        for spaceship_enemy in spaceship_list:
            if not spaceship_enemy.spaceship_animation_playing:
                spaceship_enemy.draw(window)
            else:
                spaceship_death_label = main_font.render(f"{spaceship_enemy.points}", True, self.WHITE)
                window.blit(spaceship_death_label, (spaceship_enemy.x, spaceship_enemy.y))

        for wall in wall_list:
            wall.draw(window)
            self.write_walls_health(window, main_font, wall_list)

        pygame.display.update()

    def game_over_screen(self, window, main_font, game_over_font, width, height, player_score):
        window.fill(self.GREEN)
        game_over_label = game_over_font.render("Game Over!!!", True, self.BLACK)
        new_high_score_label = main_font.render(f"New High Score!!! {player_score}", True, self.BLACK)
        window.blit(game_over_label,
                    (width / 2 - game_over_label.get_width() / 2, height / 2 - game_over_label.get_height()))
        if self.is_new_high_score(player_score):
            window.blit(new_high_score_label,
                        (width / 2 - new_high_score_label.get_width() / 2,
                         height / 2 + new_high_score_label.get_height()))
        pygame.display.update()
