#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 15:32:27 2026

@author: eliza m 
checked work and compatability with deepseek AI 
"""

#code by dani harris start 
def SelectedTile():  #insertParams
    #fill in user input
    #return True if selected 
    return True 

def callTileSwap(Tile1, Tile2): #check if swap is valid 
    if Tile1.IsAdjacentTo(Tile2):
        SwapTiles(Tile1, Tile2)
        return True
    else: #play incorrect annimation 
        #animation call here
        return False 
#code by dani harris end 

#code by emilia davis start 
'''
Written by Emilia Davis
Assisted by Claude Sonnet 5.5.
Ideas provided by a human.
All generated code understood and checked.
'''

from Grid.Vector2Int import Vector2Int

d = (Vector2Int.Right(), Vector2Int.Up())

def _findMatch(grid, minLen = 3):
    # hold currently found matches
    matches = []
    for direction in d: # scan all directions
        for pos in grid.AllPositions():
            tile = grid.GetTileByPosition(pos)
            if tile.item is None:
                continue
            # make sure not already part of match
            if any(pos in match for match in matches):
                continue
            currentMatch = [pos]
            nextPos = pos + direction # go next
            while grid.ContainsPosition(nextPos): # scan
                nextTile = grid.GetTileByPosition(nextPos)
                if nextTile.item is not None and nextTile.item == tile.item: # check it exists and matches
                    currentMatch.append(nextPos)
                    nextPos += direction
                else:
                    break
            if len(currentMatch) >= minLen: # all that are above allowed len added
                matches.append(currentMatch)
    return matches

def clearMatch(grid, minLen = 3) -> int: #get rid of tiles that are matched from grid 
    matched = _findMatch(grid, minLen)
    #print(matched)
    for pattern in matched:
        for pos in pattern:
            tile = grid.GetTileByPosition(pos)
            if tile.item is not None:
                tile.item.OnClear(pos)
            tile.item = None
    return len(matched)
#code by emilia Davis end 

#code by eliza m start 
#swap tiles at given positions, returns False if any error, True upon success
#swap is done by changing the values of dctionary and then updating posiiton in GridTile to match its key 
def SwapTiles(grid, pos1: Vector2Int, pos2: Vector2Int) -> bool: #similar to ContainsPosition, accessing position in grid 
    #what about swapping two empty tiles? 
    #check that both positions are in grid 
    if (grid.ContainsPosition(pos1) and grid.ContainsPosition(pos2)): 
        Tile1=grid.grid[pos1] 
        Tile2=grid.grid[pos2]
        if not Tile1.IsAdjacentTo(Tile2): 
            print ("tiles not adjacent")
            return False 
        grid.grid[pos1], grid.grid[pos2] = Tile2, Tile1 #swap the tiles positions in grid dictionary  
        Tile1.position, Tile2.position = pos2, pos1 #update positions to match the dictionary keys 
        return True #if it made it this far it deserves to return true 
    else: 
        print("one of the tiles is not in grid")
        return False 
#code by eliza m end 