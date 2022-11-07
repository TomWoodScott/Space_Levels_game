
import Main, Classes
import pygame, os

def save_load(stats=None, fps=None, save_load_level = True):

    Main.main(run=False)
    
    pygame.display.set_caption("Settings")
    save_button_img = pygame.transform.scale(pygame.image.load(os.path.join
                                                               ('Assets', 'save_button.png')), (270, 90))
    load_button_img = pygame.transform.scale(pygame.image.load(os.path.join
                                                               ('Assets', 'load_button.png')), (270, 90))
    remove_button_img = pygame.transform.scale(pygame.image.load(os.path.join
                                                               ('Assets', 'remove_button.png')), (270, 90))

    while save_load_level:

        Main.window.blit(Main.bg, (0, 0))
        save_button = Classes.Button(Main.window.get_width() / 2 - save_button_img.get_width() / 2, 400, save_button_img)
        load_button = Classes.Button(Main.window.get_width() / 2 - load_button_img.get_width() / 2, 500, load_button_img)
        clear_button = Classes.Button(Main.window.get_width() / 2 - remove_button_img.get_width() / 2, 600, remove_button_img)

        if save_button.draw(Main.window):
            save_data(stats=stats)


        if load_button.draw(Main.window):
            data = load_data(name=input(f'Name: '))
            print(data)


        if clear_button.draw(Main.window):
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_load_level = False
                pygame.quit()

        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(60)

    return Main.main(load=True, load_the_player=data, level=1)


def save_data(stats):
    name = str(input('Please enter user name: '))
    with open('save.txt', 'a') as save_game:
        save_game.write(str(name) + ':' + str(stats) + '\n')
    save_game.close()
        

def load_data(name):
    data_file = open('save.txt', 'r')
    data = data_file.readlines()
    try:
        for line in data:
            name_found, name_data = line.partition(':')
            if name == name_found:
                yield name_data
                data_file.close()
    except FileNotFoundError:
        print(f'{name[:-4]} does not exist, please try again')

        
        
