import numpy as np
from math import *
from pygame import *

#Points need to be counter clockwise
def polCollide(p1, p2):
    for i in range(len(p1)):
        for j in range(len(p2)):
            if lineIntersect((p1[i], p1[(i+1)%len(p1)]), (p2[j], p2[(j+1)%len(p2)])):
                return True
    return False

def lineIntersect(l1, l2):
    if l1[1][0] == l1[0][0]:
        if l2[1][0] == l2[0][0]:
            if l2[1][0] == l1[1][0]:
                return max(min(l1[0][1], l1[1][1]), min(l2[0][1], l2[1][1])) <= min(max(l1[0][1], l1[1][1]),
                                                                                    max(l2[0][1], l2[1][1]))
            else:
                return False
        else:
            m2 = (l2[1][1] - l2[0][1]) / (l2[1][0] - l2[0][0])
            b2 = l2[0][1] - m2 * l2[0][0]
            y = m2 * l1[0][0] + b2
            return min(l1[0][1], l1[1][1]) <= y <= max(l1[0][1], l1[1][1])
    if l2[1][0] == l2[0][0]:
        m1 = (l1[1][1] - l1[0][1]) / (l1[1][0] - l1[0][0])
        b1 = l1[0][1] - m1 * l1[0][0]
        y = m1 * l2[0][0] + b1
        return min(l2[0][1], l2[1][1]) <= y <= max(l2[0][1], l2[1][1])
    m1 = (l1[1][1] - l1[0][1]) / (l1[1][0] - l1[0][0])
    m2 = (l2[1][1] - l2[0][1]) / (l2[1][0] - l2[0][0])
    b1 = l1[0][1] - m1 * l1[0][0]
    b2 = l2[0][1] - m2 * l2[0][0]
    if m1 == m2:

        if b1 == b2:
            return max(min(l1[0][0], l1[1][0]), min(l2[0][0], l2[1][0])) <= min(max(l1[0][0], l1[1][0]),
                                                                                max(l2[0][0], l2[1][0]))
        else:
            return False
    else:
        x = (b2 - b1) / (m1 - m2)
        return max(min(l1[0][0], l1[1][0]), min(l2[0][0], l2[1][0])) <= x <= min(max(l1[0][0], l1[1][0]),
                                                                                 max(l2[0][0], l2[1][0]))


def rotateC(x, y, cx, cy, theta):
    return [cx + (x-cx)*cos(theta) - (y-cy)*sin(theta), cy + (x-cx)*sin(theta) + (y-cy)*cos(theta)]



