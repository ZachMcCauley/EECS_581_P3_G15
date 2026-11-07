import pygame.mouse
import Grid.TileSwap
from GameManager import GameManager
from Grid import TileSwap
from Grid.Grid import Grid
from Grid.Vector2Int import Vector2Int
from Grid.Item import Item
from random import randint

class GameplayManager(GameManager):
    def __init__(self, screen, fps = 60):
        super().__init__(screen, fps)
        # Also form our grid.
        self.grid = Grid.FormFromDims((8, 8))
        # Percentage of the window that the grid occupies for rendering
        self.gridSpace = (0.6, 0.8)
        self.validTileNames = self.resourceManager.AllItemNames()
        self.draggedTile = None
        self.canSelectTile = True
    def RunInternal(self):
        if pygame.mouse.get_pressed()[0]:
            selectingTile = self.grid.GetMousePositionInGrid()
            if self.draggedTile is not None and selectingTile is not None and self.draggedTile != selectingTile:
                t1 = self.grid.GetTileByPosition(self.draggedTile)
                t2 = self.grid.GetTileByPosition(selectingTile)
                TileSwap.ValidCheck(t1, t2)
                self.draggedTile = None
                self.canSelectTile = False
            elif self.canSelectTile:
                self.draggedTile = selectingTile
        else:
            self.draggedTile = None
        super().RunInternal()
        # And render our grid
        self.CheckAllTilesItems()
        self.grid.Render(self.screen, self.gridSpace)
    # Generate an item for a tile.
    def GetItemForTile(self, tilePosition):
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
        for pos in self.grid.AllPositions():
            tile = self.grid.GetTileByPosition(pos)
            if tile.item is None:
                self.GetItemForTile(tile.position)
    def HandleSingleEvent(self, event: pygame.event.Event) -> None:
        super().HandleSingleEvent(event)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.canSelectTile = True

    #move tiles downward until no tiles are none
    def MoveDown(self) -> None:
        moving = True #says if tiles are still moving downward
        while moving:
            moving = False #assume no tiles need to move downward until we move them
            for tile in self.grid.keys():
                if self.grid[tile].item is None: #tile is empty, needs a new item
                    moving = True #tile is changed, will need to keep moving or check grid again
                    above = tile + Vector2Int.Down() #determine position of above cell
                    if above.y == -1: #tile is at the top of the grid, generate new random item
                        spriteName = self.validTileNames[randint(0, len(self.validTileNames) - 1)]
                        sprite = self.resourceManager.GetItem(spriteName)
                        item = Item(spriteName, sprite)
                        self.grid[tile].item = item
                    else:
                        self.grid[tile].item = self.grid[tile + Vector2Int.Down()].item #tile takes item value from above tile
                        self.grid[tile + Vector2Int.Down()].item = None #above tile loses it's value