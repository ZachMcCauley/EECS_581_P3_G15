from GameplayManager import GameplayManager
from GameManagerManager import GameManagerManager
import pygame

def main() -> int:
    # PyGame initialization
    pygame.init()
    pygame.display.set_caption("Not Candy Crush")
    screenDims = GetScreenRes()
    screen = pygame.display.set_mode((screenDims[0] - 50 ,screenDims[1] - 100), pygame.RESIZABLE)
    # Create gameplay manager and let it take over.
    gmm = GameManagerManager(screen)
    gmm.AddGameManager(GameplayManager)
    gmm.Run()
    return 0

def GetScreenRes() -> tuple:
    primaryDims = pygame.display.get_desktop_sizes()[0]
    print(f"Screen dimensions: {primaryDims}")
    return primaryDims

main()