from pygame import *
from math import *
from random import *
from Minigames.spaceObjects import *
from Minigames.technicals import *
import components.mehdi as mehdi

init()

logo = image.load('textures/dvd.png')


def makeLogo():
    panel = Surface((logo.get_width(), logo.get_height()))

    panel.fill((randint(0, 255), randint(0, 255), randint(0, 255)))
    panel.blit(logo, (0, 0))

    return panel

def dvd():

    screen = Surface((mehdi.WIDTH, mehdi.HEIGHT))

    mehdi.game_music_object.stop()

    mehdi.end_music_object.play(-1, 0)

    mehdi.ending = True

    end_text = mehdi.dialog['ending']['dialog'].split('~')

    #logo = transform.scale(logo, (300, int(logo.get_height() * (300 / logo.get_width()))))

    logoSurf = makeLogo()

    FPS = 60
    clock = time.Clock()

    running = True

    x = mehdi.WIDTH // 2 - logoSurf.get_width() // 2
    y = mehdi.HEIGHT // 2 - logoSurf.get_height() // 2

    logoRect = Rect(x, y, logoSurf.get_width(), logoSurf.get_height())
    screenRect = Rect(0, 0, mehdi.WIDTH, mehdi.HEIGHT)

    vx = randint(500000, 1000000) / 500000 * (-1 if randint(0, 1) == 0 else 1)
    vy = randint(500000, 1000000) / 500000 * (-1 if randint(0, 1) == 0 else 1)

    points = []

    normal_font = font.Font("fonts/UndertaleSans.ttf", 16)

    offset = mehdi.HEIGHT

    while running:
        offset -= 0.5

        magicX = False
        magicY = False

        keys = key.get_pressed()
        for action in event.get():
            if action.type == QUIT:
                quit()
            if action.type == VIDEORESIZE:
                mehdi.resizeStuff(action.w, action.h)

        if keys[K_END]:
            return 100

        screen.fill((0, 0, 0))

        if logoRect.top == screenRect.top or logoRect.bottom == screenRect.bottom:
            points.append((logoRect.x, logoRect.y))

            vy *= -1

            magicY = True

        if logoRect.left == screenRect.left or logoRect.right == screenRect.right:
            points.append((logoRect.x, logoRect.y))

            vx *= -1

            magicX = True

        if magicX or magicY:
            logoSurf = makeLogo()

        logoRect.x += vx
        logoRect.y += vy

        if len(points) > 1:
            for i in range(1, len(points)):
                draw.line(screen, (255, 255, 255), points[i - 1], points[i], 1)

            draw.line(screen, (255, 255, 255), points[-1], (logoRect.x, logoRect.y), 1)

        screen.blit(logoSurf, (ceil(logoRect.x), ceil(logoRect.y)))

        for line in range(len(end_text)):
            screen.blit(normal_font.render(end_text[line], True, (255, 255, 255)), (10, int(offset + line * 20)))

        mehdi.drawStuff(screen)
        #display.flip()
        clock.tick(FPS)

        if magicY and magicX:
            print('OMG U GOT CORNER!!!!!')
            return True
    quit()
