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
    def FormFromDims(dims):
        pos = set()
        for x in range( dims[0]):
            for y in range(dims[1]):
                pos.add(Vector2Int(x, y))
        return Grid(pos)
    def Render(self, screen, screenSpace):
        # Determine the size of each tile
        xBounds = screen.get_size()[0] * screenSpace[0] / (self.MaxX() - self.MinX() + 1)
        yBounds = screen.get_size()[1] * screenSpace[1] / (self.MaxY() - self.MinY() + 1)
        maxTileSize = min(xBounds, yBounds)
        maxTileSize = math.floor(maxTileSize)
        for tile in self.grid.values():
            tile.Render(screen, maxTileSize)
    def MinX(self):
        toReturn = None
        for key in self.grid.keys():
            if toReturn is None or key.x < toReturn:
                toReturn = key.x
        return toReturn
    def MaxX(self):
        toReturn = None
        for key in self.grid.keys():
            if toReturn is None or key.x > toReturn:
                toReturn = key.x
        return toReturn
    def MinY(self):
        toReturn = None
        for key in self.grid.keys():
            if toReturn is None or key.y < toReturn:
                toReturn = key.y
        return toReturn
    def MaxY(self):
        toReturn = None
        for key in self.grid.keys():
            if toReturn is None or key.y > toReturn:
                toReturn = key.y
        return toReturn
    def Center(self):
        xCtr = (self.MinX() + self.MaxX()) / 2
        yCtr = (self.MinY() + self.MaxY()) / 2
        return Vector2(xCtr, yCtr)