import pygame.mouse
#import Grid.TileSwap
#import Grid.TileClear
import Grid.TileActions
from GameManagers.GameManager import GameManager
#from Grid import TileClear
from Grid import TileActions
from Grid.Grid import Grid
from Grid.Vector2Int import Vector2Int
from Grid.Item import Item
from random import randint
from GameManagers.PauseScreen import PauseScreen

class GameplayManager(GameManager):
    def __init__(self, screen, fps = 60, moves = 10, win_con = {"piece_mail":4}):
        super().__init__(screen, fps)
        # Also form our grid.
        self.grid = Grid.FormFromDims((8, 8))
        # Percentage of the window that the grid occupies for rendering
        self.gridSpace = (0.6, 0.8)
        self.validTileNames = self.resourceManager.AllItemNames()
        self.draggedTile = None
        self.canSelectTile = True
        self.rem_moves = moves
        self.win_con = win_con
        self.pauseRect = pygame.Rect(8, 8, 64, 64)
    def RunInternal(self): #return 0 if game is still running, 1 if game is won, 2 if game is lost
        won = True
        for value in self.win_con.values():
            if value != 0:
                won = False
            if won:
                self.inGameLoop = False
                print("Game Won")
                return
        if self.rem_moves <= 0:
            self.inGameLoop = False
            print("Game Lost")
            return
        if pygame.mouse.get_pressed()[0]:
            selectingTile = self.grid.GetMousePositionInGrid()
            if self.draggedTile is not None and selectingTile is not None and self.draggedTile != selectingTile:
                t1 = self.grid.GetTileByPosition(self.draggedTile)
                t2 = self.grid.GetTileByPosition(selectingTile)
                TileActions.callTileSwap(t1, t2)
                if TileActions.clearMatch(self.grid, self.win_con) == 0: #no matches were made
                    TileActions.callTileSwap(t1, t2) #revert to previous state
                else:
                    self.draggedTile = None
                    self.canSelectTile = False
                    self.rem_moves -= 1
            elif self.canSelectTile:
                self.draggedTile = selectingTile
        else:
            self.draggedTile = None
        super().RunInternal()
        # And render our grid
        TileActions.clearMatch(self.grid, self.win_con)
        self.CheckAllTilesItems()
        self.Render()
        return
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
        mousePos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.pauseRect.collidepoint(mousePos):
            self.DoPause()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.canSelectTile = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.DoPause()
    def SetRequirements(self, moves, win_con):
        self.rem_moves = moves
        self.win_con = win_con
    def Render(self):
        pauseSprite = pygame.transform.scale_by(self.resourceManager.pauseButton, 2)
        self.screen.blit(pauseSprite, self.pauseRect)
        self.grid.Render(self.screen, self.gridSpace)
    def DoPause(self):
        if not self.surrenderControl and self.inGameLoop:
            # Pause the game
            self.surrenderControl = True
            self.owner.AddGameManager(PauseScreen)
            print("Pause")