'''
Author: Jett Viduya, assisted by Claude Opus 5.5 (debugging + syntax), all ideas are provided by human + understood/checked
Purpose: handles input for tile selection and swapping
Date: 11/4/26

Left click a tile to select it, then click a neighbor to swap them.
You can also drag a tile onto a neighbor to swap.
'''

import pygame
from Grid.TileSwap import ValidCheck

class InputHandler:
    def __init__(self, grid, screenSpace, onSwap = None):
        #store the grid, screen layout, and optional swap callback
        self.grid = grid
        self.screenSpace = screenSpace
        #called as onSwap(pos1, pos2) after a swap, so match detection can hook in
        self.onSwap = onSwap
        self.selected = None    #grid position of the selected tile
        self.pressTile = None   #tile the mouse was pressed on
        self.enabled = True     #set False to ignore input (e.g. while tiles fall)

    def HandleEvent(self, event, screenSize):
        #turn left mouse presses and releases into clicks or drags
        #only care about the left mouse button
        if not self.enabled or getattr(event, "button", None) != 1:
            return
        tile = self.grid.ScreenToTile(screenSize, self.screenSpace, event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.pressTile = tile
        elif event.type == pygame.MOUSEBUTTONUP:
            pressTile, self.pressTile = self.pressTile, None
            if pressTile is None or tile is None:
                #pressed and released outside the grid counts as a click outside
                if pressTile is None and tile is None:
                    self.Click(None)
            elif tile == pressTile:
                self.Click(tile)
            else:
                #dragged from one tile onto another
                self.selected = None
                self.TrySwap(pressTile, tile)

    def Click(self, tile):
        #select or deselect a tile, or try swapping it with the selection
        if tile is None:
            #clicked outside the grid
            self.selected = None
        elif self.selected is None:
            self.selected = tile
        elif tile == self.selected:
            #clicked the same tile again
            self.selected = None
        elif self.TrySwap(self.selected, tile):
            self.selected = None
        else:
            #not next to the selected tile, so select this one instead
            self.selected = tile

    def TrySwap(self, pos1, pos2):
        #try a swap and notify the callback if it succeeds
        #ValidCheck only swaps if the two tiles are next to each other
        if not ValidCheck(self.grid.GetTileByPosition(pos1), self.grid.GetTileByPosition(pos2)):
            return False
        if self.onSwap is not None:
            self.onSwap(pos1, pos2)
        return True

    def Render(self, screen):
        #show which tile is currently selected
        #draw a gold outline around the selected tile
        if self.selected is None:
            return
        size, tileOffset, pixelOffset = self.grid.GetLayout(screen.get_size(), self.screenSpace)
        left = (tileOffset.x + self.selected.x) * size + pixelOffset[0]
        top = (tileOffset.y + self.selected.y) * size + pixelOffset[1]
        pygame.draw.rect(screen, (255, 215, 0), pygame.Rect(left, top, size, size), 4)
