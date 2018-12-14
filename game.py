import components.mehdi
from pygame import *
from Map.Map import *

class game:

    def __init__(self, screen):
        self.medhi = components.mehdi.medhi()
        #self.map = Map()
        self.gameScreen = screen
        self.gameClock = time.Clock()
        self.playerSize = 100
        self.multiplier = 1
        self.displaysize = (960, 540)

    def update(self):
        self.medhi.update(self.multiplier)
        display.update()

    def game(self):
        running = True
        while running:
            self.gameClock.tick(60)
            for e in event.get():
                if e.type == QUIT:
                    running = False
                    break
                elif e.type == KEYDOWN:
                    self.medhi.keyDown(e.key)
                elif e.type == KEYUP:
                    self.medhi.keyUp(e.key)
                elif e.type == VIDEORESIZE:
                    setGet()
                    self.multiplier = min(e.w / self.displaysize[0], e.h / self.displaysize[1])

            screen.fill((0, 0, 0))

            keys = key.get_pressed()
            #mx, my = mouse.get_pressed()[:2]

            draw.rect(self.gameScreen, (255, 255, 255), (self.medhi.game_x, self.medhi.game_y, self.playerSize * self.multiplier, self.playerSize * self.multiplier))

            self.update()


if __name__ == "__main__":
    init()
    screen = display.set_mode((960, 540), RESIZABLE)
    g = game(screen)

    g.game()
    quit()
