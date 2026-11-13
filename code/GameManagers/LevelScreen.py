'''
Author: Jett Viduya, Claude
Purpose: level select screen; shows the levels and starts the one the player clicks
Date: 11/11/26

Hover over a level to see its moves and goal, click it to play.
Click BACK (or press B) to go back to the title screen.
When a level ends, the game comes back to this screen.
'''

import pygame
from GameManagers.SelectionMenu import SelectionMenu
from GameManagers.GameplayManager import GameplayManager
from Prefabs.Button import Button
from Levels import LEVELS, DescribeGoal

#makes a simple outlined box with text in it to use as a button sprite
def MakeTextSprite(text, width, height, fontSize):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(sprite, (255, 255, 255), sprite.get_rect(), 3)
    label = pygame.font.Font(None, fontSize).render(text, True, (255, 255, 255))
    sprite.blit(label, label.get_rect(center=sprite.get_rect().center))
    return sprite

class LevelScreen(SelectionMenu):
    def __init__(self, screen, fps):
        super().__init__(screen, fps)
        self.font = pygame.font.Font(None, 48)
        #one numbered button per level, plus a back button
        for i in range(len(LEVELS)):
            self.buttons[i] = Button(MakeTextSprite(str(i + 1), 96, 96, 64), matchWidth=False)
        self.buttons["BACK"] = Button(MakeTextSprite("BACK", 256, 64, 48), matchWidth=False)

    def HandleSingleEvent(self, event: pygame.event.Event) -> None:
        super().HandleSingleEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hoveredRect == "BACK":
                self.inGameLoop = False
            elif self.hoveredRect != "NONE":
                self.StartLevel(self.hoveredRect)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            self.inGameLoop = False

    #starts gameplay with the level's moves and goal; this screen waits underneath it
    def StartLevel(self, index):
        level = LEVELS[index]
        self.surrenderControl = True
        #copy the goal so playing a level doesn't change the level list
        self.owner.AddGameManager(GameplayManager, level["moves"], dict(level["goal"]))

    def Render(self):
        screenDims = self.screen.get_size()
        #title at the top
        title = self.font.render("SELECT A LEVEL", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(screenDims[0] / 2, screenDims[1] * 0.2)))
        #level buttons in a row across the middle
        spacing = 160   #wide enough gap for the cursor between buttons
        startX = screenDims[0] / 2 - (len(LEVELS) * spacing - (spacing - 96)) / 2
        for i in range(len(LEVELS)):
            self.buttons[i].SetRect(pygame.Rect(startX + i * spacing, screenDims[1] * 0.4, 96, 96))
        self.buttons["BACK"].SetRect(pygame.Rect(screenDims[0] / 2 - 128, screenDims[1] * 0.75, 256, 64))
        for button in self.buttons.values():
            button.Render(self.screen)
        #show the hovered level's details under the row, with the cursor beside its button
        if self.hoveredRect not in ("NONE", "BACK"):
            level = LEVELS[self.hoveredRect]
            info = f"{level['name']}: {level['moves']} moves, clear {DescribeGoal(level['goal'])}"
            text = self.font.render(info, True, (255, 255, 255))
            self.screen.blit(text, text.get_rect(center=(screenDims[0] / 2, screenDims[1] * 0.6)))
        if self.hoveredRect != "NONE":
            rect = self.buttons[self.hoveredRect].rect
            cursorRect = pygame.Rect(rect.x - 64, rect.centery - 32, 64, 64)
            self.screen.blit(pygame.transform.scale_by(self.resourceManager.cursorSprite, 2), cursorRect)
