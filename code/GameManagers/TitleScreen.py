from GameManagers import SelectionMenu
from GameManagers.GameManager import GameManager
from GameManagers.GameplayManager import GameplayManager
from GameManagers.LevelScreen import LevelScreen
from GameManagers.SelectionMenu import SelectionMenu
import pygame
from Prefabs.Button import Button


class TitleScreen(SelectionMenu):
    def __init__(self, screen, fps):
        super().__init__(screen, fps)
        self.buttons["PLAY"] = Button(self.resourceManager.menuSprites["PLAY"], matchWidth=False)
        self.buttons["QUIT"] = Button(self.resourceManager.menuSprites["QUIT"], matchWidth=False)
    def HandleSingleEvent(self, event: pygame.event.Event) -> None:
        super().HandleSingleEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Left click
            match self.hoveredRect:
                case "PLAY":
                    self.surrenderControl = True
                    print("Should go to level select now")
                    self.owner.AddGameManager(LevelScreen)
                case "QUIT":
                    self.inGameLoop = False
                    print("Should quit now")
    def Render(self):
        screenDims = self.screen.get_size()
        self.buttons["PLAY"].SetRect(pygame.Rect(screenDims[0] * 0.4, screenDims[1] * 0.4, 512, 64))
        self.buttons["QUIT"].SetRect(pygame.Rect(screenDims[0] * 0.4, screenDims[1] * 0.4 + 128, 512, 64))
        titleRect = pygame.Rect(screenDims[0] * 0.35, screenDims[1] * 0.2, screenDims[0] * 0.3, 0)
        for button in self.buttons.values():
            button.Render(self.screen)
        unscaledTitle = self.resourceManager.menuSprites["TITLE"]
        titleSprite = pygame.transform.scale_by(unscaledTitle, titleRect.width / unscaledTitle.get_width())
        self.screen.blit(titleSprite, titleRect)
        cursorRect = pygame.Rect(screenDims[0] * 0.4 - 64, screenDims[1] * 0.4, 64, 64)
        match self.hoveredRect:
            case "PLAY":
                self.screen.blit(pygame.transform.scale_by(self.resourceManager.cursorSprite, 2), cursorRect)
            case "QUIT":
                cursorRect.y += 128
                self.screen.blit(pygame.transform.scale_by(self.resourceManager.cursorSprite, 2), cursorRect)