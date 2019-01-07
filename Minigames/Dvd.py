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

    while running:

        magicX = False
        magicY = False

        keys = key.get_pressed()
        for action in event.get():
            if action.type == QUIT:
                return False
            if action.type == VIDEORESIZE:
                mehdi.resizeStuff(action.w, action.h)

        screen.fill((0, 0, 0))

        if logoRect.top == screenRect.top or logoRect.bottom == screenRect.bottom:
            vy *= -1

            magicY = True

        if logoRect.left == screenRect.left or logoRect.right == screenRect.right:
            vx *= -1

            magicX = True

        if magicX or magicY:
            logoSurf = makeLogo()

        logoRect.x += vx
        logoRect.y += vy

        screen.blit(logoSurf, (ceil(logoRect.x), ceil(logoRect.y)))


        mehdi.drawStuff(screen)
        #display.flip()
        clock.tick(FPS)

        if magicY and magicX:
            print('OMG U GOT CORNER!!!!!')
            return True
    quit()
