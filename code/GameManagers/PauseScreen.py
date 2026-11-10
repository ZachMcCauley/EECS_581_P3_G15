from GameManagers.GameManager import GameManager
from GameManagers.SelectionMenu import SelectionMenu
from Prefabs.Button import Button
import pygame


class PauseScreen(SelectionMenu):
    def __init__(self, screen, fps):
        super().__init__(screen, fps)
        self.buttons["RESUME"] = Button(self.resourceManager.menuSprites["PLAY"], matchWidth=False)
        self.buttons["QUIT"] = Button(self.resourceManager.menuSprites["QUIT"], matchWidth=False)
    def HandleSingleEvent(self, event: pygame.event.Event) -> None:
        super().HandleSingleEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Left click
            match self.hoveredRect:
                case "RESUME":
                    print("Unpause")
                    self.inGameLoop = False
                case "QUIT":
                    self.inGameLoop = False
                    self.removeFromStack = 2
                    print("Quit the main game")
    def Render(self):
        screenDims = self.screen.get_size()
        self.buttons["RESUME"].SetRect(pygame.Rect(screenDims[0] * 0.4, screenDims[1] * 0.4, 512, 64))
        self.buttons["QUIT"].SetRect(pygame.Rect(screenDims[0] * 0.4, screenDims[1] * 0.4 + 128, 512, 64))
        for button in self.buttons.values():
            button.Render(self.screen)
        cursorRect = pygame.Rect(screenDims[0] * 0.4 - 64, screenDims[1] * 0.4, 64, 64)
        match self.hoveredRect:
            case "RESUME":
                self.screen.blit(pygame.transform.scale_by(self.resourceManager.cursorSprite, 2), cursorRect)
            case "QUIT":
                cursorRect.y += 128
                self.screen.blit(pygame.transform.scale_by(self.resourceManager.cursorSprite, 2), cursorRect)