from pygame import *
from math import *
from random import *
from Minigames.SpaceObjects import *
from Minigames.Technicals import *
from components.mehdi import *


def solarPropulsion(health, drawScreen, resizeScreen):

    screen = Surface((WIDTH, HEIGHT))

    FPS = 100
    clock = time.Clock()
    shipx, shipy = WIDTH // 2, HEIGHT * 0.9
    lightList = []
    running = True
    timer = 3000
    lightGathered = 0
    maxLight = 100000

    def drawPanel(x, y, theta):
        draw.line(screen, (255, 255, 0), (x - 250 * cos(theta), y -10- 250 * sin(theta)), (x + 250 * cos(theta), y -10+ 250 * sin(theta)), 10)
        draw.line(screen, (255, 255, 255), (x - 250*cos(theta), y - 250*sin(theta)), (x + 250*cos(theta), y + 250*sin(theta)), 10)
    theta = pi//4



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
            return False
        else:
            timer -= 1
            if timer % 50 == 0 and randint(1, 100) < 80:
                lightList.append(lightBeam(randint(WIDTH*-0.4, WIDTH*1.4), HEIGHT, WIDTH//2, HEIGHT//2, randint(0, 4), 100))
        if lightGathered >= maxLight:
            return True

        for l in lightList:
            l.update(screen)
            lightGathered += l.getFocus(theta)

        for i in range(len(lightList)-1, -1, -1):
            if lightList[i].time <= 0:
                del lightList[i]



        draw.rect(screen, (255, 255, 255), (int(WIDTH*0.2), int(HEIGHT*0.08), int(WIDTH*0.6), int(HEIGHT*0.07)))
        draw.rect(screen, (255, 200, 0), (int(WIDTH * 0.21), int(HEIGHT * 0.09), int(WIDTH * 0.58 * lightGathered / maxLight), int(HEIGHT * 0.05)))
        draw.rect(screen, (255, 255, 255), (int(WIDTH * 0.2), int(HEIGHT * 0.01), int(WIDTH * 0.6), int(HEIGHT * 0.07)))
        draw.rect(screen, (255, 200, 0), (int(WIDTH * 0.21), int(HEIGHT * 0.02), int(WIDTH * 0.58 * timer / 3000), int(HEIGHT * 0.05)))
        if keys[K_LEFT]:
            theta = min(pi//2, theta + 0.01)
        if keys[K_RIGHT]:
            theta = max(-pi//4, theta - 0.01)


        drawPanel(WIDTH // 2, HEIGHT // 2, theta)

        drawScreen(screen)
        #display.flip()

        clock.tick(FPS)
    quit()


if __name__ == '__main__':

    WIDTH, HEIGHT = 1080, 720
    screen = display.set_mode((1366, 768))

    def center(a, b):
        sw = a.get_width()
        sh = a.get_height()

        w = b.get_width()
        h = b.get_height()

        return (sw // 2 - w // 2, sh // 2 - h // 2)


    def drawStuff(surface):
        screen.fill((255, 255, 0))
        screen.blit(surface, center(screen, surface))

        display.flip()

    print(solarPropulsion(1, drawStuff))