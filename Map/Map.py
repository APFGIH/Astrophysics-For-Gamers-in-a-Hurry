import pytmx

class Map:

    def __init__(self):
        self.gameMap = pytmx.load_pygame("map.tmx", pixelalpha=True)

    def render(self, surface):
        for layer in self.gameMap.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.gameMap.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.gameMap.tilewidth, y * self.gameMap.tileheight))

    def make_map(self):
        mapSurface = pygame.Surface((self.mapwidth, self.mapheight))
        self.render(mapSurface)
        return mapSurface
