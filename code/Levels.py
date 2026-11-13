'''
Author: Jett Viduya, Claude
Purpose: list of levels the player can pick on the level screen
Date: 11/11/26

Each level has a name, how many moves the player gets, and the goal:
how many of each piece they need to clear to win.
To add a level, add another entry to LEVELS.
'''

LEVELS = [
    #level 1 matches the original default (10 moves, 4 mail pieces)
    {"name": "Level 1", "moves": 10, "goal": {"piece_mail": 4}},
    {"name": "Level 2", "moves": 12, "goal": {"piece_folder": 6}},
    {"name": "Level 3", "moves": 15, "goal": {"piece_chat": 6, "piece_clock": 6}},
    {"name": "Level 4", "moves": 15, "goal": {"piece_save": 9}},
    {"name": "Level 5", "moves": 20, "goal": {"piece_notepad": 8, "piece_stickynote": 8}},
]

#turns a goal like {"piece_mail": 4} into "4 mail" for showing on screen
def DescribeGoal(goal):
    return ", ".join(f"{count} {name.replace('piece_', '')}" for name, count in goal.items())
