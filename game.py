import components.mehdi as mehdi
import components.flame as flame
from pygame import *
from Map.Map import *

import Minigames.AsteroidDodge
import Minigames.MoonLaunch
import Minigames.SunProtection
import Minigames.SolarPropulsion

import traceback

class game:

    def __init__(self, screen):

        self.WIDTH, self.HEIGHT = 1080, 720
        self.mainScreen = screen

        self.mainScreen.fill((0, 0, 0))

        loading_text = mehdi.text("Loading...", 30)

        self.mainScreen.blit(loading_text,
                             mehdi.center(0, 0, self.mainScreen.get_width(), self.mainScreen.get_height(), loading_text.get_width(), loading_text.get_height()))

        display.flip()

        self.gameClock = time.Clock()
        self.multiplier = 1
        self.init_display_size = (self.WIDTH, self.HEIGHT)
        self.current_display = (self.WIDTH, self.HEIGHT)
        self.display_surface = (self.WIDTH, self.HEIGHT)
        self.aspect_ratio = self.init_display_size[0] / self.init_display_size[1]

        self.gameScreen = Surface(self.current_display)
        self.map = Map(self.gameScreen)

        self.medhi = mehdi.medhi(self.map, self.gameScreen, (self.map.start[0], self.map.start[1]) if 'position' not in flame.master_user else flame.master_user['position'])

        self.medhigames = {
            'AsteroidDodge': Minigames.AsteroidDodge.asteroidDodge,
            'MoonLaunch': Minigames.MoonLaunch.moonLaunch,
            'SunProtection': Minigames.SunProtection.sunProtection,
            'SolarPropulsion': Minigames.SolarPropulsion.solarPropulsion
        }

        self.resize(Rect(0, 0, screen.get_width(), screen.get_height()))

        self.interactionLock = False

    def update(self):
        self.mainScreen.fill((0, 0, 0))

        # Draw World
        self.map.make_map(self.gameScreen, (self.medhi.cam_x, self.medhi.cam_y))
        for npc in self.map.npc:
            npc.draw(self.gameScreen, self.medhi)
        # Player
        self.medhi.update()
        draw.rect(self.gameScreen, (255, 255, 255), (self.medhi.x - self.medhi.cam_x, self.medhi.y - self.medhi.cam_y, self.medhi.width, self.medhi.height), 3)
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


        #mehdi.txtScreen(mehdi.TextBox(mehdi.dialog['intro']['dialog'], 2, int(self.WIDTH * 0.7), 20, (255, 255, 255), self.WIDTH * 0.1, self.HEIGHT * 0.1))

        while running:
            self.gameClock.tick(120)
            for e in event.get():
                if e.type == QUIT:
                    running = False

                    return 'menu'
                    break
                elif e.type == KEYDOWN:
                    if not self.interactionLock:
                        self.medhi.keyDown(e.key)
                elif e.type == KEYUP:
                    if not self.interactionLock:
                        self.medhi.keyUp(e.key)
                elif e.type == VIDEORESIZE:
                    self.resize(e)

            keys = key.get_pressed()

            if keys[K_p]:
                for p in self.map.minigamePortal:
                    if self.medhi.playerRect.colliderect(p[0]):
                        try:
                            self.medhigames[p[1]]()
                        except:
                            print('it broke!', p[1])
                            traceback.print_exc()
                        break
                else:
                    for p in self.map.teleports:
                        if self.medhi.playerRect.colliderect(p[0]):
                            self.medhi.teleport(p[1])
                            break


            for p in self.map.informationTiles:
                if self.medhi.playerRect.colliderect(p[0]):

                    info = mehdi.dialog[p[1]]

                    if (info['automatic'] or keys[K_p]) and p[1] not in flame.master_user['dialogCompleted']:
                        mehdi.txtScreen(mehdi.TextBox(mehdi.dialog[p[1]]['dialog'], 2, int(self.WIDTH * 0.7), 20,
                                                      (255, 255, 255), self.WIDTH * 0.1, self.HEIGHT * 0.1))

                        if info['singleTrigger']:
                            flame.master_user['dialogCompleted'].append(p[1])

                    break

            if keys[K_p]:
                for npc in self.map.npc:
                    dialogue = npc.interact(self.medhi)
                    if dialogue:
                        mehdi.txtScreen(mehdi.TextBox(dialogue, 2, int(self.WIDTH * 0.7), 20,
                                                      (255, 255, 255), self.WIDTH * 0.1, self.HEIGHT * 0.1))

            # mx, my = mouse.get_pressed()[:2]

            self.update()


if __name__ == "__main__":
    init()
    screen = display.set_mode((1080, 720), RESIZABLE | HWSURFACE)
    g = game(screen)

    g.game()
    quit()
