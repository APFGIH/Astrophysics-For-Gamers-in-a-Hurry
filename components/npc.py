import pygame
import math
import components.mehdi as mehdi
import components.flame as flame

class npc:

    def __init__(self, image, rect, statement):
        self.image = image
        self.collide = self.imageRect = rect
        self.statement = []

        for s in statement.split():
            if mehdi.dialog[s]["singleTrigger"]:
                if s not in flame.master_user['dialogCompleted']:
                    self.statement.append([mehdi.dialog[s], s])
                else:
                    pass
            else:
                self.statement.append([mehdi.dialog[s], s])

    def interact(self, player):
        if math.hypot(player.playerRect.center[0] - self.collide.center[0], player.playerRect.center[1] - self.collide.center[1]) < 150:
            newdialog = []
            currentdialog = []
            for dialog in self.statement:
                currentdialog.append(dialog[0]['dialog'])
                if dialog[0]["singleTrigger"]:
                    flame.master_user['dialogCompleted'].append(dialog[1])
                else:
                    newdialog.append(dialog)

            self.statement = newdialog
            return currentdialog

        else:
            return False

    def draw(self, surface, player):
        if self.imageRect.colliderect(player.screenRect):
            surface.blit(self.image, (self.imageRect.x - player.cam_x, self.imageRect.y - player.cam_y))
