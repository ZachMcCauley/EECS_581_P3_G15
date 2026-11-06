import pygame
from Grid.Item import Item

class GridTile:
    def __init__(self, position):
        self.position = position
        self.item = None
        # Get the background for the tile
        # I suppose we can put this in resource manager too, especially if we want all tile backgrounds to be homogenous.
        self.sprite = pygame.image.load("./Resources/Tiles/ProtoTile.png").convert_alpha()
    # Returns whether two tiles are adjacent.
    def IsAdjacentTo(self, other) -> bool:
        return (self.position - other.position).SqrMagnitude() == 1
    def Render(self, screen, maxTileSize) -> None:
        scaledSprite = pygame.transform.scale_by(self.sprite, maxTileSize / 32)
        rect = pygame.Rect(self.position[0] * maxTileSize, self.position[1] * maxTileSize, maxTileSize, maxTileSize)
        screen.blit(scaledSprite, rect)
        if self.item is not None:
            self.item.Render(screen, self.position, maxTileSize)
    def StealItemFromMe(self) -> Item:
        toReturn = self.item
        self.item = None
        return toReturn