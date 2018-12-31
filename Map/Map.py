import pytmx
import pygame
import math


class Map:
    def __init__(self):
        self.gameMap = pytmx.load_pygame("Map/tileMaps/Testmap1.tmx", pixelalpha=True)
        self.width = self.gameMap.width
        self.height = self.gameMap.height
        self.tileSize = 80
        self.collisionRects = []

        for r in self.gameMap.get_layer_by_name("CollisionMap"):
            self.collisionRects.append(pygame.Rect(r.x*4, r.y*4, r.width*4, r.height*4))

        print(self.collisionRects)
        print(self.width, self.height)

    def render(self, surface, sx, sy, hx, hy, offsetx=0, offsety=0):
        for x in range(sx, 20):
            for y in range(sy, 20):
                tile = self.gameMap.get_tile_image(x, y, 0)
                if tile:
                    surface.blit(pygame.transform.scale(tile, (self.tileSize, self.tileSize)), ((x-sx) * self.tileSize - offsetx, (y-sy) * self.tileSize - offsety))

        for rect in self.collisionRects:
            pygame.draw.rect(surface, (0, 0, 0), (rect[0] - sx * self.tileSize - offsetx, rect[1] - sy * self.tileSize - offsety, rect[2], rect[3]), 3)

    def make_map(self, surface, cameralocation):
        offsetx = cameralocation[0] % self.tileSize
        offsety = cameralocation[1] % self.tileSize

        print(cameralocation)

        self.render(surface, max(0, cameralocation[0] // self.tileSize), max(0, cameralocation[1] // self.tileSize), 960 // 80, 540 // 80, offsetx, offsety)
