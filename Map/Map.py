import pytmx
import pygame
import math


class Map:
    def __init__(self):
        self.gameMap = pytmx.load_pygame("Map/tileMaps/Testmap1.tmx", pixelalpha=True)
        self.width = self.gameMap.width
        self.height = self.gameMap.height
        self.tileSize = 80
        print(self.width, self.height)

    def render(self, surface, sx, sy, hx, hy, offsetx=0, offsety=0):
        for x in range(sx, 20):
            for y in range(sy, 20):
                tile = self.gameMap.get_tile_image(x, y, 0)
                if tile:
                    surface.blit(pygame.transform.scale(tile, (self.tileSize, self.tileSize)), ((x-sx) * self.tileSize - offsetx, (y-sy) * self.tileSize - offsety))

    def make_map(self, surface, playerlocation):
        offsetx = playerlocation[0] % self.tileSize
        offsety = playerlocation[1] % self.tileSize

        print(playerlocation)

        self.render(surface, max(0, playerlocation[0] // self.tileSize - 1), max(0, playerlocation[1] // self.tileSize - 1), 960 // 80, 540 // 80, offsetx, offsety)
