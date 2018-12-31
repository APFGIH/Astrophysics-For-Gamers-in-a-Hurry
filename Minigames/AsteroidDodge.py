from pygame import *
from SpaceObjects import *
from Technicals import *
from random import *
from math import *
init()

WIDTH, HEIGHT = 1080, 720
screen = display.set_mode((WIDTH, HEIGHT))

def asteroidDodge(screen, health):

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

    while running:
        keys = key.get_pressed()
        for action in event.get():
            if action.type == QUIT:
                running = False
                break

        screen.fill((0, 0, 0))

        if timer == 0:
            return True
        else:
            timer -= 1
            if timer % 2 == 0 and randint(1, timer + 5000) <= 2500 and timer > 250:
                asteroidList.append(fallingStone(randint(WIDTH*0.05, WIDTH*0.95), 0, 0, (11000-timer)*randint(80, 120)*0.000009, 20, drawAst1))
            if any([a.collide([shipx, shipy]) for a in asteroidList]):
                return False

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

        display.flip()
        clock.tick(FPS)
    quit()

asteroidDodge(screen, 1)