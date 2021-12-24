import random

import pygame.event

from Classes import *

import time

# ----------------------------------------------------------------------------------

pygame.font.init()
pygame.mixer.init()
pygame.init()
# constants
WIDTH, HEIGHT = 400, 900

WHITE, BLACK, RED, YELLOW, GREEN, GREY, GOLD = (255, 255, 255), (0, 0, 0), (255, 0, 0), (255, 255, 0), \
                                               (0, 255, 0), (69, 62, 49), (207, 172, 21)

# spaceship constants                to do: add medium, advanced, master if needed
SPACESHIP_BASIC_WIDTH, SPACESHIP_BASIC_HEIGHT = 55, 40
SPACESHIP_BASIC_START_X, SPACESHIP_BASIC_START_Y = WIDTH / 2 - SPACESHIP_BASIC_WIDTH / 2, HEIGHT - 100
SPACESHIP_BASIC_VELOCITY = 5
# images
bg = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))
spaceship_basic = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'spaceship_basic.png')),
                                         (SPACESHIP_BASIC_WIDTH, SPACESHIP_BASIC_HEIGHT))
spaceship_medium = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'spaceship_medium.png')),
                                          (SPACESHIP_BASIC_WIDTH, SPACESHIP_BASIC_HEIGHT))
spaceship_advanced = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'spaceship_advanced.png')),
                                            (SPACESHIP_BASIC_WIDTH + 10, SPACESHIP_BASIC_HEIGHT))
spaceship_master = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'spaceship_master.png')),
                                          (SPACESHIP_BASIC_WIDTH + 10, SPACESHIP_BASIC_HEIGHT))
meteor_basic_img = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'meteor_4.png')), (100, 80))
meteor_int_img = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'meteor_2.png')), (75, 75))
meteor_boss_img = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'meteor_3.png')), (200, 200))
basic_bullet_img = pygame.transform.scale(
    pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'bullet_img.png')), 90), (4, 10))
advanced_bullet_img = pygame.transform.scale(
    pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'bullet_advanced.png')), 270),
    (10, 30))
master_bullet_img = pygame.transform.scale(
    pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'bullet_master.png')), 90), (6, 100))

# Sounds.  To do: fix bugs
pygame.mixer.music.load(os.path.join('Assets', "music.mp3"))
pygame.mixer.music.play(-1)

# display
pygame.display.set_caption("Space Levels")
window = pygame.display.set_mode((WIDTH, HEIGHT))
main_font = pygame.font.SysFont("comicsans", 20)
level_font = pygame.font.SysFont("Impact", 100)


# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

