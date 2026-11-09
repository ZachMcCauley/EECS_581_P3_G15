from GameManagers.GameManager import GameManager
from GameManagers.GameplayManager import GameplayManager
import pygame

class TitleScreen(GameManager):
    def __init__(self, screen, fps):
        super().__init__(screen, fps)
        self.playButtonRect = pygame.Rect(0, 0, 0, 0)
        self.quitButtonRect = pygame.Rect(0, 0, 0, 0)
    def RunInternal(self) -> None:
        super().RunInternal()
        # Render the title screen.
        self.Render()
    def HandleSingleEvent(self, event: pygame.event.Event) -> None:
        super().HandleSingleEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Left click
            pos = pygame.mouse.get_pos()
            if self.playButtonRect.collidepoint(pos):
                self.surrenderControl = True
                print("Should go to gameplay now")
                self.owner.AddGameManager(GameplayManager)
            elif self.quitButtonRect.collidepoint(pos):
                self.inGameLoop = False
                print("Should quit now")
    def Render(self):
        screenDims = self.screen.get_size()
        font = pygame.font.SysFont("Arial", 20)
        # TODO - Move this code into its own class to not repeat myself
        self.playButtonRect = pygame.Rect(screenDims[0] * 0.4, screenDims[1] * 0.4, screenDims[0] * 0.2, screenDims[1] * 0.1)
        self.quitButtonRect = pygame.Rect(screenDims[0] * 0.4, screenDims[1] * 0.6, screenDims[0] * 0.2, screenDims[1] * 0.1)
        playText = font.render("PLAY", True, (0, 0, 0))
        quitText = font.render("QUIT", True, (255, 255, 255))
        pygame.draw.rect(self.screen, pygame.Color("grey"), self.playButtonRect)
        pygame.draw.rect(self.screen, pygame.Color("red"), self.quitButtonRect)
        self.screen.blit(playText, self.playButtonRect)
        self.screen.blit(quitText, self.quitButtonRect)