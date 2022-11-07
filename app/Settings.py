import Main, Classes
import pygame, os

def settings(data_to_load=None, setting = True):
    Main.main(run=False)
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

        Main.window.blit(Main.bg, (0, 0))
        easy_button = Classes.Button(Main.window.get_width() / 2 - easy_button_img.get_width() / 2, 400, easy_button_img)
        medium_button = Classes.Button(Main.window.get_width() / 2 - easy_button_img.get_width() / 2, 500, medium_button_img)
        insane_button = Classes.Button(Main.window.get_width() / 2 - easy_button_img.get_width() / 2, 600, insane_button_img)
        load_button = Classes.Button(Main.window.get_width() / 2 - easy_button_img.get_width() / 2, 700, load_button_img)

        if easy_button.draw(Main.window):
            fps = 60
            setting = False
        if medium_button.draw(Main.window):
            fps = 100
            setting = False
        if insane_button.draw(Main.window):
            fps = 200
            setting = False
        if load_button.draw(Main.window):
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                setting = False
                pygame.quit()

        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(60)

    return Main.main_menu(fps, data_to_load)