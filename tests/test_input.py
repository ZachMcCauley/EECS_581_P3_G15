'''
Author: Jett Viduya, assisted by Claude Opus 5.5 (debugging + syntax), all ideas are provided by human + understood/checked
Purpose: tests for mouse input (InputHandler and Grid.ScreenToTile)
Date: 11/5/26
'''

import pygame
import pytest
from conftest import fill
from Grid.Vector2Int import Vector2Int as V
from InputHandler import InputHandler

SPACE = (0.6, 0.8)
SIZE = (800, 600)   #gives 60px tiles, grid covers x 160-639 and y 60-539

def centre(grid, x, y, size=SIZE):
    #find the screen pixel at the centre of a tile
    tile, offset, pixel = grid.GetLayout(size, SPACE)
    return ((offset.x + x + 0.5) * tile + pixel[0], (offset.y + y + 0.5) * tile + pixel[1])

def click(h, pos, button=1):
    #send a mouse press and release at the same position
    h.HandleEvent(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=button), SIZE)
    h.HandleEvent(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=pos, button=button), SIZE)

def drag(h, start, end):
    #send a mouse press and release at different positions
    h.HandleEvent(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=start, button=1), SIZE)
    h.HandleEvent(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=end, button=1), SIZE)

def name(grid, x, y):
    #get the item name at the given grid coordinates
    return grid.GetTileByPosition(V(x, y)).item.name

@pytest.fixture
def h(grid):
    #fill the grid and create an input handler for it
    fill(grid, ["ABCDEFGH", "IJKLMNOP"] * 4)
    return InputHandler(grid, SPACE)

#---------- mouse position to tile ----------

@pytest.mark.parametrize("pixel, tile", [
    ((160, 60), V(0, 0)), ((639, 539), V(7, 7)),   #first and last pixel of the grid
    ((219, 100), V(0, 0)), ((220, 100), V(1, 0)),  #either side of a tile border
    ((159, 300), None), ((640, 300), None), ((400, 59), None), ((400, 540), None), ((0, 0), None),
])
def test_screen_to_tile(grid, pixel, tile):
    #check that grid pixels and outside pixels map to the expected tile
    assert grid.ScreenToTile(SIZE, SPACE, pixel) == tile

@pytest.mark.parametrize("size", [(1920, 1080), (600, 800), (320, 240)])
def test_screen_to_tile_after_resize(grid, size):
    #check that tile centres still map correctly at different window sizes
    for pos in grid.AllPositions():
        assert grid.ScreenToTile(size, SPACE, centre(grid, pos.x, pos.y, size)) == pos

#---------- clicking ----------

def test_click_selects(h):
    #check that clicking a tile selects it
    click(h, centre(h.grid, 2, 3))
    assert h.selected == V(2, 3)

def test_click_neighbor_swaps(h):
    #check that clicking a neighboring tile swaps the items and clears the selection
    click(h, centre(h.grid, 0, 0))
    click(h, centre(h.grid, 1, 0))
    assert (name(h.grid, 0, 0), name(h.grid, 1, 0)) == ("B", "A")
    assert h.selected is None

def test_click_far_tile_moves_selection(h):
    #check that clicking a distant tile changes the selection without swapping
    click(h, centre(h.grid, 0, 0))
    click(h, centre(h.grid, 2, 2))
    assert h.selected == V(2, 2) and name(h.grid, 0, 0) == "A"

def test_click_same_tile_or_outside_deselects(h):
    #check that clicking the selected tile or outside the grid deselects it
    click(h, centre(h.grid, 0, 0))
    click(h, centre(h.grid, 0, 0))
    assert h.selected is None
    click(h, centre(h.grid, 0, 0))
    click(h, (10, 10))
    assert h.selected is None

@pytest.mark.parametrize("button", [2, 3, 4, 5])   #middle, right, scroll wheel
def test_other_buttons_ignored(h, button):
    #check that mouse buttons other than left do not select a tile
    click(h, centre(h.grid, 0, 0), button)
    assert h.selected is None

#---------- dragging ----------

def test_drag_onto_neighbor_swaps(h):
    #check that dragging onto a neighboring tile swaps the items
    drag(h, centre(h.grid, 3, 3), centre(h.grid, 3, 4))
    assert (name(h.grid, 3, 3), name(h.grid, 3, 4)) == ("D", "L")

def test_drag_onto_far_tile_or_off_grid_does_nothing(h):
    #check that dragging to a distant tile or outside does not move the tested items
    drag(h, centre(h.grid, 0, 0), centre(h.grid, 3, 0))
    drag(h, centre(h.grid, 0, 0), (10, 10))
    assert name(h.grid, 0, 0) == "A" and name(h.grid, 3, 0) == "D"

#---------- hooks and game loop ----------

def test_on_swap_and_disabled(grid):
    #check that swaps call the callback and disabled input does not call it again
    fill(grid, ["AB"] + ["........"] * 7)
    swaps = []
    h = InputHandler(grid, SPACE, onSwap=lambda a, b: swaps.append((a, b)))
    drag(h, centre(grid, 0, 0), centre(grid, 1, 0))
    assert swaps == [(V(0, 0), V(1, 0))]
    h.enabled = False
    drag(h, centre(grid, 0, 0), centre(grid, 1, 0))
    assert len(swaps) == 1

def test_game_sends_clicks_to_input():
    #check that the game forwards mouse clicks to the input handler
    from GameplayManager import GameplayManager
    gm = GameplayManager(pygame.display.get_surface())
    pos = centre(gm.grid, 2, 2)
    gm.HandleSingleEvent(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=1))
    gm.HandleSingleEvent(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=pos, button=1))
    assert gm.input.selected == V(2, 2)
