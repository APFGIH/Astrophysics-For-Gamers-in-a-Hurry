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
import time as t

# x, y, vx, vy
stars = []
prev_size = (0, 0)

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
def wallpaper(screen, size):
    global stars, prev_size

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

    pass

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

class medhi:
    def __init__(self, tileSize):
        self.tileSize = tileSize
        self.x = self.vx = self.game_x = 0
        self.y = self.vy = self.game_y = 0
        self.currentKey = -1
        self.facing = 0

    def keyDown(self, key):
        if key == K_LEFT:
            self.vx -= .50
        if key == K_RIGHT:
            self.vx += .50
        if key == K_UP:
            self.vy -= .50
        if key == K_DOWN:
            self.vy += .50

    def keyUp(self, key):
        if key == K_LEFT:
            self.vx += .5
        if key == K_RIGHT:
            self.vx -= .5
        if key == K_UP:
            self.vy += .5
        if key == K_DOWN:
            self.vy -= .5

    def update(self, multiplier):
        self.x += self.vx
        self.y += self.vy

        self.game_x = self.x * self.tileSize
        self.game_y = self.y * self.tileSize
