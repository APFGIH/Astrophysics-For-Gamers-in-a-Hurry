import pygame

class npc:

    def __init__(self, image, rect, interactionRect, statement, direction):
        self.image = image
        self.collide = interactionRect
        self.statement = statement
        self.direction = direction
        self.imageRect = rect

    def interact(self, player):
        if player.currentPosition == self.direction and self.collide.colliderect(player.playerRect):
            return self.statement
        else:
            return False

    def draw(self, surface, player):
        if self.imageRect.colliderect(player.screenRect):
            surface.blit(self.image, (self.imageRect.x - player.cam_x, self.imageRect.y - player.cam_y))
