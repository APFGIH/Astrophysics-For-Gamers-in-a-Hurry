from pygame import *
from math import *
from random import *
from Minigames.spaceObjects import *
from Minigames.technicals import *
import components.mehdi as mehdi

def solarPropulsion():
    screen = Surface((mehdi.WIDTH, mehdi.HEIGHT))

    FPS = 100
    clock = time.Clock()
    shipx, shipy = mehdi.WIDTH // 2, mehdi.HEIGHT * 0.9
    lightList = []
    running = True
    timer = 3000
    lightGathered = 0
    maxLight = 100000

    def drawPanel(x, y, theta):
        draw.line(screen, (255, 255, 0), (x - 250 * cos(theta), y -10- 250 * sin(theta)), (x + 250 * cos(theta), y -10+ 250 * sin(theta)), 10)
        draw.line(screen, (255, 255, 255), (x - 250*cos(theta), y - 250*sin(theta)), (x + 250*cos(theta), y + 250*sin(theta)), 10)
    theta = pi//4

    mehdi.txtScreen(mehdi.TextBox(
        "Terminal:  The Sun is far too extreme for a spacecraft such as this. To deal with such an issue, we must venture out even further to find a way to fix this constant collapse of space-time. Considering the sheer amount of nuclear reactions occuring on the Sun, we can use the photons released to push our solar sail! How is this possible? Photons have energy, and according to the famous formula E = mc squared, this energy can be treated as mass, therefore it's high velocity gives the photon a measurable memoentum to push the sail. We must point the sail at the photon rays coming through to maximize our velocity and escape before we burn!",
        2,
        int(800), 20,
        (255, 255, 255), 100, 100))

    while running:
        keys = key.get_pressed()
        for action in event.get():
            if action.type == QUIT:
                return False
            if action.type == VIDEORESIZE:
                mehdi.resizeStuff(action.w, action.h)

        screen.fill((0, 0, 0))
        if timer == 0:
            return 0
        else:
            timer -= 1
            if timer % 50 == 0 and randint(1, 100) < 80:
                lightList.append(lightBeam(randint(mehdi.WIDTH*-0.4, mehdi.WIDTH*1.4), mehdi.HEIGHT, mehdi.WIDTH//2, mehdi.HEIGHT//2, randint(0, 4), 100))
        if lightGathered >= maxLight:
            return int(timer/3000)*99+1

        for l in lightList:
            l.update(screen)
            lightGathered += l.getFocus(theta)

        for i in range(len(lightList)-1, -1, -1):
            if lightList[i].time <= 0:
                del lightList[i]

        draw.rect(screen, (255, 255, 255), (int(mehdi.WIDTH*0.2), int(mehdi.HEIGHT*0.08), int(mehdi.WIDTH*0.6), int(mehdi.HEIGHT*0.07)))
        draw.rect(screen, (255, 200, 0), (int(mehdi.WIDTH * 0.21), int(mehdi.HEIGHT * 0.09), int(mehdi.WIDTH * 0.58 * lightGathered / maxLight), int(mehdi.HEIGHT * 0.05)))
        draw.rect(screen, (255, 255, 255), (int(mehdi.WIDTH * 0.2), int(mehdi.HEIGHT * 0.01), int(mehdi.WIDTH * 0.6), int(mehdi.HEIGHT * 0.07)))
        draw.rect(screen, (255, 200, 0), (int(mehdi.WIDTH * 0.21), int(mehdi.HEIGHT * 0.02), int(mehdi.WIDTH * 0.58 * timer / 3000), int(mehdi.HEIGHT * 0.05)))
        if keys[K_LEFT]:
            theta = min(pi//2, theta + 0.01)
        if keys[K_RIGHT]:
            theta = max(-pi//4, theta - 0.01)
        if keys[K_END]:
            return 100


        drawPanel(mehdi.WIDTH // 2, mehdi.HEIGHT // 2, theta)

        mehdi.drawStuff(screen)
        #display.flip()

        clock.tick(FPS)
    quit()


if __name__ == '__main__':

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