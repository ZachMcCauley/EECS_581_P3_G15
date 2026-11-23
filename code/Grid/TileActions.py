#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 15:32:27 2026

authors: em, emilia davis, 
checked work and compatability with deepseek AI and chatGPT 
"""
'''
Written by Emilia Davis
Assisted by Claude Sonnet 5.5.
Ideas provided by a human.
All generated code understood and checked.
'''

from Grid.Vector2Int import Vector2Int
from Grid.Item import Item, PowerUp
from ResourceManager import ResourceManager
import pygame

def SelectedTile():  #insertParams
    #fill in user input
    #return True if selected 
    return True 

def callTileSwap(Tile1, Tile2): #check if swap is valid 
    if Tile1.IsAdjacentTo(Tile2):
        TileSwap(Tile1, Tile2)
        return True
    else: #play incorrect annimation 
        #animation call here
        return False 

def TileSwap(Tile1, Tile2):
    Tile1.item, Tile2.item = Tile2.item, Tile1.item
    return True


d = (Vector2Int.Right(), Vector2Int.Up())
def _findMatch(grid, minLen = 3):
    # hold currently found matches
    matches = []
    usedPos=set() 
    #check for powerup special matches first 
    shapes=[("T", TSHAPE), ("L", LSHAPE)] 
    '''generally: does to every position in grid, 
    tries the shape at that position and its orientations and that they have the same matching item, 
    then saves positions
    '''
    for pos in grid.AllPositions():
        tile = grid.GetTileByPosition(pos)
        if tile.item is None: continue #error check 
       
        # make sure not already part of match
        if any(pos in match for match in matches):
            continue
        for shapeName, shape in shapes: #check special shapes T,L and their orientations 
            orientations=getAllOrientations(shape) #get all possible types of the shape 
            for orientation in orientations: #for each shape... 
                if matchedShape(grid, pos, orientation): #...if its valid, check and append it 
                    matchedPos=[] 
                    for x,y in orientation: 
                        checkPos=pos+Vector2Int(x,y) 
                        matchedPos.append(checkPos) 

                        # Find the intersection within this specific orientation
                    intersectionOffset = findIntersection(orientation)
                    intersectionPos = (
                        pos + Vector2Int(*intersectionOffset)
                        if intersectionOffset is not None
                        else None
                    )
                        
                    repeat=False #cant use tile for two diff matches; this prevents it 
                    for matchP in matchedPos: #if find that already accounted for then break current loop 
                        if matchP in usedPos: 
                            repeat=True 
                            break 
                    if repeat: continue 
                    
                    matches.append({"type": shapeName, "positions": matchedPos, "intersection": intersectionPos}) #new way of saving match 
                    for matchP in matchedPos: 
                        usedPos.add(matchP)
                    
                    
    
    for direction in d: # scan all directions
        for pos in grid.AllPositions():
            tile = grid.GetTileByPosition(pos)
            if tile.item is None:
                continue
            # make sure not already part of match
            if any(pos in match["positions"] for match in matches): #matches is now dictionary so had to adjust 
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
                
         
            if len(currentMatch)>=minLen: #classify the line based on its length
                if len(currentMatch)>=5:
                    shapeName="LINE5"
                elif len(currentMatch)==4:
                    shapeName="LINE4"
                else:
                    shapeName="LINE3"
                matches.append({"type": shapeName, "positions": currentMatch})
                for matchP in currentMatch: 
                    usedPos.add(matchP)
    return matches


def clearMatch(grid, win_con ,minLen = 3, powerupPos=None) -> int: #get rid of tiles that are matched from grid 
    #do not match tiles while grid is unstable
    if not grid.IsStable():
        return 0
    matched = _findMatch(grid, minLen)
    for pattern in matched:
        matchType=pattern["type"] #use later when we decide types of powerups 
        intersectionPos = pattern.get("intersection")  # Get the intersection position if it exists
        if matchType in ("LINE4", "LINE5") and powerupPos is in pattern["positions"]:
            preservedPos = powerupPos
        for pos in pattern["positions"]: #now _findMatch() returns a dictionary with types of powerups/regular matches 
            tile = grid.GetTileByPosition(pos)
            if intersectionPos is not None and pos == intersectionPos:
                continue
            if tile.item is not None:
                tile.item.OnClear(pos)
                for key in win_con.keys():
                    if key == tile.item.name:
                        if win_con[key] > 0:
                            win_con[key] -= 1
            tile.item = None
        
        if intersectionPos is not None:
            tile = grid.GetTileByPosition(intersectionPos)

            if tile.item is not None:
                tile.item = PowerUp(
                    base_item=tile.item,
                    powerup_type=matchType,
                    sprite = ResourceManager.Instance.GetItem("rainbow_powerup").convert_alpha()
                )

        if preservedPos is not None:
            tile = grid.GetTileByPosition(preservedPos)

            if tile.item is not None:
                tile.item = PowerUp(
                    base_item=tile.item,
                    powerup_type=matchType,
                    sprite=ResourceManager.Instance.GetItem("rainbow_powerup"),
                )
                
            #discussed: need to find tile that will hold the powerup tile instead of just clearing everything 
            #prob use pattern similar to defining positions for T and L to specify a position that will have the result 
            #like intersection of the lines for T and L 
            
    return len(matched)

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
        
#shapes in grid for T, L, and xxxx, xxxxx matches 
#this is just tempate for shape, make into Vector2Int l8r and use algo for checking if shape exists from positions on grid 
#use algebra/multipliers 
TSHAPE= [(0, 0), (1, 0), (2, 0), (1, 1)]
LSHAPE= [(0, 0), (0, 1), (0, 2), (1, 0)]
LINE3= [(0, 0), (1, 0), (2, 0)]
LINE4= [(0, 0), (1, 0), (2, 0),(3, 0)]
LINE5= [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]

#want L and T shape to be recognized even when flipped REVISIT 
def rotateShape(shape): #assisted w AI 
    rotated=[]
    for x, y in shape:
        rotated.append((-y, x))
    return rotated

def flipShape(shape): #assisted w AI 
    flipped=[]
    for x, y in shape:
        flipped.append((-x, y))
    return flipped

def fixShape(shape): #other functions make coords neg, so we need to make them pos again 
    minX=min(x for x, y in shape)
    minY=min(y for x, y in shape)
    normalized=[]
    for x, y in shape:
        normalized.append((x-minX, y-minY))
    return tuple(sorted(normalized))

def getAllOrientations(shape): 
    orientations=[]
    current=shape

    for i in range(4): #rotate 4 times 
        normal=fixShape(current) #normal orientation 
        if normal not in orientations: 
            orientations.append(normal) #only append new stuff 
        
        flipped=fixShape(flipShape(current)) #reflected orientation
        if flipped not in orientations: 
            orientations.append(flipped)
        current=rotateShape(current) #rotate before next iteration 
    return orientations #all possible orientations 

def findIntersection(shape):
    #Gets the intersection of T and L matches.
    for candidate in shape:
        cx, cy = candidate
        neighbor_count = sum(
            (nx, ny) in shape
            and abs(nx - cx) + abs(ny - cy) == 1
            for nx, ny in shape
        )
        if neighbor_count >= 2:
            return candidate
    return None

def matchedShape(grid, startPos, shape): #check that a given shape has all the same tiles otherwise its not a match 
    firstTile=grid.GetTileByPosition(startPos) #get tile at the start of the shape; defined differently for each shape 
    if firstTile.item is None: #error check 
        return False
    for x, y in shape: #check every tile in the shape 
        checkPos=startPos+Vector2Int(x, y) #AI assist 
        if not grid.ContainsPosition(checkPos): #check that position is in grid 
            return False

        checkTile=grid.GetTileByPosition(checkPos)
        if checkTile.item is None: #emty tile 
            return False

        if checkTile.item!=firstTile.item: #check that tiles match 
            return False
    return True #if all checks pass then return true 