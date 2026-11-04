from GameManager import GameManager
import pygame

def main():
    pygame.init()
    pygame.display.set_caption("Not Candy Crush")
    screen = pygame.display.set_mode((1000, 1000))
    gm = GameManager(screen)
    gm.Run()
    return 0

main()