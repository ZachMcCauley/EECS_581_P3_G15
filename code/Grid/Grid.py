from Grid.Vector2Int import Vector2Int
from Grid.Vector2 import Vector2
from Grid.GridTile import GridTile
import math

class Grid:
    def __init__(self, positions):
        # Add grid spaces to dictionary
        self.grid = dict()
        for pos in positions:
            self.grid[pos] = GridTile(pos)
    @staticmethod
    def FormFromDims(dims) -> Grid:
        pos = set()
        for x in range( dims[0]):
            for y in range(dims[1]):
                pos.add(Vector2Int(x, y))
        return Grid(pos)
    def Render(self, screen, screenSpace):
        # Determine the size of each tile
        screenSize = screen.get_size()
        xBounds = screenSize[0] * screenSpace[0] / (self.MaxX() - self.MinX() + 1)
        yBounds = screenSize[1] * screenSpace[1] / (self.MaxY() - self.MinY() + 1)
        constrainedOnX = xBounds < yBounds
        maxTileSize = min(xBounds, yBounds)
        maxTileSize = math.floor(maxTileSize)
        """
        Cry about it though I may, rendering is definitely one of those places where Unity makes your life easier.
        Yes, I understand why you all wanted to use PyGame, and I don't blame you,
        but it makes my life difficult.
        
        # Placeholder values so these variables exist in this scope
        offsetX, offsetY = 0, 0
        if constrainedOnX:
            offsetX = screenSize[0] * (1 - screenSpace[0]) / 2 + maxTileSize * self.MinX()
            offsetY = screenSize[1] * screenSpace[1] / 2 + maxTileSize * self.MinY()
        else:
            offsetX = screenSize[0] * (1 - screenSpace[0]) / 2 + maxTileSize * self.MinX()
            offsetY = screenSize[1] * (1 - screenSpace[1]) / 2 + maxTileSize * self.MinY()
        """
        for tile in self.grid.values():
            tile.Render(screen, maxTileSize)
    def MinX(self) -> int:
        toReturn = None
        for key in self.grid.keys():
            if toReturn is None or key.x < toReturn:
                toReturn = key.x
        return toReturn
    def MaxX(self) -> int:
        toReturn = None
        for key in self.grid.keys():
            if toReturn is None or key.x > toReturn:
                toReturn = key.x
        return toReturn
    def MinY(self) -> int:
        toReturn = None
        for key in self.grid.keys():
            if toReturn is None or key.y < toReturn:
                toReturn = key.y
        return toReturn
    def MaxY(self) -> int:
        toReturn = None
        for key in self.grid.keys():
            if toReturn is None or key.y > toReturn:
                toReturn = key.y
        return toReturn
    def Center(self) -> Vector2:
        xCtr = (self.MinX() + self.MaxX()) / 2
        yCtr = (self.MinY() + self.MaxY()) / 2
        return Vector2(xCtr, yCtr)
    def ContainsPosition(self, pos) -> bool:
        return pos in self.grid.keys()
    def GetTileByPosition(self, pos) -> GridTile:
        return self.grid[pos]
    def AllPositions(self) -> list:
        return list(self.grid.keys())