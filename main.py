from pygame import *
from components.mehdi import *
import traceback
import glob

def login():
    pass

def menu():
    return 'about'

def about():
    global screen

    #Button object
    #back_button = menu.Button(size[0] // 4, size[1] - 130, size[0] // 2, 40, 'menu', "Back")

    #Font and help page contents
    normal_font = font.Font("fonts/Lato-Black.ttf", 14)

    frame = 0

    about_list = ['HELP',
                  '------------------------------------',
                  'BOIII',
                  'SO YOU WANNA PLAY DIS GAME HUH?',
                  'WELL ITS RLLY EZ ACTUALLY',
                  'LEGIT',
                  'YOU TAKE UR FINGERS',
                  'PRESS DOWN',
                  'ON UR KEYBOARD',
                  'AND UR DONE.',
                  'DO U SEE THAT PERIOD????',
                  'IT MEANS *MIC DROP*',
                  '',
                  'THATS RIGHT',
                  'ANYWAYS, GOD SAVE THE QUEEN',
                  'LONG LIVE THE RAHMISH EMPIRE',
                  '',
                  '',
                  'Actually just goto rahmish.com 4 help',
                  '']

    frames = []

    print('loading')

    for file in range(2, 200):
        frames.append(image.load('textures/space/%03i.jpg' % file))
        print(file)

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
                return 'help'

        mx, my = mouse.get_pos()
        m_press = mouse.get_pressed()

        #Draws about screen contents
        for y in range(0, len(about_list)):
            about_text = normal_font.render(about_list[y], True, (255, 255, 255))
            screen.blit(about_text, (size[0] // 2 - about_text.get_width() // 2, 50 + y * 20))

        #Updates button
        #nav_update = back_button.update(screen, mx, my, m_press, 15, release)

        nav_update = None

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

    navigation = 'about'

    UI = {
        'login': login,
        'menu': menu,
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