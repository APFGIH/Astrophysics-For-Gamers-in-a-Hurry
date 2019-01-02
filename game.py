import components.mehdi
from pygame import *
from Map.Map import *
import Minigames.AsteroidDodge


class game:

    def __init__(self, screen):
        self.mainScreen = screen
        self.gameClock = time.Clock()
        self.playerSize = 100
        self.multiplier = 1
        self.init_display_size = (1080, 720)
        self.current_display = (1080, 720)
        self.display_surface = (1080, 720)
        self.aspect_ratio = self.init_display_size[0] / self.init_display_size[1]

        self.gameScreen = Surface(self.current_display)
        self.map = Map(self.gameScreen)

        self.medhi = components.mehdi.medhi(self.map, self.gameScreen)

        self.medhigames = {1: Minigames.AsteroidDodge.asteroidDodge}

    def update(self):
        # Draw World
        self.map.make_map(self.gameScreen, (self.medhi.cam_x, self.medhi.cam_y))
        # Player
        self.medhi.update()
        draw.rect(self.gameScreen, (255, 255, 255), (self.medhi.x - self.medhi.cam_x, self.medhi.y - self.medhi.cam_y, self.playerSize, self.playerSize))

        # Update Game Screen
        self.mainScreen.blit(transform.scale(self.gameScreen, self.display_surface), (int(self.current_display[0]/2-self.display_surface[0]/2), int(int(self.current_display[1]/2-self.display_surface[1]/2))))
        display.update()
        self.gameScreen.fill((200, 200, 200))

    def game(self):
        running = True

        while running:
            self.gameClock.tick(120)
            for e in event.get():
                if e.type == QUIT:
                    running = False
                    break
                elif e.type == KEYDOWN:
                    self.medhi.keyDown(e.key)
                elif e.type == KEYUP:
                    self.medhi.keyUp(e.key)
                elif e.type == VIDEORESIZE:
                    self.multiplier = min(e.w / self.init_display_size[0], e.h / self.init_display_size[1])
                    self.current_display = (e.w, e.h)
                    if e.w / self.aspect_ratio <= e.h:
                        self.display_surface = (e.w, int(e.w / self.aspect_ratio))
                    else:
                        self.display_surface = (int(e.h * self.aspect_ratio), e.h)
                    self.mainScreen = display.set_mode((e.w, e.h), RESIZABLE | HWSURFACE)

                    print(e, self.aspect_ratio)

            #screen.fill((0, 0, 0))

            keys = key.get_pressed()

            if keys[K_p]:
                for p in self.map.portals:
                    print(p, self.medhi.playerRect)
                    if self.medhi.playerRect.colliderect(p[0]):
                        try:
                            self.medhigames[int(p[1])](screen, 100)
                        except:
                            print(p[1])

            # mx, my = mouse.get_pressed()[:2]

            self.update()


if __name__ == "__main__":
    init()
    screen = display.set_mode((1080, 720), RESIZABLE | HWSURFACE)
    g = game(screen)

    g.game()
    quit()
