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
    def Render(self, screen, maxTileSize, tileOffset = Vector2Int.Zero(), pixelOffset = (0, 0), timeSinceLastTick = 16) -> None:
        scaledSprite = pygame.transform.scale_by(self.sprite, maxTileSize / self.sprite.get_width())
        rect = pygame.Rect((tileOffset[0] + self.position[0]) * maxTileSize + pixelOffset[0], (tileOffset[1] + self.position[1]) * maxTileSize + pixelOffset[1], maxTileSize, maxTileSize)
        self.selectionRect = rect
        screen.blit(scaledSprite, rect)
    def RenderItem(self, screen, maxTileSize, tileOffset = Vector2Int.Zero(), pixelOffset = (0, 0), timeSinceLastTick = 16):
        if self.item is not None:
            itemOffset = (tileOffset[0] * maxTileSize + pixelOffset[0], tileOffset[1] * maxTileSize + pixelOffset[1])
            self.item.Render(screen, self.position, maxTileSize, itemOffset, timeSinceLastTick)
    def StealItemFromMe(self) -> Item:
        # Wait for tile to finish falling before item can be stolen
        if self.item is not None and self.item.GetDistanceFromOwner() > 0.01:
            return None
        # Now steal the item
        toReturn = self.item
        self.item = None
        if toReturn is not None:
            toReturn.IncrHeight()
        # Increase the fall distance
        return toReturn
    def IsStable(self):
        return self.item is not None and self.item.GetDistanceFromOwner() < 0.01