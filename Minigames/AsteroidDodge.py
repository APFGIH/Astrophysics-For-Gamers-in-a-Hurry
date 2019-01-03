from pygame import *
from math import *
from random import *
from Minigames.SpaceObjects import *
from Minigames.Technicals import *
from components.mehdi import *

init()

def asteroidDodge(health, drawScreen, resizeScreen):

    WIDTH, HEIGHT = 1080, 720

    screen = Surface((WIDTH, HEIGHT))

    FPS = 100
    clock = time.Clock()
    shipx, shipy = WIDTH // 2, HEIGHT * 0.9
    asteroidList = []
    running = True
    timer = 6000

    def drawAst1(screen, x, y):
        draw.circle(screen, (150, 150, 150), (int(x), int(y)), 20, 0)

    def drawShip(x, y):
        p = [(x - 15, y + 25), (x + 15, y + 25), (x + 15, y - 15), (x, y - 35), (x - 15, y - 15)]
        draw.polygon(screen, (250, 250, 250), [p[0], p[1], p[2], p[4]], 0)
        draw.polygon(screen, (0, 0, 255), [p[2], p[3], p[4]], 0)

    howto = "To exit the moon and ~go to Jupiter, there's an obstacle in the way. We must make it through the asteroid belt that lies between Mars and Jupiter. It's filled with giant lumps of rock and metal, over 200000 of them! It's your job to make it through without getting hit on your way there. The actual asteroid belt isn't as densely packed as this, in fact it's actually very spread out, but that wouldn't be fun, now would it?"
    intro = TextBox(howto, 2, int(WIDTH*0.7), 20, (255, 255, 255), WIDTH*0.1, HEIGHT*0.1)
    txtScreen(intro)

    while running:
        keys = key.get_pressed()
        for action in event.get():
            if action.type == QUIT:
                running = False
                break
            if action.type == VIDEORESIZE:
                resizeScreen(action.w, action.h)


        screen.fill((0, 0, 0))

        if timer == 0:
            return 100
        else:
            timer -= 1
            if timer % 2 == 0 and randint(1, timer + 5000) <= 2500 and timer > 250:
                asteroidList.append(fallingStone(randint(int(WIDTH*0.05), int(WIDTH*0.95)), 0, 0, (11000-timer)*randint(80, 120)*0.000009, 30, drawAst1))
            if any([a.collide([shipx, shipy]) for a in asteroidList]):
                return 0

        for a in asteroidList:
            a.update(screen)
            a.move()
        for i in range(len(asteroidList)-1, -1, -1):
            if asteroidList[i].y > HEIGHT*1.2:
                del asteroidList[i]

        drawShip(shipx, shipy)
        if keys[K_LEFT]:
            shipx = max(WIDTH*0.05, shipx-5)
        if keys[K_RIGHT]:
            shipx = min(WIDTH*0.95, shipx+5)

        drawScreen(screen)
        #display.flip()
        clock.tick(FPS)
    quit()
