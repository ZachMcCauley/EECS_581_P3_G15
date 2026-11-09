from GameManagers.GameManager import GameManager
from GameManagers.GameplayManager import GameplayManager
import pygame

class TitleScreen(GameManager):
    def __init__(self, screen, fps):
        super().__init__(screen, fps)
        self.playButtonRect = pygame.Rect(0, 0, 0, 0)
        self.quitButtonRect = pygame.Rect(0, 0, 0, 0)
        self.hoveredRect = "NONE"
    def RunInternal(self) -> None:
        super().RunInternal()
        # Render the title screen.
        self.Render()
    def HandleSingleEvent(self, event: pygame.event.Event) -> None:
        super().HandleSingleEvent(event)
        mousePos = pygame.mouse.get_pos()
        if self.playButtonRect.collidepoint(mousePos):
            self.hoveredRect = "PLAY"
        elif self.quitButtonRect.collidepoint(mousePos):
            self.hoveredRect = "QUIT"
        else:
            self.hoveredRect = "NONE"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Left click
            match self.hoveredRect:
                case "PLAY":
                    self.surrenderControl = True
                    print("Should go to gameplay now")
                    self.owner.AddGameManager(GameplayManager)
                case "QUIT":
                    self.inGameLoop = False
                    print("Should quit now")
    def Render(self):
        screenDims = self.screen.get_size()
        # TODO - Move this code into its own class to not repeat myself
        self.playButtonRect = pygame.Rect(screenDims[0] * 0.4, screenDims[1] * 0.4, 512, 64)
        self.quitButtonRect = pygame.Rect(screenDims[0] * 0.4, screenDims[1] * 0.4 + 128, 512, 64)
        self.screen.blit(pygame.transform.scale_by(self.resourceManager.menuSprites["PLAY"], 2), self.playButtonRect)
        self.screen.blit(pygame.transform.scale_by(self.resourceManager.menuSprites["QUIT"], 2), self.quitButtonRect)
        cursorRect = pygame.Rect(screenDims[0] * 0.4 - 64, screenDims[1] * 0.4, 64, 64)
        match self.hoveredRect:
            case "PLAY":
                self.screen.blit(pygame.transform.scale_by(self.resourceManager.cursorSprite, 2), cursorRect)
            case "QUIT":
                cursorRect.y += 128
                self.screen.blit(pygame.transform.scale_by(self.resourceManager.cursorSprite, 2), cursorRect)