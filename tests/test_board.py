'''
Author: Jett Viduya, assisted by Claude Opus 5.5 (debugging + syntax), all ideas are provided by human + understood/checked
Purpose: tests for the existing board code (grid, swapping, matching, refilling)
Date: 11/6/26

Tests marked xfail are bugs we found. When one gets fixed its test will fail,
which means the xfail line above it can be removed.
'''

import pygame
import pytest
from conftest import fill
from Grid.Grid import Grid
from Grid.Vector2 import Vector2
from Grid.Vector2Int import Vector2Int as V
from Grid.TileSwap import ValidCheck
from Grid.TileClear import _findMatch, clearMatch

NO_MATCH = ["ABABABAB", "CDCDCDCD"] * 4

#---------- grid ----------

def test_grid_is_8x8(grid):
    #check the number of grid positions and the board boundaries
    assert len(grid.AllPositions()) == 64
    assert grid.ContainsPosition(V(7, 7)) and not grid.ContainsPosition(V(8, 0))

def test_adjacency(grid):
    #check that a neighbor is adjacent but a diagonal or the same tile is not
    tile = grid.GetTileByPosition(V(3, 3))
    assert tile.IsAdjacentTo(grid.GetTileByPosition(V(4, 3)))
    assert not tile.IsAdjacentTo(grid.GetTileByPosition(V(4, 4)))   #diagonal
    assert not tile.IsAdjacentTo(tile)

#---------- swapping ----------

def test_valid_check_swaps_neighbors_only(grid):
    #check that neighboring items swap but diagonal tiles are rejected
    fill(grid, ["AB", "CD"])
    a, b, d = (grid.GetTileByPosition(V(x, y)) for x, y in [(0, 0), (1, 0), (1, 1)])
    assert ValidCheck(a, b) and (a.item.name, b.item.name) == ("B", "A")
    assert not ValidCheck(a, d) and a.item.name == "B"

@pytest.mark.xfail(strict=True, reason="BUG: Grid.SwapTiles returns True but doesn't move anything")
def test_grid_swap_tiles(grid):
    #check that swapping adjacent grid positions moves their items
    fill(grid, ["AB"])
    grid.SwapTiles(V(0, 0), V(1, 0))
    assert grid.GetTileByPosition(V(0, 0)).item.name == "B"

#---------- matching ----------

def test_no_match_on_clean_board(grid):
    #check that a board without matching runs has no matches
    assert _findMatch(fill(grid, NO_MATCH)) == []

def test_finds_row_and_column_of_three(grid):
    #check that horizontal and vertical runs of three are found
    rows = ["XXXBABAB"] + NO_MATCH[1:]
    rows[1] = "CDCDCDCY"
    rows[2] = "ABABABAY"
    rows[3] = "CDCDCDCY"
    found = [set(m) for m in _findMatch(fill(grid, rows))]
    assert {V(0, 0), V(1, 0), V(2, 0)} in found and {V(7, 1), V(7, 2), V(7, 3)} in found

@pytest.mark.xfail(strict=True, reason="BUG: a run of 4+ is counted more than once")
def test_run_of_four_counted_once(grid):
    #check that a run of four does not count any tile more than once
    found = [p for m in _findMatch(fill(grid, ["XXXXBABA"] + NO_MATCH[1:])) for p in m]
    assert len(found) == 4

@pytest.mark.xfail(strict=False, reason="BUG: the second arm of an L shape can be missed")
def test_l_shape(grid):
    #check that both arms of an L-shaped match are found
    rows = ["XXXBABAB", "XDCDCDCD", "XBABABAB"] + NO_MATCH[3:]
    assert len({p for m in _findMatch(fill(grid, rows)) for p in m}) == 5

@pytest.mark.xfail(strict=True, raises=TypeError, reason="BUG: clearMatch crashes when there is a match")
def test_clear_match(grid):
    #check that clearing a match empties a matched tile
    fill(grid, ["XXXBABAB"] + NO_MATCH[1:])
    clearMatch(grid)
    assert grid.GetTileByPosition(V(0, 0)).item is None

#---------- refilling ----------

@pytest.fixture
def gm():
    #create a gameplay manager and run enough refill passes to fill its board
    from GameplayManager import GameplayManager
    gm = GameplayManager(pygame.display.get_surface())
    for _ in range(8):
        gm.CheckAllTilesItems()
    return gm

def test_board_fills_up(gm):
    #check that every tile has an item after refilling
    assert all(gm.grid.GetTileByPosition(p).item is not None for p in gm.grid.AllPositions())

def test_empty_tile_refills_from_above(gm):
    #check that an empty tile receives the item above it
    above = gm.grid.GetTileByPosition(V(4, 4)).item
    gm.grid.GetTileByPosition(V(4, 5)).item = None
    gm.CheckAllTilesItems()
    assert gm.grid.GetTileByPosition(V(4, 5)).item is above

@pytest.mark.xfail(strict=False, reason="not done yet: the starting board can already have matches")
def test_starting_board_has_no_matches(gm):
    #check that the starting board contains no matches
    assert _findMatch(gm.grid) == []

#---------- vectors ----------

@pytest.mark.xfail(strict=True, reason="BUG: Vector2 multiplication rounds to whole numbers")
def test_vector2_multiply():
    #check that multiplying a vector preserves fractional coordinates
    assert Vector2(0.5, 1.5) * 1 == Vector2(0.5, 1.5)

@pytest.mark.xfail(strict=True, reason="BUG: comparing a vector to None crashes instead of returning False")
def test_vector_compare_to_none():
    #check that comparing a vector to None returns False
    assert (V(1, 2) == None) is False
