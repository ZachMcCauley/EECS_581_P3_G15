'''
Author: Jett Viduya, assisted by Claude Opus 5.5 (debugging + syntax), all ideas are provided by human + understood/checked
Purpose: stores the board's tiles and handles positions, bounds, rendering, and mouse position to tile conversion
Date: 11/4/26 (mouse input additions)
'''

from Grid.Vector2Int import Vector2Int
from Grid.Vector2 import Vector2
from Grid.GridTile import GridTile
import math

class Grid:
    # Create the grid
    # The input is a list of Vector2Ints representing each position a tile occupies
    def __init__(self, positions):
        #store one tile for each given position
        # Add grid spaces to dictionary
        self.grid = dict()
        for pos in positions:
            self.grid[pos] = GridTile(pos)
    @staticmethod
    # Form a grid of some tuple of dimensions
    # e.g. FormFromDims((5, 7)) produces a 5x7 Grid
    def FormFromDims(dims):
        #create positions for every column and row in the requested dimensions
        pos = set()
        for x in range( dims[0]):
            for y in range(dims[1]):
                pos.add(Vector2Int(x, y))
        return Grid(pos)
    #GetLayout and ScreenToTile for mouse input.
    #Render and ScreenToTile share GetLayout so clicks line up with what is drawn.
    def GetLayout(self, screenSize, screenSpace):
        #calculate tile size and offsets for placing the grid on screen
        xBounds = screenSize[0] * screenSpace[0] / (self.MaxX() - self.MinX() + 1)
        yBounds = screenSize[1] * screenSpace[1] / (self.MaxY() - self.MinY() + 1)
        maxTileSize = math.floor(min(xBounds, yBounds))
        tileOffset = Vector2Int(self.MinX(), self.MinY()) * -1
        pixelOffset = (screenSize[0] * (1 - screenSpace[0]) / 2, screenSize[1] * (1 - screenSpace[1]) / 2)
        return maxTileSize, tileOffset, pixelOffset
    # Display the grid on the screen
    def Render(self, screen, screenSpace):
        #draw each tile using the calculated grid layout
        maxTileSize, tileOffset, pixelOffset = self.GetLayout(screen.get_size(), screenSpace)
        for tile in self.grid.values():
            tile.Render(screen, maxTileSize, tileOffset, pixelOffset)
    #returns the grid position under a pixel, or None if it isn't over a tile
    def ScreenToTile(self, screenSize, screenSpace, pixel):
        #use the grid layout to find which tile contains the pixel
        size, tileOffset, pixelOffset = self.GetLayout(screenSize, screenSpace)
        if size <= 0:
            return None
        pos = Vector2Int(math.floor((pixel[0] - pixelOffset[0]) / size) - tileOffset.x,
                         math.floor((pixel[1] - pixelOffset[1]) / size) - tileOffset.y)
        return pos if self.ContainsPosition(pos) else None
    # Get the lowest x coordinate of a tile on the grid
    def MinX(self) -> int:
        #scan the positions for the smallest x coordinate
        toReturn = None
        for key in self.grid.keys():
            if toReturn is None or key.x < toReturn:
                toReturn = key.x
        return toReturn
    # Get the highest x coordinate of a tile on the grid
    def MaxX(self) -> int:
        #scan the positions for the largest x coordinate
        toReturn = None
        for key in self.grid.keys():
            if toReturn is None or key.x > toReturn:
                toReturn = key.x
        return toReturn
    # Get the lowest y coordinate on the grid
    def MinY(self) -> int:
        #scan the positions for the smallest y coordinate
        toReturn = None
        for key in self.grid.keys():
            if toReturn is None or key.y < toReturn:
                toReturn = key.y
        return toReturn
    # Get the highest y coordinate on the grid
    def MaxY(self) -> int:
        #scan the positions for the largest y coordinate
        toReturn = None
        for key in self.grid.keys():
            if toReturn is None or key.y > toReturn:
                toReturn = key.y
        return toReturn
    # Get the center position of the grid
    def Center(self) -> Vector2:
        #find the midpoint between the grid's coordinate bounds
        xCtr = (self.MinX() + self.MaxX()) / 2
        yCtr = (self.MinY() + self.MaxY()) / 2
        return Vector2(xCtr, yCtr)
    # Check if a position is in the grid
    def ContainsPosition(self, pos : Vector2Int) -> bool:
        #check whether this position has a tile in the grid
        return pos in self.grid.keys()
    # Get the contained tile in the grid
    def GetTileByPosition(self, pos : Vector2Int) -> GridTile:
        #look up the tile stored at this position
        return self.grid[pos]
    # Get a list of all positions in the grid.
    def AllPositions(self) -> list:
        #return the grid's position keys as a list
        return list(self.grid.keys())
    
    #swap tiles at given positions, returns False if any error, True upon success
    #swap is done by changing the values of dctionary and then updating posiiton in GridTile to match its key 
    def SwapTiles(self, pos1: Vector2Int, pos2: Vector2Int) -> bool: #similar to ContainsPosition, accessing position in grid 
        #check the positions and adjacency before attempting the swap
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
    