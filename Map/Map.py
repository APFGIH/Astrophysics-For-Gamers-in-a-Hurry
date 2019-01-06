import pytmx
import pygame
import math
from components.npc import *


class Map:
    def __init__(self, gameScreen):
        self.gameMap = pytmx.load_pygame("Map/tileMaps/world.tmx", pixelalpha=True)
        self.width = self.gameMap.width
        self.height = self.gameMap.height
        self.screenSize = gameScreen.get_size()
        self.tileSize = 48
        self.collisionRects = []
        self.minigamePortal = []
        self.informationTiles = []
        self.destinations = {}
        self.universities = []
        self.teleports = []
        self.npc = []

        for r in self.gameMap.get_layer_by_name("Collision"):
            self.collisionRects.append(pygame.Rect(r.x, r.y, r.width, r.height))

        self.start = (self.gameMap.get_layer_by_name("Start")[0].x, self.gameMap.get_layer_by_name("Start")[0].y)

        for p in self.gameMap.get_layer_by_name("Destination"):
            self.destinations[p.name] = (p.x, p.y)

        for p in self.gameMap.get_layer_by_name("InformationTiles"):
            self.informationTiles.append((pygame.Rect(p.x, p.y, p.width, p.height), p.name))

        for p in self.gameMap.get_layer_by_name("Education"):
            self.universities.append((pygame.Rect(p.x, p.y, p.width, p.height), p.name))

        for p in self.gameMap.get_layer_by_name("Portal"):
            if p.type == "Minigame":
                self.minigamePortal.append((pygame.Rect(p.x, p.y, p.width, p.height), p.name))
            elif p.type == "Teleport":
                self.teleports.append((pygame.Rect(p.x, p.y, p.width, p.height), self.destinations[p.name]))

        self.npcImages = {}

        for i in self.gameMap.get_layer_by_name("npcLayer"):
            self.npcImages[i.name] = (self.gameMap.get_tile_image_by_gid(i.gid), pygame.Rect(i.x, i.y, i.width, i.height))
            self.collisionRects.append(pygame.Rect(i.x, i.y, i.width, i.height))

        for p in self.gameMap.get_layer_by_name("Interaction"):
            self.npc.append(npc(self.npcImages[p.type][0], self.npcImages[p.type][1], pygame.Rect(p.x, p.y, p.width, p.height), "NICC BROOOOOO", p.name))

    def render(self, surface, sx, sy, hx, hy, offsetx=0, offsety=0):
        for x in range(sx, hx):
            for y in range(sy, hy):
                tile = self.gameMap.get_tile_image(x, y, 0)
                if tile:
                    surface.blit(tile, ((x-sx) * self.tileSize - offsetx, (y-sy) * self.tileSize - offsety))

        for rect in self.collisionRects:
            pygame.draw.rect(surface, (0, 0, 0), (rect[0] - sx * self.tileSize - offsetx, rect[1] - sy * self.tileSize - offsety, rect[2], rect[3]), 3)

    def make_map(self, surface, cameralocation):
        offsetx = cameralocation[0] % self.tileSize
        offsety = cameralocation[1] % self.tileSize

        self.render(surface, max(0, cameralocation[0] // self.tileSize), max(0, cameralocation[1] // self.tileSize), math.ceil((cameralocation[0] + self.screenSize[0]) / self.tileSize), math.ceil((cameralocation[1] + self.screenSize[1]) / self.tileSize), offsetx, offsety)