def main(FPS=60):
    run = True
    clock = pygame.time.Clock()
    enemies = [Enemy(random.randrange(50, WIDTH - 100), -100, meteor_basic_img)]
    player_dic = {0: Player(SPACESHIP_BASIC_START_X, SPACESHIP_BASIC_START_Y, spaceship_medium, basic_bullet_img)}

    level, lives, hp = 1, 10, 10
    wave_size = 5


    # create visuals
    def draw_window():

        player = player_dic[0]
        window.blit(bg, (0, 0))
        lives_label = main_font.render("Lives: " + str(hp), 1, WHITE)
        level_label = main_font.render("Level: " + str(level), 1, WHITE)
        game_over_label = level_font.render("GAME OVER", 1, WHITE)

        red_hp = pygame.draw.rect(window, RED, (WIDTH / 2 - 100, HEIGHT - 50, 200, 20))
        green_hp = pygame.draw.rect(window, GREEN, (WIDTH / 2 - 100, HEIGHT - 50, 200 * hp / lives, 20))

        window.blit(level_label, (WIDTH - lives_label.get_width() - 10, 10))
        window.blit(lives_label, (10, 10))
        window.blit(window, red_hp, (WIDTH / 2 - 100, HEIGHT - 50, 200, 20))
        window.blit(window, green_hp, (WIDTH / 2 - 100, HEIGHT - 50, 200 * hp / lives, 20))

        power_bar_dull = pygame.draw.rect(window, GREY, (WIDTH / 2 - 100, HEIGHT - 22, 200, 10))
        window.blit(window, power_bar_dull, (WIDTH - 24, HEIGHT - 50, 5, 20))

        temp_power_bar = 200 * player.power_bar / 20
        power_bar_inside = pygame.draw.rect(window, GOLD, (WIDTH / 2 - 100, HEIGHT - 22, temp_power_bar, 10))
        window.blit(window, power_bar_inside, (WIDTH - 24, HEIGHT - 50, 5, 20))

        if hp <= 0:
            window.blit(bg, (0, 0))
            window.blit(game_over_label,
                        (WIDTH / 2 - game_over_label.get_width() / 2, HEIGHT / 2 - game_over_label.get_height() / 2))

        # to do: add score above, depending on score choose index appropriately

        # player_level = 2
        if player.image == spaceship_advanced:
            if player.player_score >= 500:
                player.level_up(spaceship_master, master_bullet_img)
                Player.level_up_shoot_speed()

        # player_level = 1
        if player.image == spaceship_medium:
            if player.player_score >= 250:
                player.level_up(spaceship_advanced, advanced_bullet_img)
                Player.level_up_shoot_speed()

        player.draw(window)

        for enemy in enemies:
            enemy.draw(window)

        pygame.display.update()

    while run:

        clock.tick(FPS)
        # append number of enemies depending on level
        if len(enemies) == 0:
            level += 1
            wave_size = int(wave_size + 5)

            # every five levels have a boss level
            if level % 5 != 0:
                for i in range(wave_size):
                    enemy_dic = {0: Enemy(random.randrange(50, WIDTH - 100),
                                          random.randrange(-1500, -100),
                                          meteor_basic_img),
                                 1: Enemy(random.randrange(50, WIDTH - 100),
                                          random.randrange(-1500, -100),
                                          meteor_int_img, vel=1, health=3, dmg=2, score=10),
                                 2: Enemy(random.randrange(50, WIDTH - 100),
                                          random.randrange(-110, -100),
                                          meteor_boss_img, vel=0.5, health=10, dmg=6, score=50)}
                    meteor = enemy_dic[random.choice([0, 1])]
                    enemies.append(meteor)
            else:
                meteor = enemy_dic[2]
                enemies.append(meteor)

        # quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # enemies movement plus damage
        for enemy in enemies:
            enemy.move()
            if enemy.y >= HEIGHT:
                hp -= enemy.damage
                enemies.remove(enemy)

        # Player static method overseeing player movement and appending bullets
        Player.spaceship_movement(pygame.key.get_pressed(), player_dic[0])

        # player method overseeing the movement of bullets, enemy-bullet collisions, removing enemies, removing bullets,
        # incrementing score and power bar
        player_dic[0].move_bullets(enemies)
        draw_window()

        # remove enemies for cleaner display, re_draw window (now with "game over"), break out of while loop
        if hp <= 0:
            for enemy in enemies:
                enemies.remove(enemy)
            draw_window()
            time.sleep(5)
            run = False


# ----------------------------------------------------------------------

def main_menu(fps=60):
    menu = True
    pygame.display.set_caption("Main Menu")
    start_button_img = pygame.transform.scale(pygame.image.load(os.path.join
                                                                ('Assets', 'start_button_img.png')), (270, 90))
    settings_button_img = pygame.transform.scale(pygame.image.load(os.path.join
                                                                   ('Assets', 'settings_button_img.png')), (270, 90))

    while menu:

        window.blit(bg, (0, 0))
        start_button = Button(window.get_width()/2 - start_button_img.get_width()/2, 200, start_button_img)
        settings_button = Button(window.get_width()/2 - start_button_img.get_width()/2, 300, settings_button_img)
        if start_button.draw(window):
            main(fps)
        if settings_button.draw(window):
            settings()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                pygame.quit()

        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(60)


def settings():
    setting = True
    pygame.display.set_caption("Settings")
    easy_button_img = pygame.transform.scale(pygame.image.load(os.path.join
                                                                ('Assets', 'easy_button.png')), (90, 60))
    medium_button_img = pygame.transform.scale(pygame.image.load(os.path.join
                                                                   ('Assets', 'medium_button.png')), (90, 60))
    insane_button_img = pygame.transform.scale(pygame.image.load(os.path.join
                                                                   ('Assets', 'insane_button.png')), (90, 60))

    while setting:

        window.blit(bg, (0, 0))
        easy_button = Button(window.get_width()/4-35, 400, easy_button_img)
        medium_button = Button(window.get_width()*2/4-35, 400, medium_button_img)
        insane_button = Button(window.get_width()*3/4-35, 400, insane_button_img)
        if easy_button.draw(window):
            fps = 60
            setting = False
        if medium_button.draw(window):
            fps = 100
            setting = False
        if insane_button.draw(window):
            fps = 200
            setting = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                setting = False
                pygame.quit()

        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(60)

    return main_menu(fps)





if __name__ == '__main__':
    main_menu()
