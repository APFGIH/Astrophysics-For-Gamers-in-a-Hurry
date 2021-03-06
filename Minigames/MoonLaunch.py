from pygame import *
from math import *
from random import *
from Minigames.spaceObjects import *
from Minigames.technicals import *
import components.mehdi as mehdi


def moonLaunch():

    screen = Surface((mehdi.WIDTH, mehdi.HEIGHT))

    FPS = 100
    clock = time.Clock()
    lives = 3

    moonPic = transform.scale(image.load("textures/spok.jpg"), (80, 60))

    def drawEarth(screen, x, y):
        draw.circle(screen, (255, 0, 0), (int(x), int(y)), 30, 0)

    def drawMoon(screen, x, y):
        screen.blit(moonPic, (int(x-40), int(y-30)))
    running = True

    #Start and end point
    earth = Planet(int(mehdi.WIDTH*0.2), int(mehdi.HEIGHT*0.75), 0, 0, 30, 1000, drawEarth)
    moon = Planet(int(mehdi.WIDTH * 0.9), int(mehdi.HEIGHT * 0.2), 0, 0, 30, 1000, drawMoon)

    #All asteroids.obstacles
    #Asteroid 1
    Ast1x, Ast1y = int(mehdi.WIDTH * 0.4), int(mehdi.HEIGHT * 0.4)
    Ast1Pol = [(Ast1x + -5, Ast1y - 20), (Ast1x, Ast1y-25), (Ast1x + 15, Ast1y - 21), (Ast1x + 5, Ast1y), (Ast1x + 9, Ast1y + 15),
                      (Ast1x - 5, Ast1y + 25), (Ast1x-15, Ast1y + 10), (Ast1x - 5, Ast1y + 15)]
    def drawAst1(screen, x, y, r):
        p = [(x + -5, y - 20), (x, y-25), (x + 15, y - 21), (x + 5, y), (x + 9, y + 15),
                      (x - 5, y + 25), (x-15, y + 10), (x - 5, y + 15)]
        for i in range(len(p)):
            p[i] = [int(j) for j in rotateC(p[i][0], p[i][1], x, y, r)]
        draw.polygon(screen, (180, 180, 180),p
                     , 0)
    Ast1 = Asteroid(Ast1Pol, Ast1x, Ast1y, 0, 0, drawAst1, 0.01)

    #Asteroid 2
    Ast2x, Ast2y = int(mehdi.WIDTH*0.6), int(mehdi.HEIGHT*0.3)
    Ast2Pol = [(Ast2x + -5, Ast2y - 20), (Ast2x, Ast2y - 30), (Ast2x + 15, Ast2y - 15), (Ast2x + 5, Ast2y),
               (Ast2x + 9, Ast2y + 15), (Ast2x - 5, Ast2y + 25), (Ast2x - 20, Ast2y + 10), (Ast2x + -5, Ast2y + 15)]
    def drawAst2(screen, x, y, r):
        p = [(x + -5, y - 20), (x, y - 30), (x + 15, y - 15), (x + 5, y),
               (x + 9, y + 15), (x - 5, y + 25), (x - 20, y + 10), (x + -5, y + 15)]
        for i in range(len(p)):
            p[i] = [int(j) for j in rotateC(p[i][0], p[i][1], x, y, r)]
        draw.polygon(screen, (180, 180, 180),
                     p, 0)
    Ast2 = Asteroid(Ast2Pol, Ast2x, Ast2y, 0, 0, drawAst2, -0.006)

    #Asteroid 3
    Ast3x, Ast3y = int(mehdi.WIDTH*0.6), int(mehdi.HEIGHT*0.4)
    Ast3Pol = [(Ast3x + -5, Ast3y - 20), (Ast2x, Ast3y - 30), (Ast3x + 15, Ast3y - 15), (Ast3x + 5, Ast3y),
               (Ast3x + 9, Ast3y + 15), (Ast3x - 5, Ast3y + 25), (Ast3x - 20, Ast3y + 10), (Ast3x + -5, Ast3y + 15)]
    def drawAst3(screen, x, y, r):
        p = [(x + -5, y - 20), (x, y - 30), (x + 15, y - 15), (x + 5, y),
               (x + 9, y + 15), (x - 5, y + 25), (x - 20, y + 10), (x + -5, y + 15)]
        for i in range(len(p)):
            p[i] = [int(j) for j in rotateC(p[i][0], p[i][1], x, y, r)]
        draw.polygon(screen, (180, 180, 180),
                     p, 0)
    Ast3 = Asteroid(Ast3Pol, Ast3x, Ast3y, 0, 0, drawAst3, -0.007)

    #Asteroid 4
    Ast4x, Ast4y = int(mehdi.WIDTH*0.5), int(mehdi.HEIGHT*0.7)
    Ast4Pol = [(Ast4x + -5, Ast4y - 20), (Ast4x, Ast4y - 30), (Ast4x + 15, Ast4y - 15), (Ast4x + 5, Ast4y),
               (Ast4x + 9, Ast4y + 15), (Ast4x - 5, Ast4y + 25), (Ast4x - 20, Ast4y + 10), (Ast4x + -5, Ast4y + 15)]
    def drawAst4(screen, x, y, r):
        p = [(x + -5, y - 20), (x, y - 30), (x + 15, y - 15), (x + 5, y),
               (x + 9, y + 15), (x - 5, y + 25), (x - 20, y + 10), (x + -5, y + 15)]
        for i in range(len(p)):
            p[i] = [int(j) for j in rotateC(p[i][0], p[i][1], x, y, r)]
        draw.polygon(screen, (180, 180, 180),
                     p, 0)
    Ast4 = Asteroid(Ast4Pol, Ast4x, Ast4y, 0, 0, drawAst4, -0.008)

    #Asteroid 5
    Ast5x, Ast5y = int(mehdi.WIDTH*0.3), int(mehdi.HEIGHT*0.44)
    Ast5Pol = [(Ast5x + -5, Ast5y - 20), (Ast5x, Ast5y - 30), (Ast5x + 15, Ast5y - 15), (Ast5x + 5, Ast5y),
               (Ast5x + 9, Ast5y + 15), (Ast5x - 5, Ast5y + 25), (Ast5x - 20, Ast5y + 10), (Ast5x + -5, Ast5y + 15)]
    def drawAst5(screen, x, y, r):
        p = [(x + -5, y - 20), (x, y - 30), (x + 15, y - 15), (x + 5, y),
               (x + 9, y + 15), (x - 5, y + 25), (x - 20, y + 10), (x + -5, y + 15)]
        for i in range(len(p)):
            p[i] = [int(j) for j in rotateC(p[i][0], p[i][1], x, y, r)]
        draw.polygon(screen, (180, 180, 180),
                     p, 0)
    Ast5 = Asteroid(Ast5Pol, Ast5x, Ast5y, 0, 0, drawAst5, -0.009)

    #Asteroid 6
    Ast6x, Ast6y = int(mehdi.WIDTH*0.78), int(mehdi.HEIGHT*0.31)
    Ast6Pol = [(Ast6x + -5, Ast6y - 20), (Ast6x, Ast6y - 30), (Ast6x + 15, Ast6y - 15), (Ast6x + 5, Ast6y),
               (Ast6x + 9, Ast6y + 15), (Ast6x - 5, Ast6y + 25), (Ast6x - 20, Ast6y + 10), (Ast6x + -5, Ast6y + 15)]
    def drawAst6(screen, x, y, r):
        p = [(x + -5, y - 20), (x, y - 30), (x + 15, y - 15), (x + 5, y),
               (x + 9, y + 15), (x - 5, y + 25), (x - 20, y + 10), (x + -5, y + 15)]
        for i in range(len(p)):
            p[i] = [int(j) for j in rotateC(p[i][0], p[i][1], x, y, r)]
        draw.polygon(screen, (180, 180, 180),
                     p, 0)
    Ast6 = Asteroid(Ast6Pol, Ast6x, Ast6y, 0, 0, drawAst6, 0.011)

    #Spaceship being launched
    def drawShip(screen, x, y, r):
        p = [(x-15, y-25), (x+15, y-25), (x+15, y+15), (x, y+35), (x-15, y+15)]
        for i in range(len(p)):
            p[i] = [int(j) for j in rotateC(p[i][0], p[i][1], x, y, r)]
        draw.polygon(screen, (250, 250, 250), [p[0], p[1], p[2], p[4]], 0)
        draw.polygon(screen, (0, 0, 255), [p[2], p[3], p[4]], 0)
    asteroids = [Ast1, Ast2, Ast3, Ast4, Ast5, Ast6]


    #Actual spaceship
    shipx, shipy = int(mehdi.WIDTH*0.22), int(mehdi.HEIGHT*0.68)
    shipPoly = [(shipx-15, shipy-25), (shipx+15, shipy-25), (shipx+15, shipy+15), (shipx, shipy+35), (shipx-15, shipy+15)]
    spaceShip = Asteroid(shipPoly, int(mehdi.WIDTH*0.21), int(mehdi.HEIGHT*0.69), 0, 0, drawShip, 0)
    launching = False
    shipping = False
    startx, starty = mehdi.WIDTH * 0.2, mehdi.HEIGHT * 0.75
    planets = [earth, moon]

    mehdi.txtScreen(mehdi.TextBox(
        "Terminal: We must escape and venture out to the reaches of space if we are to save the universe. To pass these asteroids and reach the moon, you must launch the ship all the way to the moon without going out of orbit or colliding with an asteroid. Only 3 ships are available to aid your attempts.",
        2,
        int(800), 20,
        (255, 255, 255), 100, 100))

    while running:
        keys = key.get_pressed()
        mx, my = mouse.get_pos()

        frame_pos = mehdi.center_frame(mehdi.screen, screen)

        mx -= frame_pos[0]
        my -= frame_pos[1]

        for action in event.get():
            if action.type == QUIT:
                return False
            elif action.type == MOUSEBUTTONDOWN:

                if action.button == 1:
                    if hypot(mx - mehdi.WIDTH*0.2, my - mehdi.HEIGHT*0.75) <= 60:
                        launching = True

            elif action.type == VIDEORESIZE:
                mehdi.resizeStuff(action.w, action.h)


            elif action.type == MOUSEBUTTONUP and launching:
                if action.button == 1:
                    launching = False
                    shipping = True
                    ang = atan2(my-mehdi.HEIGHT*0.75, mx-mehdi.WIDTH*0.2)+pi
                    spaceShip.rot = ang-pi/2
                    spaceShip.x = startx + 90*cos(ang)
                    spaceShip.y = starty + 90*sin(ang)
                    spaceShip.polygon = [(spaceShip.x-15, spaceShip.y-25), (spaceShip.x+15, spaceShip.y-25), (spaceShip.x+15, spaceShip.y+15), (spaceShip.x, spaceShip.y+35), (spaceShip.x-15, spaceShip.y+15)]
                    for i in range(len(spaceShip.polygon)):
                        spaceShip.polygon[i] = [int(j) for j in rotateC(spaceShip.polygon[i][0], spaceShip.polygon[i][1], spaceShip.x, spaceShip.y, spaceShip.rot)]
                    mag = ((my-mehdi.HEIGHT*0.75)**2 + (mx-mehdi.WIDTH*0.2)**2)**0.5
                    spaceShip.xvel = 0.03*mag*cos(ang)
                    spaceShip.yvel = 0.03*mag*sin(ang)


        if keys[K_END]:
            return 100

        screen.fill((0, 0, 0))

        if shipping:
            spaceShip.update(screen)
            spaceShip.move(planets)
            spaceShip.rotate(-spaceShip.rot+atan2(-spaceShip.xvel, spaceShip.yvel))
            if any([spaceShip.collide(a) for a in asteroids]):
                lives -= 1
                shipping = False
            if spaceShip.collide(moon):
                return lives*33+1

        if lives == 0:
            return 0

        if launching:
            draw.line(screen, (255, 255, 255), (int(startx), int(starty)), (mx, my), 3)

        for a in asteroids:
            a.rotate(0)

        for a in planets+asteroids:
            a.update(screen)

        mehdi.drawStuff(screen)
        clock.tick(FPS)
    quit()

if __name__ == '__main__':
    init()

    screen = display.set_mode((mehdi.WIDTH, mehdi.HEIGHT))

    moonLaunch(screen, 1)





