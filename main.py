from pygame import *
from datetime import datetime
from components.mehdi import *
import components.menu as menu
import components.flame as flame
import game
import traceback
import glob

from Minigames.SolarPropulsion import *

# This function logs the user into the game
def login():
    display.set_caption("RahCraft Authentication Service")

    global screen, size, username, password  # Global var used to make modifying easier

    # Sets title
    title_text = text('Welcome to RahCraft! Login to continue', 20)
    screen.blit(title_text, (size[0] // 2 - title_text.get_width() // 2, size[1] // 4 - title_text.get_height() - 50))

    # Resets credential vars
    username, password = '', ''

    # Field accepting entry
    field_selected = 'Username'

    # List with field objects
    fields = {'Username': [menu.TextBox(size[0] // 4, size[1] // 2 - 100, size[0] // 2, 40, 'Username'), username],
              'Password': [menu.TextBox(size[0] // 4, size[1] // 2 - 30, size[0] // 2, 40, 'Password'), password]}

    # Button objects
    exit_button = menu.Button(size[0] // 4, size[1] // 2 + 200, size[0] // 2, 40, 'exit', 'Exit game')
    auth_button = menu.Button(size[0] // 4, size[1] // 2 + 50, size[0] // 2, 40, 'auth', 'Login')
    signup_button = menu.Button(size[0] // 4, size[1] // 2 + 100, size[0] // 2, 40, 'signup', 'Need an account? Signup here')

    while True:

        # Draws background
        wallpaper(screen)

        # Resets mouse vars
        click = False
        release = False

        # Var to pass the event to text field
        pass_event = None

        for e in event.get():

            pass_event = e

            if e.type == QUIT:
                return 'exit'

            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                click = True

            if e.type == MOUSEBUTTONUP and e.button == 1:
                release = True

            if e.type == KEYDOWN:
                # Shift enter to bypass auth
                if key.get_mods() & KMOD_CTRL and key.get_mods() & KMOD_SHIFT:
                    if e.key == K_RETURN and username:
                        return 'menu'

                # Enter to auth with credentials
                elif e.key == K_RETURN and fields['Username'][1] and fields['Password'][1]:
                    username, password = fields['Username'][1], flame.hash(fields['Password'][1], fields['Username'][1])

                    return 'auth'

                # Tab to alternate between fields
                if e.key == K_TAB:
                    if field_selected == 'Username':
                        field_selected = 'Password'
                    else:
                        field_selected = 'Username'

            # If resize, recall the function to redraw
            if e.type == VIDEORESIZE:
                screen = display.set_mode((max(e.w, 500), max(e.h, 400)), DOUBLEBUF + RESIZABLE)
                return 'login'

        mx, my = mouse.get_pos()
        m_press = mouse.get_pressed()

        # Get values from textfields
        fields[field_selected][1] = fields[field_selected][0].update(pass_event)

        # Draws and updates textfields
        for field in fields:
            fields[field][0].draw(screen, field_selected)

            if fields[field][0].rect.collidepoint(mx, my) and click:
                field_selected = field

        # Create account, redirect to website
        if signup_button.update(screen, mx, my, m_press, 15, release):
            return 'register'

        # Authenticate with credentials
        nav_update = auth_button.update(screen, mx, my, m_press, 15, release)
        if nav_update and fields['Username'][1] and fields['Password'][1]:
            # Hash password and set as var for security + match server
            username, password = fields['Username'][1], flame.hash(fields['Password'][1], fields['Username'][1])

            print(username, password)

            return nav_update

        # Exit game
        nav_update = exit_button.update(screen, mx, my, m_press, 15, release)
        if nav_update:
            return nav_update

        display.update()

def register():
    display.set_caption("RahCraft Authentication Service")

    global screen, size, username, password  # Global var used to make modifying easier

    # Sets title
    title_text = text('dis is da register', 20)
    screen.blit(title_text, (size[0] // 2 - title_text.get_width() // 2, size[1] // 4 - title_text.get_height() - 50))

    # Resets credential vars
    username, password = '', ''

    # Field accepting entry
    field_selected = 'Username'

    # List with field objects
    fields = {'Username': [menu.TextBox(size[0] // 4, size[1] // 2 - 170, size[0] // 2, 40, 'Username'), username],
              'Password1': [menu.TextBox(size[0] // 4, size[1] // 2 - 100, size[0] // 2, 40, 'Password'), password],
              'Password2': [menu.TextBox(size[0] // 4, size[1] // 2 - 30, size[0] // 2, 40, 'Password Confirmation'), password]}

    # Button objects
    exit_button = menu.Button(size[0] // 4, size[1] // 2 + 200, size[0] // 2, 40, 'exit', 'Exit game')
    register_button = menu.Button(size[0] // 4, size[1] // 2 + 50, size[0] // 2, 40, 'register_service', 'Register')
    login_button = menu.Button(size[0] // 4, size[1] // 2 + 100, size[0] // 2, 40, 'login', 'Already have an account? Login here')

    field_names = list(fields.keys())

    while True:

        # Draws background
        wallpaper(screen)

        # Resets mouse vars
        click = False
        release = False

        # Var to pass the event to text field
        pass_event = None

        for e in event.get():

            pass_event = e

            if e.type == QUIT:
                return 'exit'

            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                click = True

            if e.type == MOUSEBUTTONUP and e.button == 1:
                release = True

            if e.type == KEYDOWN:
                # Shift enter to bypass auth
                if key.get_mods() & KMOD_CTRL and key.get_mods() & KMOD_SHIFT:
                    if e.key == K_RETURN and username:
                        return 'menu'

                # Enter to auth with credentials
                elif e.key == K_RETURN and fields['Username'][1] and fields['Password1'][1] and fields['Password2'][1]:

                    if fields['Password1'][1] != fields['Password2'][1]:
                        return "information", 'Passwords do not match.', "login"

                    else:
                        username, password = fields['Username'][1], flame.hash(fields['Password1'][1], fields['Username'][1])

                        return 'register_service'

                # Tab to alternate between fields
                if e.key == K_TAB:

                    field_selected = field_names[(field_names.index(field_selected) + 1) % len(field_names)]

            # If resize, recall the function to redraw
            if e.type == VIDEORESIZE:
                screen = display.set_mode((max(e.w, 500), max(e.h, 400)), DOUBLEBUF + RESIZABLE)
                return 'register'

        mx, my = mouse.get_pos()
        m_press = mouse.get_pressed()

        # Get values from textfields
        fields[field_selected][1] = fields[field_selected][0].update(pass_event)

        # Draws and updates textfields
        for field in fields:
            fields[field][0].draw(screen, field_selected)

            if fields[field][0].rect.collidepoint(mx, my) and click:
                field_selected = field

        # Create account, redirect to website
        if login_button.update(screen, mx, my, m_press, 15, release):
            return 'login'

        # Authenticate with credentials
        nav_update = register_button.update(screen, mx, my, m_press, 15, release)
        if nav_update and fields['Username'][1] and fields['Password1'][1] and fields['Password2'][1]:

            if fields['Password1'][1] != fields['Password2'][1]:
                return "information", 'Passwords do not match.', "login"

            else:
                username, password = fields['Username'][1], flame.hash(fields['Password1'][1], fields['Username'][1])

                return 'register_service'

        # Exit game
        nav_update = exit_button.update(screen, mx, my, m_press, 15, release)
        if nav_update:
            return nav_update

        display.update()

def register_service():
    global username, password

    # Background
    wallpaper(screen)
    connecting_text = text("Processing request...", 30)
    screen.blit(connecting_text,
                center(0, 0, size[0], size[1], connecting_text.get_width(), connecting_text.get_height()))

    display.update()

    try:  # Try except incase connection fails

        msg = flame.register(username, password)

        print(msg)

        if msg == True:
            return 'menu'

        # If rejected
        else:
            # Clears fields
            username = ''
            password = ''

            return "information", msg, "login"

    except:
        return "information", '\n\n\n\n\nUnable to connect to authentication servers\nTry again later\n\n\nVisit rahmish.com/status.php for help', "login"

def token_authenticate():
    global username, password

    # Background
    wallpaper(screen)
    connecting_text = text("Authenticating...", 30)
    screen.blit(connecting_text,
                center(0, 0, size[0], size[1], connecting_text.get_width(), connecting_text.get_height()))

    if flame.cucumber():
        return 'menu'

    else:
        return 'login'


def authenticate():
    global username, password

    # Background
    wallpaper(screen)
    connecting_text = text("Authenticating...", 30)
    screen.blit(connecting_text,
                center(0, 0, size[0], size[1], connecting_text.get_width(), connecting_text.get_height()))

    display.update()

    try:  # Try except incase connection fails

        if flame.authenticate(username, password):
            return 'menu'

        # If rejected
        else:
            # Clears fields
            username = ''
            password = ''

            return 'reject'

    except:
        return "information", '\n\n\n\n\nUnable to connect to authentication servers\nTry again later\n\n\nVisit rahmish.com/status.php for help', "login"


# Function if credentials are rejected by authentication server
def reject():
    global screen  # Global variable to make resizing easier

    # Creates button object
    back_button = menu.Button(size[0] // 4, size[1] - 130, size[0] // 2, 40, 'login', "Back")

    normal_font = font.Font("fonts/UndertaleSans.ttf", 14)

    # Text contents
    auth_list = ['',
                 '',
                 '',
                 'AUTHENTICATION FAILED',
                 '',
                 'Username or Password is invalid',
                 'Ensure capslock is disabled and credentials',
                 'match those provided at time of account creation',
                 '',
                 'If you forget your password, reset it at',
                 'rahmish.com/management.php',
                 '',
                 '',
                 'RahCraft (C) Rahmish Empire, All Rahs Reserved',
                 '',
                 'Developed by: Henry Tu, Ryan Zhang, Syed Safwaan',
                 'ICS3U 2017'
                 ]

    while True:
        # Mouse state
        release = False

        # Background
        wallpaper(screen)

        for e in event.get():
            if e.type == QUIT:
                return 'exit'

            # Updates mouse state
            if e.type == MOUSEBUTTONUP and e.button == 1:
                release = True

            # Recall function on resize to redraw everything
            if e.type == VIDEORESIZE:
                screen = display.set_mode((max(e.w, 500), max(e.h, 400)), DOUBLEBUF + RESIZABLE)

                return 'reject'

        mx, my = mouse.get_pos()
        m_press = mouse.get_pressed()

        # Draws text on screen
        for y in range(0, len(auth_list)):
            about_text = normal_font.render(auth_list[y], True, (255, 255, 255))
            screen.blit(about_text, (size[0] // 2 - about_text.get_width() // 2, 50 + y * 20))

        # Updates buttons
        nav_update = back_button.update(screen, mx, my, m_press, 15, release)

        # Redirects if needed
        if nav_update is not None:
            return nav_update

        # Updates screen
        display.update()

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
        wallpaper(screen)

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
def leaderboard():
    global screen #Global screen to make resizing easier

    #Button object
    back_button = menu.Button(size[0] // 4, size[1] - 130, size[0] // 2, 40, 'menu', "Back")

    #Font and help page contents
    normal_font = font.Font("fonts/UndertaleSans.ttf", 14)

    # {
    #   "name": "Karl ZHu",
    #   "score": 69,
    #   "lastLogin": 90000
    # }


    about_list = [["Name ", "High Score ", "Last Login "]]

    for user in flame.getLeaderboard():
        about_list.append([user['name'] + " ", str(user['score']) + " ", datetime.utcfromtimestamp(user['lastLogin']).strftime('%Y-%m-%d %H:%M:%S') + " "])

    bar = normal_font.render("|", True, (255, 255, 255))
    while True:

        # Background
        wallpaper(screen)

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
                return 'leaderboard'

        mx, my = mouse.get_pos()
        m_press = mouse.get_pressed()

        #Draws about screen contents
        for y in range(0, len(about_list)):
            name = normal_font.render(about_list[y][0], True, (255, 255, 255))
            score = normal_font.render(about_list[y][1], True, (255, 255, 255))
            timestamp = normal_font.render(about_list[y][2], True, (255, 255, 255))
            screen.blit(bar, (size[0] // 2 - 300, 50 + y * 20))
            screen.blit(name, (size[0] // 2 - 100 - name.get_width(), 50 + y * 20))
            screen.blit(bar, (size[0] // 2 - 100, 50 + y * 20))
            screen.blit(score, (size[0] // 2 + 100 - score.get_width(), 50 + y * 20))
            screen.blit(bar, (size[0] // 2 + 100, 50 + y * 20))
            screen.blit(timestamp, (size[0] // 2 + 300 - timestamp.get_width(), 50 + y * 20))
            screen.blit(bar, (size[0] // 2 + 300, 50 + y * 20))

        #Updates button
        nav_update = back_button.update(screen, mx, my, m_press, 15, release)

        #Execute function if any
        if nav_update is not None:
            return nav_update

        display.update()

#Display message while waiting for server to ping back
def status_screen(status, size, screen):
    wallpaper(screen)

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
                 [1, 'about', "About"],
                 [1, 'leaderboard', "Leaderboard"],
                 [2, 'exit', "Exit"],
                 [3, 'logout', "Logout"]]

    #Create menu object
    main_menu = menu.Menu(menu_list, 0, 0, size[0], size[1])

    logo = transform.scale(image.load("textures/menu/gamelogo.png"), (size[0] // 2, int(size[0] // 6)))

    while True:
        #Resets wallpaper and graphics
        wallpaper(screen)

        screen.blit(logo, (size[0] // 2 - logo.get_width() // 2, size[1] // 2 - 100 - logo.get_height()))

        #Renders all text elements
        normal_font = font.Font("fonts/UndertaleSans.ttf", 14)

        version_text = normal_font.render("Astro Physics for Gamers in a Hurry v3.14.15.92.65i", True, (255, 255, 255))
        screen.blit(version_text, (10, size[1] - 20))

        about_text = normal_font.render("Copyright (C) APGIH Dev Squad. All Rahs Reserved!", True, (255, 255, 255))
        screen.blit(about_text, (size[0] - about_text.get_width(), size[1] - 20))

        user_text = normal_font.render("Logged in as: %s" % flame.master_user['username'], True, (255, 255, 255))
        screen.blit(user_text, (20, 20))

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

                flame.logout()

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

    about_list = ['Developed by:',
                  'Henry Tu (github.com/henrytwo)',
                  'Yuan Song (Ryan) Zhang (github.com/ryanz34)',
                  'Adam Mehdi (github.com/AdamMedee)',
                  'Jason Quan (killerwhale303 on Steam)',
                  '',
                  '',
                  'Music: Undertale Megalovania remix by SayMaxWell',
                  '',
                  '',
                  'Facts: simple.wikipedia.org',
                  '',
                  '',
                  'ENG4U ISU PROJECT',
                  'Based on github.com/RahCraft/RahCraft (ICS3U FSE)']

    clock = time.Clock()

    while True:
        release = False #Mouse state

        wallpaper(screen)

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

    size = (1080, 720)
    screen = display.set_mode(size, DOUBLEBUF + RESIZABLE)

    mixer.pre_init(44100, -16, 1, 4096)
    init()

    display.set_caption("Astro Physics for Gamers in a Hurry")

    meh_screen(screen)

    init_dialog()
    init_stars(size)
    set_screen(screen)

    navigation = 'token'

    UI = {
        'login': login,
        'token': token_authenticate,
        'menu': menu_screen,
        'about': about,
        'leaderboard': leaderboard,
        'auth': authenticate,
        'reject': reject,
        'register': register,
        'register_service': register_service
    }

    music_object = mixer.Sound('sounds/menu.ogg')
    music_object.play(-1, 0)

    print(multipleChoice(generate_quiz()))

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
                music_object.stop()

                g = game.game(screen)

                navigation = g.game()

                flame.save()

                #print('Outcome:', solarPropulsion(1, drawStuff, resizeStuff))

            elif navigation[0] == 'crash':
                navigation = crash(navigation[1], navigation[2])

            elif navigation[0] == 'information':
                navigation = information(navigation[1], navigation[2])

            else:
                #navigation = transition(screen, UI[navigation])
                navigation = UI[navigation]()

        except:
            navigation = 'menu' if flame.authenticated() else 'login'

            crash(traceback.format_exc(), 'menu')

    flame.save()

    mixer.music.stop()
    display.quit()
    raise SystemExit