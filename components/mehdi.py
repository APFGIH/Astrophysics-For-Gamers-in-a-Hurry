"""
This file contains convenience functions used several times in our game. they range from graphics centering to screen
prep.

Main Rahmish Developers: Henry Tu & Syed Safwaan
"""

# Modules to import
from pygame import *  # to allow use of graphics
from random import *  # to allow use of random generators
from math import *  # to allow use of trigonometric functions
import random
import json
import traceback
import components.flame as flame
import random
import time as t

# x, y, vx, vy
stars = []
prev_size = (0, 0)
screen = None
dialog = {}
lessons = []
fullLessons = {}

WIDTH, HEIGHT = 1080, 720

def init_dialog():
    global dialog, lessons

    with open('dialog.json') as file:
        dialog = json.loads(file.read())

    for d in dialog:
        if 'Lesson' in d:
            lessons.append(dialog[d]['dialog'])

            fullLessons[d] = dialog[d]

def generate_quiz():
    global lessons, fullLessons

    quiz = {}

    educationPool = flame.master_user['education'][:]

    if random.randint(0, 10) == 0:

        educationPool.append(random.choice(list(fullLessons.keys())))

    topic = random.choice(educationPool)

    line = (fullLessons[topic]['dialog'].split('.')[0] + '.').split()

    target = random.choice(range(len(line)))

    quiz['correctAnswer'] = line[target].upper()
    quiz['answers'] = [line[target].upper()]

    line[target] = '_____'

    quiz['question'] = 'Fill in the blank:~~' + ' '.join(line)

    for _ in range(3):
        quiz['answers'].append(random.choice(random.choice(lessons).split()).upper())

    random.shuffle(quiz['answers'])

    return quiz


def set_screen(s):
    global screen
    screen = s

def center_frame(a, b):

    sw = a.get_width()
    sh = a.get_height()

    w = b.get_width()
    h = b.get_height()

    return (sw // 2 - w // 2, sh // 2 - h //2)

def resizeStuff(w, h):
    global screen
    screen = display.set_mode((max(w, 1080), max(h, 720)), DOUBLEBUF + RESIZABLE)

def drawStuff(surface):
    global screen

    wallpaper(screen)

    x, y = center_frame(screen, surface)

    draw.rect(screen, (255, 255, 255), (x - 1, y - 1, surface.get_width() + 2, surface.get_height() + 2))
    screen.blit(surface, (x, y))

    display.flip()


def init_stars(size):
    for _ in range(100 - len(stars)):
        vx = cos(radians(random.randint(0, 360)))
        vy = sin(radians(random.randint(0, 360)))

        stars.append([randint(-50, 50) + size[0] // 2 + vx * randint(0,
        int(
        (((size[0] ** 2 + size[1] ** 2) ** 0.5) / 2))), randint(-50, 50) + size[1] // 2 + vy * randint(0,
        int(
        (((size[0] ** 2 + size[1] ** 2) ** 0.5) / 2))), vx, vy])


def transition(screen, next):
    # Blue tint
    tint = Surface((screen.get_width(), screen.get_height()))
    tint.fill((0, 0, 0))
    tint.set_alpha(10)

    clock = time.Clock()

    for _ in range(50):
        screen.blit(tint, (0, 0))
        display.flip()

        clock.tick(50)

    return next()

# Function to control printing in game code (purely for dev purposes)
def mehprint(*text):
    """ A general convenience print statement used for debugging. """

    # Boolean to evaluate whether printing is wanted
    printing = False  # must be manually changed in file

    # If user wants to print, stuff gets printed
    if printing:
        print(*text)


# Function to create loading screen
def meh_screen(screen):
    """ Creates a Rahmish loading screen. """

    # Generate logo image and text
    logo = transform.scale(image.load('textures/splash.jpg'), (screen.get_width(), screen.get_height()))  # load image
    logo_font = font.Font("fonts/UndertaleSans.ttf", 40)  # load Font object
    logo_text = logo_font.render("Super Awesome Meaningful COnnection gAmes", True, (255, 255, 255))  # render the text

    # Blit the logo and text to the screen
    screen.blit(logo, (0, 0))
    screen.blit(logo_text, center(0, 100, screen.get_width(), screen.get_height(), logo_text.get_width(),
                                  logo_text.get_height()))

    # Update the screen to display the Rahmish screen
    display.update()


