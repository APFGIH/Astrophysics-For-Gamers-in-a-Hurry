import pygame
import math

class npc:

    def __init__(self, image, rect, interactionRect, statement, direction):
        self.image = image
        self.collide = interactionRect
        self.statement = statement
        self.direction = direction
        self.imageRect = rect

    def interact(self, player):
        if math.hypot(player.playerRect.center[0] - self.collide.center[0], player.playerRect.center[1] - self.collide.center[1]) < 150:
            return self.statement
        else:
            return False

    def draw(self, surface, player):
        if self.imageRect.colliderect(player.screenRect):
            surface.blit(self.image, (self.imageRect.x - player.cam_x, self.imageRect.y - player.cam_y))
