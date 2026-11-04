from GameplayManager import GameplayManager
import pygame

def main():
    pygame.init()
    pygame.display.set_caption("Not Candy Crush")
    screenDims = GetScreenRes()
    screen = pygame.display.set_mode(screenDims, pygame.RESIZABLE)
    gm = GameplayManager(screen)
    gm.Run()
    return 0

def GetScreenRes():
    primaryDims = pygame.display.get_desktop_sizes()[0]
    print(f"Screen dimensions: {primaryDims}")
    return primaryDims

main()