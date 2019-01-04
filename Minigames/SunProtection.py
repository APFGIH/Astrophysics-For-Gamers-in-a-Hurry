from pygame import *
from math import *
from random import *
from Minigames.spaceObjects import *
from Minigames.technicals import *
from components.mehdi import *


def SunProtection(screen):

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

    hp = 2000
    theta = 0
    timer = 6000
    lightList = []

    while running:
        keys = key.get_pressed()
        for action in event.get():
            if action.type == QUIT:
                running = False
                break
            if action.type == VIDEORESIZE:
                resizeStuff(action.w, action.h)

        screen.fill((0, 0, 0))
        draw.line(screen, (150, 150, 150), (WIDTH//2+200*cos(theta-0.2), HEIGHT//4+200*sin(theta-0.2)), (WIDTH//2+200*cos(theta+0.2), HEIGHT//4+200*sin(theta+0.2)), 15)
        if keys[K_LEFT]:
            theta = min(pi, theta + 0.05)
        if keys[K_RIGHT]:
            theta = max(0, theta - 0.05)

        if timer == 0:
            return int(hp/2000)*99+1
        else:
            timer -= 1
            if timer % 50 == 0 and randint(1, 100) < 70:
                lightList.append(lightBeam(randint(0, WIDTH), HEIGHT, WIDTH//2, HEIGHT//4, randint(0, 4), 50))

        for l in lightList:
            l.update(screen)
            if abs(l.ang-theta+pi) > 0.2:
               hp -= 1
               l.x2, l.y2 = WIDTH//2, HEIGHT//4
            else:
                mag = ((WIDTH//2 - l.x)**2 + (HEIGHT//4 - l.y)**2)**0.5 - 200
                l.x2, l.y2 = int(l.x+mag*cos(l.ang)), (l.y+mag*sin(l.ang))

        if hp <= 0:
            return 0

        draw.rect(screen, (255, 255, 255), (int(WIDTH * 0.2), int(HEIGHT * 0.08), int(WIDTH * 0.6), int(HEIGHT * 0.07)))
        draw.rect(screen, (255, 200, 0), (
        int(WIDTH * 0.21), int(HEIGHT * 0.09), int(WIDTH * 0.58 * hp / 2000), int(HEIGHT * 0.05)))
        draw.rect(screen, (255, 255, 255), (int(WIDTH * 0.2), int(HEIGHT * 0.01), int(WIDTH * 0.6), int(HEIGHT * 0.07)))
        draw.rect(screen, (255, 200, 0),
                  (int(WIDTH * 0.21), int(HEIGHT * 0.02), int(WIDTH * 0.58 * timer / 6000), int(HEIGHT * 0.05)))

        for i in range(len(lightList)-1, -1, -1):
            if lightList[i].time == 0:
                del lightList[i]

        drawStuff(screen)
        clock.tick(FPS)
    quit()

#SunProtection(screen, 1)