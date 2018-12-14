from pygame import *
from components.mehdi import *
import components.menu as menu
import traceback
import glob

def login():
    pass

# Function to display a formatted crash screen instead of stopping entire program
def crash(error, previous):
    global screen  # Global variable to make resizing easier

    # Blue tint
    tint = Surface(size)
    tint.fill((0, 0, 255))
    tint.set_alpha(99)
    screen.blit(tint, (0, 0))

    # Creates button object
    back_button = menu.Button(size[0] // 4, size[1] - 200, size[0] // 2, 40, previous, "Return")

    # Converts the traceback to list
    error_message = list(map(str, error.split('\n')))

    # Joins the error message from traceback
    about_list = ['',
                  '',
                  ':( Whoops, something went wrong',
                  '', ] + error_message + ['APFPIH (C) Mehzhanquantuyson Inc, All Rahs Reserved',
                                           '',
                                           'Note: If clicking the button below doesnt',
                                           'do anything, the game is beyond broken',
                                           'and needs to be restarted',
                                           '',
                                           '',
                                           '',
                                           'Developed by: Henry Tu, Ryan Zhang, Adam Mehdi, Jason Quan',
                                           'ENG4U 2019',
                                           '']

    while True:
        release = False  # Mouse state

        for e in event.get():
            if e.type == QUIT:
                return 'exit'

            # Update mouse state
            if e.type == MOUSEBUTTONUP and e.button == 1:
                release = True

            # Recall function on resize
            if e.type == VIDEORESIZE:
                screen = display.set_mode((max(e.w, 500), max(e.h, 400)), DOUBLEBUF + RESIZABLE)
                return 'crash', error, previous

        mx, my = mouse.get_pos()
        m_press = mouse.get_pressed()

        # Draws text
        for y in range(0, len(about_list)):
            about_text = text(about_list[y], 15)
            screen.blit(about_text, (size[0] // 2 - about_text.get_width() // 2, 10 + y * 20))

        # Update button
        nav_update = back_button.update(screen, mx, my, m_press, 15, release)

        # Changes page is necessary
        if nav_update is not None:
            return nav_update

        display.update()


# Displays information in a formatted page (Much like crash)
def information(message, previous):
    global screen

    # Creates button object
    back_button = menu.Button(size[0] // 4, size[1] - 200, size[0] // 2, 40, previous, "Okay")

    # Converts the message string into a list
    message_list = list(map(str, message.split('\n')))

    while True:

        # Background
        wallpaper(screen, size)

        release = False  # MOuse state

        for e in event.get():
            if e.type == QUIT:
                return 'exit'

            # Update mouse state
            if e.type == MOUSEBUTTONUP and e.button == 1:
                release = True

            # Update display if resized
            if e.type == VIDEORESIZE:
                screen = display.set_mode((max(e.w, 500), max(e.h, 400)), DOUBLEBUF + RESIZABLE)
                return 'information', message, previous

        mx, my = mouse.get_pos()
        m_press = mouse.get_pressed()

        # Draws text
        for y in range(0, len(message_list)):
            about_text = text(message_list[y], 15)
            screen.blit(about_text, (size[0] // 2 - about_text.get_width() // 2, 10 + y * 20))

        # Update button
        nav_update = back_button.update(screen, mx, my, m_press, 15, release)

        # Update page
        if nav_update is not None:
            return nav_update

        display.update()

#When the player dies
def death(message):
    global screen

    #Draws a red tint for death effect
    tint = Surface(size)
    tint.fill((50, 0, 0))
    tint.set_alpha(99)

    screen.blit(tint, (0, 0))

    #Button params
    buttons = [menu.Button(size[0] // 4, size[1] - 200, size[0] // 2, 40, 'game', "Respawn"),
               menu.Button(size[0] // 4, size[1] - 150, size[0] // 2, 40, 'menu', "Rage quit")]

    # Load the graphics first so there is no delay for sound
    kill_text = text(message, 40)
    screen.blit(kill_text, center(0, 0, *size, *kill_text.get_size()))

    display.flip()

    # Sound effects
    load_sound(['sound/random/classic_hurt.ogg'])
    sound_object = mixer.Sound('sound/sadviolin.ogg')
    sound_object.play(0)

    while True:
        release = False #Mouse state

        for e in event.get():
            if e.type == QUIT:
                return 'exit'

            if e.type == MOUSEBUTTONUP and e.button == 1:
                release = True

            if e.type == VIDEORESIZE: #Resize screen
                screen = display.set_mode((max(e.w, 500), max(e.h, 400)), DOUBLEBUF + RESIZABLE)
                return 'death', message

        mx, my = mouse.get_pos()
        m_press = mouse.get_pressed()

        #Displays death message given by server
        kill_text = text(message, 40)
        screen.blit(kill_text, center(0, 0, *size, *kill_text.get_size()))

        #Updates buttons
        for button in buttons:

            nav_update = button.update(screen, mx, my, m_press, 15, release)

            #Execute function if button pressed
            if nav_update is not None:
                sound_object.stop()

                return nav_update

        display.update()

#Help screen
def assistance():
    global screen #Global screen to make resizing easier

    #Button object
    back_button = menu.Button(size[0] // 4, size[1] - 130, size[0] // 2, 40, 'menu', "Back")

    #Font and help page contents
    normal_font = font.Font("fonts/UndertaleSans.ttf", 14)

    about_list = ['this is some really helpful help']

    while True:

        # Background
        wallpaper(screen, size)

        release = False #Mouse state

        for e in event.get():
            if e.type == QUIT:
                return 'exit'

            #Updates mouse
            if e.type == MOUSEBUTTONUP and e.button == 1:
                release = True

            #Update screen
            if e.type == VIDEORESIZE:
                screen = display.set_mode((max(e.w, 500), max(e.h, 400)), DOUBLEBUF + RESIZABLE)
                return 'assistance'

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

#Options screen
def options():
    global screen #Global screen to make resizing easier

    #Background
    wallpaper(screen, size)

    #UI Objects
    back_button = menu.Button(size[0] // 4, size[1] - 130, size[0] // 2, 40, 'menu', "Back")
    life_switch = menu.Switch(size[0] // 4, size[1] // 2 - 20, size[0] // 2, 40, False, 'Dank memes')
    music_slider = menu.Slider(size[0] // 4, size[1] // 2 - 80, size[0] // 2, 40, music_object.get_volume(), 'Music')

    while True:

        release = False #Resets mouse state

        for e in event.get():
            if e.type == QUIT:
                return 'exit'

            #Mouse update
            if e.type == MOUSEBUTTONUP and e.button == 1:
                release = True

            #Resize
            if e.type == VIDEORESIZE:
                screen = display.set_mode((max(e.w, 500), max(e.h, 400)), DOUBLEBUF + RESIZABLE)
                return 'assistance'

        mx, my = mouse.get_pos()
        m_press = mouse.get_pressed()

        #Updates UI buttons
        nav_update = back_button.update(screen, mx, my, m_press, 15, release)
        music_slider.update(screen, mx, my, m_press, 15, release)
        music_object.set_volume(music_slider.pos)
        life_switch.update(screen, mx, my, m_press, 15, release)

        #Execute functions if any
        if nav_update is not None:
            return nav_update

        display.update()

#Display message while waiting for server to ping back
def status_screen(status, size, screen):
    wallpaper(screen, size)

    #Display text
    connecting_text = text("Updating servers...", 30)
    screen.blit(connecting_text,
                center(0, 0, size[0], size[1], connecting_text.get_width(), connecting_text.get_height()))

    status_text = text(status, 15)
    screen.blit(status_text, center(0, 50, size[0], size[1], status_text.get_width(), status_text.get_height()))

    display.flip()

def menu_screen():

    global screen

    display.set_caption("Astro Physics for Gamers in a Hurry")

    #Params of buttons
    menu_list = [[0, 'game', "Attack Gary"],
                 [1, 'options', "Options"],
                 [2, 'about', "About"],
                 [2, 'assistance', "Help"],
                 [3, 'exit', "Exit"],
                 [4, 'logout', "Logout"]]

    #Create menu object
    main_menu = menu.Menu(menu_list, 0, 0, size[0], size[1])

    #Blits logo and UI elements
    #logo = transform.scale(image.load("textures/menu/logo.png"), (size[0] // 3, int(size[0] // 3 * 51 / 301)))

    while True:
        #Resets wallpaper and graphics
        wallpaper(screen, size)

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

        #version_text = normal_font.render("Astro Physics for Gamers in a Hurry v%s" % current_build, True, (255, 255, 255))
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

    about_list = ['Adam really likes astro physics.',
                  'He is a HUGE nerd.',
                  'lol. nerd.',
                  'this is a space game.',
                  'space is pre good too.']

    clock = time.Clock()

    while True:
        release = False #Mouse state

        wallpaper(screen, size)

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

    load_wallpaper()

    navigation = 'menu'

    UI = {
        'login': login,
        'menu': menu_screen,
        'about': about,
        'assistance': assistance,
        'options': options
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
                navigation = crash(navigation[1], navigation[2])

            elif navigation[0] == 'information':
                navigation = information(navigation[1], navigation[2])

            else:
                navigation = transition(screen, UI[navigation])

        except:
            navigation = 'menu'

            crash(traceback.format_exc(), 'menu')

    mixer.music.stop()
    display.quit()
    raise SystemExit