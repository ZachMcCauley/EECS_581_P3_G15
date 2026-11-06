'''
Written by Emilia Davis.
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

def clearMatch(grid, minLen = 3) -> int:
    matched = _findMatch(grid, minLen)
    for pos in matched:
        tile = grid.GetTileByPosition(pos)
        tile.item.OnClear(pos)
        tile.item = None
    return len(matched)
 
