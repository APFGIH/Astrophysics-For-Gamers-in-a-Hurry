from pygame import *
from components.mehdi import *
import components.menu as menu
import traceback
import glob

def login():
    pass

def menu_screen():

    global screen

    display.set_caption("RahCraft")

    #Params of buttons
    menu_list = [[0, 'server_picker', "Connect to server"],
                 [1, 'options', "Options"],
                 [2, 'about', "About"],
                 [2, 'assistance', "Help"],
                 [3, 'exit', "Exit"],
                 [4, 'logout', "Logout"]]

    #Create menu object
    main_menu = menu.Menu(menu_list, 0, 0, size[0], size[1])

    #Blits logo and UI elements
    #logo = transform.scale(image.load("textures/menu/logo.png"), (size[0] // 3, int(size[0] // 3 * 51 / 301)))

    frame = 0

    while True:

        if frame < len(frames) - 1:
            frame += 1
        else:
            frame = 0

        #Resets wallpaper and graphics
        wallpaper(screen, size, frame, frames)

        #text_surface_final = Surface((text_surface.get_width() + 4, text_surface.get_height() + 4), SRCALPHA)

        #screen.blit(logo, (size[0] // 2 - logo.get_width() // 2, size[1] // 2 - 120 - logo.get_height()))
        #text_surface_final.blit(text_shadow, (2, 2))
        #text_surface_final.blit(text_surface, (0, 0))

        #Rotates MOTD
        #rotation += rotation_v

        #Reverses direction if limit hit
        #if rotation < 0 or rotation > 10:
        #    rotation_v *= -1

        #Blits MOTD
        #text_surface_final = transform.rotate(text_surface_final, rotation)
        #screen.blit(text_surface_final, (size[0] // 2 - text_surface_final.get_width() // 2 + 100, size[1] // 2 - 170))


        #Renders all text elements
        normal_font = font.Font("fonts/UndertaleSans.ttf", 14)

        #version_text = normal_font.render("RahCraft v%s" % current_build, True, (255, 255, 255))
        #screen.blit(version_text, (10, size[1] - 20))

        about_text = normal_font.render("Copyright (C) Rahmish Empire. All Rahs Reserved!", True, (255, 255, 255))
        screen.blit(about_text, (size[0] - about_text.get_width(), size[1] - 20))

        #user_text = normal_font.render("Logged in as: %s" % username, True, (255, 255, 255))
        #screen.blit(user_text, (20, 20))

        #if token:
        #    user_text = normal_font.render("AUTH ID: %s" % token, True, (255, 255, 255))
        #    screen.blit(user_text, (20, 50))

        release = False

        for e in event.get():
            if e.type == QUIT:
                return 'exit'

            #Mouse update
            if e.type == MOUSEBUTTONUP and e.button == 1:
                release = True

            #Resize
            if e.type == VIDEORESIZE:
                screen = display.set_mode((max(e.w, 657), max(e.h, 505)), DOUBLEBUF + RESIZABLE)
                return 'menu'

        mx, my = mouse.get_pos()
        m_press = mouse.get_pressed()

        #Update buttons
        nav_update = main_menu.update(screen, release, mx, my, m_press)

        #If button pressed
        if nav_update:
            #Logout
            if nav_update == 'logout':

                #Clear session
                username = ''
                token = ''

                #Erases session file
                with open('user_data/session.json', 'w') as session_file:
                    session_file.write('')

                return 'login'


            else:
                return nav_update

        display.update()


def about():
    global screen

    #Button object
    back_button = menu.Button(size[0] // 4, size[1] - 130, size[0] // 2, 40, 'menu', "Back")

    #Font and help page contents
    normal_font = font.Font("fonts/UndertaleSans.ttf", 16)

    frame = 0

    about_list = ['Adam really likes astro physics.',
                  'He is a HUGE nerd.',
                  'lol. nerd.',
                  'this is a space game.',
                  'space is pre good too.']

    clock = time.Clock()

    while True:
        release = False #Mouse state

        wallpaper(screen, size, frame, frames)

        if frame < len(frames) - 1:
            frame += 1
        else:
            frame = 0

        for e in event.get():
            if e.type == QUIT:
                return 'exit'

            #Updates mouse
            if e.type == MOUSEBUTTONUP and e.button == 1:
                release = True

            #Update screen
            if e.type == VIDEORESIZE:
                screen = display.set_mode((max(e.w, 500), max(e.h, 400)), DOUBLEBUF + RESIZABLE)
                return 'about'

        mx, my = mouse.get_pos()
        m_press = mouse.get_pressed()

        #Draws about screen contents
        for y in range(0, len(about_list)):
            about_text = normal_font.render(about_list[y], True, (255, 255, 255))
            screen.blit(about_text, (size[0] // 2 - about_text.get_width() // 2, 50 + y * 20))

        #Updates button
        nav_update = back_button.update(screen, mx, my, m_press, 15, release)

        #Execute function if any
        if nav_update is not None:
            return nav_update

        display.update()
        clock.tick(30)

if __name__ == '__main__':
    size = (960, 540)
    screen = display.set_mode(size, DOUBLEBUF + RESIZABLE)

    init()

    display.set_caption("Astro Physics for Gamers in a Hurry")

    meh_screen(screen)

    frames = []

    print('loading')

    for file in range(2, 200):
        frames.append(image.load('textures/space/%03i.jpg' % file))

    navigation = 'menu'

    UI = {
        'login': login,
        'menu': menu_screen,
        'about': about
    }

    while navigation != 'exit':
        # Ensures display is within min size to prevent overlap
        size = (screen.get_width(), screen.get_height())

        screen_update = False

        if size[0] < 657:
            size = (657, size[1])
            screen_update = True

        if size[1] < 505:
            size = (size[0], 505)
            screen_update = True

        if screen_update:
            screen = display.set_mode(size, DOUBLEBUF + RESIZABLE)

        try:
            #Handles each function depending on their required params since no params can be passed in dictionary
            if not navigation:
                raise Exception('You broke something')
            elif navigation == 'game':
                pass
                #music_object.stop()
                #game_nav = Game.game(screen, username, token, host, port, size)

                #navigation = game_nav

            elif navigation[0] == 'crash':
                pass
                #navigation = crash(navigation[1], navigation[2])

            elif navigation[0] == 'information':
                pass
                #navigation = information(navigation[1], navigation[2])

            else:
                navigation = UI[navigation]()

        except:
            navigation = 'menu'

            print(traceback.format_exc())
            #Prints error if any
            #crash(traceback.format_exc(), 'menu')

    #Closes game and terminates pygame
    mixer.music.stop()
    display.quit()
    raise SystemExit