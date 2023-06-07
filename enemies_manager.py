import random

from enemy import Enemy


class EnemyManager:
    INITIAL_MOVE_COOLDOWN_MAX = 60

    def __init__(self, enemy1_img, enemy2_img, enemy3_img,
                 enemy1_img_str, enemy2_img_str, enemy3_img_str,
                 bullet_img, enemy_death_img, enemy_death_img_str):
        self.enemy_start_x: int = 200
        self.enemy_start_y: int = 75
        self.spaceship_points_possible: list[int] = [10, 25, 50, 100, 250]

        self.enemies_row1: list[Enemy] = self.create_enemies(self.enemy_start_x, self.enemy_start_y,
                                                             enemy3_img, enemy3_img_str, 50, bullet_img,
                                                             enemy_death_img, enemy_death_img_str)
        self.enemies_row2: list[Enemy] = self.create_enemies(self.enemy_start_x, self.enemy_start_y + 25,
                                                             enemy2_img, enemy2_img_str, 25, bullet_img,
                                                             enemy_death_img, enemy_death_img_str)
        self.enemies_row3: list[Enemy] = self.create_enemies(self.enemy_start_x, self.enemy_start_y + 50,
                                                             enemy2_img, enemy2_img_str, 25, bullet_img,
                                                             enemy_death_img, enemy_death_img_str)
        self.enemies_row4: list[Enemy] = self.create_enemies(self.enemy_start_x, self.enemy_start_y + 75,
                                                             enemy1_img, enemy1_img_str, 10, bullet_img,
                                                             enemy_death_img, enemy_death_img_str)
        self.enemies_row5: list[Enemy] = self.create_enemies(self.enemy_start_x, self.enemy_start_y + 100,
                                                             enemy1_img, enemy1_img_str, 10, bullet_img,
                                                             enemy_death_img, enemy_death_img_str)
        self.all_basic_enemies: list[list[Enemy]] = [self.enemies_row1, self.enemies_row2,
                                                     self.enemies_row3, self.enemies_row4, self.enemies_row5]
        self.spaceship_enemy: list[Enemy] = []

        self.right_most_enemies: list[Enemy] = [enemy_list[-1] for enemy_list in self.all_basic_enemies]
        self.left_most_enemies: list[Enemy] = [enemy_list[0] for enemy_list in self.all_basic_enemies]

        self.move_cooldown_counter: int = 0
        self.move_cooldown_counter_max: int = self.INITIAL_MOVE_COOLDOWN_MAX
        self.move_cooldown_decrement: int = 5

        self.should_move_right: bool = True

        self.spaceship_spawn_odds: int = 500

    @staticmethod
    def create_enemies(x, y, img, img_str, points, bullet_img, death_img, death_img_str) -> list[Enemy]:
        """Returns a list of enemy objects, representing one row of enemies"""
        new_list = []
        x_pos = x
        for i in range(10):
            new_enemy = Enemy(x_pos, y, img, img_str, points, bullet_img, death_img, death_img_str)
            new_list.append(new_enemy)
            x_pos += 50
        return new_list

    def manage_enemy_movement(self, screen_margin, screen_width):
        """Moves all enemies on screen in the correct direction"""
        self.check_left_most_enemies(screen_margin)
        self.check_right_most_enemies(screen_margin, screen_width)
        for enemy_list in self.all_basic_enemies:
            for enemy in enemy_list:
                if self.should_move_right:
                    enemy.move_right()
                else:
                    enemy.move_left()
        self.move_cooldown_counter = 0

    def manage_spaceship_enemy_movement(self):
        """Moves the spaceship enemy across the screen"""
        for spaceship_enemy in self.spaceship_enemy:
            if not spaceship_enemy.spaceship_animation_playing:
                spaceship_enemy.move_spaceship_enemy(spaceship_enemy.should_move_left)

    def get_right_most_enemies(self):
        """Loops through each enemy list and appends the enemy in the right most position from each list"""
        self.right_most_enemies.clear()
        for enemy_list in self.all_basic_enemies:
            if enemy_list:
                self.right_most_enemies.append(enemy_list[-1])

    def get_left_most_enemies(self):
        """Loops through each enemy list and appends the enemy in the left most position from each list"""
        self.left_most_enemies.clear()
        for enemy_list in self.all_basic_enemies:
            if enemy_list:
                self.left_most_enemies.append(enemy_list[0])

    def change_y_pos(self):
        """Moves all enemies on screen down ten pixels"""
        for enemy_list in self.all_basic_enemies:
            for enemy in enemy_list:
                enemy.y += 20

    def check_right_most_enemies(self, screen_margin, screen_width):
        """Detects if any of the right most enemies have hit the right edge of the screen.
        If so, the enemies will move down one row, then start moving left"""
        self.get_right_most_enemies()
        if any(enemy.x == (screen_width - screen_margin * 3) for enemy in self.right_most_enemies):
            self.change_y_pos()
            self.change_max_cooldown_counter()
            self.should_move_right = False

    def check_left_most_enemies(self, screen_margin):
        """Detects if any of the left most enemies have hit the left edge of the screen.
                If so, the enemies will move down one row, then start moving right"""
        self.get_left_most_enemies()
        if any(enemy.x == screen_margin for enemy in self.left_most_enemies):
            self.change_y_pos()
            self.change_max_cooldown_counter()
            self.should_move_right = True

    def cooldown_maxed(self) -> bool:
        """Returns a boolean checking of move_cooldown_counter_max has hit 5,
        representing the maximum speed enemies can move"""
        return self.move_cooldown_counter_max == 5

    def change_max_cooldown_counter(self):
        """Reduces the move_cooldown_counter_max so that enemies will move faster"""
        if not self.cooldown_maxed():
            self.move_cooldown_counter_max -= self.move_cooldown_decrement

    def create_enemy_bullets(self):
        """Calls each enemy object's shoot method, if there are no other enemy objects directly underneath"""
        for current_list_index, enemy_list in enumerate(self.all_basic_enemies):
            enemy_lists_to_check = self.all_basic_enemies[current_list_index + 1:]
            for enemy_index, enemy in enumerate(enemy_list):
                if not enemy_lists_to_check:
                    enemy.shoot()
                    continue
                enemies_to_check = []
                for check_list in enemy_lists_to_check:
                    if enemy_index < len(check_list) and check_list[enemy_index].x == enemy.x:
                        enemies_to_check.append(check_list[enemy_index])
                if not enemies_to_check:
                    enemy.shoot()

    def manage_enemy_bullets(self, move_up: bool, height: int, player, wall_list):
        """Calls each enemy object's move_bullets method, so they will travel down the screen"""
        for enemy_list in self.all_basic_enemies:
            for enemy in enemy_list:
                enemy.move_bullets(move_up, height, player, wall_list)

    def enemies_too_low(self) -> bool:
        """Checks if any enemies have reached the bottom most point of the screen intended"""
        for enemy_list in self.all_basic_enemies:
            if any(enemy.y >= 400 for enemy in enemy_list):
                return True
        return False

    def create_spaceship_enemy(self, spaceship_img, spaceship_img_str, screen_width):
        """Randomly generates a spaceship enemy"""
        rand_num = random.randint(1, self.spaceship_spawn_odds)
        if rand_num == 1 and len(self.spaceship_enemy) == 0:
            screen_spawn_options = ["left", "right"]
            chosen_spawn_position = random.choice(screen_spawn_options)
            if chosen_spawn_position == "left":
                spaceship_enemy = Enemy(-100, 50,
                                        spaceship_img, spaceship_img_str, random.choice(self.spaceship_points_possible),
                                        should_move_left=False)
                self.spaceship_enemy = [spaceship_enemy]
            else:
                spaceship_enemy = Enemy(screen_width + 100, 50,
                                        spaceship_img, spaceship_img_str, random.choice(self.spaceship_points_possible),
                                        should_move_left=True)
                self.spaceship_enemy = [spaceship_enemy]

    def remove_spaceship_enemy(self):
        """Removes the spaceship enemy if it has travelled off the screen"""
        for spaceship_enemy in self.spaceship_enemy:
            if spaceship_enemy.x <= -200 or spaceship_enemy.x > 1100:
                self.spaceship_enemy.clear()

    def reset_enemies(self, enemy1_img, enemy2_img, enemy3_img,
                      enemy1_img_str, enemy2_img_str, enemy3_img_str, bullet_img,
                      enemy_death_img, enemy_death_img_str):
        """Recreates all the enemy lists. To be called after every enemy list is empty"""
        self.enemies_row1: list[Enemy] = self.create_enemies(self.enemy_start_x, self.enemy_start_y,
                                                             enemy3_img, enemy3_img_str, 50, bullet_img,
                                                             enemy_death_img, enemy_death_img_str)
        self.enemies_row2: list[Enemy] = self.create_enemies(self.enemy_start_x, self.enemy_start_y + 25,
                                                             enemy2_img, enemy2_img_str, 25, bullet_img,
                                                             enemy_death_img, enemy_death_img_str)
        self.enemies_row3: list[Enemy] = self.create_enemies(self.enemy_start_x, self.enemy_start_y + 50,
                                                             enemy2_img, enemy2_img_str, 25, bullet_img,
                                                             enemy_death_img, enemy_death_img_str)
        self.enemies_row4: list[Enemy] = self.create_enemies(self.enemy_start_x, self.enemy_start_y + 75,
                                                             enemy1_img, enemy1_img_str, 10, bullet_img,
                                                             enemy_death_img, enemy_death_img_str)
        self.enemies_row5: list[Enemy] = self.create_enemies(self.enemy_start_x, self.enemy_start_y + 100,
                                                             enemy1_img, enemy1_img_str, 10, bullet_img,
                                                             enemy_death_img, enemy_death_img_str)
        self.all_basic_enemies: list[list[Enemy]] = [self.enemies_row1, self.enemies_row2,
                                                     self.enemies_row3, self.enemies_row4, self.enemies_row5]
        self.reset_spaceship_enemy()

        if not self.INITIAL_MOVE_COOLDOWN_MAX <= 5:
            self.INITIAL_MOVE_COOLDOWN_MAX -= 5
        self.move_cooldown_counter_max = self.INITIAL_MOVE_COOLDOWN_MAX

        self.should_move_right = True

        self.change_enemy_shooting_probability()

    def reset_spaceship_enemy(self):
        """Removes the spaceship enemy. Should only be called by the self.reset_enemies method"""
        self.spaceship_enemy.clear()

    def change_enemy_shooting_probability(self):
        """Increases the odds of enemy objects shooting at random"""
        for enemy_list in self.all_basic_enemies:
            for enemy in enemy_list:
                enemy.shoot_probability *= 0.9
                round(enemy.shoot_probability)

    def reset_enemy_shooting_probability(self):
        """Resets the shooting probability for each enemy after a game over"""
        for enemy_list in self.all_basic_enemies:
            for enemy in enemy_list:
                enemy.shoot_probability = 1000

    def clear_all_enemy_bullets(self):
        """Removes all enemy bullets"""
        for enemy_list in self.all_basic_enemies:
            for enemy in enemy_list:
                enemy.bullets.clear()
