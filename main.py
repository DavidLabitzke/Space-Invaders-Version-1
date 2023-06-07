import pygame
from enemies_manager import EnemyManager
from player import Player
from images_manager import ImageManager
from walls_manager import WallManager

pygame.init()
pygame.font.init()

# Window Properties
WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
SCREEN_MARGIN = 20

# Frame Rate
FPS = 60


def main():
    main_font = pygame.font.SysFont("bahnschrift", 32)
    small_font = pygame.font.SysFont("bahnschrift", 24)
    game_over_font = pygame.font.SysFont("bahnschrift", 64)

    run = True
    image_manager = ImageManager()

    player = Player(WIDTH / 2 - image_manager.player_img.get_width() / 2,
                    HEIGHT - image_manager.player_img.get_height(),
                    image_manager.player_img, image_manager.player_bullet_img,
                    image_manager.player_death_animation_img, image_manager.player_death_animation_img_str)
    enemy_manager = EnemyManager(image_manager.enemy1_img, image_manager.enemy2_img,
                                 image_manager.enemy3_img, image_manager.enemy1_img_str,
                                 image_manager.enemy2_img_str, image_manager.enemy3_img_str,
                                 image_manager.enemy_bullet_img, image_manager.enemy_death_animation_img,
                                 image_manager.enemy_death_animation_img_str)

    wall_manager = WallManager(image_manager.wall_img)

    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        if player.lives <= 0 or enemy_manager.enemies_too_low():
            if image_manager.game_over_animation_timer >= 300:
                image_manager.game_over_animation_timer = 0
                if image_manager.is_new_high_score(player.score):
                    image_manager.write_new_high_score(player.score)
                player.lives = 3
                player.score = 0
                image_manager.current_level = 1
                player.ship_img = image_manager.player_img
                player.reset_player_position(WIDTH / 2 - image_manager.player_img.get_width() / 2,
                                             HEIGHT - image_manager.player_img.get_height())
                enemy_manager.reset_spaceship_enemy()
                player.bullets.clear()
                enemy_manager.clear_all_enemy_bullets()
                enemy_manager.enemy_start_y = 75
                enemy_manager.reset_enemies(image_manager.enemy1_img, image_manager.enemy2_img,
                                            image_manager.enemy3_img,
                                            image_manager.enemy1_img_str, image_manager.enemy2_img_str,
                                            image_manager.enemy3_img_str, image_manager.enemy_bullet_img,
                                            image_manager.enemy_death_animation_img,
                                            image_manager.enemy_death_animation_img_str)
                enemy_manager.INITIAL_MOVE_COOLDOWN_MAX = 60
                enemy_manager.move_cooldown_counter_max = enemy_manager.INITIAL_MOVE_COOLDOWN_MAX
                enemy_manager.reset_enemy_shooting_probability()
                wall_manager.reset_walls()

            else:
                image_manager.game_over_screen(WINDOW, main_font, game_over_font, WIDTH, HEIGHT, player.score)
                image_manager.game_over_animation_timer += 1
        else:
            image_manager.redraw_window(WINDOW, player,
                                        enemy_manager.all_basic_enemies, enemy_manager.spaceship_enemy,
                                        wall_manager.walls, main_font, small_font, WIDTH)
            if player.is_dying:
                if player.death_animation_cooldown >= 120:
                    player.death_animation_cooldown = 0
                    player.ship_img = image_manager.player_img
                    player.reset_player_position(WIDTH / 2 - image_manager.player_img.get_width() / 2,
                                                 HEIGHT - image_manager.player_img.get_height())
                    enemy_manager.reset_spaceship_enemy()
                    player.lives -= 1
                    player.bullets.clear()
                    enemy_manager.clear_all_enemy_bullets()
                    player.is_dying = False
                    continue
                player.ship_img = image_manager.animate_player_death()
                player.death_animation_cooldown += 1

            else:
                enemy_manager.move_cooldown_counter += 1

                enemy_manager.create_spaceship_enemy(image_manager.spaceship_img,
                                                     image_manager.spaceship_img_str, WIDTH)
                enemy_manager.remove_spaceship_enemy()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                keys = pygame.key.get_pressed()
                enemy_manager.manage_spaceship_enemy_movement()
                if enemy_manager.move_cooldown_counter == enemy_manager.move_cooldown_counter_max:
                    enemy_manager.manage_enemy_movement(SCREEN_MARGIN, WIDTH)
                    image_manager.change_enemy_drawings(enemy_manager.all_basic_enemies, enemy_manager.spaceship_enemy)
                player.handle_player_inputs(keys, WIDTH, SCREEN_MARGIN)
                player.move_bullets(True, HEIGHT, enemy_manager.all_basic_enemies,
                                    enemy_manager.spaceship_enemy, wall_manager.walls)
                enemy_manager.create_enemy_bullets()
                enemy_manager.manage_enemy_bullets(False, HEIGHT, player, wall_manager.walls)

                image_manager.animate_enemy_death(enemy_manager.all_basic_enemies)
                image_manager.animate_spaceship_death(enemy_manager.spaceship_enemy)

                wall_manager.remove_dead_walls()

                if all(len(enemy_list) == 0 for enemy_list in enemy_manager.all_basic_enemies):
                    image_manager.current_level += 1
                    player.lives += 1
                    if image_manager.current_level <= 6:
                        enemy_manager.enemy_start_y += 25
                    enemy_manager.reset_enemies(image_manager.enemy1_img, image_manager.enemy2_img,
                                                image_manager.enemy3_img,
                                                image_manager.enemy1_img_str, image_manager.enemy2_img_str,
                                                image_manager.enemy3_img_str, image_manager.enemy_bullet_img,
                                                image_manager.enemy_death_animation_img,
                                                image_manager.enemy_death_animation_img_str)

    pygame.quit()


if __name__ == '__main__':
    main()
