'''
Author: Jett Viduya, assisted by Claude Opus 5.5 (debugging + syntax), all ideas are provided by human + understood/checked
Purpose: shared pytest setup: headless pygame, import paths, and helper fixtures
Date: 11/6/26

- Runs pygame headless (no window opens), so tests work in CI or over SSH.
- Puts code/ on the import path so tests can import modules the same way
  main.py does (e.g. `from Grid.Grid import Grid`).
- Changes the working directory to code/ because the game loads images with
  relative paths like "./Resources/Items".
'''

import os
import sys
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame

#the game imports from code/ and loads images with paths relative to it
CODE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "code"))
sys.path.insert(0, CODE_DIR)
#start pygame once with a hidden display.
#convert_alpha() (used when tiles/items load their sprites) needs a display
#mode to be set, even in headless mode.
pygame.init()
pygame.display.set_mode((800, 600))

from Grid.Grid import Grid
from Grid.Item import Item
from Grid.Vector2Int import Vector2Int

#fill a grid from a list of strings, one string per row (y = 0 first).
#each character is an item name; '.' leaves the tile empty. example:
#    fill(grid, ["AAB",
#                "CDE"])
def fill(grid, rows):
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            grid.GetTileByPosition(Vector2Int(x, y)).item = None if ch == "." else Item(ch, pygame.Surface((8, 8)))
    return grid

#runs every test from inside code/ so image paths work
@pytest.fixture(autouse=True)
def in_code_dir(monkeypatch):
    monkeypatch.chdir(CODE_DIR)

#an empty 8x8 grid, the size the game uses
@pytest.fixture
def grid():
    return Grid.FormFromDims((8, 8))
