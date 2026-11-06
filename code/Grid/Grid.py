from Grid.Vector2Int import Vector2Int
from Grid.Vector2 import Vector2
from Grid.GridTile import GridTile
import math

class Grid:
    # Create the grid
    # The input is a list of Vector2Ints representing each position a tile occupies
    def __init__(self, positions):
        # Add grid spaces to dictionary
        self.grid = dict()
        for pos in positions:
            self.grid[pos] = GridTile(pos)
    @staticmethod
    # Form a grid of some tuple of dimensions
    # e.g. FormFromDims((5, 7)) produces a 5x7 Grid
    def FormFromDims(dims):
        pos = set()
        for x in range( dims[0]):
            for y in range(dims[1]):
                pos.add(Vector2Int(x, y))
        return Grid(pos)
    # Display the grid on the screen
    def Render(self, screen, screenSpace):
        # Determine the size of each tile
        screenSize = screen.get_size()
        xBounds = screenSize[0] * screenSpace[0] / (self.MaxX() - self.MinX() + 1)
        yBounds = screenSize[1] * screenSpace[1] / (self.MaxY() - self.MinY() + 1)
        constrainedOnX = xBounds < yBounds
        maxTileSize = min(xBounds, yBounds)
        maxTileSize = math.floor(maxTileSize)
        """
        WIP
        
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
    # Get the lowest x coordinate of a tile on the grid
    def MinX(self) -> int:
        toReturn = None
        for key in self.grid.keys():
            if toReturn is None or key.x < toReturn:
                toReturn = key.x
        return toReturn
    # Get the highest x coordinate of a tile on the grid
    def MaxX(self) -> int:
        toReturn = None
        for key in self.grid.keys():
            if toReturn is None or key.x > toReturn:
                toReturn = key.x
        return toReturn
    # Get the lowest y coordinate on the grid
    def MinY(self) -> int:
        toReturn = None
        for key in self.grid.keys():
            if toReturn is None or key.y < toReturn:
                toReturn = key.y
        return toReturn
    # Get the highest y coordinate on the grid
    def MaxY(self) -> int:
        toReturn = None
        for key in self.grid.keys():
            if toReturn is None or key.y > toReturn:
                toReturn = key.y
        return toReturn
    # Get the center position of the grid
    def Center(self) -> Vector2:
        xCtr = (self.MinX() + self.MaxX()) / 2
        yCtr = (self.MinY() + self.MaxY()) / 2
        return Vector2(xCtr, yCtr)
    # Check if a position is in the grid
    def ContainsPosition(self, pos : Vector2Int) -> bool:
        return pos in self.grid.keys()
    # Get the contained tile in the grid
    def GetTileByPosition(self, pos : Vector2Int) -> GridTile:
        return self.grid[pos]
    # Get a list of all positions in the grid.
    def AllPositions(self) -> list:
        return list(self.grid.keys())
    
    #swap tiles at given positions, returns False if any error, True upon success
    #swap is done by changing the values of dctionary and then updating posiiton in GridTile to match its key 
    def SwapTiles(self, pos1: Vector2Int, pos2: Vector2Int) -> bool: #similar to ContainsPosition, accessing position in grid 
        #check that both positions are in grid DO THIS 
        if (self.ContainsPosition(pos1) and self.ContainsPosition(pos2)): 
            Tile1=self.grid[pos1]
            Tile2=self.grid[pos2]
            if not Tile1.IsAdjacentTo(Tile2): 
                print ("tiles not adjacent")
                return False 
            self.grid[pos1], self.grid[pos2] = Tile1, Tile2 #swap the tiles positions in grid dictionary  
            Tile1.postion, Tile2.posiiton = pos1, pos2 #update positions to match the dictionary keys 
            return True #if it made it this far it deserves to return true 
        else: 
            print("tiles not in grid")
            return False 
    