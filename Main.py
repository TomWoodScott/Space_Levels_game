import pickle
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

SPACESHIP_BASIC_START_X, SPACESHIP_BASIC_START_Y = WIDTH / 2 - 55 / 2, HEIGHT - 100
SPACESHIP_BASIC_VELOCITY = 5
# images
bg = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

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
m_button_img = pygame.transform.scale(pygame.image.load(os.path.join
                                                        ('Assets', 'm_button.png')), (90, 90))

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

def main(FPS=60, data_to_load=None, level=0):
    run = True
    clock = pygame.time.Clock()
    Enemy.append(Enemy(random.randrange(50, WIDTH - 100), -100, meteor_basic_img))

    if data_to_load is not None:
        player = Player(SPACESHIP_BASIC_START_X, SPACESHIP_BASIC_START_Y, data_to_load[0], data_to_load[1],
                        data_to_load[2],
                        data_to_load[3], data_to_load[4], data_to_load[5], data_to_load[6], data_to_load[7])
    else:
        player = Player(SPACESHIP_BASIC_START_X, SPACESHIP_BASIC_START_Y)

    # create visuals
    def draw_window():
        window.blit(bg, (0, 0))
        lives_label = main_font.render("Lives: " + str(player.health), 1, WHITE)
        level_label = main_font.render("Level: " + str(player.level), 1, WHITE)
        game_over_label = level_font.render("GAME OVER", 1, WHITE)

        m_button = Button(5, HEIGHT - 80, m_button_img)
        if m_button.draw(window):
            save_load(player.stats())

        red_hp = pygame.draw.rect(window, RED, (WIDTH / 2 - 100, HEIGHT - 50, 200, 20))
        green_hp = pygame.draw.rect(window, GREEN,
                                    (WIDTH / 2 - 100, HEIGHT - 50, 200 * player.health / player.MAX_HP, 20))

        window.blit(level_label, (WIDTH - lives_label.get_width() - 10, 10))
        window.blit(lives_label, (10, 10))
        window.blit(window, red_hp, (WIDTH / 2 - 100, HEIGHT - 50, 200, 20))
        window.blit(window, green_hp, (WIDTH / 2 - 100, HEIGHT - 50, 200, 20))

        power_bar_dull = pygame.draw.rect(window, GREY, (WIDTH / 2 - 100, HEIGHT - 22, 200, 10))
        window.blit(window, power_bar_dull, (WIDTH - 24, HEIGHT - 50, 5, 20))

        temp_power_bar = 200 * player.power_bar / 20
        power_bar_inside = pygame.draw.rect(window, GOLD, (WIDTH / 2 - 100, HEIGHT - 22, temp_power_bar, 10))
        window.blit(window, power_bar_inside, (WIDTH - 24, HEIGHT - 50, 5, 20))

        if player.health <= 0:
            window.blit(bg, (0, 0))
            window.blit(game_over_label,
                        (WIDTH / 2 - game_over_label.get_width() / 2, HEIGHT / 2 - game_over_label.get_height() / 2))

        Player.level_time(player)

        player.draw(window)
        for enemy in Enemy.ENEMIES:
            enemy.draw(window)

        pygame.display.update()

    while run:

        clock.tick(FPS)
        # append number of enemies depending on level
        if len(Enemy.ENEMIES) == 0:
            level += 1
            wave_size = level * 5

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
                    Enemy.append(meteor)
            else:
                meteor = enemy_dic[2]
                Enemy.append(meteor)

        # quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # enemies movement plus damage
        for enemy in Enemy.ENEMIES:
            enemy.move(player)

        # Player static method overseeing player movement and appending bullets
        Player.spaceship_movement(pygame.key.get_pressed(), player)

        # player method overseeing the movement of bullets, enemy-bullet collisions, removing enemies, removing bullets,
        # incrementing score and power bar
        player.move_bullets()
        draw_window()

        # remove enemies for cleaner display, re_draw window (now with "game over"), break out of while loop
        if player.health <= 0:
            for enemy in Enemy.ENEMIES:
                Enemy.ENEMIES.remove(enemy)
            draw_window()
            time.sleep(5)
            run = False


# ----------------------------------------------------------------------

