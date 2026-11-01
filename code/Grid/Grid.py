from Vector2Int import Vector2Int
from GridTile import GridTile

class Grid:
    def __init__(self, positions):
        # Add grid spaces to dictionary
        self.grid = dict()
        for pos in positions:
            self.grid[pos] = GridTile(pos)
    @staticmethod
    def FormFromDims(dims):
        pos = set()
        for x in dims[0]:
            for y in dims[1]:
                pos.add(Vector2Int(x, y))
        return Grid(pos)