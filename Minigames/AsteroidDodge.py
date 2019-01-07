from pygame import *
from math import *
from random import *
from Minigames.spaceObjects import *
from Minigames.technicals import *
import components.mehdi as mehdi

init()

def asteroidDodge():

    screen = Surface((mehdi.WIDTH, mehdi.HEIGHT))

    FPS = 100
    clock = time.Clock()
    shipx, shipy = mehdi.WIDTH // 2, mehdi.HEIGHT * 0.9
    asteroidList = []
    running = True
    timer = 3000

    def drawAst1(screen, x, y):
        draw.circle(screen, (150, 150, 150), (int(x), int(y)), 20, 0)

    def drawShip(x, y):
        p = [(x - 15, y + 25), (x + 15, y + 25), (x + 15, y - 15), (x, y - 35), (x - 15, y - 15)]
        draw.polygon(screen, (250, 250, 250), [p[0], p[1], p[2], p[4]], 0)
        draw.polygon(screen, (0, 0, 255), [p[2], p[3], p[4]], 0)

    mehdi.txtScreen(mehdi.TextBox(mehdi.dialog['asteroidDodge']['dialog'], 2, int(mehdi.WIDTH*0.7), 20, (255, 255, 255), mehdi.WIDTH*0.1, mehdi.HEIGHT*0.1))

    while running:
        keys = key.get_pressed()
        for action in event.get():
            if action.type == QUIT:
                running = False
                break
            if action.type == VIDEORESIZE:
                mehdi.resizeStuff(action.w, action.h)

        screen.fill((0, 0, 0))


        if timer == 0:
            return 100
        else:
            timer -= 1
            if timer % 2 == 0 and randint(1, timer + 5000) <= 2500 and timer > 250:
                asteroidList.append(fallingStone(randint(int(mehdi.WIDTH*0.05), int(mehdi.WIDTH*0.95)), 0, 0, (5000-timer)*randint(80, 120)*0.000008, 30, drawAst1))
            if any([a.collide([shipx, shipy]) for a in asteroidList]):
                return 0

        for a in asteroidList:
            a.update(screen)
            a.move()
        for i in range(len(asteroidList)-1, -1, -1):
            if asteroidList[i].y > mehdi.HEIGHT*1.2:
                del asteroidList[i]

        draw.rect(screen, (255, 255, 255), (int(mehdi.WIDTH * 0.2), int(mehdi.HEIGHT * 0.01), int(mehdi.WIDTH * 0.6), int(mehdi.HEIGHT * 0.07)))
        draw.rect(screen, (255, 200, 0), (int(mehdi.WIDTH * 0.21), int(mehdi.HEIGHT * 0.02), int(mehdi.WIDTH * 0.58 * timer / 3000), int(mehdi.HEIGHT * 0.05)))

        drawShip(shipx, shipy)
        if keys[K_LEFT]:
            shipx = max(mehdi.WIDTH*0.05, shipx-5)
        if keys[K_RIGHT]:
            shipx = min(mehdi.WIDTH*0.95, shipx+5)

        mehdi.drawStuff(screen)
        #display.flip()
        clock.tick(FPS)
    quit()
