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
# Yes, I know this is bad practice. Do I care? No.
from Grid.TileActions import _findMatch #we are using TileActions now instead of individual files
import os
from re import fullmatch

class GameplayManager(GameManager):
    def __init__(self, screen, fps = 60, moves = 10, win_con = {"piece_mail":4}, level_num = 1):
        super().__init__(screen, fps)
        # Define our constants first
        # Percentage of the window that the grid occupies for rendering
        self.gridSpace = (0.6, 0.8)
        self.validTileNames = []
        self.draggedTile = None
        self.canSelectTile = True
        self.rem_moves = moves
        self.win_con = win_con
        self.pauseRect = pygame.Rect(8, 8, 64, 64)
        # Also form our grid.
        self.grid = None
        self.FormFromLevelInfo(level_num)
        self.combo = 0
    def FormFromLevelInfo(self, level_num=None):
        filename = "./Resources/Levels/level-" + str(level_num) + ".lvl"
        if level_num is None or not os.path.isfile(filename):
            # Also form our grid.
            self.grid = Grid.FormFromDims((8, 8))
            self.validTileNames = self.resourceManager.AllItemNames()
        else:
            file = open(filename, "r")
            # Get positions in grid
            positions = set()
            startedPositions = False
            for line in file:
                line = line.strip("\n")
                if startedPositions and not line.startswith("Vector2Int"):
                    break
                elif startedPositions:
                    # We should check our string before running eval in case it somehow contains mallicious code.
                    if not bool(fullmatch("Vector2Int\\(\\d+, *\\d+\\)", line)):
                        raise RuntimeError("Level line " + line + " is not safe to evaluate, and may be tampered with!")
                    positions.add(eval(line))
                elif line.startswith("Positions:"):
                    startedPositions = True
                    continue
                else:
                    continue
            self.grid = Grid(positions)
            # Determine which items are in play.
            startedItems = False
            file.seek(0)
            for line in file:
                line = line.strip("\n")
                if startedItems and line.endswith(":"):
                    break
                elif startedItems:
                    self.validTileNames.append(line)
                elif line.startswith("Items:"):
                    startedItems = True
                    continue
                else:
                    continue
            file.close()
            for space in self.grid.AllPositions():
                self.GenerateItemForTile(space, False)
            self.ChangeTilesToAvoidMatches()
    def RunInternal(self): #return 0 if game is still running, 1 if game is won, 2 if game is lost
        won = self.HasWon()
        if won and self.grid.IsStable():
            self.inGameLoop = False
            print("Game Won")
            return
        if self.rem_moves <= 0 and self.grid.IsStable():
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
        self.combo += TileActions.clearMatch(self.grid, self.win_con)
        if self.grid.IsStable():
            self.combo = 0
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
            self.GenerateItemForTile(tilePosition, True)
    def GenerateItemForTile(self, tilePosition, doFall):
        # Tile is at top of grid. Generate a new item.
        spriteName = self.validTileNames[randint(0, len(self.validTileNames) - 1)]
        sprite = self.resourceManager.GetItem(spriteName)
        item = Item(spriteName, sprite, 1 if doFall else 0)
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
        elif event.type == pygame.KEYDOWN and event.key in {pygame.K_p, pygame.K_b}:
            self.DoPause()
    def SetRequirements(self, moves, win_con):
        self.rem_moves = moves
        self.win_con = win_con
    def Render(self):
        # Render Catland
        catName = "catLand"
        if self.combo >= 2:
            catName = "catLandBazinga"
        elif self.rem_moves <= 0:
            catName = "catLandEvil"
        elif self.HasWon():
            catName = "catLandGood"
        catSprite = self.resourceManager.GetCat(catName)
        catSprite = pygame.transform.scale_by(catSprite, (self.screen.get_size()[0] / catSprite.get_width()))
        self.screen.blit(catSprite, (0, (self.screen.get_size()[1] - catSprite.get_height()) / 2))
        pauseSprite = pygame.transform.scale_by(self.resourceManager.pauseButton, 2)
        self.screen.blit(pauseSprite, self.pauseRect)
        self.grid.Render(self.screen, self.gridSpace, self.timeSinceLastTick)
    def DoPause(self):
        if not self.surrenderControl and self.inGameLoop:
            # Pause the game
            self.surrenderControl = True
            self.owner.AddGameManager(PauseScreen)
            print("Pause")
    """
        Reassign the items in tiles to avoid any matches.
        Call this when the grid is initially formed
        This is not the most efficient implementation of
        This function, and it's worst case time complexity
        Is O(Infinity), but I don't care.
    """
    def ChangeTilesToAvoidMatches(self):
        matches = _findMatch(self.grid)
        while len(matches) > 0:
            firstMatch = matches[0]
            pos = firstMatch["positions"][0]
            self.GenerateItemForTile(pos, False)
            matches = _findMatch(self.grid)

    def HasWon(self):
        won = True
        for value in self.win_con.values():
            if value != 0:
                won = False
        return won