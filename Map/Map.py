import pytmx
import pygame


class Map:
    def __init__(self):
        self.gameMap = pytmx.load_pygame("Map/tileMaps/untitled.tmx", pixelalpha=True)
        self.width = self.gameMap.width
        self.height = self.gameMap.height
        self.tileSize = self.gameMap.tilewidth

    def render(self, surface, sx, sy, hx, hy):
        for layer in self.gameMap.visible_layers:
            for x in range(hx-sx):
                for y in range(hy-sy):
                    tile = self.gameMap.get_tile_image(x+sx, y+sy, layer)
                    if tile:
                        surface.blit(tile, (x * self.gameMap.tilewidth, y * self.gameMap.tileheight))

    def make_map(self, surface, dimension, playerlocation):
        # stuff
        pass
