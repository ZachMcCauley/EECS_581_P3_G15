'''
Author: Jett Viduya, assisted by Claude Opus 5.5 (debugging + syntax), all ideas are provided by human + understood/checked
Purpose: shared setup for the tests (runs pygame without a window)
Date: 11/5/26
'''

import os
import sys
import pytest

os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame

#the game imports from code/ and loads images with paths relative to it
CODE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "code"))
sys.path.insert(0, CODE_DIR)
pygame.init()
pygame.display.set_mode((800, 600))

from Grid.Grid import Grid
from Grid.Item import Item
from Grid.Vector2Int import Vector2Int

def fill(grid, rows):
    #fill a grid from strings, one per row; each letter is an item name, "." is empty
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            grid.GetTileByPosition(Vector2Int(x, y)).item = None if ch == "." else Item(ch, pygame.Surface((8, 8)))
    return grid

@pytest.fixture(autouse=True)
def in_code_dir(monkeypatch):
    #run each test from the code directory so resource paths work
    monkeypatch.chdir(CODE_DIR)

@pytest.fixture
def grid():
    #provide an empty 8x8 grid for tests
    return Grid.FormFromDims((8, 8))
