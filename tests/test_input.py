'''
Author: Jett Viduya, assisted by Claude Opus 5.5 (debugging + syntax), all ideas are provided by human + understood/checked
Purpose: tests for mouse input (dragging tiles in GameplayManager and Grid.GetMousePositionInGrid)
Date: 11/6/26

The mouse is faked, so no window or real mouse is needed.
Boards are filled with known letters so we can see exactly what moved.
'''

import pygame
import pytest
from conftest import fill
from Grid.Vector2Int import Vector2Int as V

#row 0 has X X A X, so swapping (2,0) and (3,0) makes three X's in a row
BOARD = ["XXAXABAB"] + ["CDCDCDCD", "ABABABAB"] * 3 + ["CDCDCDCD"]

#the game reads the mouse every frame with pygame.mouse, so this replaces
#get_pos and get_pressed with values the test controls
class FakeMouse:
    def __init__(self, monkeypatch):
        self.pos, self.buttons = (0, 0), (False, False, False)
        monkeypatch.setattr(pygame.mouse, "get_pos", lambda: self.pos)
        monkeypatch.setattr(pygame.mouse, "get_pressed", lambda *a, **k: self.buttons)

#a game with the known board drawn once, plus a fake mouse
@pytest.fixture
def game(monkeypatch):
    from GameManagers.GameplayManager import GameplayManager
    gm = GameplayManager(pygame.display.get_surface())
    fill(gm.grid, BOARD)
    gm.grid.Render(gm.screen, gm.gridSpace)   #sets each tile's selectionRect
    return gm, FakeMouse(monkeypatch)

#the centre pixel of a tile on screen
def at(gm, x, y):
    return gm.grid.GetTileByPosition(V(x, y)).selectionRect.center

#hold a button on one tile for a frame, then move to another tile for a frame
def drag(gm, mouse, start, end, button=0):
    pressed = [False, False, False]
    pressed[button] = True
    mouse.buttons = tuple(pressed)
    mouse.pos = at(gm, *start)
    gm.RunInternal()
    mouse.pos = at(gm, *end)
    gm.RunInternal()

#let go of the mouse (the game listens for the button-up event)
def release(gm, mouse):
    mouse.buttons = (False, False, False)
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=mouse.pos, button=1))
    gm.RunInternal()

#the item name at a grid position
def name(gm, x, y):
    return gm.grid.GetTileByPosition(V(x, y)).item.name

#every item name on the board, to check nothing moved
def snapshot(gm):
    return {p: name(gm, p.x, p.y) for p in gm.grid.AllPositions()}

#---------- mouse position to tile ----------

#the centre of every tile maps back to that tile
def test_mouse_over_each_tile(game):
    gm, mouse = game
    for pos in gm.grid.AllPositions():
        mouse.pos = at(gm, pos.x, pos.y)
        assert gm.grid.GetMousePositionInGrid() == pos

#pixels in the margin around the grid map to nothing
@pytest.mark.parametrize("pixel", [(0, 0), (5, 300), (799, 599)])
def test_mouse_outside_grid(game, pixel):
    gm, mouse = game
    mouse.pos = pixel
    assert gm.grid.GetMousePositionInGrid() is None

#mapping still correct after the window is resized (landscape, portrait, small)
@pytest.mark.parametrize("size", [(1920, 1080), (600, 800), (320, 240)])
def test_mouse_lines_up_after_resize(game, size):
    gm, mouse = game
    gm.screen = pygame.Surface(size)
    gm.grid.Render(gm.screen, gm.gridSpace)
    for pos in gm.grid.AllPositions():
        mouse.pos = at(gm, pos.x, pos.y)
        assert gm.grid.GetMousePositionInGrid() == pos

#---------- dragging ----------

#drag onto a neighbor that makes a match: the swap stays and the match clears
def test_drag_that_makes_match_swaps_and_clears(game):
    gm, mouse = game
    drag(gm, mouse, (2, 0), (3, 0))
    assert name(gm, 3, 0) == "A"   #the A moved over and stayed
    assert not gm.canSelectTile    #must let go before the next swap

#swap that makes no match is undone
def test_drag_without_match_is_undone(game):
    gm, mouse = game
    before = snapshot(gm)
    drag(gm, mouse, (5, 0), (6, 0))
    assert snapshot(gm) == before

#drag onto a tile that isn't next to it does nothing
@pytest.mark.parametrize("end", [(2, 2), (3, 1)])   #two away, diagonal
def test_drag_to_non_neighbor_does_nothing(game, end):
    gm, mouse = game
    before = snapshot(gm)
    drag(gm, mouse, (2, 0), end)
    assert snapshot(gm) == before

#right click and middle click are ignored
@pytest.mark.parametrize("button", [1, 2])   #middle, right
def test_other_buttons_ignored(game, button):
    gm, mouse = game
    before = snapshot(gm)
    drag(gm, mouse, (2, 0), (3, 0), button)
    assert snapshot(gm) == before and gm.draggedTile is None

#letting go of the mouse after a swap allows the next one
def test_letting_go_allows_next_swap(game):
    gm, mouse = game
    drag(gm, mouse, (2, 0), (3, 0))
    release(gm, mouse)
    assert gm.canSelectTile and gm.draggedTile is None

#a quit event still stops the game loop
def test_quit_still_works(game):
    gm, mouse = game
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    gm.RunInternal()
    assert gm.inGameLoop is False
