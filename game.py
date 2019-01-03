import components.mehdi
from pygame import *
from Map.Map import *
import Minigames.AsteroidDodge
import traceback

class game:

    def __init__(self, screen):
        self.mainScreen = screen

        self.mainScreen.fill((0, 0, 0))

        loading_text = components.mehdi.text("Loading...", 30)

        self.mainScreen.blit(loading_text,
                             components.mehdi.center(0, 0, self.mainScreen.get_width(), self.mainScreen.get_height(), loading_text.get_width(), loading_text.get_height()))

        display.flip()

        self.gameClock = time.Clock()
        self.playerSize = 40
        self.multiplier = 1
        self.init_display_size = (1080, 720)
        self.current_display = (1080, 720)
        self.display_surface = (1080, 720)
        self.aspect_ratio = self.init_display_size[0] / self.init_display_size[1]

        self.gameScreen = Surface(self.current_display)
        self.map = Map(self.gameScreen)

        self.medhi = components.mehdi.medhi(self.map, self.gameScreen)

        self.medhigames = {1: Minigames.AsteroidDodge.asteroidDodge}

        self.resize(Rect(0, 0, screen.get_width(), screen.get_height()))

    def update(self):
        # Draw World
        self.map.make_map(self.gameScreen, (self.medhi.cam_x, self.medhi.cam_y))
        # Player
        self.medhi.update()
        draw.rect(self.gameScreen, (255, 255, 255), (self.medhi.x - self.medhi.cam_x, self.medhi.y - self.medhi.cam_y, self.playerSize, self.playerSize), 3)
        self.gameScreen.blit(self.medhi.currentFrame, (self.medhi.x - self.medhi.cam_x, self.medhi.y - self.medhi.cam_y))

        # Update Game Screen
        self.mainScreen.blit(transform.scale(self.gameScreen, self.display_surface), (int(self.current_display[0]/2-self.display_surface[0]/2), int(int(self.current_display[1]/2-self.display_surface[1]/2))))
        display.update()
        self.gameScreen.fill((200, 200, 200))

    def resize(self, e):
        self.multiplier = min(e.w / self.init_display_size[0], e.h / self.init_display_size[1])
        self.current_display = (e.w, e.h)
        if e.w / self.aspect_ratio <= e.h:
            self.display_surface = (e.w, int(e.w / self.aspect_ratio))
        else:
            self.display_surface = (int(e.h * self.aspect_ratio), e.h)
        self.mainScreen = display.set_mode((e.w, e.h), RESIZABLE | HWSURFACE)
        self.mainScreen.fill((0, 0, 0))

        print(e, self.aspect_ratio)

    def game(self):
        running = True

        while running:
            self.gameClock.tick(120)
            for e in event.get():
                if e.type == QUIT:
                    running = False

                    return 'menu'
                    break
                elif e.type == KEYDOWN:
                    self.medhi.keyDown(e.key)
                elif e.type == KEYUP:
                    self.medhi.keyUp(e.key)
                elif e.type == VIDEORESIZE:
                    self.resize(e)

            keys = key.get_pressed()

            if keys[K_p]:
                for p in self.map.portals:
                    print(p, self.medhi.playerRect)
                    if self.medhi.playerRect.colliderect(p[0]):
                        try:
                            self.medhigames[int(p[1])](100, components.mehdi.drawStuff, components.mehdi.resizeStuff)
                        except:
                            print('it broke!', p[1])
                            traceback.print_exc()

            # mx, my = mouse.get_pressed()[:2]

            self.update()


if __name__ == "__main__":
    init()
    screen = display.set_mode((1080, 720), RESIZABLE | HWSURFACE)
    g = game(screen)

    g.game()
    quit()
