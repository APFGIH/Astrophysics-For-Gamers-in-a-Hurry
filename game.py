import components.mehdi as mehdi
import components.flame as flame
import random
import time as t
from pygame import *
from Map.Map import *

import Minigames.AsteroidDodge
import Minigames.Dvd
import Minigames.MoonLaunch
import Minigames.SunProtection
import Minigames.SolarPropulsion

import json

import traceback

class game:

    def __init__(self, screen):

        self.normal_font = font.Font("fonts/UndertaleSans.ttf", 25)

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

        self.mehdi = mehdi.mehdi(self.map, self.gameScreen, (self.map.start[0], self.map.start[1]) if 'position' not in flame.master_user else flame.master_user['position'])

        self.mehdigames = {
            'exit': mehdi.meme,
            'Dvd': Minigames.Dvd.dvd,
            'AsteroidDodge': Minigames.AsteroidDodge.asteroidDodge,
            'MoonLaunch': Minigames.MoonLaunch.moonLaunch,
            'SunProtection': Minigames.SunProtection.sunProtection,
            'SolarPropulsion': Minigames.SolarPropulsion.solarPropulsion
        }

        self.postmehdigames = {
            'Dvd': 'exit',
            'AsteroidDodge': 'Jupiter',
            'MoonLaunch': 'Moon',
            'SunProtection': 'Sun',
            'SolarPropulsion': 'Wasteland'
        }

        self.mehdigameeducation = {
            'Dvd': 10,
            'AsteroidDodge': 4,
            'MoonLaunch': 2,
            'SunProtection': 6,
            'SolarPropulsion': 8
        }

        self.resize(Rect(0, 0, screen.get_width(), screen.get_height()))

        self.interactionLock = False

    def update(self):
        self.mainScreen.fill((0, 0, 0))

        # Draw World
        self.map.make_map(self.gameScreen, (self.mehdi.cam_x, self.mehdi.cam_y))
        for npc in self.map.npc:
            npc.draw(self.gameScreen, self.mehdi)
        # Player
        self.mehdi.update()
        #draw.rect(self.gameScreen, (255, 255, 255), (self.mehdi.x - self.mehdi.cam_x, self.mehdi.y - self.mehdi.cam_y, self.mehdi.width, self.mehdi.height), 3)
        self.gameScreen.blit(self.mehdi.currentFrame, (self.mehdi.x - self.mehdi.cam_x, self.mehdi.y - self.mehdi.cam_y))

        for p in self.map.slotmachine:
            if p[0].colliderect(self.mehdi.screenRect):
                self.gameScreen.blit(p[1], (p[0].x - self.mehdi.cam_x, p[0].y-self.mehdi.cam_y))
        for p in self.map.bank:
            if p[0].colliderect(self.mehdi.screenRect):
                self.gameScreen.blit(p[1], (p[0].x - self.mehdi.cam_x, p[0].y-self.mehdi.cam_y))

        score_text = self.normal_font.render('Score: %i' % flame.master_user['score'], True, (255, 255, 255))
        self.gameScreen.blit(score_text, (20, 20))

        money_text = self.normal_font.render('Money: %i' % flame.master_user['zhekkos'], True, (255, 255, 255))
        self.gameScreen.blit(money_text, (20, 60))

        offsetX = 0
        offsetY = 0

        if flame.master_user['tremble']:
            offsetX = random.randint(-100, 100) * (t.time() - flame.master_user['trembleTime']) / 3600
            offsetY = random.randint(-100, 100)* (t.time() - flame.master_user['trembleTime']) / 3000

        # Update Game Screen
        self.mainScreen.blit(transform.scale(self.gameScreen, self.display_surface), (int(self.current_display[0]/2-self.display_surface[0]/2) + offsetX, int(int(self.current_display[1]/2-self.display_surface[1]/2)) + offsetY))

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
                        self.mehdi.keyDown(e.key)
                elif e.type == KEYUP:
                    if not self.interactionLock:
                        self.mehdi.keyUp(e.key)
                elif e.type == VIDEORESIZE:
                    self.resize(e)

            keys = key.get_pressed()

            if keys[K_p]:
                for p in self.map.minigamePortal:
                    if self.mehdi.playerRect.colliderect(p[0]):
                        # Feature
                        self.mehdi.klist = [False, False, False, False]
                        self.mehdi.vx = 0
                        self.mehdi.vy = 0


                        if len(flame.master_user['education']) >= self.mehdigameeducation[p[1]]:

                            if mehdi.eat_zhekkos(1000000):

                                if mehdi.multipleChoice(mehdi.generate_quiz()):


                                    try:
                                        result = self.mehdigames[p[1]]()

                                        if result:
                                            self.mehdi.teleport(self.map.destinations[self.postmehdigames[p[1]]])

                                            flame.master_user['score'] += result

                                            flame.save()

                                        else:

                                            mehdi.txtScreen(mehdi.TextBox('You failed the mission! Luckily, NASA Software Engineers were able recover your mind from a backup and restore your last position.', 2,
                                                int(self.WIDTH * 0.7), 20,
                                                (255, 255, 255), self.WIDTH * 0.1, self.HEIGHT * 0.1))


                                    except:
                                        print('it broke!', p[1])
                                        traceback.print_exc()
                                    break

                                else:
                                    mehdi.txtScreen(mehdi.TextBox('You failed the pre-flight exam! The rocket was not able to launch.', 2,
                                        int(self.WIDTH * 0.7), 20,
                                        (255, 255, 255), self.WIDTH * 0.1, self.HEIGHT * 0.1))

                                    break


                        else:
                            mehdi.txtScreen(mehdi.TextBox('You do not have enough education! To fly to the next location, you must have atleast %i degrees. (You currently have %i degrees)~~Visit the University to obtain a degree!' % (self.mehdigameeducation[p[1]], len(flame.master_user['education'])), 2, int(self.WIDTH * 0.7), 20,
                                                          (255, 255, 255), self.WIDTH * 0.1, self.HEIGHT * 0.1))

                else:
                    for p in self.map.teleports:
                        if self.mehdi.playerRect.colliderect(p[0]):
                            self.mehdi.teleport(p[1])
                            break


            for p in self.map.informationTiles:
                if self.mehdi.playerRect.colliderect(p[0]):

                    info = mehdi.dialog[p[1] + ('1' if 'Intro' in p[1] else '')]

                    if (info['automatic'] or keys[K_p]) and p[1] not in flame.master_user['dialogCompleted']:
                        self.mehdi.klist = [False, False, False, False]
                        self.mehdi.vx = 0
                        self.mehdi.vy = 0

                        print('Dialog triggered', p[1])

                        if 'Intro' in p[1]:

                            if 'EQ' in p[1] and not flame.master_user['tremble']:
                                flame.master_user['tremble'] = True
                                flame.master_user['trembleTime'] = t.time()

                            count = 1

                            while p[1] + str(count)in mehdi.dialog:

                                mehdi.txtScreen(mehdi.TextBox(mehdi.dialog[p[1] + str(count)]['dialog'], 2, int(self.WIDTH * 0.7), 20,
                                                              (255, 255, 255), self.WIDTH * 0.1, self.HEIGHT * 0.1))

                                count += 1
                        else:
                            mehdi.txtScreen(mehdi.TextBox(mehdi.dialog[p[1]]['dialog'], 2, int(self.WIDTH * 0.7), 20,
                                                          (255, 255, 255), self.WIDTH * 0.1, self.HEIGHT * 0.1))

                        if info['singleTrigger']:
                                flame.master_user['dialogCompleted'].append(p[1])

                    break

            if keys[K_p]:
                for npc in self.map.npc:
                    dialogue = npc.interact(self.mehdi)
                    if dialogue:
                        # Feature
                        self.mehdi.klist = [False, False, False, False]
                        self.mehdi.vx = 0
                        self.mehdi.vy = 0
                        for d in dialogue:
                            mehdi.txtScreen(mehdi.TextBox(d, 2, int(self.WIDTH * 0.7), 20,
                                                          (255, 255, 255), self.WIDTH * 0.1, self.HEIGHT * 0.1))


                for p in self.map.bank:
                    if self.mehdi.playerRect.colliderect(p[0]):
                        # Feature
                        self.mehdi.klist = [False, False, False, False]
                        self.mehdi.vx = 0
                        self.mehdi.vy = 0

                        if t.time() >= flame.master_user['lastFreeZhekko'] + 86400:
                            mehdi.txtScreen(mehdi.TextBox('Bank of Mehdi~~Yay! You got 10 000 000 free Zhekkos!', 2, int(self.WIDTH * 0.7), 20,
                                                          (255, 255, 255), self.WIDTH * 0.1, self.HEIGHT * 0.1))
                            flame.master_user['lastFreeZhekko'] = t.time()
                            flame.master_user['zhekkos'] += 10000000

                            flame.save()

                        else:
                            mehdi.txtScreen(
                                mehdi.TextBox('Bank of Mehdi~~Whoa whoa whoa...~~You must wait %i more seconds to get free zhekkos.' % (flame.master_user['lastFreeZhekko'] + 86400 - t.time()), 2, int(self.WIDTH * 0.7), 20,
                                                          (255, 255, 255), self.WIDTH * 0.1, self.HEIGHT * 0.1))


                for p in self.map.slotmachine:
                    if self.mehdi.playerRect.colliderect(p[0]):
                        # Feature
                        self.mehdi.klist = [False, False, False, False]
                        self.mehdi.vx = 0
                        self.mehdi.vy = 0

                        amount = 5000

                        if mehdi.eat_zhekkos(amount):
                            if random.randint(0, 10) == 0:
                                flame.master_user['zhekkos'] = (flame.master_user['zhekkos'] + amount) * 5

                                mehdi.txtScreen(
                                    mehdi.TextBox('MehdiCasino~~Yay! You won at x5 multiplier !!!!! You now have %i Zhekkos.' % flame.master_user['zhekkos'], 2, int(self.WIDTH * 0.7), 20,
                                                          (255, 255, 255), self.WIDTH * 0.1, self.HEIGHT * 0.1))

                                flame.save()

                            else:
                                mehdi.txtScreen(
                                    mehdi.TextBox('MehdiCasino~~You lost. You now have %i Zhekkos.' % flame.master_user['zhekkos'], 2, int(self.WIDTH * 0.7), 20,
                                                          (255, 255, 255), self.WIDTH * 0.1, self.HEIGHT * 0.1))


                for p in self.map.universities:
                    if self.mehdi.playerRect.colliderect(p[0]):
                        # Feature
                        self.mehdi.klist = [False, False, False, False]
                        self.mehdi.vx = 0
                        self.mehdi.vy = 0

                        if mehdi.eat_zhekkos(1000):

                            lessonNames = list(mehdi.fullLessons.keys())

                            random.shuffle(lessonNames)

                            for topic in lessonNames:
                                if topic not in flame.master_user['education']:


                                    mehdi.txtScreen(mehdi.TextBox('Here\'s your daily dose of education!~~' + mehdi.fullLessons[topic]['dialog'], 2, int(self.WIDTH * 0.7), 20,
                                                                  (255, 255, 255), self.WIDTH * 0.1, self.HEIGHT * 0.1))

                                    flame.master_user['score'] += 50
                                    flame.master_user['education'].append(topic)
                                    flame.save()

                                    mehdi.txtScreen(mehdi.TextBox('Congrats! You now have a degree in %s!~~The University of Loowater has issued 50 points!~~You now have a total of %i degrees.' % (topic.split('Lesson')[0].upper(), len(flame.master_user['education'])), 2,
                                                                  int(self.WIDTH * 0.7), 20,
                                                                  (255, 255, 255), self.WIDTH * 0.1, self.HEIGHT * 0.1))
                                    break


                            else:
                                mehdi.txtScreen(mehdi.TextBox('You are a big nerd and have too much education', 2,
                                    int(self.WIDTH * 0.7), 20,
                                    (255, 255, 255), self.WIDTH * 0.1, self.HEIGHT * 0.1))

            # mx, my = mouse.get_pressed()[:2]

            self.update()


if __name__ == "__main__":
    init()
    screen = display.set_mode((1080, 720), RESIZABLE | HWSURFACE)
    g = game(screen)

    g.game()
    quit()
