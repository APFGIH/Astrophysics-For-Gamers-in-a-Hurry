from pygame import *
from math import *
from cmath import *
from Minigames.Technicals import *

class Planet:
    def __init__(self, x, y, xvel, yvel, size, mass, pic):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.mass = mass
        self.pic = pic
        self.size = size
        self.rect = [self.x - self.size, self.y - self.size, self.size*2, self.size*2]
        self.polygon = [(self.x - self.size, self.y - self.size), (self.x + self.size, self.y - self.size),
                        (self.x + self.size, self.y + self.size), (self.x - self.size, self.y + self.size)]

    def move(self, planetList):
        self.x += self.xvel
        self.y += self.yvel
        self.rect = [self.x - self.size, self.y - self.size, self.size * 2, self.size * 2]
        self.polygon = [(self.x - self.size, self.y - self.size), (self.x + self.size, self.y - self.size), (self.x + self.size, self.y + self.size), (self.x - self.size, self.y + self.size)]
        for p in planetList:
            if p != self:
                dist = max(1, hypot(self.x - p.x, self.y - p.y))
                ang = atan2(self.y - p.y, self.x - p.x)
                self.xvel += (p.mass / dist**2) * -cos(ang)
                self.yvel += (p.mass / dist**2) * -sin(ang)

    def collidePlanet(self, p):
        return hypot(self.x - p.x, self.y - p.y) <= (p.size + self.size)

    def update(self, screen):
        self.pic(screen, self.x, self.y)



class Asteroid:
    def __init__(self, polygon, x, y, xvel, yvel, pic, nrot):
        self.polygon = polygon
        self.o = self.polygon
        self.a = x
        self.b = y
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.pic = pic
        self.rot = 0
        self.nrot = nrot



    def move(self, planetList):
        self.x += self.xvel
        self.y += self.yvel
        for i in range(len(self.polygon)):
            self.polygon[i] = [self.polygon[i][0]+self.xvel, self.polygon[i][1]+self.yvel]
        for p in planetList:
            if p != self:
                dist = max(1, hypot(self.x - p.x, self.y - p.y))
                ang = atan2(self.y - p.y, self.x - p.x)
                self.xvel += (p.mass / dist**2) * -cos(ang)
                self.yvel += (p.mass / dist**2) * -sin(ang)

    #Rotates polygon hitbox using complex nums
    def rotate(self, theta):
        newPol = []
        self.rot += self.nrot
        self.rot += theta
        for p in self.polygon:
            newPol.append(rotateC(p[0], p[1], self.x, self.y, self.nrot+theta))
        self.polygon = newPol

            

    def collide(self, obj):
        return getBoundingBox(self.polygon).colliderect(getBoundingBox(obj.polygon))
        #return polCollide(self.polygon, obj.polygon)

    def update(self, screen):
        self.pic(screen, self.x, self.y, self.rot)


class fallingStone:
    def __init__(self, x, y, xvel, yvel, size, pic):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.size = size
        self.pic = pic

    def move(self):
        self.x += self.xvel
        self.y += self.yvel

    def collide(self, p):
        return hypot(p[0]-self.x, p[1]-self.y) <= self.size

    def update(self, screen):
        self.pic(screen, self.x, self.y)


class lightBeam:
    def __init__(self, x, y, x2, y2, power, time):
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.power = power
        self.time = time
        self.col = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (100, 0, 100)][power]
        self.strength = (5+power)**2
        self.ang = atan2(y2-y, x2-x)

    def getFocus(self, theta):
        return 75*sin((theta-self.ang))**6

    def update(self, screen):
        self.time -= 1
        draw.line(screen, self.col, (self.x, self.y), (self.x2, self.y2), 5)








