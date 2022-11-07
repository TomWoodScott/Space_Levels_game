from Main import *
from Classes import *

def settings(data_to_load=None, setting = True):
    main(run=False)
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
