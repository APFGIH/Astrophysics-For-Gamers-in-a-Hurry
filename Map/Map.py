import pytmx
import pygame
import math
import components.mehdi

class Map:
    def __init__(self, gameScreen):
        self.gameMap = pytmx.load_pygame("Map/tileMaps/world.tmx", pixelalpha=True)
        self.width = self.gameMap.width
        self.height = self.gameMap.height
        self.screenSize = gameScreen.get_size()
        self.tileSize = 48
        self.collisionRects = []
        self.portals = []

        for r in self.gameMap.get_layer_by_name("Collision"):
            self.collisionRects.append(pygame.Rect(r.x, r.y, r.width, r.height))

        self.start = (self.gameMap.get_layer_by_name("Start")[0].x, self.gameMap.get_layer_by_name("Start")[0].y)

        for p in self.gameMap.get_layer_by_name("Portal"):
            self.portals.append((pygame.Rect(p.x, p.y, p.width, p.height), p.name))

    def render(self, surface, sx, sy, hx, hy, offsetx=0, offsety=0):
        for x in range(sx, hx):
            for y in range(sy, hy):
                tile = self.gameMap.get_tile_image(x, y, 0)
                if tile:
                    surface.blit(pygame.transform.scale(tile, (self.tileSize, self.tileSize)), ((x-sx) * self.tileSize - offsetx, (y-sy) * self.tileSize - offsety))

        for rect in components.mehdi.thiccRects:
            pygame.draw.rect(surface, (255, 0, 0), (rect[0] - sx * self.tileSize - offsetx, rect[1] - sy * self.tileSize - offsety, rect[2], rect[3]), 3)

    def make_map(self, surface, cameralocation):
        offsetx = cameralocation[0] % self.tileSize
        offsety = cameralocation[1] % self.tileSize

        self.render(surface, max(0, cameralocation[0] // self.tileSize), max(0, cameralocation[1] // self.tileSize), math.ceil((cameralocation[0] + self.screenSize[0]) / self.tileSize), math.ceil((cameralocation[1] + self.screenSize[1]) / self.tileSize), offsetx, offsety)
