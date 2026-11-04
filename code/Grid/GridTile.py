import pygame

class GridTile:
    def __init__(self, position):
        self.position = position
        self.item = None
        self.sprite = pygame.image.load("./Resources/Tiles/ProtoTile.png").convert_alpha()
    def IsAdjacentTo(self, other):
        return (self.position - other.position).SqrMagnitude() == 1
    def Render(self, screen, maxTileSize):
        scaledSprite = pygame.transform.scale_by(self.sprite, maxTileSize / 32)
        rect = pygame.Rect(self.position[0] * maxTileSize, self.position[1] * maxTileSize, maxTileSize, maxTileSize)
        screen.blit(scaledSprite, rect)