# Function to size wallpaper in background
def wallpaper(screen):
    global stars, prev_size

    size = (screen.get_width(), screen.get_height())

    if size != prev_size:
        prev_size = size
        stars = []

        init_stars(size)

    """ Resizes wallpaper in menu background. """

    for _ in range(100 - len(stars)):
        stars.append([randint(-5, 5) + size[0] // 2, randint(-5, 5) + size[1] // 2, cos(radians(random.randint(0, 360))), sin(radians(random.randint(0, 360)))])

    # Fill the screen with black to clear it
    screen.fill((0, 0, 0))

    for i in range(len(stars) - 1, -1, -1):

        star = stars[i]

        if Rect(0, 0, size[0], size[1]).collidepoint(star[0], star[1]):

            star[0] += star[2]
            star[1] += star[3]

            draw.circle(screen, (255, 255, 255), (int(star[0]), int(star[1])), int(5 * (((star[0] - size[0] // 2) ** 2 + (star[1] - size[1] // 2) ** 2) ** 0.5)/(((size[0] ** 2 + size[1] ** 2) ** 0.5) / 2)))
        else:
            del stars[i]


# Function to make Minecraft-style text
def text(text, size):
    """ Generates and returns Minecraft-style text. """

    # Load the Minecraft Font object
    minecraft_font = font.Font("fonts/UndertaleSans.ttf", size)

    # Make the background and surface text
    text_surface = minecraft_font.render(text, True, (255, 255, 255))  # surface text
    text_shadow = minecraft_font.render(text, True, (0, 0, 0))  # background text

    # Create the surfaces for blitting and blit to them
    shadow_surface = Surface((text_surface.get_width(), text_surface.get_height()))  # create surface
    shadow_surface.blit(text_shadow, (0, 0))  # blit text shadow to surface
    shadow_surface.set_alpha(100)  # make text shadow surface slightly transparent

    # Create the master text surface
    text_surface_final = Surface((text_surface.get_width() + 2, text_surface.get_height() + 2), SRCALPHA)

    # Blit the text shadow and text surface to the master surface
    text_surface_final.blit(text_shadow, (2, 2))  # text shadow
    text_surface_final.blit(text_surface, (0, 0))  # text surface

    # Return the final surface for use in the outer scope
    return text_surface_final


# Function to load and play sound immediately
def load_sound(sound_list):
    """ Loads and plays a sound instantly. """

    # Load the sound as a Sound object
    #sound_object = mixer.Sound(choice(sound_list))

    # Play the sound
    #sound_object.play(0)


# Function to center a surface on another surface
def center(x, y, canvas_w, canvas_h, object_w, object_h):
    """ Returns a positional tuple that will centre a surface on another surface. """

    # Do some math and return a positional tuple for use in the outer scope
    return x + canvas_w // 2 - object_w // 2, y + canvas_h // 2 - object_h // 2


# Function to center a surface on a given point
def point_center(point_x, point_y, object_w, object_h):
    """ Returns a positional tuple that will centre a surface on a point. """

    # Do some more math and return a positional tuple for use in the outer scope
    return point_x - (object_w // 2), point_y - (object_h // 2)


# Function to centrally rotate a surface
def joint_rotate(surf, angle):
    """ Returns a rotated surface independent of the original supplied surface. """

    # Create a copy of the supplied surface
    new_surf = surf.copy()

    # Return the rotated copy to the outer scope
    return transform.rotate(new_surf, -degrees(angle))

class mehdi:
    def __init__(self, map, gameSurface, startPos):
        self.tileSize = map.tileSize
        self.x = startPos[0]
        self.vx = self.cam_x = self.ovx = 0
        self.y = startPos[1]
        self.vy = self.cam_y = self.ovy = 0
        self.screenWidth, self.screenHeight = gameSurface.get_size()
        self.currentKey = -1
        self.facing = 0
        self.map = map
        self.multiplier = 1
        self.gameSurface = gameSurface
        self.width = 40
        self.height = 60
        self.playerRect = Rect(self.x, self.y, self.width, self.height)
        self.screenRect = Rect(self.cam_x, self.cam_y, self.screenWidth, self.screenHeight)

        self.klist = [False, False, False, False]

        self.animations = {'d': [transform.scale2x(image.load('textures/PlayerAnimation/d (' + str(x) + ').png')).convert_alpha() for x in range(1, 5)],
                           'l': [transform.scale2x(image.load('textures/PlayerAnimation/l (' + str(x) + ').png')).convert_alpha() for x in range(1, 3)],
                           'r': [transform.scale2x(image.load('textures/PlayerAnimation/r (' + str(x) + ').png')).convert_alpha() for x in range(1, 3)],
                           'u': [transform.scale2x(image.load('textures/PlayerAnimation/u (' + str(x) + ').png')).convert_alpha() for x in range(1, 5)]}

        self.currentPosition = 'd'
        self.currentAnimation = self.animations['d'][:]
        self.currentFrame = self.animations[self.currentPosition][0]
        self.animationTick = 30
        self.currentTick = 0
        self.animationLock = False

    def keyDown(self, key):
        self.ovx = self.vx
        self.ovy = self.vy

        if key == K_LEFT:
            self.vx -= 10
            self.klist[0] = True
        if key == K_RIGHT:
            self.vx += 10
            self.klist[1] = True
        if key == K_UP:
            self.vy -= 10
            self.klist[2] = True
        if key == K_DOWN:
            self.vy += 10
            self.klist[3] = True

    def keyUp(self, key):
        self.ovx = self.vx
        self.ovy = self.vy

        if key == K_LEFT and self.klist[0]:
            self.vx += 10
            self.klist[0] = False
        if key == K_RIGHT and self.klist[1]:
            self.vx -= 10
            self.klist[1] = False
        if key == K_UP and self.klist[2]:
            self.vy += 10
            self.klist[2] = False
        if key == K_DOWN and self.klist[3]:
            self.vy -= 10
            self.klist[3] = False

    def teleport(self, location):
        self.klist = [False, False, False, False]
        self.vx = 0
        self.vy = 0

        self.x = location[0]
        self.y = location[1]


        flame.master_user['position'] = [self.x, self.y]


    def update(self):
        self.currentTick += 1

        thiccRects = self.map.collisionRects[:]

        legitX = self.playerRect.x // self.map.tileSize
        legitY = self.playerRect.y // self.map.tileSize

        animationvy = self.vy
        animationvx = self.vx

        for x in range(legitX - 2, legitX + 3):
            for y in range(legitY - 2, legitY + 3):

                try:
                    tileID = self.map.gameMap.get_tile_gid(x, y, 0)

                    if tileID == 1:
                        thiccRects.append(Rect(x * self.map.tileSize, y * self.map.tileSize, self.map.tileSize, self.map.tileSize))

                except:
                    traceback.print_exc()

        self.playerRect.x = max(0, self.vx + self.x)

        for block in thiccRects:  # for every block in the block list
            if self.playerRect.colliderect(block):

                if self.vx < 0:
                    self.playerRect.left = block.right
                    animationvx = 0
                elif self.vx > 0:
                    self.playerRect.right = block.left
                    animationvx = 0

        self.x = self.playerRect.x

        self.playerRect.y = max(0, self.vy + self.y)

        for block in thiccRects:
            if self.playerRect.colliderect(block):

                if self.vy >= 0:
                    self.playerRect.bottom = block.top
                    animationvy = 0
                elif self.vy < 0:
                    self.playerRect.top = block.bottom
                    animationvy = 0

        self.y = self.playerRect.y

        flame.master_user['position'] = [self.x, self.y]

        if self.animationLock == 'x' and self.ovx != self.vx:
            self.animationLock = ''
            self.ovx = self.vx

        if self.animationLock == 'y' and self.ovy != self.vy:
            self.animationLock = ''
            self.ovy = self.vy

        if animationvx > 0:
            if self.currentPosition == 'r' and self.currentTick >= self.animationTick:
                self.currentTick = 0
                self.currentFrame = self.currentAnimation[0]
                self.currentAnimation.append(self.currentAnimation.pop(0))
            elif not self.animationLock:
                self.animationLock = 'x'
                self.currentPosition = 'r'
                self.currentAnimation = self.animations['r'][:]
                self.currentFrame = self.currentAnimation[0]

        elif animationvx < 0:
            if self.currentPosition == 'l' and self.currentTick >= self.animationTick:
                self.currentTick = 0
                self.currentFrame = self.currentAnimation[0]
                self.currentAnimation.append(self.currentAnimation.pop(0))
            elif not self.animationLock:
                self.animationLock = 'x'
                self.currentPosition = 'l'
                self.currentAnimation = self.animations['l'][:]
                self.currentFrame = self.currentAnimation[0]

        if animationvy < 0:
            if self.currentPosition == 'u' and self.currentTick >= self.animationTick:
                self.currentTick = 0
                self.currentFrame = self.currentAnimation[0]
                self.currentAnimation.append(self.currentAnimation.pop(0))
            elif not self.animationLock:
                self.animationLock = 'y'
                self.currentPosition = 'u'
                self.currentAnimation = self.animations['u'][:]
                self.currentFrame = self.currentAnimation[0]

        elif animationvy > 0:
            if self.currentPosition == 'd' and self.currentTick >= self.animationTick:
                self.currentTick = 0
                self.currentFrame = self.currentAnimation[0]
                self.currentAnimation.append(self.currentAnimation.pop(0))
            elif not self.animationLock:
                self.animationLock = 'y'
                self.currentPosition = 'd'
                self.currentAnimation = self.animations['d'][:]
                self.currentFrame = self.currentAnimation[0]

        if animationvx == 0 and animationvy == 0:
            self.currentFrame = self.animations[self.currentPosition][0]

        self.draw()

    def draw(self):
        if self.x - self.screenWidth // 2 < 0:
            self.cam_x = 0
        elif self.x + self.screenWidth // 2 > self.map.width * self.tileSize:
            self.cam_x = self.map.width * self.tileSize - self.screenWidth
        else:
            self.cam_x = self.x - self.screenWidth // 2

        if self.y - self.screenHeight // 2 < 0:
            self.cam_y = 0
        elif self.y + self.screenHeight // 2 > self.map.height * self.tileSize:
            self.cam_y = self.map.height * self.tileSize - self.screenHeight
        else:
            self.cam_y = self.y - self.screenHeight // 2

        self.screenRect.x = self.cam_x
        self.screenRect.y = self.cam_y


#Animated textboxes
class TextBox:
    def __init__(self, text, delay, width, size, col, x, y, prompt=True):
        self.text = text
        self.delay = delay
        self.width = width
        self.fnt = font.Font("fonts/UndertaleSans.ttf", size)
        self.col = col
        self.text_surface = self.fnt.render("I", True, col)  # surface text
        self.h = self.text_surface.get_height()
        self.text_surface = self.fnt.render("", True, col)  # surface text
        self.lines = [self.text_surface]
        self.cur = 0
        self.curline = " "
        self.size = size
        self.t = 0
        self.x = x
        self.y = y
        self.prompt = prompt

    def animate(self):
        if self.cur < len(self.text) and self.t % self.delay == 0:
            if self.text[self.cur] != "~" and (self.text_surface.get_width() + self.size < self.width or not (self.text[self.cur] == " " and self.text_surface.get_width()+6*self.size > self.width)):
                self.curline += self.text[self.cur]
                self.text_surface = self.fnt.render(self.curline, True, self.col)
                self.cur += 1
            else:
                self.curline = " "
                if self.text[self.cur] != "~":
                    self.curline += self.text[self.cur]
                self.lines.append(0)

                self.text_surface = self.fnt.render(self.curline, True, self.col)
                self.cur += 1

        elif self.cur == len(self.text):
            self.lines.append(0)
            self.text_surface = self.fnt.render(" ", True, self.col)
            self.lines[-1] = self.text_surface
            self.lines.append(0)
            if self.prompt:
                self.text_surface = self.fnt.render("PRESS [A] TO CONTINUE", True, self.col)
            else:
                self.text_surface = self.fnt.render(" ", True, self.col)
            self.lines[-1] = self.text_surface
            self.cur += 1
        self.lines[-1] = self.text_surface
        self.t += 1
        if self.cur > len(self.text):
            return True

    def finish(self):
        a = self.animate()
        if not a:
            self.finish()


    def update(self, screen):
        for i in range(len(self.lines)):
            screen.blit(self.lines[i], (self.x, self.y+self.h*i))


def txtScreen(tb):

    screen = Surface((WIDTH, HEIGHT))

    running = True
    clock = time.Clock()
    while running:
        screen.fill((0, 0, 0))
        keys = key.get_pressed()
        for action in event.get():
            if action.type == QUIT:
                running = False
                break
            if action.type == VIDEORESIZE:
                resizeStuff(action.w, action.h)

        a = tb.animate()
        tb.update(screen)
        if a and keys[K_a]:
            return
        elif keys[K_s]:
            tb.finish()
        drawStuff(screen)
        clock.tick(500)
    quit()



def multipleChoice(dict):

    screen = Surface((WIDTH, HEIGHT))
    ans = dict["correctAnswer"]
    opts = dict["answers"]
    quest = dict["question"]
    shuffle(opts)
    f = font.Font("fonts/UndertaleSans.ttf", 38)
    screen.fill((0, 0, 0))
    a = TextBox(quest, 1, 650, 38, (255, 255, 255), 150, 40, False)
    b = TextBox("1.) "+opts[0], 1, 650, 38, (255, 255, 255), 150, 400, False)
    c = TextBox("2.) "+opts[1], 1, 650, 38, (255, 255, 255), 150, 460, False)
    d = TextBox("3.) "+opts[2], 1, 650, 38, (255, 255, 255), 150, 520, False)
    e = TextBox("4.) "+opts[3], 1, 650, 38, (255, 255, 255), 150, 580, False)
    n = opts.index(ans)
    a.finish(); b.finish(); c.finish(); d.finish(); e.finish()
    a.update(screen); b.update(screen); c.update(screen); d.update(screen); e.update(screen)


    running = True
    clock = time.Clock()
    while running:

        keys = key.get_pressed()
        for action in event.get():
            if action.type == QUIT:
                running = False
                break
            if action.type == VIDEORESIZE:
                resizeStuff(action.w, action.h)
        if keys[K_1]:
            return 0 == n
        elif keys[K_2]:
            return 1 == n
        elif keys[K_3]:
            return 2 == n
        elif keys[K_4]:
            return 3 == n

        drawStuff(screen)
        clock.tick(500)
    quit()