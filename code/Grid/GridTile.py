import pygame
from Grid.Item import Item
from Grid.Vector2Int import Vector2Int


class GridTile:
    def __init__(self, position):
        self.position = position
        self.item = None
        self.selectionRect = None
        # Get the background for the tile
        # I suppose we can put this in resource manager too, especially if we want all tile backgrounds to be homogenous.
        self.sprite = pygame.image.load("./Resources/Tiles/ProtoTile.png").convert_alpha()
    # Returns whether two tiles are adjacent.
    def IsAdjacentTo(self, other) -> bool:
        return (self.position - other.position).SqrMagnitude() == 1
    def Render(self, screen, maxTileSize, tileOffset = Vector2Int.Zero(), pixelOffset = (0, 0)) -> None:
        scaledSprite = pygame.transform.scale_by(self.sprite, maxTileSize / self.sprite.get_width())
        rect = pygame.Rect((tileOffset[0] + self.position[0]) * maxTileSize + pixelOffset[0], (tileOffset[1] + self.position[1]) * maxTileSize + pixelOffset[1], maxTileSize, maxTileSize)
        self.selectionRect = rect
        screen.blit(scaledSprite, rect)
        if self.item is not None:
            itemOffset = (tileOffset[0] * maxTileSize + pixelOffset[0], tileOffset[1] * maxTileSize + pixelOffset[1])
            self.item.Render(screen, self.position, maxTileSize, itemOffset)
    def StealItemFromMe(self) -> Item:
        toReturn = self.item
        self.item = None
        return toReturn