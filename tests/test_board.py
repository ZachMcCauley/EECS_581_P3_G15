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
from Grid.Vector2 import Vector2
from Grid.Vector2Int import Vector2Int as V
from Grid import TileActions
from Grid.TileClear import _findMatch, clearMatch

#8x8 board with no 3-in-a-row anywhere (checkerboard of 4 item types)
NO_MATCH = ["ABABABAB", "CDCDCDCD"] * 4

#---------- grid ----------

#an 8x8 grid has 64 tiles, and bounds checks work on the edges (what clicks rely on)
def test_grid_is_8x8(grid):
    assert len(grid.AllPositions()) == 64
    assert grid.ContainsPosition(V(7, 7)) and not grid.ContainsPosition(V(8, 0))

#only the 4 tiles directly next to a tile count as adjacent
def test_adjacency(grid):
    tile = grid.GetTileByPosition(V(3, 3))
    assert tile.IsAdjacentTo(grid.GetTileByPosition(V(4, 3)))
    assert not tile.IsAdjacentTo(grid.GetTileByPosition(V(4, 4)))   #diagonal
    assert not tile.IsAdjacentTo(tile)                             #same tile

#---------- swapping ----------

#callTileSwap exchanges the items of neighbors and leaves non-neighbors alone
def test_call_tile_swap_swaps_neighbors_only(grid):
    fill(grid, ["AB", "CD"])
    a, b, d = (grid.GetTileByPosition(V(x, y)) for x, y in [(0, 0), (1, 0), (1, 1)])
    assert TileActions.callTileSwap(a, b) and (a.item.name, b.item.name) == ("B", "A")
    assert not TileActions.callTileSwap(a, d) and a.item.name == "B"

#swapping twice puts the board back, which is what undoing a no-match swap relies on
def test_swapping_twice_restores_board(grid):
    fill(grid, ["AB"])
    a, b = grid.GetTileByPosition(V(0, 0)), grid.GetTileByPosition(V(1, 0))
    TileActions.callTileSwap(a, b)
    TileActions.callTileSwap(a, b)
    assert (a.item.name, b.item.name) == ("A", "B")

#SwapTiles moves the tiles and every tile still knows its own position afterwards
def test_swap_tiles_keeps_positions_in_sync(grid):
    fill(grid, ["AB"])
    assert TileActions.SwapTiles(grid, V(0, 0), V(1, 0))
    assert grid.GetTileByPosition(V(0, 0)).item.name == "B"
    for pos in grid.AllPositions():
        assert grid.GetTileByPosition(pos).position == pos

#SwapTiles refuses diagonal and off-grid swaps
def test_swap_tiles_rejects_bad_moves(grid):
    fill(grid, ["AB", "CD"])
    assert not TileActions.SwapTiles(grid, V(0, 0), V(1, 1))   #diagonal
    assert not TileActions.SwapTiles(grid, V(0, 0), V(-1, 0))  #off the grid

#---------- matching ----------

#a clean board has nothing to match
def test_no_match_on_clean_board(grid):
    assert _findMatch(fill(grid, NO_MATCH)) == []

#a horizontal and a vertical row of three are both found, including at the far edge
def test_finds_row_and_column_of_three(grid):
    rows = ["XXXBABAB"] + NO_MATCH[1:]
    rows[1] = "CDCDCDCY"
    rows[2] = "ABABABAY"
    rows[3] = "CDCDCDCY"
    found = [set(m) for m in _findMatch(fill(grid, rows))]
    assert {V(0, 0), V(1, 0), V(2, 0)} in found and {V(7, 1), V(7, 2), V(7, 3)} in found

#clearMatch empties the matched tiles and nothing else
def test_clear_match_empties_only_matched_tiles(grid):
    fill(grid, ["XXXBABAB"] + NO_MATCH[1:])
    assert clearMatch(grid) == 1
    assert all(grid.GetTileByPosition(V(x, 0)).item is None for x in range(3))
    assert grid.GetTileByPosition(V(3, 0)).item.name == "B"

#a row of 4 should be one match; every X tile in it, only once
@pytest.mark.xfail(strict=True, reason="BUG: a run of 4+ is found more than once, so clearMatch's count is too high")
def test_run_of_four_counted_once(grid):
    fill(grid, ["XXXXBABA"] + NO_MATCH[1:])
    assert clearMatch(grid) == 1

#both arms of an L shape should be found
@pytest.mark.xfail(strict=False, reason="BUG: a tile already in a horizontal match is skipped when scanning "
                                         "vertically, so the vertical arm of an L/T shape can be missed")
def test_l_shape(grid):
    rows = ["XXXBABAB", "XDCDCDCD", "XBABABAB"] + NO_MATCH[3:]
    assert len({p for m in _findMatch(fill(grid, rows)) for p in m}) == 5

#---------- refilling ----------

#a game with its board filled up (one pass per row in the worst case)
@pytest.fixture
def gm():
    from GameplayManager import GameplayManager
    gm = GameplayManager(pygame.display.get_surface())
    for _ in range(8):
        gm.CheckAllTilesItems()
    return gm

#every tile has an item once the board fills
def test_board_fills_up(gm):
    assert all(gm.grid.GetTileByPosition(p).item is not None for p in gm.grid.AllPositions())

#an emptied tile gets the item from the tile above it
def test_empty_tile_refills_from_above(gm):
    above = gm.grid.GetTileByPosition(V(4, 4)).item   #y-1 is "above" on screen
    gm.grid.GetTileByPosition(V(4, 5)).item = None
    gm.CheckAllTilesItems()
    assert gm.grid.GetTileByPosition(V(4, 5)).item is above

#---------- vectors ----------

#float vectors keep their decimals when multiplied
def test_vector2_multiply_keeps_decimals():
    assert Vector2(0.5, 1.5) * 1 == Vector2(0.5, 1.5)

#comparing a vector to something that isn't a vector should just be False
@pytest.mark.xfail(strict=True, reason="BUG: __eq__ assumes 'other' is a vector; comparing to None raises AttributeError instead of returning False")
def test_vector_compare_to_none():
    assert (V(1, 2) == None) is False
