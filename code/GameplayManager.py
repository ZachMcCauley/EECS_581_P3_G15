'''
Author: Jett Viduya, assisted by Claude Opus 5.5 (debugging + syntax), all ideas are provided by human + understood/checked
Purpose: runs the gameplay screen: fills the board, handles events, and draws the grid
Date: 11/4/26 (mouse input additions)
'''

from GameManager import GameManager
from Grid.Grid import Grid
from Grid.Vector2Int import Vector2Int
from Grid.Item import Item
from random import randint
from InputHandler import InputHandler

class GameplayManager(GameManager):
    def __init__(self, screen, fps = 60):
        #set up the game grid, item names, and input handler
        super().__init__(screen, fps)
        # Also form our grid.
        self.grid = Grid.FormFromDims((8, 8))
        # Percentage of the window that the grid occupies for rendering
        self.gridSpace = (0.6, 0.8)
        self.validTileNames = self.resourceManager.AllItemNames()
        self.input = InputHandler(self.grid, self.gridSpace)
    def HandleSingleEvent(self, event):
        #handle the game event and pass it to the input handler
        super().HandleSingleEvent(event)
        self.input.HandleEvent(event, self.screen.get_size())
    def RunInternal(self):
        #refill and draw the board and its selection each frame
        super().RunInternal()
        # And render our grid
        self.CheckAllTilesItems()
        self.grid.Render(self.screen, self.gridSpace)
        self.input.Render(self.screen)
    # Generate an item for a tile.
    def GetItemForTile(self, tilePosition):
        #fill a tile from above or generate an item at the top
        # Down is up. Don't think about it too hard.
        if self.grid.ContainsPosition(tilePosition + Vector2Int.Down()):
            # Tile is not at top of grid. Pull from above.
            aboveTile = self.grid.GetTileByPosition(tilePosition + Vector2Int.Down())
            self.grid.GetTileByPosition(tilePosition).item = aboveTile.StealItemFromMe()
        else:
            # Tile is at top of grid. Generate a new item.
            spriteName = self.validTileNames[randint(0, len(self.validTileNames) - 1)]
            sprite = self.resourceManager.GetItem(spriteName)
            item = Item(spriteName, sprite)
            self.grid.GetTileByPosition(tilePosition).item = item
    def CheckAllTilesItems(self):
        #look for empty tiles and try to refill each one
        for pos in self.grid.AllPositions():
            tile = self.grid.GetTileByPosition(pos)
            if tile.item is None:
                self.GetItemForTile(tile.position)