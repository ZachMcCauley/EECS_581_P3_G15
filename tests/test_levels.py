'''
Author: Jett Viduya, Claude
Purpose: tests for the level screen and level list
Date: 11/11/26
'''

import pygame
import pytest
from Levels import LEVELS, DescribeGoal

#an owner that records which screen gets opened instead of running it
class FakeOwner:
    def __init__(self):
        self.added = []
    def AddGameManager(self, manager, *args):
        self.added.append((manager, args))

#a level screen drawn once (so its buttons have positions) with a fake mouse
@pytest.fixture
def screen_and_mouse(monkeypatch):
    from GameManagers.LevelScreen import LevelScreen
    ls = LevelScreen(pygame.display.get_surface(), 60)
    ls.SetOwner(FakeOwner())
    ls.Render()
    mouse = {"pos": (0, 0)}
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: mouse["pos"])
    return ls, mouse

#hover a button and left click it
def click(ls, mouse, key):
    mouse["pos"] = ls.buttons[key].rect.center
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=mouse["pos"], button=1))
    ls.ProcessInputs()

#every level has moves and a goal made of real piece names
def test_levels_are_valid(screen_and_mouse):
    ls, mouse = screen_and_mouse
    pieces = ls.resourceManager.AllItemNames()
    for level in LEVELS:
        assert level["moves"] > 0
        assert all(name in pieces and count > 0 for name, count in level["goal"].items())

#goals show up in a readable form
def test_describe_goal():
    assert DescribeGoal({"piece_mail": 4, "piece_save": 2}) == "4 mail, 2 save"

#clicking a level starts gameplay with that level's moves and goal
@pytest.mark.parametrize("index", range(len(LEVELS)))
def test_click_level_starts_it(screen_and_mouse, index):
    from GameManagers.GameplayManager import GameplayManager
    ls, mouse = screen_and_mouse
    click(ls, mouse, index)
    manager, args = ls.owner.added[-1]
    assert manager is GameplayManager
    assert args == (LEVELS[index]["moves"], LEVELS[index]["goal"])
    assert ls.surrenderControl and ls.inGameLoop   #waits underneath, doesn't close

#playing a level gets a copy of the goal, so the level list never changes
def test_goal_is_copied(screen_and_mouse):
    ls, mouse = screen_and_mouse
    click(ls, mouse, 0)
    assert ls.owner.added[-1][1][1] is not LEVELS[0]["goal"]

#the back button and the B key both close the level screen
def test_back_button(screen_and_mouse):
    ls, mouse = screen_and_mouse
    click(ls, mouse, "BACK")
    assert not ls.inGameLoop and not ls.EndedInQuit

def test_b_key_goes_back(screen_and_mouse):
    ls, mouse = screen_and_mouse
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_b))
    ls.ProcessInputs()
    assert not ls.inGameLoop

#clicking empty space does nothing
def test_click_empty_space(screen_and_mouse):
    ls, mouse = screen_and_mouse
    mouse["pos"] = (1, 1)
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(1, 1), button=1))
    ls.ProcessInputs()
    assert ls.owner.added == [] and ls.inGameLoop

#the game really gets the level's moves and goal when started through the manager
def test_manager_passes_level_to_gameplay():
    from GameManagerManager import GameManagerManager
    from GameManagers.GameplayManager import GameplayManager
    gmm = GameManagerManager(pygame.display.get_surface())
    gmm.AddGameManager(GameplayManager, 12, {"piece_folder": 6})
    gm = gmm.managerStack[-1]
    assert gm.rem_moves == 12 and gm.win_con == {"piece_folder": 6}