def main_menu(fps=60, data_to_load=None):
    menu = True
    pygame.display.set_caption("Main Menu")
    start_button_img = pygame.transform.scale(pygame.image.load(os.path.join
                                                                ('Assets', 'start_button_img.png')), (270, 90))
    settings_button_img = pygame.transform.scale(pygame.image.load(os.path.join
                                                                   ('Assets', 'settings_button_img.png')), (270, 90))

    while menu:

        window.blit(bg, (0, 0))
        start_button = Button(window.get_width() / 2 - start_button_img.get_width() / 2, 200, start_button_img)
        settings_button = Button(window.get_width() / 2 - start_button_img.get_width() / 2, 300, settings_button_img)

        if start_button.draw(window):
            main(fps, data_to_load)
        if settings_button.draw(window):
            settings(data_to_load=None)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                pygame.quit()

        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(60)


def settings(data_to_load=None):
    setting = True
    pygame.display.set_caption("Settings")
    easy_button_img = pygame.transform.scale(pygame.image.load(os.path.join
                                                               ('Assets', 'easy_button.png')), (270, 90))
    medium_button_img = pygame.transform.scale(pygame.image.load(os.path.join
                                                                 ('Assets', 'medium_button.png')), (270, 90))
    insane_button_img = pygame.transform.scale(pygame.image.load(os.path.join
                                                                 ('Assets', 'insane_button.png')), (270, 90))
    load_button_img = pygame.transform.scale(pygame.image.load(os.path.join
                                                               ('Assets', 'load_button.png')), (270, 90))

    while setting:

        window.blit(bg, (0, 0))
        easy_button = Button(window.get_width() / 2 - easy_button_img.get_width() / 2, 400, easy_button_img)
        medium_button = Button(window.get_width() / 2 - easy_button_img.get_width() / 2, 500, medium_button_img)
        insane_button = Button(window.get_width() / 2 - easy_button_img.get_width() / 2, 600, insane_button_img)
        load_button = Button(window.get_width() / 2 - easy_button_img.get_width() / 2, 700, load_button_img)

        if easy_button.draw(window):
            fps = 60
            setting = False
        if medium_button.draw(window):
            fps = 100
            setting = False
        if insane_button.draw(window):
            fps = 200
            setting = False
        if load_button.draw(window):
            name = input(f'Please enter user name: ') + '.pkl'
            try:
                with open(name, 'rb') as load_game:
                    data = pickle.load(load_game)
                    main_menu(data_to_load=data)
            except FileNotFoundError:
                print(f'{name[:-4]} is not a save file')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                setting = False
                pygame.quit()

        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(60)

    return main_menu(fps, data_to_load)


def save_load(stats=None, fps=None):
    print(stats)
    save_load_level = True
    pygame.display.set_caption("Settings")
    save_button_img = pygame.transform.scale(pygame.image.load(os.path.join
                                                               ('Assets', 'save_button.png')), (270, 90))
    load_button_img = pygame.transform.scale(pygame.image.load(os.path.join
                                                               ('Assets', 'load_button.png')), (270, 90))

    while save_load_level:

        window.blit(bg, (0, 0))
        save_button = Button(window.get_width() / 2 - save_button_img.get_width() / 2, 400, save_button_img)
        load_button = Button(window.get_width() / 2 - load_button_img.get_width() / 2, 500, load_button_img)
        clear_button = Button(window.get_width() / 2 - load_button_img.get_width() / 2, 600, load_button_img)
        i, j = 0, 0
        if save_button.draw(window):
            if i == 0:
                i += 1
                name = input(f'Please enter user name: ') + '.pkl'
                with open(name, 'wb') as save_game:
                    pickle.dump(stats, save_game)

        if load_button.draw(window):
            if j == 0:
                name = input(f'Please enter user name: ') + '.pkl'
                try:
                    with open(name, 'rb') as load_game:
                        data = pickle.load(load_game)
                        main_menu(data_to_load=data)
                except FileNotFoundError:
                    print(f'{name[:-4]} does not exist, please try again')
                j += 1

        if clear_button.draw(window):
            name = input(f'Please enter the user you would like to clear: ') + '.pkl'
            try:
                with open(name, 'rb') as file:
                    file.close()
            except FileNotFoundError:
                print(f'{name[:-4]} does not exist, please try again')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_load_level = False
                pygame.quit()

        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(60)

    return main(load=True, load_the_player=data, level=1)


if __name__ == '__main__':
    main_menu()
